from config import rand
import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense
from keras.utils import to_categorical
from keras.models import load_model

from LogWork import Ai_Log_N

class MultiTargetAIModule:
    def __init__(self, window_size, model_file="AI/ai_model_multi.keras"):
        
        self.raw_log = Ai_Log_N(rand)
        self.window_size = window_size
        self.model_file = model_file
        self.model = None

        self.color_map = {'К': 0, 'Р': 1}
        self.parity_map = {'even': 0, 'odd': 1}
        self.range_map = {'LOW': 0, 'MID': 1, 'HIGH': 2}

    def encode(self, entry):
        color = self.color_map.get(entry[0], 0)
        parity = self.parity_map.get(entry[1], 0)
        zone = self.range_map.get(entry[2], 1)
        number = int(entry[3]) / 36
        return [color, parity, zone, number]

    def prepare_data(self):
        encoded_log = [self.encode(entry) for entry in self.raw_log]
        if len(encoded_log) <= self.window_size:
            return None
        
        X, y_color, y_parity, y_range, y_number = [], [], [], [], []
        for i in range(len(encoded_log) - self.window_size):
            X.append(encoded_log[i:i+self.window_size])
            next_entry = self.raw_log[i + self.window_size]
            y_color.append(to_categorical(self.color_map.get(next_entry[0], 0), num_classes=2))
            y_parity.append(to_categorical(self.parity_map.get(next_entry[1], 0), num_classes=2))
            y_range.append(to_categorical(self.range_map.get(next_entry[2], 1), num_classes=3))
            y_number.append(int(next_entry[3]) / 36)

        return (
            np.array(X),
            {
                "color": np.array(y_color),
                "parity": np.array(y_parity),
                "range": np.array(y_range),
                "number": np.array(y_number),
            }
        )

    def build_model(self):
        inputs = Input(shape=(self.window_size, 4))
        x = LSTM(64)(inputs)

        out_color = Dense(2, activation='softmax', name="color")(x)
        out_parity = Dense(2, activation='softmax', name="parity")(x)
        out_range = Dense(3, activation='softmax', name="range")(x)
        out_number = Dense(1, name="number")(x)

        self.model = Model(inputs=inputs, outputs=[out_color, out_parity, out_range, out_number])
        self.model.compile(
            optimizer='adam',
            loss={
                "color": "categorical_crossentropy",
                "parity": "categorical_crossentropy",
                "range": "categorical_crossentropy",
                "number": "mean_squared_error"
            }
        )

    def train(self, epochs=10):
        result = self.prepare_data()
        if result is None:
            print("Недостаточно данных для обучения.")
            return
        
        X, y = self.prepare_data()
        self.build_model()
        self.model.fit(X, y, epochs=epochs, verbose=1)
        self.model.save(self.model_file)

    def load(self):
        self.model = load_model(self.model_file)

    def predict(self):
        if self.model is None:
            return []
        recent = self.raw_log[-self.window_size:]
        if len(recent) < self.window_size:
            return []

        input_data = np.array([self.encode(entry) for entry in recent])
        input_data = np.reshape(input_data, (1, self.window_size, 4))
        prediction = self.model.predict(input_data, verbose=0)

        results = []

        color_idx = np.argmax(prediction[0])
        results.append({
            "параметр": "цвет",
            "значение": "К" if color_idx == 0 else "Ч",
            "уверенность": float(prediction[0][0][color_idx]),
            "модуль": self.__class__.__name__
        })

        parity_idx = np.argmax(prediction[1])
        results.append({
            "параметр": "четность",
            "значение": "even" if parity_idx == 0 else "odd",
            "уверенность": float(prediction[1][0][parity_idx]),
            "модуль": self.__class__.__name__
        })

        range_idx = np.argmax(prediction[2])
        results.append({
            "параметр": "диапазон",
            "значение": ["LOW", "MID", "HIGH"][range_idx],
            "уверенность": float(prediction[2][0][range_idx]),
            "модуль": self.__class__.__name__
        })

        results.append({
            "параметр": "число",
            "значение": round(prediction[3][0][0] * 36),
            "уверенность": 1.0,
            "модуль": self.__class__.__name__
       })

        return results

