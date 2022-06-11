Пример запуска сервера:
---
uwsgi --ini myapp.ini  --callable app --processes 4 --threads 2

Использования клиента, создание endpoint:
---
/bin/python3 web_client.py create_endpoint endpoint_name

Отправка сообщения в лог:
---
/bin/python3 web_client.py echo_message endpoint_name code_returned_by_server text_of_message

