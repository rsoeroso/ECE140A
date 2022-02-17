function get_sensor() {
    return document.getElementById('sensor').value;
}
function get_average() {
    return document.getElementById('average').value;
}
function submit() {
    let sensor_id = get_sensor();
    let average_id = get_average();
    let theURL = '/' + sensor_id + '/' + average_id + '/2';
    fetch(theURL)
    .then(response=>response.json())
    .then(function(response) {
        for(var key in response) {
            document.getElementById(key).textContent = key + '\t: ' + response[key];
        }
    });
}
function LED_on() {
    let theURL = '/0/0/1';
    fetch(theURL)
}
function LED_off() {
    let theURL = '/0/0/0';
    fetch(theURL)
}