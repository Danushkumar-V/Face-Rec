import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import timedelta
import pandas as pd



# df = pd.DataFrame(
#     columns=["Roll_No","Date","Time","Attendence"])
path = 'ImageAttendence'
roll_no=[]
date_1=[]
roll_no_2=[]
date_2=[]
now=datetime.now()

images = []
classNames = []
myList = os.listdir(path)
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print('Encoding Completed')



df=pd.read_csv("attendance_data/Attendance.csv",index_col=0)
def markAttendance(name):
   

    # df=pd.read_csv("attendance_data/Attendance.csv",index_col=0)
    #df['Time'] = df['Time'].astype('datetime64[ns]')
    print(df.info())
    now=datetime.now()
    date=now.strftime("%d-%m-%y")
    time=now.strftime("%H:%M:%S")
    time_1 = datetime.strptime(time, '%H:%M:%S')
  
    time_delta = timedelta(hours=time_1.hour, minutes=time_1.minute, seconds=time_1.second)
    if (name not in roll_no) | (date not in date_1) :
        roll_no.append(name)
        date_1.append(date)
        date=now.strftime("%d-%m-%y")
        time1=now.strftime("%H:%M:%S")
        time_2 = datetime.strptime(time1, '%H:%M:%S')
        df.loc[len(df)] = [name, date, time_2]

    a=df[(df["Roll_No"] == name) & (df["Date"] == date)]["Time"].reset_index()
    
    max_value1 = a.Time.max()
   
    delta = timedelta(hours=max_value1.hour, minutes=max_value1.minute, seconds=max_value1.second)
    now_plus_10 = (delta + timedelta( minutes=2 ))

    if  (now_plus_10 <= time_delta) :
        print("dk")
        df.loc[len(df)] = [name, date, time_1]
    df.to_csv("attendance_data/Attendance.csv")
    csv_2(name,date)


column_names=["Roll_No","Date","Check_in","Check_out","Attendance"]
new_df=pd.DataFrame(columns = column_names)
# new_df=pd.read_csv("/content/csv_2.csv",index_col=0)
def csv_2(name,date):
    df=pd.read_csv("attendance_data/Attendance.csv")
    a=df[(df["Roll_No"] == name) & (df["Date"] == date)]["Time"].reset_index()
    min_value = a.Time.min()
    max_value = a.Time.max()
    


    if (name not in roll_no_2) | (date not in date_2) :
        roll_no_2.append(name)
        date_2.append(date)
        new_df.loc[len(new_df)] = [name, date, min_value, max_value,"p"]
    i=new_df[new_df['Roll_No']==name].index.values
    new_df.at[i, "Check_out"] = max_value
    new_df.to_csv("attendance_data/csv_2.csv")
    print(new_df)




cap = cv2.VideoCapture(0)
# address="http://192.168.1.12:8080/video"
# cap.open(address)

while (cap.isOpened()):
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
        



        cv2.imshow('Webcam', img)
        cv2.waitKey(1)
