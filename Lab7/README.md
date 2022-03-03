# Lab 7 Report

# Prepared by: 
# Gino Calgaro, PID A15613364
# Rasya Soeroso, PID A16088908

# Date: 3/1/22

## Tutorials

<hr>

### Tutorial 1: Say Cheese!
    
In Tutorial 1, we must install OpenCV on our Raspberry Pi in order to interface with the ArduCam.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut1/cvinstall.png?raw=true" />
</p>

<p align="center"> <b><i>Installing OpenCV on the Raspberry Pi, through an SSH connection.</i></b> </p>

<br>

We then run the following code to check which version of OpenCV we have installed:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut1/cvversion.png?raw=true" />
</p>

<p align="center"> <b><i>Above, we can see that we have installed version 4.5.5 of OpenCV.</i></b> </p>

<br>

Once we verify that we have a working installation of OpenCV, we then run the lsusb command to check if the Raspberry Pi is detecting the ArduCam:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut1/lsusb.png?raw=true" />
</p>

<p align="center"> <b><i>Running the lsusb command shows that the ArduCam is detected on the Pi.</i></b> </p>

<br>

Now we are ready to take photos with the ArduCam! Here is a test photo:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut1/test.jpg?raw=true" />
</p>

<p align="center"> <b><i>Quick snapshot of a hallway.</i></b> </p>

<br>

Tutorial 1 is now complete. Now onto Tutorial 2!

<hr>

### Tutorial 2: Sudoku Solver

In Tutorial 2, we use a Sudoku puzzle to get familiar with the image processing capabilities of OpenCV and Tesseract.



<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i></i></b> </p>


<hr>

## Challenges

<hr>

### Challenge 1: Number plate recognition on Pi

In this challenge, we made an application to detect a number plate text. 

The user first chooses which plate number they want to detect. Next, the user click the submit button to send the request to the server. 

We implemented an HTML document that has a drop down menu of number from 1-3. The input then extracted by a RESTful functions which will ask the server to process user's request.

### Functions

#### ```rest.js```

- click_submit():

When user hits the submit button, this function is triggered. It gets the input from the drop down menu and send a URI to the server. It fetches the response back and inject the corresponding cropped plate image and the detected text into the webpage. 

#### ```detector.py```

- get_plate(req):

  This function takes the plate id received by the server and read an image that corresponds to the id. Next, it calls ```detect_plate(img, id)``` which gives the _roi_ (cropped section containing the plate, NumPy) and _coord_ (center of the roi image, NumPy array). The roi is then passed to ```get_text(img, id)``` which gives the detected text from a number plate. Additionally, we store the data to our SQL database and send back the response to the client. 

- detect_plate(img, id):

  Here, we preprocess the number plate and return the cropped image focusing on the number as a Numpy array. First, we blur the image to eliminate noises. Then, we perform Canny edge filter to detect a wide range of edges in our image. Next, we pass our filtered image to ```cv2.findContours``` and check if quadrilateral shapes exist. Finally, we cropped the image according to each orientation and return the roi and coordinates of the corners in the original image. 

- get_text(img, id):

  In this function, we performed additional preprocessing of the cropped image according of the plate id. We perform thresholding for all images and color inversion only for the second image. This ensures that we have black text and white as the background. Then, we pass the filtered image to ```pytesseract``` as well as eliminate the whitespace in the resulting text. This function returns the detected text.
  
<p align="center">
  <img src="" />
</p>

<p align="center"> <b><i></i></b> </p>

https://youtu.be/Wod1qqLDnPI