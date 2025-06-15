from config import rand
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from keras.utils import to_categorical

from LogWork import Ai_Log_N

class AI_ParityModule:
    def __init__(self,window_size,model_file='AI/AI_ParityModel.keras'):
        
        self.raw_log =  Ai_Log_N(rand)
        self.window_size = window_size
        self.model_file = model_file
        self.model = None
        
        self.color_map = {'К':0, 'Ч':1}
        self.parity_map = {'even':0,'odd':1}
        self.range_map = {'LOW':0,'MID':1,'HIGH':2}
        
    def encode(self,entry):
        
        color = self.color_map.get(entry[0], 0)
        parity = self.parity_map.get(entry[1],0)
        zone = self.range_map.get(entry[2],0)
        number = int(entry[3]) / 36
        return [color,parity,zone,number]
    
    def prepare_data(self):
        
        encoded_log = [self.encode(entry) for entry in self.raw_log]
        if len(encoded_log) <= self.window_size:
            return None
        
        x,y = [],[]
        for i in range(len(encoded_log) - self.window_size):
            x.append(encoded_log[i:i+self.window_size])
            y.append(self.parity_map.get(self.raw_log[i+self.window_size][1],0))
        x = np.array(x)
        y = to_categorical(y,num_classes=2)
        return x, y
        
    def build_model(self):
        
        self.model = Sequential()
        self.model.add(LSTM(64,input_shape=(self.window_size,4)))
        self.model.add(Dense(2, activation='softmax'))
        self.model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
        
    def train(self,epochs=10):
        result = self.prepare_data()
        if result is None:
            print("Недостаточно данных для обучения.")
            return
        
        x,y = self.prepare_data()
        self.build_model()
        self.model.fit(x,y, epochs=epochs,verbose=1)
        self.model.save(self.model_file)
        
    def load(self):
        
        self.model = load_model(self.model_file)
        
    def predict(self):
        if self.model is None:
            return None
        recent = self.raw_log[-self.window_size:]
        if len(recent) < self.window_size:
            return None

        input_data = np.array([self.encode(entry) for entry in recent])
        input_data = np.reshape(input_data, (1, self.window_size, 4))
        prediction = self.model.predict(input_data, verbose=0)
        predicted_class = np.argmax(prediction[0])

        return {
            "параметр": "четность",
            "значение": "even" if predicted_class == 0 else "odd",
            "уверенность": float(prediction[0][predicted_class]),
            "модуль": self.__class__.__name__
       }