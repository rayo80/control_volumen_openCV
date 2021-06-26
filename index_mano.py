import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    image=cv2.imread("imagen_0003.jpg")
    height, width, _ = image.shape
    image =cv2.flip(image,1) #la imagen de entrada ta reflejada

    img_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #de bgr a rgb 

    results = hands.process(img_rgb)
    #una mano
    #print('Handedness:', results.multi_handedness)
    #puntos de mano824)
    #print('Hand landmarks:', results.multi_hand_landmarks)
    if results.multi_hand_landmarks is not None:
        #coordenada en x de pulgar
        # for hand_landmarks in results.multi_hand_landmarks:
        #     x1 = int(hand_landmarks.landmark[8].x*width)
        #     y1 = int(hand_landmarks.landmark[8].y*height)
        #     cv2.circle(image,(x1,y1),3,(255,0,0),3)
        #     print(x1,y1)
        
        #pintar todo
        index=[4,8,12,16,20]
        for hand_landmarks in results.multi_hand_landmarks:
            for i in index:
                x1 = int(hand_landmarks.landmark[i].x*width)
                y1 = int(hand_landmarks.landmark[i].y*height)
                cv2.circle(image,(x1,y1),3,(255,0,0),3)
                print(x1,y1)
        
        

            



    image =cv2.flip(image,1)

cv2.imshow("Images",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

