# Lab 8 Report

# Prepared by: 
# Gino Calgaro, PID A15613364
# Rasya Soeroso, PID A16088908

# Date: 3/18/22

## Tutorials

<hr>

### Tutorial 1: Introduction to CAD

Tutorial 1 has us using CAD to design a camera mount that works with our stepper motor.

We decided to use Solidworks to create the mount design, as it is the most familiar CAD program to us.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut1/cad.png?raw=true" />
</p>

<p align="center"> <b><i>Above is the completed drawing for the camera mount.</i></b> </p>

<br>

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut1/3d.png?raw=true" />
</p>

<p align="center"> <b><i>The finished 3D model in Solidworks.</i></b> </p>

<br>

Adding the camera to the mount and the stepper motor was straightforward:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut1/camera.png?raw=true" />
</p>

<p align="center"> <b><i>Full assembly of camera, mount, and motor.</i></b> </p>

<br>

We are now ready to move on to Tutorial 2!

<hr>

### Tutorial 2: Introduction to GPS

In Tutorial 2, we set up the GPS module with the Raspberry Pi so we can get our location.

Firstly, we went ahead and soldered the pins to the PCB to get more consistency with measuring the location. Next, we built the circuit on the breadboard.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/circuit.png?raw=true" />
</p>

<p align="center"> <b><i>Above is the GPS circuit interfacing with the Pi.</i></b> </p>

<br>

Next, we took the software precautions necessary to get the GPS working with the Pi. After editing the boot code, we are able to see the UART module in the serial connections.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/serial.png?raw=true" />
</p>

<p align="center"> <b><i>We can see that the GPS module is connected to the Pi.</i></b> </p>

<br>

We followed the tutorial to disable the 'tty' device, so we can retrieve the data from the GPS module:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/disable.png?raw=true" />
</p>

<p align="center"> <b><i>Disabling the 'tty' service.</i></b> </p>

<br>

After allowing the GPS to initialize, regular GPS data starting coming through the module.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/data.png?raw=true" />
</p>

<p align="center"> <b><i>Here is a snippet of the received data from the GPS.</i></b> </p>

<br>

After fixing a couple variables in the code, we ran the code, which then returned a Google Maps link to our location.
<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/home.png?raw=true" />
</p>

<p align="center"> <b><i>The GPS was able to identify that we are in Ramona, CA.</i></b> </p>

<br>

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut2/home2.png?raw=true" />
</p>

<p align="center"> <b><i>More output showing that the GPS is working correctly.</i></b> </p>

<br>

Moreover, we were able to implement Reverse Geocoding into our code. This will be important for the challenge later on.

For now, we are ready to move on to Tutorial 3!

<hr>

### Tutorial 3: Color Segmentation

In Tutorial 3, we learn how to use the ArduCam with the Pi and OpenCV to selectively mask objects from images based on their colors. For this tutorial, we are only concerned with masking red objects.

To mask the red objects in the frame, we use HSV values to select and save the red pixels, while getting rid of the rest.

Running the code shows how a red box in the camera frame is masked.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut3/box.png?raw=true" />
</p>

<p align="center"> <b><i>Here is our red box subject.</i></b> </p>

<br>

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut3/mask.png?raw=true" />
</p>

<p align="center"> <b><i>After the code completes, we can see that the red box is masked from the rest of the image.</i></b> </p>

<br>

This masking function will be essential for the final challenge.

We now move on to Tutorial 4!

<hr>

### Tutorial 4: Stepper Motors

In Tutorial 4, we learn how to connect a Stepper motor to the Pi and how to control it.

First, we build the circuit, according to the Freenove tutorial:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut4/circuit.png?raw=true" />
</p>

<p align="center"> <b><i>The Stepper motor circuit.</i></b> </p>

<br>

<p align="center">
  <img src="https://media3.giphy.com/media/dKn1G69yPKKmdB9VcM/giphy.gif" />
</p>

<p align="center"> <b><i>Running the code shows how the Stepper motor works to accurately rotate the camera.</i></b> </p>

<br>

Changing the wait time between steps causes the motor to spin faster or slower, depending on if the wait time is reduced or increased, respectively.

We are now ready for Tutorial 5!

<hr>

### Tutorial 5: PID Controller

In Tutorial 5, we learn how to implement a PID controller to accurately and efficiently detect a certain object in the camera frame. 

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab8/Images/tut5/code.png?raw=true" />
</p>

<p align="center"> <b><i>We found that a Kp value of 0.001 worked well with the PID controller.</i></b> </p>

<br>

Having an effective PID controller is important for detecting our object in the image as fast as possible.

With all of the Tutorials complete, we are finally ready for the last Challenge.

<hr>

## Challenges

<hr>

### Challenge 1: ECE 140a Final Boss


In this challenge, we made an application to detect an object using a camera then its GPS coordinates and address. We provide three objects to detect in which the user chooses it. Next, the user clicks the ```submit``` button to send the request to the server. The server will query the object characteristics from the database and process it for the camera to detect. After the object is successfully detected, it will then find the GPS coordinates of the object and return it back to the client. Additionally, the user will have an option to store the objects' location data into the database by clicking the ```Store object location``` button. If the user chose to do that, the server will insert the object location data to the database.

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

### Functions
#### ```rest.js```

- click_submit():

  When user hits the ```submit``` button, this function is triggered. It retreives an input from the drop down menu and send a URI to the server. It fetches the response back and inject the corresponding GPS coordinates detected into the webpage. 

- click_store():

  When user hits the ```Store object location``` button, this function is triggered. It sends a URI, telling the server to store the previously retreived object's coordinates into the database. 

#### ```app.py```

- get_object(req):
  
  This function is called when the client requests a route to detect a particular object and retrieve its location. First, it parses the object id. Next, it query the HSV value of the object from the database. Then, it calls ```find_object()``` function, instructing the camera to detect the object of interest. When the object is found, it returns a response that consists of object name, GPS coordinates, and address (city and country).

- store_location(req):

  When the user decided to store the object location into the database, this function is called. It first checks whether the same type of object already exists in the database. If we found the same type of object, we append a number at the end of object's name based on the inserting order. If an object doesn't exist in the database yet, it directly stores the name as it is. 

<br>

### Testing and Implementation

## [Link to Demo Video]()

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<br>

Lab 8 is now complete!