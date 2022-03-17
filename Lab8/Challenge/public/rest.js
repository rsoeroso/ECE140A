function click_submit() {
    let object_id = document.getElementById('object').value;
    let theURL= '/objects/'+object_id;

    let store_msg = document.getElementById('store_msg'); 
    store_msg.innerHTML = '';
    
    fetch(theURL)
    .then(response=>response.json())
    .then(function(response) {
        let error = document.getElementById('error'); 
        let GPS_coord = document.getElementById('GPS_coord');

        error.innerHTML = response['error'];
        GPS_coord.innerHTML = 'GPS coordinates: ' + response['GPS_coord'];
    });
}

function click_store() {
    let object_id = document.getElementById('object').value;
    let theURL= '/store_loc/'+object_id;
    fetch(theURL)
    .then(response=>response.json())
    .then(function(response) {
        let store_msg = document.getElementById('store_msg'); 
        store_msg.innerHTML = response['store_msg']
    });
}