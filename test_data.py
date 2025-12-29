# Тестовые данные -1
CurrentUsernamePassword = [
    {
        'username': 'standard_user',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    },
{
        'username': 'problem_user',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    },

{
        'username': 'error_user',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    }
    ]

################# Тестовые данные -2
CurrentLoginInvalidPassword = [
    {
        'username': 'standard_user',
        'password': 'secret_s',
        'expected_result': 'Ошибка авторизации'
    },
{
        'username': 'problem_user',
        'password': '1223secret_sauce',
        'expected_result': 'Ошибка авторизации'
    },

{
        'username': 'error_user',
        'password': 'secret_Sauce',
        'expected_result': 'Ошибка авторизации'
    }]

################Тестовые данные -3
Locked_user = [
    {
    'username': 'locked_out_user',
    'password': 'secret_sauce',
    'expected_result': 'Пользователь заблокирован'
    }
]
################ Тестовые данные -4
LoginWithEmptyFields = [
    {
        'username': '',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    },
{
        'username': '     ',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    },

{
        'username': '            ',
        'password': 'secret_sauce',
        'expected_result': 'Успешный вход'
    }



]

################ Тестовые данные -5

Performance_glitch_user = [
{
    'username': 'performance_glitch_user',
    'password': 'secret_sauce',
    'expected_result': 'Корректный переход  несмотря на задержки'
} ]

#
# test_cases = {
#     'CurrentUsernamePassword' :{
#         'username': 'current_user_name',
#         'password': 'current_password',
#         'expected_resut': 'Успешный вход'
#     },
#     '2.	CurrentLoginInvalidPassword': {
#         'username': 'current_user_name',
#         'password': 'wrong_password',
#         'expected_resut': 'Ошибка авторизации'
#     },
#     'Locked_user': {
#         'username': 'locked_out_user',
#         'password': 'current_password',
#         'expected_resut': 'Пользователь заблокирован'
#     },
#     'LoginWithEmptyFields': {
#         'username': '',
#         'password': 'current_password',
#         'expected_resut': 'Поле username  обязательно для заполнения'
#     },
#     'Performance_user': {
#         'username': '5.	performance_glitch_user',
#         'password': 'current_password',
#         'expected_resut': 'Корректный переход  несмотря на задержки'
#     },
# }
#
#
#
