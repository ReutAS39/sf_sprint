## sf_sprint

______
### Стек технологий 


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
______
### Описание проекта

_API мобильного приложения для Android и IOS.
*Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их на сервер, как только появится доступ в Интернет.*
*Модератор будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.*_

*Турист с помощью мобильного приложения сможет внести следующие данные о перевале:*
+ ***координаты перевала и его высоту;***
+ ***категорию трудности;***
+ ***название перевала;***
+ ***несколько фотографий перевала;***
+ ***информацию о пользователе, который передал данные о перевале:***
  + ***ФИО пользователя;***
  + ***почта;***
  + ***телефон.***

*После этого турист нажимает кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовает метод submitData.*

______

### Документация для Эндпоинтов 
 
```python
POST/submitData/
 ```
 
 *принимает JSON в теле запроса с информацией о перевале. Пример JSON-а:*

``` sh
{
  "user":{
		"email": "qwerty@mail.ru", 
		"fam": "Пупкин", 
		"name": "Василий", 
		"otc": "Иванович", 
		"phone": "+7 555 55 55"
		}, 
   "coords":{
		"latitude": "45.3842",
		"longitude": "7.1525",
		"height": "1200"
		},
# Категория трудности. В разное время года перевал может иметь разную категорию трудности
  level:{
		"winter": "", 
		"summer": "1А",
		"autumn": "1А",
		"spring": ""
		},
 
  images: [{data:"<картинка1>", title:"Седловина"}, {data:"<картинка>", title:"Подъём"}]
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "", // что соединяет, текстовое поле
}

```

***Результат метода: JSON***

+ *status — код HTTP, целое число:*
 
    *500 — ошибка при выполнении операции;*
    
    *400 — Bad Request (при нехватке полей);*
    
    *200 — успех.*
    
+ *message — строка:*

   *Причина ошибки (если она была);*
    
    *Отправлено успешно;*
    
    *Если отправка успешна, дополнительно возвращается id вставленной записи.*
    
    *id — идентификатор, который был присвоен объекту при добавлении в базу данных.*
    
    
***Примеры oтветов:***

*{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}*

*{ "status": 200, "message": null, "id": 42 }*


*После того, как турист с помощью мобильного приложения отправил информацию о перевале, будет проведена модерация для каждого нового объекта, с изменением значения поля status.*

***Допустимые значения поля status:***

+ *'new';*
+ *'pending' — если модератор взял в работу;*
+ *'accepted' — модерация прошла успешно;*
+ *'rejected' — модерация прошла, информация не принята.*

______

```python
GET /submitData/<id>
```
*получает одну запись (перевал) по её id с выведением всей информацию об перевале, в том числе статус модерации.*



```python
PATCH /submitData/<id>
```

*позволяет отредактировать существующую запись (замена), при условии, что она в статусе "new". При этом редактировать можно все поля, кроме тех, что содержат ФИО, адрес почты и номер телефона. В качестве результата изменения приходит ответ содержащий следующие данные:*

 *state:*
     *1 — если успешно удалось отредактировать запись в базе данных.*
     *0 — в отредактировать запись не удалось.*
    
 *message: сообщение о причине неудачного обновления записи.*


   
```python
GET /submitData/?user__email=<email>
```
*позволяет получить данные обо всех объектах, которые пользователь с почтой `<email>` отправил на сервер.*


```python
GET /swagger/
```
*Подробная документация по работе с API.*

### Установка 

*1. Клонируйте репозиторий:*

   ```bash
   git clone https://github.com/ReutAS39/sf_sprint.git
   ```

*2. Перейдите в директорию проекта:*

   ```bash
   cd sf_sprint
   ```

*3. Создайте и активируйте виртуальное окружение:*

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

*4. Установите зависимости:*

   ```bash
   pip install -r requirements.txt
   ```


