Пример запуск скрипта:
---
/bin/python3 task1.py -p test.csv -i 2

Для сбора статистики был использован psutil.
cpu_percent может вернуть значение больше 100:
---
A value > 100.0 can be returned in case of processes running multiple threads on different CPU cores.