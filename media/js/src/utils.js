define(function() {

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sanitize(s) {
        // http://shebang.brandonmintern.com/
        // foolproof-html-escaping-in-javascript/
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(s));
        return div.innerHTML;
    }

    function visibleContentHeight() {
        var viewportheight;

        // the more standards compliant browsers (mozilla/netscape/opera/IE7
        // use window.innerWidth and window.innerHeight
        if (typeof window.innerWidth !== 'undefined') {
            viewportheight = window.innerHeight;
        } else if (typeof document.documentElement !== 'undefined' &&
            typeof document.documentElement.clientWidth !== 'undefined' &&
                document.documentElement.clientWidth !== 0) {
            // IE6 in standards compliant mode (i.e. with a valid doctype
            // as the first line in the document)
            viewportheight = document.documentElement.clientHeight;
        } else {
            // older versions of IE
            viewportheight =
                document.getElementsByTagName('body')[0].clientHeight;
        }

        return viewportheight - (
            100 + $('header').outerHeight() +  $('.search-bar').outerHeight() +
            $('.advanced-filters').outerHeight());
    }

    return {
        csrfSafeMethod: csrfSafeMethod,
        sanitize: sanitize,
        visibleContentHeight: visibleContentHeight
    };
});
