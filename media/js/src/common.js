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
        'utils': 'src/utils',
        'Vue': vuePath,
    },
    shim: {
        'bootstrap': {
            'deps': ['jquery']
        }
    },
    urlArgs: urlArgs
});
