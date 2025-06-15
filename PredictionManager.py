import config
from telethon import events
from Analyzer.ColorAnalyzer import ColorAnalyzer
from Analyzer.ParityAnalyzer import ParityAnalyzer
from Analyzer.RangeAnalyzer import RangeAnalyzer
from Analyzer.NumberAnalyzer import NumberAnalyzer
from Analyzer.ComboAnalyzer import ComboAnalyzer
from Analyzer.ReactiveAnalyzer import ReactiveAnalyzer
from Analyzer.AI_Module.AI_AllTargetModule import MultiTargetAIModule
from Analyzer.AI_Module.AI_ColorModule import AI_ColorModule
from Analyzer.AI_Module.AI_NumberModule import AI_NumberModule
from Analyzer.AI_Module.AI_ParityModule import AI_ParityModule
from Analyzer.AI_Module.AI_RangeModule import AI_RangeModule

import os  
import json

manager_instance = None
round_counter = 0

class PredictionManager:
    def __init__(self, client, chat_id):
        self.client = client
        self.chat_id = chat_id
        self.mode = config.DECISION_MODE
        self.prediction_enabled = False
        
        self.analyze_intervals = {
            'ColorAnalyzer': 1,
            'ParityAnalyzer': 1,
            'RangeAnalyzer': 1,
            'NumberAnalyzer': 1,
            'ComboAnalyzer': 1,
            'ReactiveAnalyzer': 1,
        }
        self.ai_retrain_interval = 1
        
        self.analyzers = [
            ColorAnalyzer(config.ColorLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity),
            ParityAnalyzer(config.ParityLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity),
            RangeAnalyzer(config.RangeLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity),
            NumberAnalyzer(config.NumberLenLog, config.NumberLenPattern, config.min_count, config.min_probabi1lity),
            ComboAnalyzer(config.ComboLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity,"ColorParity"),
            ComboAnalyzer(config.ComboLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity,"ColorRange"),
            ComboAnalyzer(config.ComboLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity,"ParityRange"),
            ComboAnalyzer(config.ComboLenLog, config.min_pattern_len, config.max_pattern_len, config.min_count, config.min_probabi1lity,"ColorParityRange"),
            ReactiveAnalyzer('цвет', config.ReactiveLenLog,config.default_triggers, config.min_count, config.min_probabi1lity),
            ReactiveAnalyzer('четность', config.ReactiveLenLog,config.default_triggers, config.min_count, config.min_probabi1lity),
            ReactiveAnalyzer('диапазон', config.ReactiveLenLog,config.default_triggers, config.min_count, config.min_probabi1lity),
            MultiTargetAIModule(window_size=config.AiWindow),
            AI_ColorModule(window_size=config.AiWindow),
            AI_ParityModule(window_size=config.AiWindow),
            AI_RangeModule(window_size=config.AiWindow),
            AI_NumberModule(window_size=config.AiWindow),
        ]

    def is_enabled(self):
        return self.prediction_enabled

    def toggle_prediction(self):
        self.prediction_enabled = not self.prediction_enabled
        return self.prediction_enabled

    def analyze_all(self):
        global round_counter
        round_counter += 1

        for analyzer in self.analyzers:
            name = analyzer.__class__.__name__
            if name in self.analyze_intervals:
                interval = self.analyze_intervals[name]
                if round_counter % interval == 0:
                    try:
                        analyzer.analyze()
                        if hasattr(analyzer, 'save_patterns'): 
                            filename = f"patterns/{name}.json"
                            os.makedirs("patterns", exist_ok=True)
                            analyzer.save_patterns(filename)
                    except Exception as e:
                        print(f"Ошибка анализа в {name}: {e}")

        if round_counter % self.ai_retrain_interval == 0:
            for analyzer in self.analyzers:
                if hasattr(analyzer, 'train'):
                    try:
                        analyzer.train()
                        print(f"ИИ модуль {analyzer.__class__.__name__} переобучен")
                    except Exception as e:
                        print(f"Ошибка переобучения {analyzer.__class__.__name__}: {e}")

    def get_all_predictions(self):
        results = []
        for analyzer in self.analyzers:
            try:
                predictions = analyzer.predict()
                if isinstance(predictions, list):
                    results.extend(predictions)
                else:
                    results.append(predictions)
            except Exception as e:
                print(f"Ошибка в {analyzer.__class__.__name__}: {e}")
        return results

    def combine_predictions(self, target_param):
        predictions = self.get_all_predictions()
        filtered = [p for p in predictions if p and p['параметр'] == target_param]
        if not filtered:
            return None

        if self.mode == 'единогласие':
            values = set(p['значение'] for p in filtered)
            return filtered[0]['значение'] if len(values) == 1 else None

        elif self.mode == 'взвешенный':
            score = {}
            for p in filtered:
                val = p['значение']
                weight = config.MODULE_WEIGHTS.get(p['модуль'], 1)
                conf = p.get('уверенность', 1)
                score[val] = score.get(val, 0) + weight * conf
            return max(score, key=score.get)

        elif self.mode == 'большинство':
            count = {}
            for p in filtered:
                val = p['значение']
                count[val] = count.get(val, 0) + 1
            return max(count, key=count.get)

        else:
            raise ValueError(f"Неизвестный режим: {self.mode}")

    def run_prediction(self, new_data):
        if not self.prediction_enabled:
            return None

        return {
            'цвет': self.combine_predictions('цвет'),
            'четность': self.combine_predictions('четность'),
            'диапазон': self.combine_predictions('диапазон'),
            'число': self.combine_predictions('число')
        }
    
    def load_all_patterns(self):
        for analyzer in self.analyzers:
            name = analyzer.__class__.__name__
            if hasattr(analyzer, 'load_patterns'):
                try:
                    filename = f"patterns/{name}.json"
                    if os.path.exists(filename):
                        analyzer.load_patterns(filename)
                        print(f"Загружены шаблоны из {filename}")
                except Exception as e:
                    print(f"Ошибка загрузки шаблонов {name}: {e}")



async def PredictionManagerSetup(client, chat_id):
    global manager_instance
    manager_instance = PredictionManager(client, chat_id)

    @client.on(events.NewMessage(chats=chat_id, pattern='(?i)^/предскажи$'))
    async def handle_predict(event):
        if not manager_instance:
            await event.respond("Менеджер не инициализирован")
            return
        predictions = manager_instance.run_prediction(new_data={})
        if predictions:
            text = "\n".join(f"{k.title()}: {v}" for k, v in predictions.items() if v)
            await event.respond(f"🔮 Предсказание:\n{text}")
        else:
            await event.respond("Нет доступных предсказаний")

    @client.on(events.NewMessage(chats=chat_id, pattern='(?i)^/анализируй$'))
    async def handle_analyze(event):
        if not manager_instance:
            await event.respond("Менеджер не инициализирован")
            return
        manager_instance.analyze_all()
        await event.respond("✅ Все модули проанализировали и обновили шаблоны")

    @client.on(events.NewMessage(chats=chat_id, pattern='(?i)^/переключи$'))
    async def toggle_prediction(event):
        state = manager_instance.toggle_prediction()
        status = "🔮 Прогноз ВКЛЮЧЕН" if state else "🔕 Прогноз ВЫКЛЮЧЕН"
        await event.respond(status)

    @client.on(events.NewMessage(chats=chat_id, pattern='(?i)^/выгрузи$'))  # ← ДОБАВЛЕНО: команда загрузки шаблонов
    async def handle_load_patterns(event):
        if not manager_instance:
            await event.respond("Менеджер не инициализирован")
            return
        manager_instance.load_all_patterns()
        await event.respond("📥 Все шаблоны загружены из файлов")