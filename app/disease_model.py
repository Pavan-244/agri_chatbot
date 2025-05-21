# app/disease_model.py

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import numpy as np
import os

# Paths (adjust as needed)
DATA_DIR = "data/plantvillage"
MODEL_PATH = "models/crop_model.h5"
IMG_SIZE = (128, 128)
BATCH_SIZE = 32

def train_model():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_data = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        subset='training',
        class_mode='categorical'
    )

    val_data = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        subset='validation',
        class_mode='categorical'
    )

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(train_data.num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_data, epochs=10, validation_data=val_data)
    model.save(MODEL_PATH)

    print("✅ Model trained and saved.")

# Run this once manually
# train_model()
# app/disease_model.py (continued)

def load_trained_model():
    return load_model(MODEL_PATH)

def predict_disease(image_path, model=None):
    if model is None:
        model = load_trained_model()

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_index = np.argmax(predictions[0])
    
    class_labels = os.listdir(DATA_DIR)
    class_labels.sort()  # Ensure alphabetical order matching training

    return class_labels[class_index], float(np.max(predictions[0]))
