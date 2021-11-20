## ИИ Хакатоны и лекции по искусственному интеллекту. Челябинск 2021

### Решение команды OSError111 для кейса Росаккредитации

Полное наименование кейса: автоматизация определения кода Единого Перечня товаров для произведенной продукции)

В данном проекте для вашего удобства всё упаковано в docker-compose, поэтому имея данный инструмент вы с легкостью
запустите наш код!

### Установка и запуск

1) Установите docker-compose на свою ОС, если ещё не сделали этого
2) Склонируйте данный репозиторий  
   `git clone https://github.com/alexgoryushkin/hackathon_ai_chelyaninsk_2021_OSError111.git`
3) Перейдите в папку с проектом  
   `cd hackathon_ai_chelyaninsk_2021_OSError111`
4) Запустите сервисы с помощью docker-compose  
   `docker-compose up`
5) ...
6) PROFIT!!!

После запуска вам станет доступна веб страница нашего приложения.  
Найти её можно по адресу [http://localhost:80](http://localhost:80)

### Quick start

На главной странице доступны 2 блока - `Быстрая провека` и `Проверка файла`. В режиме `Быстрая провека` вы вводите
название товара и выбираете его категори(ю/и).  
Наш сервис определяет правильно ли указаны категории, и если нет, то предлагает свои варианты.  
Вы можете не выбирать никаких категорий вообще и довольствоваться лишь результатом нашего сервиса.

В блоке `Проверка файла` вы можете загрузить **xlsx** файл с данными о товарах для массовой проверки. На первой странице
будут искаться столбцы с заголовками
`Общее наименование продукции` и `Раздел ЕП РФ (Код из ФГИС ФСА для подкатегории продукции)`  
Категория продукции устанавливается по коду, строковое значение не рассматривается.

После загрузки файла он будет обработан, это может занять некоторое время. Страницу приложения не обязательно держать
открытой во время проверки. После завершения проверки вы можете ознакомиться с результатами.


***

# Типы

## Task

```typescript
{
    id:number,
    time:string
}
```

## Category

```typescript
{
    name:String,
    code:String
}
```

## SubTask

```typescript
{
    id:number,
    userCategories:[Category],
    defaultCategories:  [Category],
    isValid: boolean
}
```

# API

## POST /api/express

### Request

```typescript
{
    headers:{
        "Content-Type": "application/json"
    },
    body:{
        name: str
        codes:[Number]
    }
}
```

### Response

```typescript
{
    сategories:[Category],
    isValid: boolean
}
```


## POST /api/tasks

### Request

```typescript
{
    headers:{
        "Content-Type": "multipart/form-data",
    },
    body:{
        file:blob
    }
}
```

### Response

```typescript
{
    task: Task
}
```

## GET /api/tasks?skip=Number&take=Number

### Response

```typescript
{
    tasks:[Task]
}
```
## GET  /api/tasks/:id?skip=Number&take=Number

### Response

```typescript
{
    subTasks:[SubTask]
}
```