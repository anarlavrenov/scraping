# 1. Установить selenium через pip install
# 2. Установить веб драйвер для браузера, в котором работаю и закинуть его в директорию с проектом

# Импортируемый объект webdriver будет связываться со скачанным веб драйвером
# и будет переводить код в действие внутри браузера
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Импортирую класс для нахождения элементов
from selenium.webdriver.common.by import By
# Импортирую класс для нажатия кнопки Enter
from selenium.webdriver.common.keys import Keys
# Импортирую класс для работы с полями множественного выбора
from selenium.webdriver.support.ui import Select

# Создаю сервисный объект, который будет принимать путь до драйвера
s = Service('./chromedriver.exe')

# Создаю объект, в который буду отправлять команды
driver = webdriver.Chrome(service=s)

# Делаю get запрос на страницу входа в платформу
driver.get('https://github.com/login')

# Нахожу элемент (инпут ввода имени пользователя)
# Когда элемент найден, могу производить с ним логические операции
elem = driver.find_element(By.ID, 'login_field')
elem.send_keys('anarlavrenov')

# Нахожу элемент (инпут ввода пароля пользователя). Переменную указываю такую же
elem = driver.find_element(By.ID, 'password')
elem.send_keys('fdnjcthdbc1996')

# Находясь на поле ввода пароля, снова вызываю метод send_keys,
# внутри которого вызываю класс Keys и его метод ENTER
elem.send_keys(Keys.ENTER)

# Нахожу ссылку на настройки профиля через Xpath
# Такой подход(скрипт) по нахождению элемента не делали на занятии по Xpath,
# поэтому обрати внимание
# Все операции предварительно делал в консоли (debug), потом просто вставил
# И перехожу на страницу настроек профиля
elem = driver.find_element(By.XPATH, "//a[contains(@href,'/settings/profile')]")
settings_link = elem.get_attribute('href')
driver.get(settings_link)

# Перехожу на страницу редактирования визуальной темы гитхаба
# Принцип такой же, как и в примере выше,
# только не задаю лишнюю переменную для ссылки, чем делаю код короче
elem = driver.find_element(By.XPATH, "//a[contains(@href, '/settings/appearance')]")
driver.get(elem.get_attribute('href'))

# Нахожу выпадашку, заношу её в объект класса Select и выбираю из выпадашки
# нужный элемент через его value
theme_mode = driver.find_element(By.ID, 'color_mode_type_select')
select = Select(theme_mode)
select.select_by_value('single')

# Метод, который вызывается относительно любого элемента
# внутри формы. В моём случае - это theme_mode (выпадашка)
# Не применяю, поскольку нет кнопки 'сохранить на странице',
# там автосохранение
# theme_mode.submit()



