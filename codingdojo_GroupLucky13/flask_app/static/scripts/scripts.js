function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    let display = document.getElementById('location');
    let lat = position.coords.latitude;
    let long = position.coords.longitude;
    display.innerHTML = `Location: ${lat} Latitude and ${long} Longitude`;
}