## Task 2
---

### Общие сведения
Задача решена с помощью python 3.4, sqlalchemy и mysql


### Окружение, установка и запуск
Подразумевается, что проект будет запускаться на Ubuntu 14.04 x64.

Установка необходимых пакетов
```
sudo apt-get install libmysqlclient-dev python3-pip libffi-dev
```

```
sudo pip3 install virtualenv
```

Клонируем проект
```
git clone git@github.com:ExordiumFrozen/alar-studios-database.git
cd alar-studios-database
```

Подразумевается, что mysql уже установлен и готов к работе.
Если нет, то:
```
sudo apt-get install mysql-server
```

Создаем базу для работы:
```
mysql -u root -p
create database task2_exordium;
grant all privileges on task2_exordium.* to 'task2_exordium'@'%' identified by 'task2_exordium'
flush privileges
```

Настраиваем окружение, инициируем базу и выполняем миграцию для создания таблиц:
```
virtualenv .
source bin/activate
pip install -r requirements.txt
```

Проверяем, есть ли целевая таблица, удаляем ее, создаем и наполняем данными:
```
./fill_database.py

```

Запускаем удаление ненужных записей:
```
./delete_rows.py
```

### Описание решения задачи
Все условия, поставленные в задаче, выполнены.  

1. Данные удаляются пачками по 100 строк.
2. Пауза между удалениями - 200ms.
3. Таблица содержит поля id и timestamp.
4. Удаляются данные старше 5 дней от текущего момента.
5. Использована sqlalchemy и mysql. Raw запросы.
6. Сид базы - `fill_database.py` - создается 21600 строк. То есть, одна запись на каждые 40 секунд на протяжении 10 суток.

Задача удаления решена очень просто - выбираем id записей, которые необходимо удалить.  
Затем получаем по 100 записей, и удаляем их самым простым запросом - `delete from table where id in ();`.  
Пауза между удалениями - 200 миллисекунд.


### Что можно было сделать лучше в данной реализации
- нужно обрабатывать исключения;
- настройки подключения можно вынести в конфигурационный файл;
- сделать более информативный вывод;
- взаимодействие с пользователем через аргументы командной строки;
- сид базы с помощью миграции;
- логирование результатов работы

### Но, этой задачи не было бы при соблюдении следующих рекомендаций
Я глубоко убежден своим и опытом многих профессионалов в том, что RDBMS хороши и эффективны при соблюдении соотношения чтение/запись на уровне 70/30.  

Из этой задачи следует, что в "проекте" не очень важные, часто меняющиеся данные пишутся в rdbms.  
Более того, эти данные со временем устаревают, что приводит к необходимости их удалять.  
Похоже на подписки, уведомления или социальные связи. Быть может, это какая-то статистика.  

В любом случае, следующие рекомендации могли бы предотвратить подобную ситуацию:
- в случае необходимости использовать sql - сделать партиционирование по критерю даты. В таком случае будут более мелкие таблицы, которые можно легко чистить, удалять никак не влияя на работу приложения;  
- подобная ситуация вредна при работе с postgres и интенсивной записи - vacuum, даже будучи правильно настренным, будет часто забирать себе ресурсы;  
- в данной ситуации более подходящим хранилищем для подобного рода данных выглядит mongodb для данных пользователей, elasticsearch для статистических данных, данных о событиях и т.д.

### Дополнительные сведения
На решение этой задачи потрачено 2 часа.

