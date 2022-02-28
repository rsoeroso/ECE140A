function click_submit() {
    let plate_id = document.getElementById('textInput').value;
    let theURL= '/plates/'+plate_id;
    
    fetch(theURL)
    .then(response=>response.json())
    .then(function(response) {
        let img = document.getElementById('image'); 
        let text_detected = document.getElementById('text_detected');

        img.src = 'images/' + response['image'];
        text_detected.innerHTML = response['text_detected'];
    });
}