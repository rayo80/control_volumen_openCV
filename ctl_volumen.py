#------CONTROL DE VOLUMEN CON LOS DEDOS-------
import cv2
import mediapipe as mp
import math
#librerias pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



#esta funcion permite tener solo los valores x e y de los 24 puntos 
#evitaremos de esta manera invocar landmarks cuando solo se requiere calcular
def my_lm(mp_lm):
     lms = []
     for __,lm in enumerate(mp_lm):
         cx=int(lm.x*width)
         cy=int(lm.y*height)
         lms.append((cx,cy))
     return lms

#funcion para calcular distancia
def distancia(p1,p2):
  return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


#funcion que pinta union de dos puntos 
def union(p1,p2):
  cx=int((p1[0]+p2[0])/2)
  cy=int((p1[1]+p2[1])/2)
  return cx,cy

#control de volumen
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    #ancho y alto
    height, width, _ = image.shape
    #voltear la imagen y cambiar de bgr a rgb
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    # Dibujo de las marcas en la mano
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      index=[4,8,12,16,20]
      for hand_landmarks in results.multi_hand_landmarks:

        #pintar los valores establecidos en el index
        for i in index:
                x = int(hand_landmarks.landmark[i].x*width)
                y = int(hand_landmarks.landmark[i].y*height)
                cv2.circle(image,(x,y),3,(255,0,0),3)
                cv2.putText(image,f'{i}',(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)


        #invoco la funcion para reorganizar los puntos
        lms1=my_lm(hand_landmarks.landmark)
        #invoco a la funcion para calcular la distancia 4 y 8
        dist1=distancia(lms1[4],lms1[8])
        cv2.line(image,lms1[4],lms1[8],(255,255,0),5)
        print(dist1)
        #indicar el centro 
        x_u,y_u=union(lms1[4],lms1[8])
        cv2.putText(image,f'{int(dist1)}',(x_u,y_u),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

        #Control del volumen
        miVol =volume.GetMasterVolumeLevelScalar()*100
        print(miVol)


        if dist1<70 and miVol>1:
          miVol -=1
          volume.SetMasterVolumeLevelScalar(miVol/100,None)
          cv2.circle(image,(x_u,y_u),3,(0,255,0),3)

        if dist1>=70 and miVol<99:
          miVol =miVol+1
          volume.SetMasterVolumeLevelScalar(miVol/100,None)
          cv2.circle(image,(x_u,y_u),3,(0,0,255),3)
        #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()