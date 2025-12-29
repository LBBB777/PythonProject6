from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import Locked_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException  # Добавлен импорт для обработки таймаута

import allure


################ Негативное тестирование: проверяем авторизацию с логином заблокированного пользователя и неверным паролем #########################################

class TestLockedAccountAuthorization(unittest.TestCase):
    @allure.feature('Авторизация: заблокированный логин, верный пароль')  # Добавляем описание функциональности
    @allure.story(' Негативное тестирование')  # Добавляем описание сценария

    #  Запустить драйвер и открыть страницу
    def setUp(self):
        with allure.step("Запускаю драйвер и открываю страницу"):
            # Создаю экземпляр класса TestSetup_A
            self.test_setup = TestSetup_A()
            # Открытие страницы
            self.test_setup.driver_a.get("https://www.saucedemo.com/")
            # Неявное ожидание !!!!!!!!!
            self.test_setup.driver_a.implicitly_wait(10)  # секунды

        # Закрываю страницу

    def tearDown(self):
        with allure.step("Закрываю страницу после каждого теста"):
            self.test_setup.driver_a.quit()

    # Ожидаю появления элементов на странице
    def wait_for_element(self, by, value, timeout=10):
        with allure.step("Ожидаю появления элементов на странице"):
            try:
                return WebDriverWait(self.test_setup.driver_a, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            except TimeoutException:  # Уточнили тип исключения
                allure.attach(
                    name="Ошибка ожидания элемента",
                    body=f"Элемент {value} не найден за {timeout} секунд",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False

        # Нахожу элементы по ID

    def get_field_username(self):
        with allure.step("Поиск поля username"):
            return self.wait_for_element(By.ID, "user-name")

    def get_field_password(self):
        with allure.step("Поиск поля password"):
            return self.wait_for_element(By.ID, "password")

    def get_field_login_button(self):
        with allure.step("Поиск кнопки входа"):
            return self.wait_for_element(By.ID, "login-button")

    # Создаю  метод подстановки в переменную  username и password  данных из test_data.py
    def perform_authorization(self, username, password):
        with allure.step(f"Выполнение авторизации с {username}/{password}"):
            # Находим поле username, вводим username
            username_field = self.get_field_username()
            if username_field:
                with allure.step(f"Ввод username: {username}"):
                    username_field.clear()  # Добавлено очищение поля
                    username_field.send_keys(username)
            # Находим поле password, вводим password
            password_field = self.get_field_password()
            if password_field:
                with allure.step(f"Ввод password: {password}"):
                    password_field.clear()  # Добавлено очищение поля
                    password_field.send_keys(password)
            # Находим поле логина, вводим логин
            login_button = self.get_field_login_button()
            if login_button:
                with allure.step("Нажатие кнопки входа"):
                    login_button.click()

        # Создаю тестовый метод, который будет подставлять переменные авторизации из тестовых данных и кликать на кнопку

    @allure.testcase(None, name="Тест- попытка авторизации с логином заблокированного пользователя и неверным паролем")
    def test_substitution_variable(self):
        for variable in Locked_user:
            print("\n----------------------------------------")
            print(
                f"ТЕСТИРУЮ ПАРУ С ЗАБЛОКИРОВАННЫМ ЛОГИНОМ ПОЛЬЗОВАТЕЛЯ: {variable['username']}/{variable['password']}")
            print("----------------------------------------\n")

            # Ждем перехода  по введенным данным
            with allure.step(f'Тестирование пары {variable["username"]}/{variable["password"]}'):

                try:
                    # Очищаем куки перед каждой попыткой
                    self.test_setup.driver_a.delete_all_cookies()

                    # Возвращаемся на страницу входа перед каждой попыткой
                    self.test_setup.driver_a.get("https://www.saucedemo.com/")

                    # Выполняем авторизацию
                    with allure.step('Выполнение авторизации'):
                        self.perform_authorization(
                            variable['username'],
                            variable['password']
                        )

                    # Проверяем результат
                    with allure.step('Проверка наличия сообщения об ошибке'):
                        try:
                           # Находим контейнер с ошибкой
                            error_message = WebDriverWait(self.test_setup.driver_a, 20).until(
                                EC.visibility_of_element_located(
                                    (By.CSS_SELECTOR, ".error-message-container.error")
                                    # Используем CSS селектор по атрибуту data-test
                                )
                            )
                            full_massege = error_message.text.strip()

                            expected_exact_message = 'Epic sadface: Sorry, this user has been locked out'
                            # Ищем ключевую фразу в тексте
                            if expected_exact_message in full_massege:
                                actual_message: str = expected_exact_message
                                print(f"Извлечено ожидаемое сообщение: {actual_message}")
                            else:
                                # Логирование неудачи в Allure
                                allure.attach(
                                    name="Неудачная попытка найти сообщение об ошибке",
                                    body=f"Логин: {variable['username']}\n"
                                         f"Пароль: {variable['password']}\n"
                                         f"Ожидаемое сообщение: {expected_exact_message}\n"
                                         f"Фактическое сообщение: {full_massege}",
                                    attachment_type=allure.attachment_type.TEXT
                                )
                                raise ValueError(
                                    f"Не найдено ожидаемое сообщение об ошибке: ожидаемое {expected_exact_message},фактическое{full_massege}")

                        except TimeoutException:
                            self.fail("Сообщение об ошибке не появилось в течение 15 секунд")
                        except Exception as e:
                            self.fail(f"Ошибка при проверке сообщения об ошибке: {str(e)}")

                    # Создаю данные для проверки URL
                    with allure.step(
                            'Создаю данные для проверки URL  и проверяю что пользователь остался на странице авторизации'):
                        authorization_form_url = 'https://www.saucedemo.com/'
                        website_url = 'https://www.saucedemo.com/inventory.html'
                        actual_url = self.test_setup.driver_a.current_url

                        # Проверяем URL по заданной логике
                        if actual_url == authorization_form_url:
                            # Если текущий URL совпадает с формой авторизации
                            print('Ура! Пользователь с заблокированным логином остановлен на странице авторизации')
                            print(
                                f"ОТЧЕТ:\n"
                                f"1)Тестировалась пара логин/пароль из словаря заблокированных логинов и верных паролей (Locked_user):\n"
                                f"логин - {variable['username']}, "
                                f"пароль - {variable['password']}")
                            print(
                                f'2)После авторизации по заблокированному логину на странице авторизации\nимеется сообщение "{actual_message}"  '
                            )
                            allure.attach(
                                name="Успех! Пользователь с неверным паролем остался на странице авторизации!",
                                body=f"Логин: {variable['username']}\n"
                                         f"Пароль: {variable['password']}\n"
                                         f"URL: {actual_url}",
                                attachment_type=allure.attachment_type.TEXT
                                )

                                # Скриншот успеха
                            allure.attach(
                                name="Скриншот успеха! Пользователь с неверным паролем остался на странице авторизации!",
                                body=self.test_setup.driver_a.get_screenshot_as_png(),
                                attachment_type=allure.attachment_type.PNG
                            )

                        elif actual_url == website_url:
                            # Если текущий URL совпадает с URL сайта
                            self.fail(f"Критическая ошибка: пользователь с заблокированным логином попал на сайт!!!\n"
                                      f"Текущий URL: {actual_url}")

                        else:
                            # Если URL не совпадает ни с одной из ожидаемых страниц
                            self.fail(
                                f"Неожиданный URL после неудачной авторизации пользователя с заблокированным логином: {actual_url}\n"
                                f"Ожидалась страница авторизации: {authorization_form_url}")


                        # !!!!!!!!!!!!!!!! Возвращаемся на страницу входа после проверки пары логин-пароль
                        try:
                            self.test_setup.driver_a.back()
                        except Exception as back_e:
                            print("Не удалось вернуться на страницу входа")
                            allure.attach(
                                name="Ошибка возврата  на страницу входа",
                                body=str(back_e).encode('utf-8'),
                                attachment_type=allure.attachment_type.TEXT
                            )
                        # Очищаем форму входа после проверки
                        self.test_setup.driver_a.refresh()

                except Exception as outer_e:
                    print(f"Критическая ошибка в тесте : {outer_e}")
                    # Обработка критической ошибки
                    allure.attach(
                    name="Критическая ошибка в тесте",
                    body=str(outer_e).encode('utf-8'),
                    attachment_type=allure.attachment_type.TEXT
                    )
                    try:
                        # Пытаемся вернуться на страницу входа
                        self.test_setup.driver_a.get("https://www.saucedemo.com/")

                    except Exception as recovery_e:
                        print(f"Ошибка восстановления: {recovery_e}")
                        allure.attach(
                            name="Ошибка попытки вернуться на страницу входа",
                            body=str(recovery_e).encode('utf-8'),
                            attachment_type=allure.attachment_type.TEXT
                        )
                    #  Логирование неудачной попытки
                    print(f"Тестирование пары {variable['username']}/{variable['password']} не завершено успешно")
                    allure.attach(
                        name="Неудачное тестирование",
                        body=f"Тестирование пары {variable['username']}/{variable['password']} не завершено".encode('utf-8'),
                        attachment_type=allure.attachment_type.TEXT
                    )


if __name__ == '__main__':
    unittest.main()
