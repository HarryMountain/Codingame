import base64
import pickle
import zlib
import tensorflow as tf

# Load NN
model = tf.keras.models.load_model('driving_nn_config.h5')

model.save('test_nn_save')

'''
# Save as binary to file
file_to_save_nn = open('pickled_nn.sav', 'wb')
pickle.dump(model, file_to_save_nn)
file_to_save_nn.close()

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

xx = tf.keras.utils.serialize_keras_object(model)
print(xx)
'''
x = base64.b64encode(zlib.compress(pickle.dumps(model)))
print(x)
