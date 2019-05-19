# USAGE
# When encoding on laptop/desktop with more memory (more accurate)
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# When encoding on Raspberry Pi (faster, pretty accurate):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# import the necessary packages
from imutils import paths
from face_recognition import face_recognition
import users
import argparse
import pickle
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--users", required=True,
    help="path to input directory of user images + info")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
    help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["users"]))

# initialize the list of known encodings and known names
knownEncodings = []
knownUsers = users.get_all_users()
# knownNames = []

# loop over the image paths
for (i, user) in enumerate(knownUsers):
    print("[INFO] processing user {}/{}".format(i + 1,
        len(knownUsers)))
    name = users.get_name_from_id(user)
    
    for imagePath in users.get_pictures_from_id(user) :
    
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, \
            model=args["detection_method"])

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            # knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "users": knownUsers}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
