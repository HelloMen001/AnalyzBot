from collections import Counter, defaultdict
import json
from LogWork import ColorLog_N, ParityLog_N, RangeLog_N

class ReactiveAnalyzer:
    def __init__(self,type,LenLog, triggers, min_count, min_probability):
        self.Log = self._load_history(type,LenLog)
        
        
        self.triggers = triggers         
        self.min_count = min_count            
        self.min_probability = min_probability
        
        self.patterns = []
        
    def _load_history(self,type,LenLog):
        if type == 'цвет':
            return ColorLog_N(LenLog)
        elif type == 'четность':
            return ParityLog_N(LenLog)
        elif type == 'диапазон':
            return RangeLog_N(LenLog)
        
    def analyze(self):
        results = defaultdict(list)
        self.patterns.clear()
        
        for trigger in self.triggers:
            t_len = len(trigger)
            for i in range(len(self.Log) - t_len):
                if self.Log[i:i + t_len] == trigger:
                    if i + t_len < len(self.Log):
                        next_value = self.Log[i + t_len]
                        results[tuple(trigger)].append(next_value)
                        
        
        for trigger,outcomes in results.items():
            if len(outcomes) < self.min_count:
                continue
                
            counter = Counter(outcomes)
            most_common, count = counter.most_common(1)[0]
                
            probability = count / len(outcomes)
            if probability < self.min_probability:
                continue
                
            coeff = round((probability - 0.5) * 10, 2)
                
            self.patterns.append({
                "триггер": list(trigger),
                "реакция": most_common,
                "вероятность": round(probability,2),
                "частота": count,
                "коэф": coeff
            })
    
    def save_patterns(self,filename):
        with open(filename,'w',encoding='utf-8') as f:
            json.dump(self.patterns,f, ensure_ascii=False, indent=2)
            
    def load_patterns(self,filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.patterns = json.load(f)
            
    def get_patterns(self):
        return self.patterns
    
    def predict(self):
        for pattern_info in sorted(self.patterns, key=lambda x: len(x['шаблон']), reverse=True):
            pattern = pattern_info['шаблон']
            if len(self.Log) < len(pattern):
                continue

            recent = tuple(self.Log[-len(pattern):])
            if recent == pattern:
                return {
                    'параметр': self.type,
                    'значение': pattern_info['следующее'],
                    'вероятность': pattern_info['вероятность'],
                    'модуль': 'ColorAnalyzer',
                    'коэф': pattern_info['коэф']
                }
        return None



#analyzer = ReactiveAnalyzer(
#    type='parity',
#    LenLog=3000,
#    triggers=default_triggers['parity'],
#    min_count=3,
#    min_probability=0.6
#)