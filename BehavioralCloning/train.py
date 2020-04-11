from data_processing import get_data_generators

from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Activation, Flatten, Dropout, Lambda
from keras.layers import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.advanced_activations import ELU, ReLU
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, Callback



def create_model():
    model = Sequential()

    # Add three 5x5 convolution layers (output depth 24, 36, and 48), each with 2x2 stride
    model.add(Conv2D(128, (2, 2), input_shape=(160, 320, 1)))
    model.add(Activation('relu'))
    model.add(Conv2D(128, (2, 2)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (2, 2)))
    model.add(Activation('relu'))

    #model.add(Dropout(0.50))
    
    # # Add two 3x3 convolution layers (output depth 64, and 64)
    # model.add(Conv2D(64, (3, 3)))
    # model.add(Activation('relu'))
    # model.add(Conv2D(64, (3, 3)))
    # model.add(Activation('relu'))

    # Add a flatten layer
    model.add(Flatten())

    # Add three fully connected layers (depth 100, 50, 10), tanh activation (and dropouts)
    model.add(Dense(100))
    model.add(Activation('relu'))
    #model.add(Dropout(0.50))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dropout(0.50))
    model.add(Dense(10))
    model.add(Activation('relu'))
    #model.add(Dropout(0.50))

    # Add a fully connected output layer
    model.add(Dense(1))

    model.compile(optimizer=Adam(lr=1e-4), loss='mse')

    return model

def train_model(model, train_gen, val_gen, steps):

    filepath = "model-{epoch:02d}-{val_accuracy:.2f}.h5"
    checkpoint = ModelCheckpoint(filepath) 

    history = model.fit_generator(train_gen, epochs=3, steps_per_epoch=steps)



def main():
    train_gen, val_gen, steps = get_data_generators(32)

    model = create_model()
    
    train_model(model, train_gen, val_gen, steps)

if __name__=='__main__':
    main()