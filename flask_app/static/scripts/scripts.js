function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    let latId = document.getElementById('lat-id');
    let longId = document.getElementById('lon-id');
    let lat = position.coords.latitude;
    let long = position.coords.longitude;
    latId.value = lat;
    longId.value = long;
}