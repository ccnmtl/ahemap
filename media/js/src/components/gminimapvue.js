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
                        'featureType': 'administrative.province',
                        'elementType': 'geometry.stroke',
                        'stylers': [
                            {
                                'visibility': 'on'
                            },
                            {
                                'saturation': '100'
                            },
                            {
                                'gamma': '10.00'
                            },
                            {
                                'lightness': '-100'
                            },
                            {
                                'weight': '2.13'
                            },
                            {
                                'color': '#6c757d'
                            }
                        ]
                    },
                    {
                        'featureType': 'landscape.man_made',
                        'stylers': [{'visibility': 'off'}]
                    },
                    {
                        'featureType': 'poi',
                        'stylers': [{'visibility': 'off'}]
                    },
                    {
                        'featureType': 'poi.school',
                        'stylers': [{'visibility': 'on'}]
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