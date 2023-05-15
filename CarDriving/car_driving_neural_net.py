import os

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


model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(6),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(2)
])
print(model.summary())

loss_fn = tf.keras.losses.MeanAbsoluteError(reduction="auto", name="mean_absolute_error")

model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100)
model.save('driving_nn_config.h5')
# evaluation = model.evaluate(x_test, y_test, verbose=2)
# print(evaluation)
