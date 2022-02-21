function get_sensor() {
    return document.getElementById('sensor').value;
}
function get_average() {
    return document.getElementById('average').value;
}
function show_plant() {
    let plant_id = get_plant();
    if (plant_id == 1) {
        document.getElementById('pic').src = 'monstera.jpg';
        document.getElementById('light').textContent = 'Thrives in bright to medium indirect light. Not suited for intense, direct sun but can be acclimated to withstand it.'
        document.getElementById('humidity').textContent = 'Normal room humidity will do, but prefers humid conditions if possible.'
        document.getElementById('temp').textContent = 'Prefers temps in the 65°F-85°F range (18°C-30°C). It’s best not to let it go below 60°F (15°C).'
    }
    else if (plant_id == 2) {
        document.getElementById('pic').src = 'alocasia.jpg';
        document.getElementById('light').textContent = 'Thrives in medium to bright indirect light. Alocasia can go into a dormancy phase and dieback during fall and winter.'
        document.getElementById('humidity').textContent = 'Your Alocasia prefers a spot with ample humidity.'
        document.getElementById('temp').textContent = 'Prefers temps in the 65°F-85°F range (18°C-30°C). It’s best not to let it go below 60°F (15°C).'
    }
    else {
        document.getElementById('pic').src = 'zz.jpg';
        document.getElementById('light').textContent = 'Thrives in medium to bright indirect light, but can tolerate low indirect light. Not suited for intense, direct sun.'
        document.getElementById('humidity').textContent = 'This plant does not require any extra humidity.'
        document.getElementById('temp').textContent = 'Prefers temps in the 65°F-75°F range (18°C-24°C). It’s best not to let it go below 45°F (8°C).'
    }
}
function get_plant() {
    return document.getElementById('plant').value;
}
function submit() {
    let sensor_id = get_sensor();
    let average_id = get_average();
    let plant_id = get_plant();
    let msg = '';
    let low_light = 741;
    let high_light = 882;
    
    let theURL = '/' + sensor_id + '/' + average_id + '/2';
    fetch(theURL)
    .then(response=>response.json())
    .then(function(response) {
        // for(var key in response) {
        //     document.getElementById(key).textContent = key + '\t: ' + response[key];
        // }
        document.getElementById('error').textContent = response['error'];
        document.getElementById('light_avg').textContent = 'Light\t\t\t: ' + response['light_avg'];
        document.getElementById('temp_avg').textContent = 'Temperature\t: ' + response['temp_avg'] + '°C';
        document.getElementById('humid_avg').textContent = 'Humidity\t\t: ' + response['humid_avg'] + '%';

        if (response['error'] == '') {
            let msg1 = '';
            let msg2 = '';
            let msg3 = '';
            if (plant_id == 1) {
                // Monstera
                if (response['light_avg'] >= high_light) {
                    msg1 = ''
                }
                else {
                    msg1 = 'Too dark! ' 
                }
                if (response['temp_avg'] < 15) {
                    msg2 = 'Too cold! '
                }
                else if (response['temp_avg'] > 30) {
                    msg2 = 'Too warm! '
                }
                else {
                    msg2 = ''
                }
                if (response['humid_avg'] < 50) {
                    msg3 = 'Increase humidity! '
                }
                else {
                    msg3 = ''
                }
            }
            else if (plant_id == 2) {
                // Alocasia
                if (response['light_avg'] >= low_light) {
                    msg1 = ''
                }
                else {
                    msg1 = 'Too dark! '
                }
                if (response['temp_avg'] < 15) {
                    msg2 = 'Too cold! '
                }
                else if (response['temp_avg'] > 30) {
                    msg2 = 'Too warm! '
                }
                else {
                    msg2 = ''
                }
                if (response['humid_avg'] < 50) {
                    msg3 = 'Increase humidity! '
                }
                else {
                    msg3 = ''
                }
            }
            else {
                // ZZ plant
                if (response['light_avg'] > high_light) {
                    msg1 = 'Too bright! '
                }
                else {
                    msg1 = ''
                }
                if (response['temp_avg'] < 8) {
                    msg2 = 'Too cold! '
                }
                else if (response['temp_avg'] > 24) {
                    msg2 = 'Too warm! '
                }
                else {
                    msg2 = ''
                }
            }
            if (msg1 != '' || msg2 != '' || msg3 != '') {
                msg = msg1 + msg2 + msg3
            }
            else {
                msg = 'Perfect brightness, temperature, and humidity!'
            }
        }
        document.getElementById('msg').textContent = msg;
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