# import the necessary packages
import cv2
import numpy as np
import os
import sys
 
# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

count = 0

for filename in os.listdir("Dataset"):
    if not filename.endswith(".jpg"):
        print (filename, " is not a .jpg, skipping...\n")
        continue
    
    print (filename, "...\n")

    image = cv2.imread(os.path.join("Dataset",filename), 1)
#   cv2.imshow("Image", image)
#        key = cv2.waitKey(0)

    # Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Show the frame
    #cv2.imshow("Frame", image)

    # Wait for key
    # key = cv2.waitKey(1) & 0xFF
    
    faceDetected = False
    # Draw a rectangle around every found face
    for (x,y,w,h) in faces:
        print("Found a face in ", filename,"!\n")
        faceDetected = True
        # Create rectangle around the face
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
        # Save the image
        cv2.imwrite(os.path.join("Results",filename), image)
        
    count+=1    
    print (count, " images processed")
        
    if len(sys.argv) > 1 and count >= int(sys.argv[1]):
                print ("Reached count, done\n")
                break

print("complete\n")

#cv2.destroyAllWindows()
