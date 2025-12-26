# TestSetup.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import uuid
import os
import shutil
import psutil
import sys

class TestSetup_A:
    def __init__(self):

        self.close_existing_chrome()
        # Создаем уникальную директорию
        user_data_dir = f"/tmp/chrome-{uuid.uuid4()}"
        os.makedirs(user_data_dir, exist_ok=True)

        chrome_options = Options()
        if sys.platform == 'win32':
            chrome_options.add_argument(r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data')
            chrome_options.add_argument('--profile-directory=Profile 1')
            chrome_options.add_argument(r'--load-extensions=C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 1\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.92.10_0 ')
        else:
            chrome_options.add_argument('--no-sandbox')  # Отключение песочницы безопасности
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument('--disable-dev-shm-usage')  # Устранение проблем с ресурсами
            chrome_options.add_argument("--headless=new")
        # Настройки для работы в Docker


        # Убираем следующие строки, так как они не будут работать в Docker:


        self.driver_a = webdriver.Chrome(
        #    service=Service('/usr/local/bin/chromedriver'),  # Путь внутри Docker-контейнера //
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )


        self.driver_a.set_page_load_timeout(10)

    def close_existing_chrome(self):
        # Получаем все процессы Chrome
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == 'chrome':
                    print(f"Завершаем процесс Chrome с PID: {proc.info['pid']}")
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def get(self, url):
        self.driver_a.get(url)

    def quit(self):
        self.driver_a.quit()  # Добавлен корректный метод закрытия


