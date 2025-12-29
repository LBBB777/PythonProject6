# Используем образ Selenium с Chrome как базовый
FROM selenium/standalone-chrome:142.0-chromedriver-142.0-20251202

# Переключаемся на root для установки
USER root

# Устанавливаем зависимости для сборки Python
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y libssl-dev && \
    apt-get install -y libffi-dev && \
    apt-get install -y zlib1g-dev

# Устанавливаем Python 3.10 и pip
RUN apt-get install -y wget && \
    wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz && \
    tar xzf Python-3.10.0.tgz && \
    cd Python-3.10.0 && \
    ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall

# Устанавливаем pip для Python 3.10
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.10

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости Python
RUN pip3.10 install --no-cache-dir -r requirements.txt

# !! ДОБАВЛЯЕМ НОВЫЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ДЛЯ DRIVER !!
# Уточняем правильный путь к ChromeDriver
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_PATH=/usr/bin/google-chrome

# Настраиваем существующие переменные окружения
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# Открываем порт для Selenium (если необходимо)
EXPOSE 4444

# Создаем пользователя selenium
RUN groupadd -r selenium && \
    useradd -r -g selenium -m selenium

# !! ИЗМЕНЯЕМ НАСТРОЙКИ ПРАВ ДОСТУПА !!
# Используем правильный путь к ChromeDriver
RUN chmod +x /usr/bin/chromedriver && \
    chmod +x /usr/bin/google-chrome

# Возвращаемся к пользователю selenium
USER selenium

# !! ИЗМЕНЯЕМ КОМАНДУ ЗАПУСКА !!
CMD ["sh", "-c", \
     "trap 'pkill -9 -f 'chrome'' EXIT; \
      python3.10 -m unittest discover -s tests"]
