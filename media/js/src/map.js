requirejs(['./common'], function(common) {
    const libs = ['jquery', 'bootstrap', 'Vue', 'vue2leaflet', 'utils'];
    requirejs(libs,
        function($, bootstrap, Vue, vue2leaflet, utils) {
            new Vue({
                el: '#map-container',
                template: '#map-template',
                data: function() {
                    return {
                        institutions: [],
                        zoom: 5,
                        center: vue2leaflet.L.latLng(37.0902, -95.7129),
                        url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
                        attribution:
                            '&copy; <a href="http://osm.org/copyright">' +
                            'OpenStreetMap</a> contributors',
                        map: null,
                        mapName: 'the-map',
                        selectedSite: null,
                        searchTerm: '',
                        searchResults: null,
                        searchResultHeight: 0
                    };
                },
                components: {
                    'l-map': vue2leaflet.LMap,
                    'l-tile-layer': vue2leaflet.LTileLayer,
                    'l-marker': vue2leaflet.LMarker
                },
                methods: {
                    latlng: function(lat, lng) {
                        return vue2leaflet.L.latLng(lat, lng);
                    },
                    search: function(event) {
                    }
                },
                created: function() {
                    const url = AHE.baseUrl + 'api/institution/';
                    $.getJSON(url, (data) => {
                        this.institutions = data;
                    });
                },
                mounted: function() {
                    // reposition the zoom control
                    this.$children[0].mapObject
                        .zoomControl.setPosition('topright');
                }
            });
        }
    );
});
