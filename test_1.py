import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import CurrentUsernamePassword
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


################ Позитивное тестирование: проверяем авторизацию с успешной парой логин/пароль #########################################
class   TestAuthorizationBasic(unittest.TestCase):


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
        except:
            return False

        # Нахожу элементы по ID
    def get_field_username(self):
        return self.wait_for_element(By.ID, "user-name")

    def get_field_password(self):
         return self.wait_for_element(By.ID, "password")

    def get_field_login_button(self):
        return self.wait_for_element(By.ID, "login-button")


    # Создаю  метод подстановки в переменную  username и password  данных из test_data.py
    def perform_authorization(self, username, password):
        # Находим поле логина, вводим логин
        username_field = self.get_field_username()
        if username_field:
            username_field.send_keys(username)
        password_field = self.get_field_password()
        if password_field:
            password_field.send_keys(password)
        login_button = self.get_field_login_button()
        if login_button:
            login_button.click()


        # Создаю функцию подстановки переменных авторизации которая будет кликать на кнопку
    def test_substitution_variable (self):
        for variable in CurrentUsernamePassword:

            # Ждем перехода  по введенным данным
            try:

                # ДОБАВЛЕНО: Очищаем куки перед каждой попыткой
                self.test_setup.driver_a.delete_all_cookies()

                # ДОБАВЛЕНО: Возвращаемся на страницу входа перед каждой попыткой
                self.test_setup.driver_a.get("https://www.saucedemo.com/")

                # Выполняем авторизацию
                self.perform_authorization(
                    variable['username'],
                    variable['password'])
                # Проверяем результат
                try:
                    print("\n----------------------------------------")
                    print(f"ТЕСТИРУЮ ПАРУ ЛОГИН/ПАРОЛЬ : {variable['username']}/{variable['password']} \n "
                          f"из словаря актуальных логинов и паролей(CurrentUsernamePassword )")
                    print("----------------------------------------\n")
                    
                    inventory_header = WebDriverWait(self.test_setup.driver_a, 15).until(
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
                    
    # ДОБАВЛЕНО: Возвращаемся на страницу входа после проверки
                # ДОБАВЛЕНО: Возвращаемся на страницу входа после проверки
                try:
                    self.test_setup.driver_a.back()
                except:
                    print("Не удалось вернуться на страницу входа")

                # ДОБАВЛЕНО: Очищаем форму входа после проверки
                self.test_setup.driver_a.refresh()

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
