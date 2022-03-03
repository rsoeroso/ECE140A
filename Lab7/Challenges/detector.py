from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
# Import OpenCV
import cv2
import numpy as np
from PIL import Image
import pytesseract
import random as rng
import datetime
rng.seed(12345)

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

cursor.execute("TRUNCATE Plates")

# Read the images
image_url = "./public/images/Arizona_47.jpg"
img1 = cv2.imread(image_url, 0)
image_url = "./public/images/Contrast.jpg"
img2 = cv2.imread(image_url, 0)
image_url = "./public/images/Delaware_Plate.png"
img3 = cv2.imread(image_url, 0)
# 0 is a simple alias for cv2.IMREAD_GRAYSCALE

# JSON which maps plates to ID
plate_photos = [
    {"id":1, "img": "Arizona_47.jpg"},
    {"id":2, "img": "Contrast.jpg"},
    {"id":3, "img": "Delaware_Plate.png"}
]

def get_perspective(img, location, height = 450, width = 800):
	pts1 = np.float32([location[0], location[3], location[1], location[2]])
	pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
	# Apply Perspective Transform Algorithm
	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	result = cv2.warpPerspective(img, matrix, (width, height))
	return result

def detect_plate(img, id):

    if id == 1:
        img_color = cv2.imread('./public/images/Arizona_47.jpg', 1)
        image = cv2.imread('./public/images/Arizona_47.jpg', 0)

        src = cv2.GaussianBlur(image, (5, 5), 0)
        ret3, th3 = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite("Thresh.png", th3)
    
        # Perform Edge detection
        edged = cv2.Canny(th3, 100, 255) 
        cv2.imwrite("Canny.png", edged)

        # Get contours
        contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
        # Find the convex hull object for each contour
        hull_list = []
        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            hull_list.append(hull)
        # Draw contours + hull results
        drawing = np.zeros((th3.shape[0], th3.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv2.drawContours(drawing, contours, i, color)
            cv2.drawContours(drawing, hull_list, i, color)
        # Show in a window
        cv2.imwrite('Contours.png', drawing)
        img = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)

        location = None
        
        rect = cv2.minAreaRect(contours[1])
        l = list(rect)
        l[0] = (551, 300)
        l[1] = (621, 200)
        t_change = tuple(l)
        box = cv2.boxPoints(t_change) # cv2.boxPoints(rect) for OpenCV 3.x
        box = np.int0(box)
        cv2.drawContours(drawing,[box],0,(0,255, 0),2)
        cv2.imwrite('Contours.png', drawing)

        # draw the biggest contour (c) in green
        img_box = cv2.drawContours(img_color.copy(),[box],0,(0,255, 0),2)
        cv2.imwrite("Result2.png", np.hstack([img_color, img_box]))
        # Finds rectangular contour
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02*peri, True) 
            if len(approx) == 4:
                location = approx
                break
            
    else:
        if (id == 2):
            image = cv2.imread('./public/images/Contrast.jpg', 0)
        else:
            image = cv2.imread('./public/images/Delaware_Plate.png', 0)
        # Add a Gaussian Blur to smoothen the noise
        blur = cv2.medianBlur(image, 3)
        # cv2.imwrite("Blur.png", blur)

        # Perform Edge detection
        edged = cv2.Canny(blur, 30, 200) 
        # cv2.imwrite("Canny.png", edged)

        # Get contours
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest 15 contours
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

        # Find best polygon and get location
        location = None

        # Finds rectangular contour
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02*peri, True) 
            if len(approx) == 4:
                location = approx
                break

    # Handle cases when no quadrilaterals are found        
    if type(location) != type(None):
        # print("Corners of the contour are: ",location)
        coord = location.reshape(-1).reshape((4,2))
    else:
        if id != 1:
            print("No plate found")
        coord = np.array([-1,-1]*4).reshape((4,2))

    if type(location) != type(None):
        result = get_perspective(image, location)
        # cv2.imwrite("Result2.png", result)
    
    width = 450
    length = 800
    if id == 2:
        y = 110
        x = 5
        cropped = result[0+y:width-y+80, 0+x:length-x]
        # cv2.imwrite("cropped2.png", cropped)
    elif id == 3:
        y = 90
        x = 90
        cropped = result[0+y:width-y-15, 0+x:length-x]
        # cv2.imwrite("cropped3.png", cropped)
    else:
        cropped = th3[187:387, 300:865]
        width = int(cropped.shape[1])
        halfHeight = int(cropped.shape[0] * 0.2)
        halfWidth = int(cropped.shape[1] * 0.3)
        dim = (halfWidth, halfHeight)
  
        cropped = cv2.resize(cropped, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("cropped1.png", cropped)

    roi = cropped
    return roi, coord

def get_text(img, id):
    roi = cv2.threshold(img, 0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C | cv2.THRESH_OTSU)[1]
    if id == 2:
        roi = 255 - roi
    
    try:
        text = pytesseract.image_to_string(roi, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        # Clear whitespaces in text
        text = text.replace(" ","")
        text = text.replace('\n','')
        text = text.replace('\x0c','')
        print("Car Detected. Number Plate: " + text)

        return text

    except:
        print("No text found")

def index_page(req):
    return FileResponse('index.html')

def get_plate(req):
    idx = int(req.matchdict['plate_id'])-1
    id = idx + 1

    if id == 1:
        image_url = "Arizona_47.jpg"
    elif id == 2:
        image_url = "Contrast.jpg"
    else:
        image_url = "Delaware_Plate.png"
    
    image = cv2.imread(image_url, 0) 
    roi, coord = detect_plate(image_url, id)
    text = get_text(roi, id)

    response = {
        'error':            '',
        'image':            image_url,
        'text_detected':    text
    }

    query = "INSERT INTO Plates (Name, Plate, created_at) VALUES (%s, %s, %s)"
    values = [
        (image_url, text, datetime.datetime.now())
    ]
    cursor.executemany(query, values)
    db.commit()

    return response

if __name__ == "__main__":
    with Configurator() as config:
        # create a route for home
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')
        
        # create a route for plates
        config.add_route('plates', '/plates/{plate_id}')
        config.add_view(get_plate, route_name='plates', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)  
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()