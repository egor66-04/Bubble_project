import subprocess
import time
import sys
import os

# --- ⚙️ ОБНОВЛЕННЫЕ НАСТРОЙКИ ---
REMOTE_USER = "root"
REMOTE_IP = "217.60.249.39"
SERVER_PASSWORD = "6=n5Ye7L1axcKKul"

# Порт, на котором сайт откроется в интернете (можно менять)
REMOTE_TUNNEL_PORT = "33333" 
# Порт, на котором запущен Django у тебя на ПК
LOCAL_PORT = "8000"
# -------------------------------

def create_vbs_script():
    """Создает скрипт, который сам нажмет клавиши для ввода пароля"""
    # StrictHostKeyChecking=no — чтобы не спрашивал yes/no при первом подключении
    ssh_command = f"ssh -o StrictHostKeyChecking=no -R {REMOTE_TUNNEL_PORT}:127.0.0.1:{LOCAL_PORT} -N {REMOTE_USER}@{REMOTE_IP}"
    
    vbs_content = f"""
    Set WshShell = WScript.CreateObject("WScript.Shell")
    
    ' Запускаем CMD с командой SSH
    WshShell.Run "cmd /k {ssh_command}", 9
    
    ' Ждем 2.5 секунды, пока сервер ответит
    WScript.Sleep 2500
    
    ' Вводим пароль (имитируем нажатия)
    WshShell.SendKeys "{SERVER_PASSWORD}"
    WshShell.SendKeys "{{ENTER}}"
    """
    
    with open("temp_auth.vbs", "w") as file:
        file.write(vbs_content)

def run_everything():
    django_process = None

    try:
        # 1. Запуск Django
        print(f"🚀 Запускаем Django (порт {LOCAL_PORT})...")
        django_cmd = [sys.executable, "manage.py", "runserver", LOCAL_PORT]
        django_process = subprocess.Popen(django_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        time.sleep(2) 

        # 2. Запуск SSH через VBS
        print(f"\n🤖 Подключаемся к {REMOTE_IP}...")
        print(f"⚠️  УБЕРИТЕ РУКИ ОТ КЛАВИАТУРЫ! ВВОЖУ ПАРОЛЬ...")
        
        create_vbs_script()
        
        # Запуск VBS (скрыто нажимает кнопки)
        subprocess.call("cscript //nologo temp_auth.vbs", shell=True)
        
        # Удаляем временный файл
        time.sleep(1)
        if os.path.exists("temp_auth.vbs"):
            os.remove("temp_auth.vbs")

        print(f"\n✅ Готово! Черное окно с SSH должно остаться открытым.")
        print(f"🌐 Твой сайт доступен здесь: http://{REMOTE_IP}:{REMOTE_TUNNEL_PORT}")
        print("⌨️  Нажми Ctrl+C здесь, чтобы выключить всё.\n")

        django_process.wait()

    except KeyboardInterrupt:
        print("\n👋 Остановка...")

    finally:
        if django_process:
            os.system(f"taskkill /F /PID {django_process.pid} >nul 2>&1")
        # Убиваем SSH
        os.system("taskkill /F /IM ssh.exe >nul 2>&1")
        if os.path.exists("temp_auth.vbs"):
            os.remove("temp_auth.vbs")

if __name__ == "__main__":
    run_everything()