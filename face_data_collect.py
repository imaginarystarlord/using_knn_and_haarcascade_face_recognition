import cv2
import numpy as np

#Init Camera
cap = cv2.VideoCapture(0)

#Face Detection using Haar Cascade
file_name = input('Enter The Name of person whose data to be collected with consent :) ')
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
skip =0
face_data = []
dataset_path = './data/'
while True:
	ret,frame = cap.read()
	if ret==False:
		continue
	gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(frame,1.3,5)
	if len(faces)==0:
		continue
	faces = sorted(faces,key=lambda f:f[2]*f[3])
	#pick the last face, because of maximum area
	for face in faces[-1:]:
		x,y,w,h = face
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
		#extracting the face(crop out the required area):Region of Interest
		offset = 10
		face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section = cv2.resize(face_section,(100,100))
		skip+=1
		if skip%10==0:
			face_data.append(face_section)
			print(len(face_data))
			
	cv2.imshow('Frame',frame)
	cv2.imshow('Face Section',face_section)
	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed==ord('q'):
		break
#coverting our face_list in numpy array
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))
#saving this in file
np.save(dataset_path+file_name+'.npy',face_data)
print('Data has been successfully saved in '+dataset_path+file_name+'.npy' )
cap.release()
cv2.destroyAllWindows()