from collections import Counter, defaultdict
import json
from LogWork import ParityLog_N

class ParityAnalyzer:
    def __init__(self, LenParityLog, min_pattern_len, max_pattern_len, min_count, min_probability):
        self.Log = ParityLog_N(LenParityLog)
        
        self.min_len = min_pattern_len        
        self.max_len = max_pattern_len        
        self.min_count = min_count            
        self.min_probability = min_probability
        
        self.patterns = []
        
    def analyze(self):
        pattern_data = defaultdict(list)
        self.patterns.clear()
        
        for n in range(self.min_len,self.max_len+1):
            for i in range(len(self.Log)-n):
                pattern = tuple(self.Log[i:i+n])
                next_parity = self.Log[i+n]
                pattern_data[pattern].append(next_parity)
            
        
        for pattern,results in pattern_data.items():
            if len(results) < self.min_count:
                continue
                
            counter = Counter(results)
            most_parity, count = counter.most_common(1)[0]
                
            probability = count / len(results)
            if probability < self.min_probability:
                continue
                
            coeff = round((probability - 0.5) * 10, 2)
                
            self.patterns.append({
                "шаблон": pattern,
                "следующее": most_parity,
                "вероятность": probability,
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
                    'параметр': 'четность',
                    'значение': pattern_info['следующее'],
                    'вероятность': pattern_info['вероятность'],
                    'модуль': 'ColorAnalyzer',
                    'коэф': pattern_info['коэф']
                }
        return None