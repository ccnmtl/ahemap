requirejs(['./common'], function() {
    const a = ['jquery', 'utils', 'bootstrap', 'Vue', 'mapVue'];
    requirejs(a, function($, utils, bootstrap, Vue, maps) {
        new Vue({
            el: '#map-container',
            components: {
                'google-map': maps.GoogleMapVue
            }
        });
    });
});
