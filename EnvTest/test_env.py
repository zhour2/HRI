import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)
mpDraw = mp.solutions.drawing_utils

# Load class names