# Задача 2
# Написать программу, которая будет синхронизировать два каталога: каталог-источник и каталог-реплику. Задача программы – приводить содержимое каталога-реплики в соответствие содержимому каталога-источника.
# Требования:
# 	•	Сихронизация должна быть односторонней: после завершения процесса синхронизации содержимое каталога-реплики должно в точности соответствовать содержимому каталогу-источника;
# 	•	Синхронизация должна производиться периодически;
# 	•	Операции создания/копирования/удаления объектов должны логироваться в файле и выводиться в консоль;
# 	•	Пути к каталогам, интервал синхронизации и` путь к файлу логирования должны задаваться параметрами командной строки при запуске программы.`

import os
import argparse
import time
import shutil
import logging
import hashlib

from os import walk

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-s", "--source", required=True, type=str, help="source directory")
parser.add_argument("-t", "--target", required=True, type=str, help="target directory")
parser.add_argument("-i", "--interval", required=True, type=int, help="sync period in sec")
parser.add_argument("-l", "--log", required=True, type=str, help="path to log file")

# Read arguments from command line
args = parser.parse_args()

# Configgure logger
logging.basicConfig(format=u'[%(asctime)s] %(message)s', level=logging.INFO, handlers=[
        logging.FileHandler(args.log),
        logging.StreamHandler()
    ])

def md5(fname):
    hash_md5 = hashlib.md5()
    hash_md5.update( open(fname,'rb').read() )
    return hash_md5.hexdigest()

def copy_file(file_names, source, _source, target):
    for file_name in file_names:
        # Source path
        s_path = source + '/' + file_name
        # Getting target path
        t_path = s_path.replace(_source, target)
        # If path is not exist
        if not (os.path.exists(t_path)):
            shutil.copy(s_path, t_path)
            logging.info(s_path + ' copied to ' + t_path)
        # If path is exist but md5 is not equal
        elif md5(s_path) != md5(t_path):
            shutil.copy(s_path, t_path)
            logging.info(s_path + ' copied to ' + t_path)

def delete_file(file_names, source, _target, target):
    for file_name in file_names:
        # Source path
        t_path = target + '/' + file_name
        # Getting target path
        s_path = t_path.replace(_target, source)
        # If path is not exist
        if not (os.path.exists(s_path)):
            os.remove(t_path)
            logging.info(t_path + ' removed ')

def walk_through_source(source, target):
    # While walk through, source is changing, need some const
    _source = source
    # Walk through source to copy/create objects at target
    for (source, dir_names, file_names) in walk(source):
        # if anydirs exists
        if len(dir_names) != 0:
            for dir_name in dir_names:
                # Source path to dir name
                s_path = source + '/' + dir_name
                # Getting target path
                t_path = s_path.replace(_source, target)
                # If dir is not exist
                if not (os.path.isdir(t_path)):
                    os.mkdir(t_path)
                    logging.info(s_path + ' created at ' + t_path)
                # If any files exist
                if len(file_names) != 0:
                    copy_file(file_names, source, _source, target)
        else:
            # If any files exist
            if len(file_names) != 0:
                copy_file(file_names, source, _source, target)

def walk_through_target(source, target):
    _target = target
    # Walk through target to remove objects from source
    for (target, dir_names, file_names) in walk(target):
        # if anydirs exists
        if len(dir_names) != 0:
            for dir_name in dir_names:
                # Target path to dir name
                t_path = target + '/' + dir_name
                # If dir is not exist at source
                s_path = t_path.replace(_target, source)
                if not (os.path.isdir(s_path)):
                    shutil.rmtree(t_path)
                    logging.info(t_path + ' removed ')
                # If any files exist
                if len(file_names) != 0:
                    delete_file(file_names, source, _target, target)
        else:
            # If any files exist
            if len(file_names) != 0:
                delete_file(file_names, source, _target, target)

def sync(source, target):
    walk_through_source(source, target)
    walk_through_target(source, target)
    
while True:
  sync(args.source, args.target)
  time.sleep(args.interval)