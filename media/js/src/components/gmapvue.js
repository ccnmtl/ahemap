const libs = ['jquery', 'multiselect', 'utils'];
define(libs, function($, multiselect, utils) {
    const GoogleMapVue = {
        props: [],
        template: '#google-map-template',
        components: {
            'multiselect': multiselect.Multiselect
        },
        data: function() {
            return {
                map: null,
                mapName: 'the-map',
                selectedSite: null,
                sites: [],
                searchTerm: '',
                searchResults: null,
                searchResultHeight: 0,
                bounds: null,
                states: utils.states,
                state: null,
                graduationRates: utils.graduationRates,
                graduationRate: null,
                twoYear: null,
                fourYear: null,
                center: null,
                zoom: 5
            };
        },
        methods: {
            changeCriteria: function() {
                this.clearSelectedSite();
                this.clearResults();

                // trigger a new search if the search criteria is valid
                if (this.twoYear || this.fourYear ||
                        this.graduationRate || this.state || this.searchTerm) {
                    this.search();
                }
            },
            clearCriteria: function(evt) {
                evt.preventDefault();
                this.clearSelectedSite();
                this.clearResults();

                this.searchResults = null;
                this.searchTerm = null;
                this.graduationRate = null;
                this.state = null;
                this.twoYear = null;
                this.fourYear = null;

                $('#two-year-program').focus();
            },
            clearResults: function() {
                this.searchResults = null;
                this.bounds = null;
                this.markerOpacity(1);
                this.map.setCenter(this.center);
                this.map.setZoom(this.zoom);
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
            getSiteById: function(siteId) {
                let result;
                this.sites.forEach((site) => {
                    if (site.id === siteId) {
                        result = site;
                    }
                });
                return result;
            },
            siteIconUrl: function(site) {
                return AHE.staticUrl + 'png/marker.png';
            },
            selectedIconUrl: function(site) {
                return AHE.staticUrl + 'png/marker-selected.png';
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
            resize: function(event) {
                this.searchResultHeight = utils.visibleContentHeight();
            },
            selectSite: function(site) {
                if (site.marker.getOpacity() < 1) {
                    return; // dimmed sites aren't clickable
                }

                this.clearSelectedSite();

                const url = this.selectedIconUrl();
                site.marker.setIcon(url);
                this.selectedSite = site;
                this.markerShow(site.marker);
            },
            search: function(event) {
                this.clearSelectedSite();
                this.clearResults();
                $('html').addClass('busy');

                $.when(this.searchForSite()).done((sites) => {
                    if (sites.length === 1) {
                        // single site found
                        const site = this.getSiteById(sites[0].id);
                        this.searchResults = [site];
                        this.selectSite(site);
                    } else if (sites.length > 1) {
                        // multiple sites found via keyword + year range
                        this.searchResults = [];
                        this.siteResults(sites);
                        this.map.fitBounds(this.bounds);
                    } else {
                        // no results at all
                        this.markerOpacity(0.25);
                        this.searchResults = [];
                        this.map.setCenter(this.center);
                        this.map.setZoom(this.zoom);
                    }
                    $('html').removeClass('busy');
                });
            },
            searchForSite: function() {
                let url = AHE.baseUrl + 'api/institution/?';
                if (this.searchTerm) {
                    url += '&q=' + utils.sanitize(this.searchTerm);
                }
                if (this.twoYear) {
                    url += '&twoyear=' + this.twoYear;
                }
                if (this.fourYear) {
                    url += '&fouryear=' + this.fourYear;
                }
                if (this.state) {
                    url += '&state=' + this.state.id;
                }
                if (this.graduationRate) {
                    url += '&rate=' + this.graduationRate.id;
                }
                return $.getJSON(url);
            },
            siteResults: function(results) {
                this.bounds = new google.maps.LatLngBounds();
                this.sites.forEach((site) => {
                    let opacity = 1;
                    if (!results.find(function(obj) {
                        return obj.id === site.id;
                    })) {
                        // dim the icon, this site is not in the results
                        opacity = .25;
                    } else {
                        this.searchResults.push(site);
                        this.bounds.extend(site.marker.position);
                        this.bounds = utils.enlargeBounds(this.bounds);
                    }
                    site.marker.setOpacity(opacity);
                });
            },
            searchDetail: function(siteId) {
                const site = this.getSiteById(siteId);
                this.selectSite(site);
            },
            searchList: function(event) {
                this.clearSelectedSite();
                this.map.fitBounds(this.bounds);
            }
        },
        created: function() {
            const url = AHE.baseUrl + 'api/institution/';
            $.getJSON(url, (data) => {
                this.sites = data;
            });
        },
        mounted: function() {
            let elt = document.getElementById(this.mapName);
            this.center = new google.maps.LatLng(37.0902, -95.7129);
            this.map = new google.maps.Map(elt, {
                mapTypeControl: false,
                clickableIcons: false,
                zoom: this.zoom,
                streetViewControl: false,
                center: this.center,
                fullscreenControlOptions: {
                    position: google.maps.ControlPosition.RIGHT_BOTTOM,
                },
                styles: [
                    {
                        'featureType': 'landscape.man_made',
                        'stylers': [{'visibility': 'off'}]
                    },
                    {
                        'featureType': 'poi',
                        'stylers': [{'visibility': 'off'}]
                    }
                ]
            });

            // eslint-disable-next-line scanjs-rules/call_addEventListener
            window.addEventListener('resize', this.resize);

            this.$watch('twoYear', this.changeCriteria);
            this.$watch('fourYear', this.changeCriteria);
            this.$watch('graduationRate', this.changeCriteria);
            this.$watch('state', this.changeCriteria);
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
            this.searchResultHeight = utils.visibleContentHeight();
        }
    };
    return {
        GoogleMapVue: GoogleMapVue
    };
});