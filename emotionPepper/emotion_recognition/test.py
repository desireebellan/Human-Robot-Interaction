# to use CPU
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf

config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=5,
                        inter_op_parallelism_threads=5, 
                        allow_soft_placement=True,
                        device_count = {'CPU' : 1,
                                        'GPU' : 0}
                       )
from emotion_recognition.model import get_model_emotions
from emotion_recognition.utils import clean_text, tokenize_words
from emotion_recognition.config import embedding_size, sequence_length
from emotion_recognition.preprocess import categories
from keras.preprocessing.sequence import pad_sequences


import pickle

path=os.path.abspath('.')+'/emotion_recognition/'

print("Loading vocab2int")
vocab2int = pickle.load(open(path+"data/vocab2int.pickle", "rb"))
model = get_model_emotions(len(vocab2int), sequence_length=sequence_length, embedding_size=embedding_size)
model.load_weights(path+"results/model_v1_0.68_0.74.h5")
model.save('my_model.h5')

def predict_emotion(text,emotion):
    tf.keras.backend.clear_session()
    
    graph = tf.compat.v1.get_default_graph()
    text = tokenize_words(clean_text(text), vocab2int)
    x = pad_sequences([text], maxlen=sequence_length)

    new_model = tf.keras.models.load_model('my_model.h5')
    #prediction = new_model.predict_classes(x)[0]
    
    probs = new_model.predict(x)[0]
    print(emotion)
    print("Probs:")
    for i, category in categories.items():
        print("{} : {:.2f}%".format(category.capitalize(),probs[i]*100))
        if category == emotion:
            index = i
    #print("The most dominant:", categories[prediction])
    return probs[index]
