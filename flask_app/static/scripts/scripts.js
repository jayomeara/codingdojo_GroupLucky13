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

async function getAddress(){
    let lat = document.getElementById('lat-id').value;
    let long = document.getElementById('lon-id').value;
    let key = 'https://api.geocodify.com/v2/reverse?api_key=27be93eef5f40a54861619efa7617d2a9d924ba5';
    let request = key.concat('&lat=', lat, '&lng=', long);
    console.log(request)
    let response = await fetch(request)
    if (response.ok) {
        let json = await response.json();
        // console.log(json.response.features[0].properties);
        let address = json.response.features[0].properties;

        document.getElementById('street').value = address.street;
        document.getElementById('city').value = address.locality;
        document.getElementById('state').value = address.region_a;
        document.getElementById('country').value = address.country_code;
    } else {
        alert("HTTP-Error: " + response.status);
    }
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
            <td><a href="/view/cache/${caches[i].id}"><button>View Comments</button></a></td>
        </tr>
        `
    }
}

async function search_caches() {
    let city = document.getElementById('city').value;
    let state = document.getElementById('state').value
    let request = '/searchall/' + city + "/" + state
    let caches = await fetch(request)
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
            <td><a href="/view/cache/${caches[i].id}"><button>View Comments</button></a></td>
        </tr>
        `
    }
}

function display_comment_form(comment_button) {
    let target = document.querySelector('#add-comment-container')
    target.style.display = 'flex';
    comment_button.style.display = 'none';
}

function cancel_comment_form() {
    let target = document.querySelector('#add-comment-container')
    target.style.display = 'none';
    target = document.querySelector('#comment_button');
    target.style.display = '';
}