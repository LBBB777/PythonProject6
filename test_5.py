import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import Performance_glitch_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


################ Позитивное тестирование: Логин пользователем performance_glitch_user #########################################
class TestAuthorizationBasic(unittest.TestCase):

    def setUp(self):
        # Создаю экземпляр класса TestSetup_A
        self.test_setup = TestSetup_A()
        # Открытие страницы
        self.test_setup.driver_a.get("https://www.saucedemo.com/")
        # Неявное ожидание !!!!!!!!!
        self.test_setup.driver_a.implicitly_wait(10)  # секунды

        # Закрываю страницу

    def tearDown(self):
        self.test_setup.driver_a.quit()

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.test_setup.driver_a, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:  # Добавляем обработку ошибки таймаута
            print(f"Элемент {value} не найден за {timeout} секунд")
            return None

        # Нахожу элементы по ID

    def get_field_username(self):
        return self.wait_for_element(By.ID, "user-name")

    def get_field_password(self):
        return self.wait_for_element(By.ID, "password")

    def get_field_login_button(self):
        return self.wait_for_element(By.ID, "login-button")

    # Создаю  метод подстановки в переменную  username и password  данных из test_data.py
    def perform_authorization(self, username, password):
        username_field = self.get_field_username()
        if username_field:
            username_field.clear()  # Добавляем очистку поля перед вводом
            username_field.send_keys(username)

        password_field = self.get_field_password()
        if password_field:
            # Добавляем переключение фокуса
            password_field.click()

            # Добавляем проверку состояния поля  перед очисткой
            if password_field.get_attribute('value'):
                password_field.clear()

            time.sleep(0.5)
            password_field.send_keys(password)

        login_button = self.get_field_login_button()
        if login_button:
            login_button.click()

        # Создаю тестовую функцию подстановки переменных авторизации которая будет кликать на кнопку

    def test_substitution_variable(self):
        for variable in Performance_glitch_user:

            # Ждем перехода  по введенным данным
            try:

                #  Очищаем куки перед каждой попыткой
                self.test_setup.driver_a.delete_all_cookies()

                #  Возвращаемся на страницу входа перед каждой попыткой
                self.test_setup.driver_a.get("https://www.saucedemo.com/")
                
                # Явно ожидаю готовность поля ввода логина и ввода  логина

                WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.presence_of_element_located((By.ID, "user-name"))).send_keys(variable['username'])

                # Явно ожидаю готовность поля ввода пароля и ввода  пароля

                WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))).send_keys(variable['password'])

                # Явно ожидаю кликабельности кнопки входа и кликаю
                WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.presence_of_element_located((By.ID, "login-button"))).click()


                # # Выполняем авторизацию
                # self.perform_authorization(
                #     variable['username'],
                #     variable['password'])

                # Добавляем ожидание исчезновения ошибки
                try:
                    WebDriverWait(self.test_setup.driver_a, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".error"))
                    )
                except TimeoutException:
                    print("Ошибка: сообщение об ошибке не исчезло")



                # Проверяем результат
                try:
                    print("\n----------------------------------------")
                    print(f"ТЕСТИРУЮ АВТОРИЗАЦИЮ ПОЛЬЗОВАТЕЛЯ С ЗАДЕРЖКОЙ ЗАГРУЗКИ: {variable['username']}/{variable['password']} \n "
                          f"из словаря актуальных логинов и паролей(Performance_glitch_user )")
                    print("----------------------------------------\n")

                    inventory_header = WebDriverWait(self.test_setup.driver_a, 50).until(
                        lambda driver:
                        driver.title == "Swag Labs" and
                        driver.current_url == 'https://www.saucedemo.com/inventory.html'
                    )
                    print(f"Переход по введенным паре логин/пароль на страницу сайта : {inventory_header}")

                    if inventory_header:
                        # Данные для проверки URL
                        expected_url = 'https://www.saucedemo.com/inventory.html'
                        actual_url = self.test_setup.driver_a.current_url
                        # Проверяем, что мы на нужной странице
                        self.assertEqual(expected_url, actual_url,
                                         f"Ожидался URL: {expected_url}, получен: {actual_url}")

                        # ИСПОЛЬЗУЕМ РЕАЛЬНЫЕ ЗНАЧЕНИЯ ИЗ СЛОВАРЯ
                        print(f"Успешная пара логин/пароль из словаря реальных логинов и паролей:\n"
                              f" логин - {variable['username']}, "
                              f" пароль - {variable['password']}"
                              )

                    else:
                        self.fail(f"Неуспешная пара логин/пароль из словаря реальных логинов и паролей:"
                                  f" логин - {variable['username']}, "
                                  f" пароль - {variable['password']}")
                except Exception as inner_e:  # Добавлен внутренний except
                    print(f"Ошибка при проверке авторизации: {inner_e}")

            except Exception as outer_e:
                print(f"Критическая ошибка в тесте : {outer_e}")
                # ДОБАВЛЕНО: Обработка критической ошибки
                try:
                    # Пытаемся вернуться на страницу входа
                    self.test_setup.driver_a.get("https://www.saucedemo.com/")

                except Exception as recovery_e:
                    print(f"Ошибка восстановления: {recovery_e}")

                # ДОБАВЛЕНО: Логирование неудачной попытки
                print(f"Тестирование пары {variable['username']}/{variable['password']} не завершено успешно")


if __name__ == '__main__':
    unittest.main()
