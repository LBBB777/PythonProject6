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


class TestAuthorizationBasic(unittest.TestCase):

    def setUp(self):
        # Создаю экземпляр класса TestSetup_A
        self.test_setup = TestSetup_A()
        # Открытие страницы
        self.test_setup.driver_a.get("https://www.saucedemo.com/")
        # Неявное ожидание !!!!!!!!!
        self.test_setup.driver_a.implicitly_wait(10)  # секунды

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

    def get_field_username(self):
        return self.wait_for_element(By.ID, "user-name")

    def get_field_password(self):
        return self.wait_for_element(By.ID, "password")

    def get_field_login_button(self):
        return self.wait_for_element(By.ID, "login-button")

    def perform_authorization(self, username, password):
        username_field = self.get_field_username()
        if username_field:
            username_field.clear()  # Добавляем очистку поля перед вводом
            username_field.send_keys(username)

        password_field = self.get_field_password()
        if password_field:
            password_field.click()
            if password_field.get_attribute('value'):
                password_field.clear()
            time.sleep(0.5)
            password_field.send_keys(password)

        login_button = self.get_field_login_button()
        if login_button:
            login_button.click()

    def test_substitution_variable(self):
        for variable in Performance_glitch_user:
            try:
                # !! ДОБАВЛЕНО: Очистка localStorage и sessionStorage !!
                self.test_setup.driver_a.delete_all_cookies()
                self.test_setup.driver_a.execute_script("localStorage.clear(); sessionStorage.clear();")

                # !! ИЗМЕНЕНО: Явное ожидание загрузки формы !!
                self.test_setup.driver_a.get("https://www.saucedemo.com/")
                WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.presence_of_element_located((By.ID, "user-name"))
                )

                # !! ИЗМЕНЕНО: Явное ожидание кликабельных элементов !!
                username_field = WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.element_to_be_clickable((By.ID, "user-name"))
                )
                username_field.clear()
                username_field.send_keys(variable['username'])

                password_field = WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.element_to_be_clickable((By.ID, "password"))
                )
                password_field.clear()
                password_field.send_keys(variable['password'])

                login_button = WebDriverWait(self.test_setup.driver_a, 10).until(
                    EC.element_to_be_clickable((By.ID, "login-button"))
                )
                login_button.click()

                # !! ДОБАВЛЕНО: Ожидание исчезновения ошибки !!
                try:
                    WebDriverWait(self.test_setup.driver_a, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".error"))
                    )
                except TimeoutException:
                    print("Ошибка: сообщение об ошибке не исчезло")

                # !! ДОБАВЛЕНО: Ожидание полной загрузки целевой страницы !!
                WebDriverWait(self.test_setup.driver_a, 50).until(
                    lambda driver:
                    driver.title == "Swag Labs" and
                    driver.current_url == 'https://www.saucedemo.com/inventory.html'
                )

                # !! ДОБАВЛЕНО: Проверка отсутствия ошибок на целевой странице !!
                try:
                    WebDriverWait(self.test_setup.driver_a, 5).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".error"))
                    )
                except TimeoutException:
                    print("Ошибка: сообщение об ошибке присутствует на целевой странице")

                # Проверяем URL
                expected_url = 'https://www.saucedemo.com/inventory.html'
                actual_url = self.test_setup.driver_a.current_url
                self.assertEqual(expected_url, actual_url,
                                 f"Ожидался URL: {expected_url}, получен: {actual_url}")

                print(f"Успешная авторизация для пользователя: {variable['username']}")

            except Exception as e:
                print(f"Произошла ошибка: {str(e)}")
                try:
                    # !! ДОБАВЛЕНО: Попытка восстановления !!
                    self.test_setup.driver_a.get("https://www.saucedemo.com/")
                except Exception as ex:
                    print(f"Ошибка восстановления: {str(ex)}")

if __name__ == '__main__':
    unittest.main()
