requirejs(['./common'], function() {
    const a = ['jquery', 'bootstrap', 'Vue', 'miniMapVue'];
    requirejs(a, function($, bootstrap, Vue, maps) {
        new Vue({
            el: '#map-container',
            components: {
                'google-mini-map': maps.GoogleMiniMapVue
            }
        });
    });
});
