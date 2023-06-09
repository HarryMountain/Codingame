import json
import os

import numpy as np
import tensorflow as tf

from CarDriving.NeuralNet import create_nn_from_json

# iterate over files in the directory of fitting data to get training data
x_train = []
y_train = []
directory = 'training_data'
#for filename in os.listdir(directory): todo
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
    tf.keras.layers.Dense(32, input_shape=(6,), activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    #tf.keras.layers.Dropout(0.2),
    #tf.keras.layers.Dense(20, activation='relu'),
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
print(model.summary())

# Output model config as JSON
model_dict = {}
layer_index = 0
for layer in model.layers:
    model_dict['Layer ' + str(layer_index)] = layer.get_config()
    weight_index = 0
    for weights in layer.get_weights():
        model_dict['Weights ' + str(layer_index) + ':' + str(weight_index)] = json.dumps(weights.tolist())
        weight_index += 1
    layer_index += 1

# Write out model parameters as JSON
json_file_name = 'saved_nn.json'
with open(json_file_name, "w") as json_file:
    json.dump(model_dict, json_file)

nn_from_file = create_nn_from_json(json_file_name)
total_eror = 0
for i in range(len(x_train)):
    in_memory_predict = model.predict(np.array([x_train[i]]))[0]
    from_file_predict = nn_from_file.evaluate(x_train[i])
    print(in_memory_predict, from_file_predict)
    for j in range(len(in_memory_predict)):
        total_eror += (in_memory_predict[j] - from_file_predict[j])**2
print('Total error : ' + str(total_eror))


#evaluation = model.evaluate(x_train, y_train, verbose=2)
#print(evaluation)

