# Задача 1
# Написать программу, которая будет запускать процесс и с указанным интервалом времени собирать о нём следующую статистику:
# Загрузка CPU (в процентах);
# Потребление памяти: Working Set и Private Bytes (для Windows-систем) или Resident Set Size и Virtual Memory Size (для Linux-систем);
# Количество открытых хендлов (для Windows-систем) или файловых дескрипторов (для Linux-систем).
# Сбор статистики должен осуществляться всё время работы запущенного процесса. 
# Путь к файлу, который необходимо запустить, и интервал сбора статистики должны указываться пользователем. Собранную статистику необходимо сохранить на диске. 
# Представление данных должно в дальнейшем позволять использовать эту статистику для автоматизированного построения графиков потребления ресурсов.

import argparse
import os
import psutil
import time
import csv
import datetime

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-p", "--path", required=True, type=str, help="save output to file")
parser.add_argument("-i", "--interval", required=True, type=int, help="stat collection time interval")

# Read arguments from command line
args = parser.parse_args()

# Open file
def open_file(path):
    try: 
        return open(path, 'w')
    except Exception as error:
        print(error)

# Write a header
def write_header(writer):
    try:
        writer.writerow(['time', 'CPU_usage', 'RSS_bytes', 'VMS_bytes', 'File_Descriptor_number'])
    except Exception as error:
        print(error)

def monitor_process(path):
    # Open file
    with open(path, 'a+') as f:
        # Open writer
        writer = csv.writer(f)
        try:        
            writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), process.cpu_percent(interval=0.1), process.memory_info().rss, process.memory_info().vms, file_descriptors(process.open_files())])
        except Exception as error:
            print(error)

# Count file descriptors
def file_descriptors(open_files):
    try:
        print(len(open_files))
        for f in open_files:
            print(f)
            print(f.fd)
            sum_fd = f.fd
        return sum_fd
    except Exception as error:
        print(error)

# Getting process details
process = psutil.Process(os.getpid())

# Getting period in seconds from args
interval = args.interval

with open(args.path, 'w') as f:
    # Open and write header
    write_header(csv.writer(f))

while True:
    monitor_process(args.path)
    time.sleep(args.interval)
