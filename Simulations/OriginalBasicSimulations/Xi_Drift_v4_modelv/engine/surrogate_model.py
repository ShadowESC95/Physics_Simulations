import tensorflow as tf
from tensorflow.keras.layers import Conv2D, LSTM, Dense

class FieldSurrogate(tf.keras.Model):
    def __init__(self, grid_size=64):
        super().__init__()
        self.encoder = tf.keras.Sequential([
            Conv2D(32, 3, activation='gelu', padding='same', input_shape=(grid_size, grid_size, 1)),
            Conv2D(64, 3, activation='gelu', padding='same'),
            Conv2D(128, 3, activation='gelu', padding='same')
        ])
        self.lstm = LSTM(128, return_sequences=True)
        self.decoder = Conv2D(1, 3, activation='linear', padding='same')
        
    def call(self, inputs):
        x = self.encoder(inputs)
        x = self.lstm(x)
        return self.decoder(x)
    
    def train_step(self, xi_prev, xi_next):
        with tf.GradientTape() as tape:
            pred = self(xi_prev)
            loss = tf.reduce_mean((pred - xi_next)**2)
        grads = tape.gradient(loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        return loss
