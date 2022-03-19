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

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<hr>

### Tutorial 3: Color Segmentation

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<hr>

### Tutorial 4: Stepper Motors

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<hr>

### Tutorial 5: PID Controller

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

<hr>

## Challenges

<hr>

### Challenge 1: ECE 140a Final Boss


In this challenge, we made an application to detect an object using a camera then its GPS coordinates and address. We provide three objects to detect in which the user chooses it. Next, the user clicks the ```submit``` button to send the request to the server. The server will query the object characteristics from the database and process it for the camera to detect. After the object is successfully detected, it will then find the GPS coordinates of the object and return it back to the client. Additionally, the user will have an option to store the objects' location data into the database by clicking the ```Store object location``` button. If the user chose to do that, the server will insert the object location data to the database.

<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i>.</i></b> </p>

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

Lab 8 is now complete!