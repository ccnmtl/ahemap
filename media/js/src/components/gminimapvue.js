const libs = ['jquery'];
define(libs, function($) {
    const GoogleMiniMapVue = {
        props: ['latitude', 'longitude'],
        template: '#google-mini-map-template',
        data: function() {
            return {
                mapName: 'the-map'
            };
        },
        mounted: function() {
            const elt = document.getElementById(this.mapName);
            const pos = new google.maps.LatLng(this.latitude, this.longitude);
            this.map = new google.maps.Map(elt, {
                mapTypeControl: false,
                clickableIcons: false,
                zoom: 15,
                streetViewControl: false,
                center: pos,
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

            this.marker = new google.maps.Marker({
                position: pos,
                map: this.map,
                icon: AHE.staticUrl + 'png/marker-selected.png'
            });
        }
    };
    return {
        GoogleMiniMapVue: GoogleMiniMapVue
    };
});