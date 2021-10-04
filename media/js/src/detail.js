requirejs(['./common'], function() {
    const a = ['jquery', 'bootstrap', 'Vue', 'miniMapVue'];
    requirejs(a, function($, bootstrap, Vue, maps) {
        new Vue({
            el: '.flatpage-container',
            components: {
                'google-mini-map': maps.GoogleMiniMapVue
            },
            methods: {
                onBackToMap: function(evt) {
                    const mapUrl = AHE.baseUrl + 'map/';
                    if (document.referrer.indexOf(mapUrl) < 0) {
                        window.location.href = '/map/';
                    } else {
                        history.go(-1);
                    }
                }
            }
        });
    });
});
