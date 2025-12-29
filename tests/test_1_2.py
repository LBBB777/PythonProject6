from selenium.webdriver.common.by import By
from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import CurrentUsernamePassword
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure  # Добавляем импорт Allure

class TestAuthorizationBasic(unittest.TestCase):
    @allure.feature('Авторизация: актуальный логин, верный пароль')  # Добавляем описание функциональности
    @allure.story('Позитивное тестирование')  # Добавляем описание сценария

    def setUp(self):
        with allure.step("Настройка теста"):
            self.test_setup = TestSetup_A()
            self.test_setup.driver_a.get("https://www.saucedemo.com/")
            self.test_setup.driver_a.implicitly_wait(10)  # секунды

    def tearDown(self):
        with allure.step("Очистка после теста"):
            self.test_setup.driver_a.quit()

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.test_setup.driver_a, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            return False

    def get_field_username(self):
        return self.wait_for_element(By.ID, "user-name")

    def get_field_password(self):
        return self.wait_for_element(By.ID, "password")

    def get_field_login_button(self):
        return self.wait_for_element(By.ID, "login-button")

    def perform_authorization(self, username, password):
        username_field = self.get_field_username()
        if username_field:
            username_field.send_keys(username)
        password_field = self.get_field_password()
        if password_field:
            password_field.send_keys(password)
        login_button = self.get_field_login_button()
        if login_button:
            login_button.click()

    # Создаю тестовый метод, который будет подставлять переменные авторизации из тестовых данных и кликать на кнопку
    @allure.testcase(None, name="Тест авторизации с актуальной парой логин/пароль")
    def test_substitution_variable(self):
        for variable in CurrentUsernamePassword:
            print("\n----------------------------------------")
            print(f"ТЕСТИРУЮ ПАРУ ЛОГИН/ПАРОЛЬ: {variable['username']}/{variable['password']} \n"
                  f"из словаря актуальных логинов и паролей(CurrentUsernamePassword)")
            print("----------------------------------------\n")

            with allure.step(f'Тестирование пары {variable["username"]}/{variable["password"]}'):
                try:
                    self.test_setup.driver_a.delete_all_cookies()
                    self.test_setup.driver_a.get("https://www.saucedemo.com/")

                    with allure.step('Выполнение авторизации'):
                        self.perform_authorization(
                            variable['username'],
                            variable['password'])

                    with allure.step('Проверка результата'):

                        try:
                            inventory_header = WebDriverWait(self.test_setup.driver_a, 15).until(
                                lambda driver:
                                driver.title == "Swag Labs" and
                                driver.current_url == 'https://www.saucedemo.com/inventory.html'
                            )
                            print(f"Переход по введенным паре логин/пароль на страницу сайта: {inventory_header}")

                            if inventory_header:
                                expected_url = 'https://www.saucedemo.com/inventory.html'
                                actual_url = self.test_setup.driver_a.current_url
                                self.assertEqual(expected_url, actual_url,
                                                f"Ожидался URL: {expected_url}, получен: {actual_url}")

                                print(f"Успешная пара логин/пароль из словаря реальных логинов и паролей:\n"
                                      f"логин - {variable['username']}, "
                                      f"пароль - {variable['password']}")

                                # Успешная авторизация в Allure
                                allure.attach(
                                    name="Успешная авторизация",
                                    body=f"Логин: {variable['username']}\n"
                                         f"Пароль: {variable['password']}\n"
                                         f"URL: {actual_url}",
                                    attachment_type=allure.attachment_type.TEXT
                                )

                                # Скриншот успеха
                                allure.attach(
                                    name="Скриншот успешной авторизации",
                                    body=self.test_setup.driver_a.get_screenshot_as_png(),
                                    attachment_type=allure.attachment_type.PNG
                                )
                            else:
                                # Логирование неудачи в Allure
                                allure.attach(
                                    name="Неудачная попытка авторизации",
                                    body=f"Логин: {variable['username']}\n"
                                         f"Пароль: {variable['password']}",
                                    attachment_type=allure.attachment_type.TEXT
                                )

                                # Скриншот ошибки
                                allure.attach(
                                    name="Скриншот ошибки",
                                    body=self.test_setup.driver_a.get_screenshot_as_png(),
                                    attachment_type=allure.attachment_type.PNG
                                )
                                # Неудачная авторизация
                                self.fail(f"Неуспешная пара логин/пароль: "
                                          f"логин - {variable['username']}, "
                                          f"пароль - {variable['password']}")
                        except Exception as inner_e:
                            print(f"Ошибка при проверке: {inner_e}")
                            allure.attach(
                                name="Ошибка проверки",
                                body=str(inner_e).encode('utf-8'),
                                attachment_type=allure.attachment_type.TEXT
                            )

                    # Возврат на страницу входа
                    try:
                        with allure.step('Возврат на страницу входа'):
                            self.test_setup.driver_a.back()
                    except Exception as back_e:
                        print(f"Ошибка возврата: {back_e}")
                        allure.attach(
                            name="Ошибка возврата  на страницу входа",
                            body=str(back_e).encode('utf-8'),
                            attachment_type=allure.attachment_type.TEXT
                        )

                    # Очистка формы
                    self.test_setup.driver_a.refresh()

                except Exception as outer_e:
                    print(f"Критическая ошибка: {outer_e}")
                    allure.attach(
                        name="Критическая ошибка",
                        body=str(outer_e).encode('utf-8'),
                        attachment_type=allure.attachment_type.TEXT
                    )

                    try:
                        with allure.step('Восстановление'):
                            self.test_setup.driver_a.get("https://www.saucedemo.com/")
                    except Exception as recovery_e:
                        print(f"Ошибка восстановления: {recovery_e}")
                        allure.attach(
                            name="Ошибка восстановления",
                            body=str(recovery_e).encode('utf-8'),
                            attachment_type=allure.attachment_type.TEXT
                        )

                    print(f"Тестирование пары {variable['username']}/{variable['password']} не завершено")
                    allure.attach(
                        name="Неудачное тестирование",
                        body=f"Тестирование пары {variable['username']}/{variable['password']} не завершено".encode('utf-8'),
                        attachment_type=allure.attachment_type.TEXT
                    )

if __name__ == '__main__':
   
    unittest.main()

                                      
