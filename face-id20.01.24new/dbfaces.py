import cv2
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def insertOrUpdate(Id, Name, Age, Gen, CR):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        cmd = f"UPDATE People SET Name='{Name}' WHERE ID={Id}"
        cmd2 = f"UPDATE People SET Age={Age} WHERE ID={Id}"
        cmd3 = f"UPDATE People SET Gender='{Gen}' WHERE ID={Id}"
        cmd4 = f"UPDATE People SET CR='{CR}' WHERE ID={Id}"
    else:
        cmd = f"INSERT INTO People(ID,Name,Age,Gender,CR) Values({Id},'{Name}',{Age},'{Gen}','{CR}')"
        cmd2 = ""
        cmd3 = ""
        cmd4 = ""
    conn.execute(cmd)
    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.execute(cmd4)
    conn.commit()
    conn.close()



def face_photo(Id):
    sampleNum = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"dataSet/User.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Face", img)
        cv2.waitKey(1)
        if sampleNum > 20:
            break

def face_from_video(path, id):
    video_path = path
    cap = cv2.VideoCapture(video_path)

    # Check if the video capture object is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    sampleNum = 0

    # Load the face detection classifier
    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while cap.isOpened():
        ret, img = cap.read()

        # Check if the frame is read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"dataSet/User.{id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(100)

        #cv2.imshow("Face", img)
        cv2.waitKey(1)

        if sampleNum > 20:
            break


def face_from_photo(path,id):
        img = cv2.imread(path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.imwrite(f"dataSet/User.{id}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) 
            cv2.waitKey(100)
        cv2.imshow("Face", img)
        cv2.waitKey(1)


cam.release()
cv2.destroyAllWindows()
