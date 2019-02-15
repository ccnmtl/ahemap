const libs = ['jquery', 'utils'];
define(libs, function($, utils) {
    const GoogleMapVue = {
        props: ['title', 'icon', 'showsites'],
        template: '#google-map-template',
        data: function() {
            return {
                map: null,
                mapName: 'the-map',
                newPin: null,
                newTitle: '',
                selectedSite: null,
                sites: [],
                searchTerm: '',
                searchResults: null,
                searchResultHeight: 0,
            };
        },
        computed: {
            latlng: {
                get: function() {
                    if (this.newPin) {
                        return 'SRID=4326;POINT(' +
                            this.newPin.position.lng() + ' ' +
                            this.newPin.position.lat() + ')';
                    }
                },
            }
        },
        methods: {
            getSearchTerm: function() {
                return this.searchTerm;
            },
            getSelectedSite: function() {
                return this.selectedSite || this.newPin;
            },
            getSiteById: function(siteId) {
                let result;
                this.sites.forEach((site) => {
                    if (site.id === siteId) {
                        result = site;
                    }
                });
                return result;
            },
            isReadOnly: function() {
                return this.readonly === 'true';
            },
            isSearching: function() {
                return this.searchResults && this.searchResults.length > 0;
            },
            siteIconUrl: function(site) {
                const icon = 'government';
                return AHE.staticUrl + 'png/pin-' + icon + '.png';
            },
            markerOpacity: function(opacity) {
                this.sites.forEach((site) => {
                    if (site.marker) {
                        site.marker.setOpacity(opacity);
                    }
                });
            },
            markerShow: function(marker) {
                const OPTIMAL_ZOOM = 15;

                let bounds = this.map.getBounds();
                if (!bounds.contains(marker.getPosition()) ||
                        this.map.getZoom() < OPTIMAL_ZOOM) {
                    // zoom in on the location, but not too close
                    this.map.setZoom(OPTIMAL_ZOOM);
                    this.map.panTo(marker.position);
                }
            },
            clearNewPin: function(event) {
                if (!this.newPin) {
                    return;
                }

                this.newPin.setMap(null);
                this.newPin = null;
                this.searchTerm = '';
                this.newTitle = '';
            },
            clearSearch: function() {
                this.searchResults = null;
                this.searchTerm = null;
            },
            clearSelectedSite: function() {
                if (!this.selectedSite) {
                    return;
                }
                // reset the icon to the site's category
                const url = this.siteIconUrl(this.selectedSite);
                this.selectedSite.marker.setIcon(url);
                this.selectedSite = null;
            },
            clearAll: function() {
                this.clearNewPin();
                this.clearSearch();
                this.clearSelectedSite();
            },
            selectSite: function(site) {
                if (site.marker.getOpacity() < 1) {
                    return; // dimmed sites aren't clickable
                }

                this.clearNewPin();
                this.clearSelectedSite();

                site.marker.setIcon(); // show pointy red icon
                this.selectedSite = site;
                this.markerShow(site.marker);

                if (!this.isSearching()) {
                    this.searchTerm = this.selectedSite.title;
                }
            },
            searchForSite: function() {
                const url = AHE.baseUrl + 'api/institution/?' +
                    'q=' + utils.sanitize(this.searchTerm);
                return $.getJSON(url);
            },
            searchForAddress: function() {
                if (!this.searchTerm) {
                    return Promise.resolve();
                }

                const self = this;
                return new Promise(function(resolve, reject) {
                    self.geocoder.findPlaceFromQuery({
                        query: self.searchTerm,
                        fields: ['formatted_address', 'geometry', 'types']
                    }, function(results) {
                        resolve(results);
                    });
                });
            },
            geocode: function(event) {
                this.clearNewPin();
                this.clearSelectedSite();

                $.when(this.searchForAddress())
                    .done((addresses) => {
                        if (addresses) {
                            this.geocodeResults(addresses);
                        }
                    });
            },
            resetSearch: function(event) {
                this.searchTerm = '';
                this.search();
            },
            search: function(event) {
                this.clearNewPin();
                this.clearSelectedSite();
                this.searchResults = null;
                $('html').addClass('busy');

                // Kick off a sites search & a geocode search
                $.when(this.searchForSite(), this.searchForAddress())
                    .done((sites, addresses) => {
                        if (!this.searchTerm) {
                            // filtering solely by year range
                            this.siteResults(sites[0]);
                        } else if (sites[0].length === 1) {
                            // single site found
                            const site = this.getSiteById(sites[0][0].id);
                            this.searchResults = [site];
                            this.selectSite(site);
                        } else if (sites[0].length > 1) {
                            // multiple sites found via keyword + year range
                            this.searchResults = [];
                            const bounds = this.siteResults(sites[0]);
                            this.map.fitBounds(bounds);
                            this.searchResultHeight =
                                utils.getVisibleContentHeight();
                        } else if (addresses) {
                            // no sites found, try to display geocode result
                            this.geocodeResults(addresses);
                        } else {
                            // no results at all
                            this.markerOpacity(0.25);
                            this.searchResults = [];
                        }
                        $('html').removeClass('busy');
                    });
            },
            siteResults: function(results) {
                let bounds = new google.maps.LatLngBounds();
                this.sites.forEach((site) => {
                    let opacity = 1;
                    if (!results.find(function(obj) {
                        return obj.id === site.id;
                    })) {
                        // dim the icon, this site is not in the results
                        opacity = .25;
                    } else if (this.searchTerm) {
                        this.searchResults.push(site);
                        bounds.extend(site.marker.position);
                        bounds = utils.enlargeBounds(bounds);
                    }
                    site.marker.setOpacity(opacity);
                });
                return bounds;
            },
            geocodeResults: function(results) {
                this.searchTerm = results[0].formatted_address;
                const position = results[0].geometry.location;

                // zoom in on the location, but not too far
                let bounds = new google.maps.LatLngBounds();
                bounds.extend(position);
                bounds = utils.enlargeBounds(bounds);
                this.map.fitBounds(bounds);

                if (this.autodrop === 'true') {
                    const marker = new google.maps.Marker({
                        position: position,
                        map: this.map,
                        icon: AHE.staticUrl +
                            'png/pin-' + this.icon + '.png'
                    });
                    this.newPin = marker;
                }
            },
            reverseGeocode: function(marker) {
                this.reverseGeocoder.geocode({
                    latLng: marker.getPosition(),
                }, (responses) => {
                    if (responses && responses.length > 0) {
                        this.searchTerm = responses[0].formatted_address;
                    } else {
                        this.searchTerm = '';
                    }
                });
            },
            resize: function(event) {
                this.searchResultHeight = utils.getVisibleContentHeight();
            },
            searchDetail: function(siteId) {
                const site = this.getSiteById(siteId);
                this.selectSite(site);
            },
            searchList: function(event) {
                this.clearSelectedSite();
            },
            searchByTag: function(tag) {
                this.searchTerm += ' tag:' + tag;
                this.search();
            },
            searchByCategory: function(category) {
                this.searchTerm += ' category:' + category;
                this.search();
            }
        },
        created: function() {
            if (this.showsites === 'true') {
                const url = AHE.baseUrl + 'api/institution/';
                $.getJSON(url, (data) => {
                    this.sites = data;
                });
            }
        },
        mounted: function() {
            let elt = document.getElementById(this.mapName);

            this.map = new google.maps.Map(elt, {
                mapTypeControl: false,
                clickableIcons: false,
                zoom: 5,
                streetViewControl: false,
                center: new google.maps.LatLng(37.0902, -95.7129),
                fullscreenControlOptions: {
                    position: google.maps.ControlPosition.RIGHT_BOTTOM,
                }
            });

            // initialize geocoder & Google's places services
            this.reverseGeocoder = new google.maps.Geocoder();
            this.geocoder = new google.maps.places.PlacesService(this.map);

            // set initial address marker if specified in properties
            if (this.latitude && this.longitude) {
                const listener = this.map.addListener('idle', (ev) => {
                    const position = new google.maps.LatLng(
                        this.latitude, this.longitude);
                    const marker = new google.maps.Marker({
                        position: position,
                        map: this.map,
                        icon: AHE.staticUrl + 'png/pin-' +
                            this.icon + '.png'
                    });
                    this.newPin = marker;
                    this.searchTerm = this.title;
                    this.markerShow(marker);

                    google.maps.event.removeListener(listener);
                });
            }

            // eslint-disable-next-line scanjs-rules/call_addEventListener
            window.addEventListener('resize', this.resize);
        },
        updated: function() {
            this.sites.forEach((site) => {
                if (!site.marker) {
                    const position = new google.maps.LatLng(site.lat, site.lng);
                    const marker = new google.maps.Marker({
                        position: position,
                        map: this.map,
                        icon: this.siteIconUrl(site)
                    });
                    site.marker = marker;
                    site.iconUrl = this.siteIconUrl(site);
                    google.maps.event.addListener(marker, 'click', (e) => {
                        this.selectSite(site);
                    });
                }
            });
        }
    };
    return {
        GoogleMapVue: GoogleMapVue
    };
});