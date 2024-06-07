import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'static/photos'

def getImagesWithID(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    faces = []
    IDs = []
    for image_path in image_paths:
        face_img = Image.open(image_path).convert('L')
        face_np = np.array(face_img, 'uint8')
        # Extract the ID from the filename, assumed to be the part before the extension
        filename = os.path.basename(image_path)
        ID_str = filename.split('_')[1]
        ID = int(ID_str.split('.')[0])  # This now only takes the number before the '.'
        faces.append(face_np)
        IDs.append(ID)
        cv2.imshow("training", face_np)
        cv2.waitKey(10)
    return np.array(IDs), faces


# Ensure the recognizer directory exists
os.makedirs('recognizer', exist_ok=True)

IDs, faces = getImagesWithID(path)
recognizer.train(faces, IDs)
recognizer.write('recognizer/trainingData.yml')
cv2.destroyAllWindows()
