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

In Tutorial 2, we use a Sudoku puzzle to get familiar with the image processing capabilities of OpenCV and PyTesseract.

To get started, we first followed the instructions for installing PyTesseract on our machine. We were able to test the given image to see if PyTesseract was working correctly:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut2/tess.png?raw=true" />
</p>

<p align="center"> <b><i>Running the test image shows that PyTesseract is detecting text from the image correctly.</i></b> </p>

<br>

With that configured, we were now able to follow the instructions for implementing a Sudoku solver. We copied over the code for processing the given Sudoku image with OpenCV. After applying several filters such as blur and threshold, as well as perspective editing, we were able to get the following output:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut2/result.png?raw=true" />
</p>

<p align="center"> <b><i>We can see that, by using funcionalities built into OpenCV, we are able to extract the Sudoku table in the correct perspective.</i></b> </p>

<br>

Running the produced image through the PyTesseract algorithm (one number box at a time) produces the following text conversion:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/tut2/sudoku.png?raw=true" />
</p>

<p align="center"> <b><i>In the terminal, the code shows the coordinates of the found contour corners of the Sudoku table, as well as the output of running each number box through PyTesseract.</i></b> </p>

<br>

Although we were not able to implement an actual Sudoku solving algorithm, this Tutorial was crucial for understanding how to take regular images and use OpenCV for extracting the text from them.

We are now ready to complete the Challenge!

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

<br>

### Testing and Implementation

## [Link to Demo Video](https://youtu.be/Wod1qqLDnPI)

Since the given plate for Arizona was much more complicated to edge detect than the other plates, we implemented a more rigorous image processing pipeline for that plate, as described below:

First, we took the original image and converted it to grayscale, followed by using a Gaussian blur to reduce noise.

Next, we used a combination of binary and OTSU thresholding to get a crisp image of the plate, as shown below:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/thresh.png?raw=true" />
</p>

<p align="center"> <b><i>Result from using thresholding on the blurred image.</i></b> </p>

<br>

We then sent this thresholded image through Canny processing to detect edge lines, as shown below:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/Canny.png?raw=true" />
</p>

<p align="center"> <b><i>Getting the edge lines, using Canny.</i></b> </p>

<br>

With the Canny image, we were now ready for finding the image contours. We then took the first 3 largest contours and used one of them to create a minimum bounding rectangle around the plate text:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/contours.png?raw=true" />
</p>

<p align="center"> <b><i>The minimum bounding rectangle will work nicely for cropping the plate text.</i></b> </p>

<br>

With the area to crop selected, we can observe how the original image will be cropped by placing the minimum bounding rectangle on the original image:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/result.png?raw=true" />
</p>

<p align="center"> <b><i>The original image placed next to the image with the cropping area shown.</i></b> </p>

<br>

Now that we had the cropping region confirmed, we used the rectangle to crop the thresholded image in order to convert the plate text in PyTesseract. We also had to "squish" the image such that the OCR could detect the text more easily.

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/cropped.png?raw=true" />
</p>

<p align="center"> <b><i>The cropped image is both horizontally and vertically compressed so the text can be extracted.</i></b> </p>

<br>

Finally, we run the code in order to test if the plate detection is working correctly:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/test.png?raw=true" />
</p>

<p align="center"> <b><i>For the most part, our algorithm is working! The OCR algorithm mistakes the '8' for a 'B'.</i></b> </p>

<br>

We got the Arizona plate implemented! The other two plates were much easier to process by using a pipeline of applying blur, Canny, and finding contours.

<br>

Now with our detection algorithm working correctly, we ran the local server in order to verify that the webpage was displaying the correct plates and their respective texts.

**Arizona Plate:**

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/1.png?raw=true" />
</p>

<br>

**California Plate:**

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/2.png?raw=true" />
</p>

<br>

**Delaware Plate:**

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/3.png?raw=true" />
</p>

<br>

Additionally, we can see that the terminal is functioning correctly to display the plate text:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/allplates.png?raw=true" />
</p>

<p align="center"> <b><i>Expected output shown in the terminal. Again, the OCR algorithm is not perfect.</i></b> </p>

<br>

Finally, we want to be sure that the plate information is being stored in the MySQL database. Following the demo video, we check the Plates table to see if the data is being saved:

<p align="center">
  <img src="https://github.com/rsoeroso/ECE140A/blob/main/Lab7/screenshots/chal1/mysql.png?raw=true" />
</p>

<p align="center"> <b><i>All of our plate data is dynamically stored in our MySQL database when the user hits the 'Submit' button.</i></b> </p>

<br>

We now have a local web server that runs our algorithm to detect the plate text and display it to the user, while storing the requested information into the MySQL database. 

<br>

Lab 7 is now complete!