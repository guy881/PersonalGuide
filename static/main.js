/**
 * Created by Stevens on 30.03.2016.
 */
var userLatLng = {
    lat: 52,
    lng: 11
};
var map;
var markers = [];
var site_url = "http://127.0.0.1:5000"

function addMarkerWithTimeout(sight, timeout) {
    window.setTimeout(function () {
        markers.push(new google.maps.Marker({
            position: {lat: sight.lat, lng: sight.lng},
            map: map,
            title: sight.name,
            animation: google.maps.Animation.DROP
        }));
    }, timeout);
}

function initMap() {
    $('#container').html('<div id="map"></div>');
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 52, lng: 11},
        zoom: 9
    });

    if (navigator.geolocation) {
        function error(err) {
            console.warn(err.message);
        }

        function success(position) {
            userLatLng = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            console.log(userLatLng);
            map.setCenter(userLatLng);
            map.setZoom(13);

            // get sights from API
            console.log(site_url + "/popular_sights_for_map/" + userLatLng.lat + ',' + userLatLng.lng);
            $.getJSON(site_url + "/popular_sights_for_map/" + userLatLng.lat + ',' + userLatLng.lng, function (sights) {
                console.log(sights);

                // drop markers after timeout to the map
                var timeout = 30;
                for (i = 0; i < sights.length; i++) {
                    addMarkerWithTimeout(sights[i], i * timeout);
                }

                window.setTimeout(function () {
                    var bounds = new google.maps.LatLngBounds();
                    for( i = 0; i < sights.length; i++) {
                        bounds.extend(markers[i].getPosition());
                    }
                    // map.setCenter(bounds.getCenter());
                    // map.fitBounds(bounds);
                }, timeout * sights.length );   // all markers will be on their places
            });
        }

        navigator.geolocation.getCurrentPosition(success, error);
    }
    else {
        alert("Nie wspiera geolokalizacji.");
    }
}
