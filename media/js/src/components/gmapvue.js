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
                mapName: 'the-map',
                selectedSite: null,
                sites: [],
                searchTerm: '',
                searchResults: null,
                searchResultHeight: 0,
                states: utils.states,
                state: null,
                graduationRates: utils.graduationRates,
                graduationRate: null,
                twoYear: null,
                fourYear: null
            };
        },
        methods: {
            onBackToSearchList: function(event) {
                this.clearSelectedSite();
                this.map.fitBounds(this.bounds);
            },
            onChangeCriteria: function() {
                this.clearSelectedSite();
                this.clearResults();

                const params = this.searchCriteria();
                if (Object.keys(params).length > 0) {
                    this.search(params);

                    // track history
                    const url = '/map/?' + $.param(params);
                    window.history.replaceState({}, '', url);
                }
            },
            onClear: function(evt) {
                evt.preventDefault();
                this.clearSelectedSite();
                this.clearResults();

                this.searchTerm = null;
                this.graduationRate = null;
                this.state = null;
                this.twoYear = null;
                this.fourYear = null;

                $('#two-year-program').focus();
                window.history.replaceState({}, '', '/map/');
            },
            onClearSelectedSite: function() {
                this.clearSelectedSite();
                window.history.replaceState({}, '', '/map/');
            },
            onSelectSite: function(site) {
                this.selectSite(site);

                if (!this.searchResults) {
                    window.history.replaceState(
                        {}, '', '/map/?site=' + site.id);
                }
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
                this.selectedSite.marker.setIcon(this.siteIconUrl);
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

                site.marker.setIcon(this.selectedIconUrl);
                this.selectedSite = site;
                this.markerShow(site.marker);
            },
            searchCriteria: function() {
                let params = {};
                if (this.searchTerm) {
                    params['q'] = utils.sanitize(this.searchTerm);
                }
                if (this.twoYear) {
                    params['twoyear'] = this.twoYear;
                }
                if (this.fourYear) {
                    params['fouryear'] = this.fourYear;
                }
                if (this.state) {
                    params['state'] = this.state.id;
                }
                return params;
            },
            search: function(criteria) {
                $('html').addClass('busy');

                $.getJSON(this.baseUrl + $.param(criteria)).done((sites) => {
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
            setState: function(params) {
                if ('site' in params) {
                    const siteId = parseInt(params['site'], 10);
                    const site = this.getSiteById(siteId);
                    this.selectSite(site);
                    return;
                }

                if ('state' in params && params.state) {
                    for (let s of this.states) {
                        if (s.id === params.state) {
                            this.state = s;
                        }
                    }
                }
                if ('q' in params) {
                    this.searchTerm = utils.sanitize(params.q);
                }
                if ('twoyear' in params) {
                    this.twoYear = params.twoyear === 'true';
                }
                if ('fouryear' in params) {
                    this.fourYear = params.fouryear === 'true';
                }
                this.onChangeCriteria();
            }
        },
        created: function() {
            this.baseUrl = AHE.baseUrl + 'api/institution/?';
            this.bounds = null;
            this.zoom = 5;
            this.center = new google.maps.LatLng(37.0902, -95.7129);
            this.siteIconUrl = AHE.staticUrl + 'png/marker.png';
            this.selectedIconUrl = AHE.staticUrl + 'png/marker-selected.png';
        },
        mounted: function() {
            let elt = document.getElementById(this.mapName);
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

            const url = AHE.baseUrl + 'api/institution/';
            $.getJSON(url, (data) => {
                this.sites = data;
                this.sites.forEach((site) => {
                    const position = new google.maps.LatLng(site.lat, site.lng);
                    const marker = new google.maps.Marker({
                        position: position,
                        map: this.map,
                        icon: this.siteIconUrl
                    });
                    site.marker = marker;
                    site.iconUrl = this.siteIconUrl;
                    google.maps.event.addListener(marker, 'click', (e) => {
                        this.onSelectSite(site);
                    });
                });

                // load state if there are query params
                const params = utils.queryParams();
                if (Object.keys(params).length > 0) {
                    this.setState(params);
                }

                // search criteria changes as the user interacts with the form
                this.$watch('twoYear', this.onChangeCriteria);
                this.$watch('fourYear', this.onChangeCriteria);
                this.$watch('graduationRate', this.onChangeCriteria);
                this.$watch('state', this.onChangeCriteria);
            });
        },
        updated: function() {
            this.searchResultHeight = utils.visibleContentHeight();
        }
    };
    return {
        GoogleMapVue: GoogleMapVue
    };
});