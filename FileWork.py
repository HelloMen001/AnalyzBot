from file_read_backwards import FileReadBackwards


#Функции чтения файла
def read_counter():
    try:
        with open('counter.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

#Сохранение переменных в файл
def write_counter(value):
    with open('counter.txt', 'w') as f:
        f.write(str(value))
        
#Функция взятия N строк
def read_last_n_lines(filename,n):
    lines = []
    with FileReadBackwards(filename,encoding = 'utf-8') as frb:
        for line in frb:
            if line.split(" - ")[2].split(": ")[1].strip() !="🟢":
                lines.append(line.strip())
                if len(lines) >= n:
                    break
        return lines[::-1]
    