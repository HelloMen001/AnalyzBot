from FileWork import read_last_n_lines
from config import fileN


def ColorLog_N(n):
    Log = read_last_n_lines(fileN,n)
    ColorLog = []
    for line in Log:
        color_part = line.split(" - ")[2]
        color = color_part.split(": ")[1].strip()
        if color == "🔴":
            ColorLog.append("К")
        else:
            ColorLog.append("Ч")
    return ColorLog


def ParityLog_N(n):
    Log = read_last_n_lines(fileN,n)
    ParityLog = []
    for line in Log:
        Parity_part = line.split(" - ")[4]
        Parity = Parity_part.split(": ")[1].strip()
        if Parity == "1":
            ParityLog.append("even")
        else:
            ParityLog.append("odd")
    return ParityLog


def RangeLog_N(n):
    Log = read_last_n_lines(fileN,n)
    RangeLog = []
    for line in Log:
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        if 1<=number<=12:
            RangeLog.append("LOW")
        elif 13<=number<=24:
            RangeLog.append("MID")
        else:
            RangeLog.append("HIGH")
    return RangeLog


def NumberLog_N(n):
    Log = read_last_n_lines(fileN,n)
    NumberLog = []
    
    for line in Log:
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        
        NumberLog.append(number)
    
    return NumberLog


def ComboColorParity_N(n):
    Log = read_last_n_lines(fileN,n)
    ComboColorParityLog = []
    for line in Log:
        Combo = ""
        
        color_part = line.split(" - ")[2]
        color = color_part.split(": ")[1].strip()
        if color == "🔴":
            Combo += "К"
        else:
            Combo += "Ч"
            
        Parity_part = line.split(" - ")[4]
        Parity = Parity_part.split(": ")[1].strip()
        if Parity == "1":
            Combo += "even"
        else:
            Combo += "odd"
        ComboColorParityLog.append(Combo)
    return ComboColorParityLog


def ComboColorRange_N(n):
    Log = read_last_n_lines(fileN,n)
    ComboColorRangeLog = []
    for line in Log:
        Combo = ""
        
        color_part = line.split(" - ")[2]
        color = color_part.split(": ")[1].strip()
        if color == "🔴":
            Combo += "К"
        else:
            Combo += "Ч"
            
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        if 1<=number<=12:
            Combo += "LOW"
        elif 13<=number<=24:
            Combo += "MID"
        else:
            Combo += "HIGH"
            
        ComboColorRangeLog.append(Combo)
    return ComboColorRangeLog


def ComboParityRange_N(n):
    Log = read_last_n_lines(fileN,n)
    ComboParityRangeLog = []
    for line in Log:
        Combo = ""
        
        Parity_part = line.split(" - ")[4]
        Parity = Parity_part.split(": ")[1].strip()
        if Parity == "1":
            Combo += "even"
        else:
            Combo += "odd"
            
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        if 1<=number<=12:
            Combo += "LOW"
        elif 13<=number<=24:
            Combo += "MID"
        else:
            Combo += "HIGH"
            
        ComboParityRangeLog.append(Combo)
    return ComboParityRangeLog
        
        
def ComboColorParityRange_N(n):
    Log = read_last_n_lines(fileN,n)
    ComboColorParityRangeLog = []
    for line in Log:
        Combo=""
        
        color_part = line.split(" - ")[2]
        color = color_part.split(": ")[1].strip()
        if color == "🔴":
            Combo += "К"
        else:
            Combo += "Ч"
            
        Parity_part = line.split(" - ")[4]
        Parity = Parity_part.split(": ")[1].strip()
        if Parity == "1":
            Combo += "even"
        else:
            Combo += "odd"
            
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        if 1<=number<=12:
            Combo += "LOW"
        elif 13<=number<=24:
            Combo += "MID"
        else:
            Combo += "HIGH"
            
        ComboColorParityRangeLog.append(Combo)
    return ComboColorParityRangeLog



def Ai_Log_N(n):
    Log = read_last_n_lines(fileN,n)
    Log_Data = []
    
    for line in Log:
        Data = []
        color_part = line.split(" - ")[2]
        color = color_part.split(": ")[1].strip()
        if color == "🔴":
            Data.append("К")
        else:
            Data.append("Ч")
            
        Parity_part = line.split(" - ")[4]
        Parity = Parity_part.split(": ")[1].strip()
        if Parity == "1":
            Data.append("even")
        else:
            Data.append("odd")
            
        number_part = line.split(" - ")[3]
        number = int(number_part.split(": ")[1].strip())
        if 1<=number<=12:
            Data.append("LOW")
        elif 13<=number<=24:
            Data.append("MID")
        else:
            Data.append("HIGH")
            
        Data.append(number)
        Log_Data.append(Data)
    return Log_Data