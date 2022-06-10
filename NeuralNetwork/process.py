from keras.datasets import mnist
from keras.models import Model, load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Input
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.layers.core import Lambda
from keras import backend as K
import numpy as np
import os
import matplotlib.pyplot as plt
from dataBase import dataHandle

#主流程
def mainProcess():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    random_index = np.random.randint(len(x_test), size=1)#隨機取數(array型態)

    #儲存圖片
    saveImage(x_test, random_index)

    #使用模型
    x_test = x_test.reshape(10000, 28, 28, 1)
    result_array = useModel(x_test, y_test, random_index)

    #寫入DB
    dataHandle(result_array)

    return result_array

#儲存圖片
def saveImage(x_test, random_index):
    image_path = '/app/img/num_' + str(random_index[0]) + '.png'
    plt.imsave(image_path, x_test[random_index[0]], cmap='Greys')#存取圖片

#使用模型
def useModel(x_test, y_test, random_index):
    VAE = Model()
    model_file_name = "handwriting_VAE.h5"
    file_path = "/app/" + model_file_name
    if os.path.isfile(file_path):
        VAE = load_model(model_file_name)
    else:
        VAE = createModel()
    VAE = load_model(model_file_name)

    #判斷是否預測成功
    predict_result = 0#預設預測失敗
    if(np.int64(y_test[random_index[0]]) == np.argmax(VAE.predict(x_test[random_index]))):
        predict_result = 1#預測成功

    #回傳資料
    result_array = [np.argmax(VAE.predict(x_test[random_index])), y_test[random_index[0]],
                    random_index[0], predict_result]

    return result_array

def createModel():
    #取訓練資料
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    #資料轉型
    x_train = x_train.reshape(60000, 28, 28, 1)
    y_train = np_utils.to_categorical(y_train, 10)

    #Convolution
    f_1 = Conv2D(32, (3,3), padding='same', input_shape=(28, 28, 1), activation='relu')
    f_mp1 = MaxPooling2D(pool_size=(2,2))
    f_2 = Conv2D(64, (3,3), padding='same', input_shape=(28, 28, 1), activation='relu')
    f_mp2 = MaxPooling2D(pool_size=(2,2))
    f_3 = Conv2D(128, (3,3), padding='same', input_shape=(28, 28, 1), activation='relu')
    f_mp3 = MaxPooling2D(pool_size=(2,2))
    f_fl = Flatten()

    #Encode layers
    enc_1 = Dense(200, activation='relu')
    enc_mean = Dense(2)
    enc_log_var = Dense(2)

    #Decode layers
    dec_1 = Dense(200, activation='relu')
    dec_2 = Dense(10, activation='softmax')

    #建立Model
    x = Input(shape=(28, 28, 1))
    z_1 = f_1(x)
    z_2 = f_2(f_mp1(z_1))
    z_3 = f_3(f_mp2(z_2))
    z_4 = f_fl(f_mp3(z_3))
    enc_x = enc_1(z_4)
    z_mean = enc_mean(enc_x)
    z_log_var = enc_log_var(enc_x)

    z = Lambda(sampling, output_shape=(2,))([z_mean, z_log_var])
    dec_x1 = dec_1(z)
    dec_x2 = dec_2(dec_x1)

    VAE = Model(x, dec_x2)
    VAE.compile(loss='mse', optimizer=SGD(lr=0.01), metrics=['accuracy'])
    VAE.fit(x_train, y_train, batch_size=32, epochs=10)
        
    #儲存Weights,Ｍodel
    VAE.save_weights("handwriting_VAE_weights.h5")
    #open("handwriting_VAE.json", 'w').write(VAE.to_json())
    VAE.save("handwriting_VAE.h5")

    return VAE

#抽樣模型
def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(2,), mean=0., stddev=1)

    return z_mean + K.exp(z_log_var / 2) * epsilon