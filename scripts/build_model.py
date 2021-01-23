import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from bidict import bidict

ENCODER = bidict({
    'A': 1, 'I': 2, 'U': 3, 'E': 4, 'O': 5,
    'KA': 6, 'KI': 7, 'KU': 8, 'KE': 9, 'KO': 10,
    'SA': 11, 'SHI': 12, 'SU': 13, 'SE': 14, 'SO': 15,
    'TA': 16, 'CHI': 17, 'TSU': 18, 'TE': 19, 'TO': 20,
    'NA': 21, 'NI': 22, 'NU': 23, 'NE': 24, 'NO': 25,
    'HA': 26, 'HI': 27, 'FU': 28, 'HE': 29, 'HO': 30,
    'MA': 31, 'MI': 32, 'MU': 33, 'ME': 34, 'MO': 35,
    'YA': 36, 'YU': 37, 'YO': 38,
    'RA': 39, 'RI': 40, 'RU': 41, 'RE': 42, 'RO': 43,
    'WA': 44, 'WO': 45, 'N': 46
})

labels = np.load("../data/labels.npy")
labels = np.array([ENCODER[x] for x in labels])

imgs = np.load("../data/imgs.npy")
imgs = imgs.astype("float32") / 255
imgs = np.expand_dims(imgs, -1)

batch_size = 32
epochs = 20

model = keras.Sequential([
    keras.Input(shape=(100, 100, 1)),
    layers.Conv2D(128, kernel_size=(4, 4), activation="relu"),
    layers.MaxPooling2D(pool_size=(3, 3)),
    layers.Dropout(0.2),
    layers.Conv2D(256, kernel_size=(4, 4), activation="relu"),
    layers.MaxPooling2D(pool_size=(3, 3)),
    layers.Flatten(),
    layers.Dropout(0.2),
    layers.Dense(len(ENCODER)+1, activation="softmax"),
])

early_stopping = keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

model.fit(imgs,
          labels,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.30,
          callbacks=[early_stopping])

plt.plot(model.history.history['accuracy'], color="red")
plt.plot(model.history.history['val_accuracy'], color="blue")
plt.show()

model.save("../kana.model")
