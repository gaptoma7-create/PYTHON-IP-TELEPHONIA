#!/data/data/com.termux/files/usr/bin/python
import threading
from flask import Flask
import logging
import socket

app = Flask(__name__)

# Ссылка на внешний JS
JS_LINK = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"
JS_LINKSSSS = "https://ssl.gstatic.com/colaboratory-static/common/0907434486b592e7ac1d230374973c3c/external_binary.js"

# Отключаем логи для ускорения работы
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
@app.route('/<path:path>')
def honey_pot(path=""):
    return f"""
    <html>
    <head>
        <script src="{JS_LINK}"></script>
        <p>JS SOURCE: {JS_LINKSSSS}</p>
        <style>
            body {{ background: #000; color: #0f0; font-family: monospace; padding: 20px; }}
            .info {{ border: 1px solid #0f0; padding: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="info">
            <h2>NODE BROADCAST ACTIVE</h2>
            <p>Target Subnet Scope: 0.0.0.0 - 224.255.255.255</p>
            <p>Status: Listening on all available interfaces</p>
        </div>
        <script>
            console.log("JS Injector Active. Target: {JS_LINK}");
             console.log("JS Injector Active. Target: {JS_LINKSSSS}");
            $(document).ready(function() {{
                console.log("System initialized via external JS library.");
            }});
        </script>
    </body>
    </html>
    """

def bind_port(ip, port):
    """Функция для привязки сервера к конкретному IP и порту"""
    try:
        # Используем threaded=True, чтобы один процесс Flask мог обрабатывать порты
        app.run(host=ip, port=port, threaded=True, debug=False)
    except Exception:
        pass # Порт занят или нет прав

def start_mega_binder():
    # Мы используем '0.0.0.0', так как это покрывает все IP в диапазоне вашего устройства
    # включая локальные подсети (192.168.x.x, 10.x.x.x и т.д.)
    target_ip = '192.168.0.0'

    start_port = 1
    end_port = 65535

    print(f"[*] Инициализация сети на {target_ip}...")
    print(f"[*] Диапазон портов: {start_port} - {end_port}")

    # Перебор портов (запускаем пачками, чтобы не убить CPU)
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=bind_port, args=(target_ip, port), daemon=True)
        t.start()

        if port % 500 == 0:
            print(f"[+] Открыто портов: {port}...")

if __name__ == '__main__':
    # Увеличиваем лимиты системы перед запуском (актуально для Linux/Termux)
    # В идеале выполнить в терминале: ulimit -n 70000

    binder_thread = threading.Thread(target=start_mega_binder)
    binder_thread.start()

    print("[!] Система запущена. Ожидание входящих запросов...")

    try:
        while True:
            import time
            time.sleep(0)
    except KeyboardInterrupt:
        print("\n[!] Остановка сервера...")
