requirejs(['./common'], function(common) {
    const libs = ['jquery', 'bootstrap', 'Vue', 'vue2leaflet', 'utils'];
    requirejs(libs,
        function($, bootstrap, Vue, vue2leaflet, utils) {
            new Vue({
                el: '#content',
                data: function() {
                    return {
                        zoom: 5,
                        center: vue2leaflet.L.latLng(37.0902, -95.7129),
                        url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
                        attribution:
                            '&copy; <a href="http://osm.org/copyright">' +
                            'OpenStreetMap</a> contributors'
                    };
                },
                components: {
                    'l-map': vue2leaflet.LMap,
                    'l-tile-layer': vue2leaflet.LTileLayer,
                    'l-marker': vue2leaflet.LMarker
                },
                methods: {
                },
                created: function() {
                },
                mounted: function() {
                },
                updated: function() {
                }
            });
        }
    );
});
