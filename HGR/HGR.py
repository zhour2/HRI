import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2, Preview
import time
import socket

def send_event(event_data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = "127.0.0.1" #socket.gethostname()
    port = 8000
    event_bytes = str(event_data).encode('utf-8')
    client_socket.sendto(event_bytes, (host, port))
    print(f"Send to {host}:{port}")
    

def preprocess_frame(frame):
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    resized_frame = cv2.resize(frame, (224, 224))
    normalized_frame = resized_frame / 255.0
    return np.expand_dims(normalized_frame, axis=0)



def main():
    model = tf.keras.models.load_model('model.h5')
    #model = tf.keras.models.load_model('model_hand.h5')

    gesture_labels = {
        0: "BeGood",
        1: "Greeting",
        2: "Praise",
        3: "RocknRoll",
        4: "Stop",
        5: "Victory"
    }


    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)
    picam2.start()

    confidence_threshold = 0.95


    try:
        while True:
            frame = picam2.capture_array()
            input_frame = preprocess_frame(frame)
            prediction = model.predict(input_frame)
            gesture_index = np.argmax(prediction, axis=1)[0]
            confidence = prediction[0][gesture_index]

            if confidence >= confidence_threshold:
                recognized_gestures = gesture_labels.get(gesture_index, "Unknown")
                print(f"Idx: {gesture_index}, Recgnoized Gesture: {recognized_gestures}, Confidence: {confidence}")
                send_event(gesture_index)
            else:
                recognized_gestures = "Unknown"
                
            
            cv2.imshow('HGR', frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

            #time.sleep(0.5)

    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()