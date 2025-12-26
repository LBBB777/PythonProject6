import unittest
import TestSetup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.profile
import time
# from TestSetup import TestSetup     #  слева имя файла (без расширения .py)   справа - имя класса внутри этого файла
import allure


class TestEffectiveMobile(unittest.TestCase):

    def setUp(self):
        self.test_setup = TestSetup.TestSetup()

    #     # Настройка драйвера
    #     #service = Service("D:/po/ChromeDriver/chromedriver-win64/chromedriver.exe")
    #
    #     chrome_options = Options()
    # # C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.92.10_0
    #
    #     #profile = "C:/Users/USER/AppData/Local/Google/Chrome/User Data/Default"
    #     chrome_options.add_argument(r'--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data')
    #     chrome_options.add_argument('--profile-directory=Profile 1')
    #
    #     chrome_options.add_argument(r'--load-extensions=C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 1\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.92.10_0 ')
    #     chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    #     chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    #     # chrome_options.add_argument(f'--profile-directory=Default')
    #     #expander_chrome = "C:/Users/USER/AppData/Local/Google/Chrome/User Data/Default/Extensions/omghfjlpggmjjaagoclmmobgdodcjboh/3.92.10_0"
    #     #chrome_options.add_argument("--load-extension=C:/Users/USER/AppData/Local/Google/Chrome/User Data/Default/Extensions/omghfjlpggmjjaagoclmmobgdodcjboh/3.92.10_0")
    #     #chrome_options.add_argument('--no-first-run')
    #     #print(chrome_options.extensions)
    #     self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)    #
    #     #print(chrome_options.arguments)
    #     self.driver.set_page_load_timeout(10)  # Таймаут 10 секунд #

    @allure.feature('Тестирование функционала страницы авторизации')
    @allure.story('Авторизация с валидными данными')
    def test_open_website(self):
        try:
            # Пытаемся открыть сайт
            with allure.step('Пытаемся открыть сайт'):
                self.test_setup.driver.get("https://www.effective-mobile.ru/")
                self.test_setup.driver.switch_to.window(self.test_setup.driver.window_handles[0])
                time.sleep(3)  # Даём время на загрузку

            # Проверяем, открылась ли страница
            with allure.step('Проверяем, открылась ли страница'):
                if "Effective Mobile" in self.test_setup.driver.title:
                    print("ОТЛИЧНО! Сайт успешно загружен")
                else:
                    print(f"ВНИМАНИЕ! Ошибка загрузки страницы")
                    print(f"Текущий заголовок: {self.test_setup.driver.title}")
                    print(f"Текущий URL: {self.test_setup.driver.current_url}")


        # except TimeoutException:
        #     print("ВНИМАНИЕ! Превышено время ожидания загрузки страницы.")

        # except Exception as e:
        #     print(f"ВНИМАНИЕ! Произошла ошибка: {str(e)}")
        except TimeoutException:
            with allure.step(f'Обработка исключения — тайм-аут загрузки'):
                print("ВНИМАНИЕ! Превышено время ожидания загрузки страницы.")

        except Exception as e:
            with allure.step(f'Обработка неожиданного исключения: {str(e)}'):
                print(f"ВНИМАНИЕ! Произошла ошибка: {str(e)}")

    def tearDown(self):
        # Закрываем браузер
        self.test_setup.driver.quit()


if __name__ == '__main__':
    unittest.main()

    # C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default
    #
    # C:\Users\USER\AppData\Local\Google\Chrome\User
    # Data\Profile
    # 1\Extensions\omghfjlpggmjjaagoclmmobgdodcjboh\3.92
    # .10_0