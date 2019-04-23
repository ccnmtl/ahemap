define(function() {

    const populations = [
        {id: 'small', name: 'Small', range: '< 2,000'},
        {id: 'medium', name: 'Medium', range: '2,000 - 10,000'},
        {id: 'large', name: 'Large', range: '> 10,000'}
    ];

    const states = [
        {name: 'Alabama', id: 'AL', lat: '32.806671', lng: '-86.79113'},
        {name: 'Alaska', id: 'AK', lat: '61.370716', lng: '-152.404419'},
        {name: 'Arizona', id: 'AZ', lat: '33.729759', lng: '-111.431221'},
        {name: 'Arkansas', id: 'AR', lat: '34.969704', lng: '-92.373123'},
        {name: 'California', id: 'CA', lat: '36.116203', lng: '-119.681564'},
        {name: 'Colorado', id: 'CO', lat: '39.059811', lng: '-105.311104'},
        {name: 'Connecticut', id: 'CT', lat: '41.597782', lng: '-72.755371'},
        {name: 'Delaware', id: 'DE', lat: '39.318523', lng: '-75.507141'},
        {name: 'District of Columbia', id: 'DC',
            lat: '38.9072', lng: '-77.0369'},
        {name: 'Florida', id: 'FL', lat: '27.766279', lng: '-81.686783'},
        {name: 'Georgia', id: 'GA', lat: '33.040619', lng: '-83.643074'},
        {name: 'Hawaii', id: 'HI', lat: '21.094318', lng: '-157.498337'},
        {name: 'Idaho', id: 'ID', lat: '44.240459', lng: '-114.478828'},
        {name: 'Illinois', id: 'IL', lat: '40.349457', lng: '-88.986137'},
        {name: 'Indiana', id: 'IN', lat: '39.849426', lng: '-86.258278'},
        {name: 'Iowa', id: 'IA', lat: '42.011539', lng: '-93.210526'},
        {name: 'Kansas', id: 'KS', lat: '38.5266', lng: '-96.726486'},
        {name: 'Kentucky', id: 'KY', lat: '37.66814', lng: '-84.670067'},
        {name: 'Louisiana', id: 'LA', lat: '31.169546', lng: '-91.867805'},
        {name: 'Maine', id: 'ME', lat: '44.693947', lng: '-69.381927'},
        {name: 'Maryland', id: 'MD', lat: '39.063946', lng: '-76.802101'},
        {name: 'Massachusetts', id: 'MA', lat: '42.230171', lng: '-71.530106'},
        {name: 'Michigan', id: 'MI', lat: '43.326618', lng: '-84.536095'},
        {name: 'Minnesota', id: 'MN', lat: '45.694454', lng: '-93.900192'},
        {name: 'Mississippi', id: 'MS', lat: '32.741646', lng: '-89.678696'},
        {name: 'Missouri', id: 'MO', lat: '38.456085', lng: '-92.288368'},
        {name: 'Montana', id: 'MT', lat: '46.921925', lng: '-110.454353'},
        {name: 'Nebraska', id: 'NE', lat: '41.12537', lng: '-98.268082'},
        {name: 'Nevada', id: 'NV', lat: '38.313515', lng: '-117.055374'},
        {name: 'New Hampshire', id: 'NH', lat: '43.452492', lng: '-71.563896'},
        {name: 'New Jersey', id: 'NJ', lat: '40.298904', lng: '-74.521011'},
        {name: 'New Mexico', id: 'NM', lat: '34.840515', lng: '-106.248482'},
        {name: 'New York', id: 'NY', lat: '42.165726', lng: '-74.948051'},
        {name: 'North Carolina', id: 'NC', lat: '35.630066', lng: '-79.806419'},
        {name: 'North Dakota', id: 'ND', lat: '47.528912', lng: '-99.784012'},
        {name: 'Ohio', id: 'OH', lat: '40.388783', lng: '-82.764915'},
        {name: 'Oklahoma', id: 'OK', lat: '35.565342', lng: '-96.928917'},
        {name: 'Oregon', id: 'OR', lat: '44.572021', lng: '-122.070938'},
        {name: 'Pennsylvania', id: 'PA', lat: '40.590752', lng: '-77.209755'},
        {name: 'Rhode Island', id: 'RI', lat: '41.680893', lng: '-71.51178'},
        {name: 'South Carolina', id: 'SC', lat: '33.856892', lng: '-80.945007'},
        {name: 'South Dakota', id: 'SD', lat: '44.299782', lng: '-99.438828'},
        {name: 'Tennessee', id: 'TN', lat: '35.747845', lng: '-86.692345'},
        {name: 'Texas', id: 'TX', lat: '31.054487', lng: '-97.563461'},
        {name: 'Utah', id: 'UT', lat: '40.150032', lng: '-111.862434'},
        {name: 'Vermont', id: 'VT', lat: '44.045876', lng: '-72.710686'},
        {name: 'Virginia', id: 'VA', lat: '37.769337', lng: '-78.169968'},
        {name: 'Washington', id: 'WA', lat: '47.400902', lng: '-121.490494'},
        {name: 'West Virginia', id: 'WV', lat: '38.491226', lng: '-80.954453'},
        {name: 'Wisconsin', id: 'WI', lat: '44.268543', lng: '-89.616508'},
        {name: 'Wyoming', id: 'WY', lat: '42.755966', lng: '-107.30249'}
    ];

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

    function enlargeBounds(bounds) {
        // Don't zoom in too far on only one marker
        // http://stackoverflow.com/questions/3334729/
        // google-maps-v3-fitbounds-zoom-too-close-for-single-marker
        if (bounds.getNorthEast().equals(bounds.getSouthWest())) {
            var extendPoint1 = new google.maps.LatLng(
                bounds.getNorthEast().lat() + 0.001,
                bounds.getNorthEast().lng() + 0.001);
            var extendPoint2 = new google.maps.LatLng(
                bounds.getNorthEast().lat() - 0.001,
                bounds.getNorthEast().lng() - 0.001);
            bounds.extend(extendPoint1);
            bounds.extend(extendPoint2);
        }
        return bounds;
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

        return viewportheight -
            (8 +
             jQuery('.advanced-filters').offset().top +
             jQuery('.advanced-filters').outerHeight());
    }

    function queryParams() {
        // https://stackoverflow.com/questions/901115/
        // how-can-i-get-query-string-values-in-javascript
        const pl = /\+/g;  // Regex to sub addition symbol with space
        const search = /([^&=]+)=?([^&]*)/g;
        const decode = function(s) {
            return decodeURIComponent(s.replace(pl, ' '));
        };
        const query = window.location.search.substring(1);

        let match;
        let urlParams = {};
        while ((match = search.exec(query))) {
            urlParams[decode(match[1])] = decode(match[2]);
        }
        return urlParams;
    }

    return {
        csrfSafeMethod: csrfSafeMethod,
        enlargeBounds: enlargeBounds,
        queryParams: queryParams,
        populations: populations,
        sanitize: sanitize,
        states: states,
        visibleContentHeight: visibleContentHeight
    };
});
