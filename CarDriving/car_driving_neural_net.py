import os

import numpy as np
import tensorflow as tf

# iterate over files in the directory of fitting data to get training data
x_train = []
y_train = []
directory = 'training_data'
# for filename in os.listdir(directory): todo
for filename in ['nn_fit_data_1']:
    file = os.path.join(directory, filename)
    with open(file, 'r') as f:
        for line in f:
            line = line.rstrip().split(',')
            values = [float(x) for x in line]
            x_train.append(values[:6])
            y_train.append(values[6:])
x_train = np.array(x_train)
y_train = np.array(y_train)

model = tf.keras.models.Sequential([
    #tf.keras.layers.Input(shape=(6,)),
    tf.keras.layers.Dense(32, input_shape=(6,), activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(2, activation='sigmoid')
])
print(model.summary())

#loss_fn = tf.keras.losses.MeanAbsoluteError()
#loss_fn = tf.keras.losses.MeanSquaredLogarithmicError()
loss_fn = tf.keras.losses.MeanSquaredError()

#model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
model.compile(loss=loss_fn, metrics=['accuracy'])
model.fit(x=x_train, y=y_train, epochs=2000)
model.save('driving_nn_config.h5')
evaluation = model.evaluate(x_train, y_train, verbose=2)
print(evaluation)

for i in range(len(x_train)):
    print(model.predict(np.array([x_train[i]]))[0])
