import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import LoginWithEmptyFields
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException  # Добавлен импорт для обработки таймаута

###############Пустые пароли####################

class TestAuthorization(unittest.TestCase):
    #  Запустить драйвер и открыть страницу
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

    # Ожидаю появления элементов на странице
    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.test_setup.driver_a, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:  # Уточнили тип исключения
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
        # Находим поле username, вводим username
        username_field = self.get_field_username()
        if username_field:
            username_field.clear()  # Добавлено очищение поля
            username_field.send_keys(username)
        # Находим поле password, вводим password
        password_field = self.get_field_password()
        if password_field:
            username_field.clear()  # Добавлено очищение поля
            password_field.send_keys(password)
        # Находим поле логина, вводим логин
        login_button = self.get_field_login_button()
        if login_button:
            login_button.click()

        # Создаю тестовый метод, который будет подставлять переменные авторизации из тестовых данных и кликать на кнопку

    def test_substitution_variable(self):
        for variable in LoginWithEmptyFields:

            # Ждем перехода  по введенным данным
            try:

                # Очищаем куки перед каждой попыткой
                self.test_setup.driver_a.delete_all_cookies()

                # Возвращаемся на страницу входа перед каждой попыткой
                self.test_setup.driver_a.get("https://www.saucedemo.com/")

                # Выполняем авторизацию
                self.perform_authorization(
                    variable['username'],
                    variable['password'])

                # # Добавляем ожидание после авторизации-отладка теста
                # ################################### Получаем весь текст страницы для отладки
                # visible_text = self.test_setup.driver_a.find_element(By.TAG_NAME, "body").text
                # print("\nВИДИМЫЙ ТЕКСТ НА СТРАНИЦЕ//ОТЛАДКА:\n")  # Выводим весь текст видимый на странице
                # print(visible_text) # Выводим весь текст видимый на странице
                #
                # try:
                #     # Ждем появления либо сообщения об ошибке, либо успешной авторизации
                #     WebDriverWait(self.test_setup.driver_a, 20).until(
                #         lambda driver:
                #         EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container.error")) or
                #         EC.url_changes("https://www.saucedemo.com/")
                #     )
                # except TimeoutException:
                #     self.fail("Не произошло ни успешной авторизации, ни появления сообщения об ошибке")


                # Проверяем результат
                try:
                    print("\n----------------------------------------")
                    print(
                        f"ТЕСТИРУЮ ПАРУ С АКТУАЛЬНЫМ ЛОГИНОМ И ПУСТЫМ ПАРОЛЕМ: {variable['username']}/{variable['password']}")
                    print("----------------------------------------\n")

                    # Нахожу и сохраняю индикатор ошибки: Драйвером ищу текст  Epic sadface: Sorry, this user has been locked outи
                    #  и кладу в переменную  login_error
                    # Находим элемент с сообщением об ошибке авторизации
                    # login_error = WebDriverWait(self.test_setup.driver_a, 15).until(
                    #     EC.presence_of_element_located(
                    #         (By.XPATH, "//h3[contains(text(), 'Epic sadface: Sorry, this user has been locked out')]"
                    #          )
                    #     ))
                    #
                    #
                    try:
                        login_error = WebDriverWait(self.test_setup.driver_a, 15).until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR,
                                 "h3[data-test='error']")  # Используем CSS селектор по атрибуту data-test
                            )
                        )
                        error_message = login_error.text.strip()
                        expected_message = 'Epic sadface: Password is required'
                        if expected_message in error_message:
                            self.assertTrue(expected_message in error_message,
                            f"Сообщение об ошибке соответсвует ожидаемому: {expected_message}")
                        else:
                             self.fail(f"Неверное сообщение об ошибке."
                                     f"Ожидалось: {expected_message}, "
                                     f"получено: {error_message}")

                    except TimeoutException:
                        self.fail("Сообщение об ошибке не появилось в течение 15 секунд")
                    except Exception as e:
                        self.fail(f"Ошибка при проверке сообщения об ошибке: {str(e)}")

                    # Создаю данные для проверки URL
                    authorization_form_url = 'https://www.saucedemo.com/'
                    website_url = 'https://www.saucedemo.com/inventory.html'
                    actual_url = self.test_setup.driver_a.current_url

                    # Проверяем URL по заданной логике
                    if actual_url == authorization_form_url:
                        # Если текущий URL совпадает с формой авторизации
                        print('Ура! Пользователь с заблокированным логином остановлен на странице авторизации')
                        print(
                            f"ОТЧЕТ:\n"
                            f"1)Тестировалась пара логин/пароль из словаря c актуальными логинами пустыми паролями (LoginWithEmptyFields):\n"
                            f"логин - {variable['username']}, "
                            f"пароль - {variable['password']}")
                        print(
                            f'2) После авторизации по заблокированному логину на странице авторизации имеется\nожидаемое сообщение для пользователя: "{login_error.text}" \n')

                    elif actual_url == website_url:
                        # Если текущий URL совпадает с URL сайта
                        self.fail(f"Критическая ошибка: пользователь с заблокированным логином попал на сайт!!!\n"
                                  f"Текущий URL: {actual_url}")

                    else:
                        # Если URL не совпадает ни с одной из ожидаемых страниц
                        self.fail(
                            f"Неожиданный URL после неудачной авторизации пользователя с заблокированным логином: {actual_url}\n"
                            f"Ожидалась страница авторизации: {authorization_form_url}")

                except Exception as inner_e:
                    print(f"Ошибка при проверке авторизации: {inner_e}")
                    self.fail("Тест не смог проверить авторизацию пользоывателя с заблокированным логином")

                # !!!!!!!!!!!!!!!! Возвращаемся на страницу входа после проверки пары логин-пароль
                try:
                    self.test_setup.driver_a.back()
                except:
                    print("Не удалось вернуться на страницу входа")

                # Очищаем форму входа после проверки
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
