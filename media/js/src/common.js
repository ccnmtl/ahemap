let vuePath = 'lib/vue/vue.min';
let urlArgs = 'bust=' + (new Date()).getTime();
if (AHE.debug == 'true') {
    vuePath = 'lib/vue/vue';
    urlArgs = '';
}

requirejs.config({
    baseUrl: AHE.staticUrl + 'js/',
    paths: {
        'bootstrap': 'lib/bootstrap/js/bootstrap.bundle.min',
        'domReady': 'lib/require/domReady',
        'jquery': 'lib/jquery-3.3.1.min',
        'leaflet': 'lib/leaflet/leaflet',
        'utils': 'src/utils',
        'Vue': vuePath,
        'vue2leaflet': 'lib/vue2-leaflet/vue2-leaflet.min',
    },
    shim: {
        'bootstrap': {
            'deps': ['jquery']
        },
        'vue2-leaflet': {
            'deps': ['jquery', 'bootstrap', 'Vue']
        },
        'utils': {
            'deps': ['jquery']
        }
    },
    urlArgs: urlArgs
});
