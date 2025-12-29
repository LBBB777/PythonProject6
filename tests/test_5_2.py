from selenium.common import TimeoutException
from TestSetupAuthoriz import TestSetup_A
import unittest
from test_data import Performance_glitch_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure

################ Позитивное тестирование:  тестируется открытие страницы несмотря на возможные задержки #########################################
class TestAuthorizationPerformanceGlitchUser(unittest.TestCase):
    @allure.feature('Авторизация: актуальный логин, верный пароль, задержка загрузки страницы')  # Добавляем описание функциональности
    @allure.story(' Нагрузочное тестирование')  # Добавляем описание сценария

    #  Запустить драйвер и открыть страницу
    def setUp(self):
        with allure.step("Запускаю драйвер и открываю страницу"):
            # Создаю экземпляр класса TestSetup_A
            self.test_setup = TestSetup_A()
            # Открытие страницы
            self.test_setup.driver_a.get("https://www.saucedemo.com/")
            # Добавляем проверку успешной загрузки страницы
            with allure.step("Проверка загрузки страницы авторизации"):
                allure.attach(
                    name="Скриншот открытой страницы",
                    body=self.test_setup.driver_a.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )
                # Неявное ожидание !!!!!!!!!
                self.test_setup.driver_a.implicitly_wait(10)


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


        # Создаю тестовую функцию подстановки переменных авторизации которая будет кликать на кнопку
    @allure.testcase(None, name="Тест- авторизации пользователя в условиях длительной загрузки страницы. Логин/пароль -верные")
    def test_substitution_variable(self):
        for variable in Performance_glitch_user:
            print("\n----------------------------------------")
            print(
                f"ТЕСТИРУЮ АВТОРИЗАЦИЮ ПОЛЬЗОВАТЕЛЯ С ЗАДЕРЖКОЙ ЗАГРУЗКИ: {variable['username']}/{variable['password']} \n "
                f"из словаря актуальных логинов и паролей(Performance_glitch_user )")
            print("----------------------------------------\n")
            # Ждем перехода  по введенным данным
            with allure.step(f'Тестирование пары {variable["username"]}/{variable["password"]}'):
                try:

                    #  Очищаем куки перед каждой попыткой
                    with allure.step("Очистка куки перед тестированием"):
                        self.test_setup.driver_a.delete_all_cookies()

                    #  Возвращаемся на страницу входа перед каждой попыткой
                    with allure.step("Переход на страницу авторизации"):
                        self.test_setup.driver_a.get("https://www.saucedemo.com/")


                    # Ожидание готовности полей
                    with allure.step("Ожидание готовности полей ввода"):
                    # Явно ожидаю готовность поля ввода логина и ввода  логина
                        WebDriverWait(self.test_setup.driver_a, 10).until(
                            EC.presence_of_element_located((By.ID, "user-name"))).send_keys(variable['username'])

                        # Явно ожидаю готовность поля ввода пароля и ввода  пароля
    
                        WebDriverWait(self.test_setup.driver_a, 10).until(
                            EC.presence_of_element_located((By.ID, "password"))).send_keys(variable['password'])

                        # Явно ожидаю кликабельности кнопки входа и кликаю
                        WebDriverWait(self.test_setup.driver_a, 10).until(
                            EC.presence_of_element_located((By.ID, "login-button"))).click()

                    # Шаг проверки исчезновения ошибки
                    with allure.step("Проверка исчезновения сообщения об ошибке"):
                        # Добавляем ожидание исчезновения ошибки
                        try:
                            WebDriverWait(self.test_setup.driver_a, 10).until_not(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, ".error"))
                            )
                        except TimeoutException:
                            print("Ошибка: сообщение об ошибке не исчезло")

                    # Шаг проверки результата
                    with allure.step("Проверка успешной авторизации"):
                    # Проверяем результат
                        try:
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
                                allure.attach(
                                    name="Проверка URL",
                                    body=f"Ожидаемый URL: {expected_url}\nФактический URL: {actual_url}",
                                    attachment_type=allure.attachment_type.TEXT
                                )

                                self.assertEqual(expected_url, actual_url,
                                                 f"Ожидался URL: {expected_url}, получен: {actual_url}")

                                # ИСПОЛЬЗУЕМ РЕАЛЬНЫЕ ЗНАЧЕНИЯ ИЗ СЛОВАРЯ
                                print(f"Успешная пара логин/пароль из словаря реальных логинов и паролей:\n"
                                      f" логин - {variable['username']}, "
                                      f" пароль - {variable['password']}"
                                      )
                                # Скриншот успеха
                                allure.attach(
                                    name="Скриншот успешной авторизации",
                                    body=self.test_setup.driver_a.get_screenshot_as_png(),
                                    attachment_type=allure.attachment_type.PNG
                                )
                            else:
                                self.fail(f"Неуспешная пара логин/пароль из словаря реальных логинов и паролей:"
                                          f" логин - {variable['username']}, "
                                          f" пароль - {variable['password']}")
                        except Exception as inner_e:  # Добавлен внутренний except
                            print(f"Ошибка при проверке авторизации: {inner_e}")
                            allure.attach(
                                name="Ошибка при проверке авторизации",
                                body=str(inner_e),
                                attachment_type=allure.attachment_type.TEXT
                            )

                except Exception as outer_e:
                    print(f"Критическая ошибка в тесте : {outer_e}")
                    allure.attach(
                        name="Критическая ошибка в тесте",
                        body=str(outer_e).encode('utf-8'),
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Обработка критической ошибки
                    with allure.step("Попытка восстановления после ошибки"):

                        try:
                            # Делаем скриншот ошибки
                            allure.attach(
                                name="Скриншот при ошибке",
                                body=self.test_setup.driver_a.get_screenshot_as_png(),
                                attachment_type=allure.attachment_type.PNG
                            )
                            # Пытаемся вернуться на страницу входа
                            self.test_setup.driver_a.get("https://www.saucedemo.com/")
                        except Exception as recovery_e:
                            allure.attach(
                                name="Ошибка восстановления",
                                body=str(recovery_e).encode('utf-8'),
                                attachment_type=allure.attachment_type.TEXT
                            )

                            # Добавляем лог неудачной попытки
                            allure.attach(
                                name="Неудачная попытка тестирования",
                                body=f"Тестирование пары {variable['username']}/{variable['password']} не завершено успешно",
                                attachment_type=allure.attachment_type.TEXT
                            )
                            print(f"Ошибка восстановления: {recovery_e}")

                    #Логирование неудачной попытки
                        print(f"Тестирование пары {variable['username']}/{variable['password']} не завершено успешно")


if __name__ == '__main__':
    unittest.main()
