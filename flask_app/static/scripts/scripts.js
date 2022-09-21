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

async function get_all_caches() {
    let caches = await fetch('/get_all_caches')
        .then( response => response.json() )
    console.log(caches);
    let position = document.getElementById('cache_table_body')
    position.innerHTML = '';
    for(let i = 0; i < caches.length; i++) {
        position.innerHTML += `
        <tr>
            <td>${ caches[i]['latitude']}</td>
            <td>${ caches[i]['longitude']}</td>
            <td>${ caches[i]['description']}</td>
            <td><img width="400" height="200" src="https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=400&height=200&center=lonlat:${caches[i].longitude },${caches[i].latitude}&zoom=14&apiKey=ce3b7da4754d40ba881a68789118ecbd"></td>
            <td><a href="/usercaches/edit/${caches[i].id}"><button>Edit</button></a></td>
            <td><a href="/usercaches/delete/${caches[i].id}"><button>Delete</button></a></td>
        </tr>
        `
    }
}