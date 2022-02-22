# Lab 6 Report: Midterm

# Prepared by: 
# Gino Calgaro, PID A15613364
# Rasya Soeroso, PID A16088908

# Date: 2/21/22

## Tutorials

<hr>

### Tutorial 1: Setup Raspberry Pi
    
In Tutorial 1, we set up the Rasberry Pi for the first time. This includes running the PiOS imaging program and flashing the SD card.

Once we got the Raspberry Pi up and running, we checked for updates:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/tut1/IMG_9439.jpg?raw=true" />
</p>

<p align="center"> <b><i>Running sudo apt update shows that all of our files are up to date.</i></b> </p>

Running the upgrade command showed that there was nothing eligible to upgrade.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/tut1/IMG_9440.jpg?raw=true" />
</p>

<p align="center"> <b><i>No upgrades were completed.</i></b> </p>

With that out of the way, we could get the MySQL connector added to the Raspberry Pi. This is essential for the midterm challenge.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/tut1/IMG_9441.jpg?raw=true" />
</p>

<p align="center"> <b><i>Shown above is the MySQL connector working as expected.</i></b> </p>

With MySQL installed, we created a new user with all admin privileges granted.

In order to test that the Pi is working correctly, we cloned the code for Lab 5, Tutorial 3. Output is shown below:

<img src="screenshots/t1.png" alt="home page" width="300">
<img src="screenshots/t2.png" alt="home page" width="300">
<img src="screenshots/t3.png" alt="home page" width="300">
<img src="screenshots/t4.png" alt="home page" width="300">
<img src="screenshots/t5.png" alt="home page" width="300">
<img src="screenshots/t6.png" alt="home page" width="300">

With that taken care of, the Raspberry Pi is functioning with Python, as expected. Now we are ready to move on to Tutorial 2!

<br><br>

<hr>

### Tutorial 2: Basic I/O on Raspberry Pi

In this Tutorial, we learned to use sensors from our kit on Raspberry Pi. First, we connected the ultrasonic sensor and the piezoelectric buzzer to the breadboard, as instructed in the tutorial. After we run the provided code, we observed that the ultrasonic sensor was sampled every second, returning a distance value in cm. The buzzer will ring whenever the distance is greater than 0, i.e. whenever the ultrasonic sensor detects any object in front of it. We also learned the two ways of setting up Raspberry Pi in Python; ```GPIO.setmode(GPIO.BCM)``` and ```GPIO.setmode(GPIO.BOARD)```. This is crucial for determining the initialization of the pins in our code. 

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/tut2/IMG_9456.jpg?raw=true" />
</p>

<p align="center"> <b><i>Above is the complete circuit for Tutorial 2.</i></b> </p>

With both tutorials completed, we now have the necessary tools to complete the Midterm Challenge!

<hr>

## Challenges

<hr>

### Challenge 1: Midterm

#### Running the Program

The ```requirements.txt``` file should list all Python libraries that the program depends on, and they will be installed using:

    pip3 install -r requirements.txt

First, we need to initialize theh database by runnning ```init-db.py``` once:

    python3 init-db.py

Finally, we can run the program using:

    python3 app.py

## Report

## [Link to Demo Video](https://youtu.be/AtVoYA2o84A)

For our Midterm, we decided to implement a website that offers feedback on lighting, temperature, and humidity conditions, as they pertain to household plants!

In order to implement this, we decided to use the Photoresistor (to measure light) and the DHT11 sensor (to measure temperature and humidity), which were both included in our starter kit.

As an extra feature, we added an LED bar graph that interacts with a button on the webpage.

Here is an image of the final breadboard circuit:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/chal1/IMG_9458.jpg?raw=true" />
</p>

<p align="center"> <b><i>We can see that the circuit contains all the components necessary for our implementation.</i></b> </p>

#### Our sensor sampling works as follows:

The user first chooses which plant they would like to consider. Next, the user chooses which sensor(s) to read from and at which frequency.

The frequencies:

<ol>
	<li> Just now: Sensors are sampled once; one entry is entered into each respective MySQL table for the sensors.</li>
	<li> 1 min: The sensors are sampled for one minute. <b>NOTE:</b> the DHT11 sensor takes about 2.5 seconds to sample. This rate is reflected accordingly in the sample times, i.e. the sample rate is about one reading every 3 seconds.</li>
	<li> 5 mins: The sensors are sampled for 5 minutes. Again, if the sensor includes the DHT11, we have to reduce our sampling rate.
</ol>

Once the user has chosen all of the above criteria, they hit the 'Submit' button and the sensors are sampled. If the sensors are sampled more than once (i.e. sampled for 1 min or 5 mins), a timer appears on the webpage and begins a countdown accordingly.

### Code

To begin, we first had to create a new MySQL database, called Lab6. This database contains two tables, Photoresistor and DHT11. These tables contain the sampled values for both sensors.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/chal1/initdb.png?raw=true" />
</p>

<p align="center"> <b><i>Above is the code for initializing our database and tables. We can see that each table inserts a dummy value to begin.</i></b> </p>

Next, we designed an HTML webpage with all of the above criteria, as so:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/chal1/webpage.png?raw=true" />
</p>

<p align="center"> <b><i>All images, text, buttons, and dropdown lists are present on our HTML page. We can see that we have added aspects of CSS to the webpage too.</i></b> </p>

In order for our webpage to actually function correctly, we had to implement RESTful functions in both our app.py and rest.js files.

### Functions

#### ```app.py```

- get_everything(req):

  The get_everything(req) function is the main handler of our webpage. It takes in a series of IDs in a single route, which dictates which sensors we are sampling and at which frequency we are sampling them.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab6/screenshots/chal1/geteverything.png?raw=true" />
</p>

<p align="center"> <b><i>When the user hits submit, the get_everything function is called with a route. As shown in the comments in the image, the sequence of IDs from the route correspond to which sensors we are sampling and at which frequency we are sampling them.</i></b> </p>

- getTemperature()

- getHumidity()

- getLight()

- shiftOut()

#### ```rest.js```

- get_sensor()

  Get the user-selected value from the sensor options in the HTML document. The values are; 1: Photoresistor and DHT-11, 2: Photoresistor only, 3: DHT-11 only. This function is later called in ```submit()``` to indicate which sensor(s) to display.

- get_average()

  Get the user-selected value from the average options in the HTML document. The values are; 1: Just Now, 2: 1 min, 3: 5 mins. This function is later called in ```submit()``` to indicate which time period the server should take the average value from.

- get_plant()

  Get the user-selected value from the plant options in the HTML document. The values are; 1: Monstera Deliciosa, 2: Alocasia 'Regal Shield', 3: ZZ Plant. 

- show_plant()

  Based on the plant selected, this function injects the corresponding plant image and its descriptions. The descriptions include sunlight, humidity, and temperature requirements of the selected plant. 

- submit()

  This function is triggered when the user clicks the submit button. It change the ```timer``` element in the HTML document based on the value returned by ```get_average()```. Then, it stores the values from ```get_sensor()```, ```get_average()```, and ```get_plant()``` into ```sensor_id```, ```average_id```, and ```plant_id``` respectively. From those IDs, this function constructs a URI in the form /sensor_id/average_id/LED_id. Here, we set ```LED_id``` = 2 since the LED is controlled by a different button. Next, we fetch the URI and parsed the response in JSON format. The elements inside the response is then injected back to the HTML document. In this function, we created a series of conditional statements to handle the message based on the sensor(s) readings. The messages can be a combination of: _Too cold!_ or _Too warm!_ if the temperature reading is below or above the temperature threshold for a particular plant, _Too dark!_ or _Too bright!_ if the photoresistor reading is below or above the threshold value for a particular plant, _Increase humidity!_ if the humidity reading is below the required value. Otherwise, the message is set to indicate that the light, temperature, and humidity requirements are met. Finally, the message is injected back to HTML so that it is visible to the user. 

- LED_on()

  Set the URI to be /0/0/1, and send the request to the server. This will triger the server to turn on the LED bargraph only. The server will receive 0 as ```sensor_id``` and ```average_id``` which will do nothing on the sensor(s) readings.

- startTimer()

- checkSecond(sec)




