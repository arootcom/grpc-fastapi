# Один микросервис - один контейнер. День 1

Это первая статья о том, как идея проходит путь от прототипа до полноценного продукта — с участием архитектуры на каждом шагу. Формат — ADR (Architecture Decision Records): каждое решение зафиксировано по дням, чтобы показать реальную эволюцию проекта. Продукт вымышленный, проблемы — настоящие. Те самые, с которыми сталкиваются архитекторы и команды. Документация и код — в открытом доступе на [GitHub](https://github.com/arootcom/grpc-fastapi).

## Контекст

В процессе разработки находится [прототип](https://github.com/arootcom/grpc-fastapi/tree/day1) на Python, состоящий из:

* Трех gRPC-микросервисов: заказы, резервирование и лояльность
* API-шлюза (оркестратора) с последовательным вызовом методов: резервирование товаров → применение лояльности → сохранение заказа

Текущая архитектура:

* Микросервисы запускаются как отдельные процессы через [asyncio](https://docs.python.org/3/library/asyncio.html)
* Все компоненты упакованы в один [контейнер](https://github.com/arootcom/grpc-fastapi/blob/main/docker-compose-singl.yaml)

Выявленные проблемы: Несмотря на независимость микросервисов, ошибка в одном сервисе может вызвать каскадный сбой в других. Это создает риски для:

* Масштабируемости
* Отказоустойчивости
* Мониторинга
* Безопасности

![Component](./day1/deploy-singl.svg)


Далее описан процесс запуска и исследования прототипа микросервисной архитектуры на базе Python с использованием gRPC и Docker. Прототип включает в себя три микросервиса (заказы, резервирование и лояльность) и API-шлюз (оркестратор) для координации запросов.

### Запуск прототипа

1. Подготовка окружения

Чтобы запустить прототип, необходимо в первую очередь собрать образ контейнера. Для этого выполните следующие действия:

Шаг 1. Клонирование репозитория

Склонируйте репозиторий проекта на локальную машину.

```
$ git clone git@github.com:arootcom/grpc-fastapi.git
$ cd ./grpc-fastapi
```

Шаг 2. Переключение на рабочую ветку

Переключитесь на ветку day1. 

```
$ git remote update
$ git checkout -b day1 origin/day1
$ git pull
```

Если всё выполнено верно, при просмотре списка локальных веток вы увидите следующий результат, где рабочая ветка будет помечена знаком *.

```
$ git branch
* day1
  main
```

Шаг 3. Сборка образа

Соберите образ контейнера python3-grpc. 

```
$ docker build -t python3-grpc .
```

Список доступных локально собранных образов должен обязательно содержать две записи.

```
$ docker images
REPOSITORY     TAG       IMAGE ID       CREATED        SIZE
python3-grpc   latest    1c1383197816   45 hours ago   1.25GB
python         3         4db51a7249e1   2 weeks ago    1.12GB
```

Шаг 4. Запуск сервиса

Теперь всё готово для запуска.

```
$ docker-compose -f docker-compose-signl.yaml up
main  | 2025-12-19 09:26:34.346 | INFO     | servers.server:__init__:42 - Enable reflation server
main  | 2025-12-19 09:26:34.354 | INFO     | servers.server:register:48 - Register: Order Service
main  | 2025-12-19 09:26:34.354 | INFO     | servers.server:register:50 - Register: Reserve Service
main  | 2025-12-19 09:26:34.354 | INFO     | servers.server:register:52 - Register: Loyalty Service
main  | 2025-12-19 09:26:34.354 | INFO     | servers.server:run:58 - *** Сервис gRPC запущен: 0.0.0.0:50091 ***
```

2. Конфигурация и запуск

Сервис main запускается вызовом команды python [main.py](https://github.com/arootcom/grpc-fastapi/blob/day1/app/main.py).

Для управления контейнерами в приложении используется [Docker Compose](https://docs.docker.com/compose/). Параметры окружения описаны в файле [docker-compose-single.yaml](https://github.com/arootcom/grpc-fastapi/blob/day1/docker-compose-singl.yaml).

```yaml
version: '3.8'
name: "grpc-fastapi-singl"
services:
  main:
    container_name: main
    image: python3-grpc
    volumes:
      - "./app:/usr/src/app"
    environment:
      - GRPC_HOST_ORDERS=0.0.0.0
      - GRPC_HOST_LOYALTIES=0.0.0.0
      - GRPC_HOST_RESERVE=0.0.0.0
      - GRPC_HOST_LOCAL=0.0.0.0
      - GRPC_PORT=50091
      - SERVICE_PORT=1111
      - SERVICE_HOST_LOCAL=0.0.0.0
    ports:
      - "8080:1111"
      - "8787:50091"
    command: "python main.py"
```

3. Инициализация

Enable Reflection Server — это сервис, который позволяет клиентам динамически обнаруживать сервисы и их методы на сервере gRPC во время выполнения.

Принцип работы:

Работает по протоколу gRPC Server Reflection Protocol для обнаружения сервисов.

Реализация:

Инициализация реализована в [singleton-классе](https://habr.com/ru/companies/otus/articles/779914/) [servers.server](https://github.com/arootcom/grpc-fastapi/blob/day1/app/servers/server.py), который гарантирует, что у класса будет только один экземпляр. После инициализации выполняется регистрация доступных сервисов в данном экземпляре сервера и его запуск.

```python
from loguru import logger
from grpc import aio
from grpc_reflection.v1alpha import reflection
    
[skip]

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
           self.SERVER_ADDRESS = f'{os.environ["GRPC_HOST_LOCAL"]}:{os.environ["GRPC_PORT"]}'
            self.server = aio.server(ThreadPoolExecutor(max_workers=10))
            self.server.add_insecure_port(self.SERVER_ADDRESS)

            SERVICE_NAMES = (
                order_pb2.DESCRIPTOR.services_by_name["OrderService"].full_name,
                reserve_pb2.DESCRIPTOR.services_by_name["ReserveService"].full_name,
                loyalty_pb2.DESCRIPTOR.services_by_name["LoyaltyService"].full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self.server)
            logger.info(f'Enable reflation server')

            self.initialized = True
[skip]

    def register(self) -> None:
        order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), self.server)
        logger.info(f'Register: Order Service')
        reserve_pb2_grpc.add_ReserveServiceServicer_to_server(ReserveService(), self.server)
        logger.info(f'Register: Reserve Service')
        loyalty_pb2_grpc.add_LoyaltyServiceServicer_to_server(LoyaltyService(), self.server)
        logger.info(f'Register: Loyalty Service')

    async def run(self) -> None:
        self.register()
        await self.server.start()
        logger.info(f'*** Сервис gRPC запущен: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

[skip]
```

### Исследование прототипа

1. Просмотр запущенных контейнеров

При просмотре запущенных контейнеров вы увидите один контейнер с именем main (колонка NAMES).

```
$ docker ps 
CONTAINER ID   IMAGE          COMMAND            CREATED      STATUS      PORTS                                                                                        NAMES
0064b53278c2   python3-grpc   "python main.py"   4 days ago   Up 3 days   0.0.0.0:8080->1111/tcp, [::]:8080->1111/tcp, 0.0.0.0:8787->50091/tcp, [::]:8787->50091/tcp   main

```

Конфигурация портов:

Два порта, определённые в контейнере, проброшены на порты localhost

* Порт 8080 принимает запросы по [HTTP](https://ru.wikipedia.org/wiki/HTTP)
* Порт 8787 принимает запросы по [gRPC](https://ru.wikipedia.org/wiki/GRPC)

2. REST API: создание заказа

Используем для запроса утилиту командной строки [curl](https://ru.wikipedia.org/wiki/CURL).

```
$ curl -X 'POST' 'http://localhost:8080/order?name=test&completed=false' -H 'accept: application/json'
``` 

Результат обработки запроса:

```json
{
  "notificationType": "ORDER_NOTIFICATION_TYPE_ENUM_OK",
  "order": {
    "uuid": "9841d6f7-69df-4986-b837-65c386acb41d"
  }
}
```

![](./day1/sq-curl-singl.svg)

В консоли, где запущен docker-compose, вы увидите логи — последовательные записи о вызовах и результатах работы связанных бизнес-логикой микросервисов:

* Получение входящего запроса и запрос на резервирование

```
main  | INFO:     172.22.0.1:56680 - "POST /order?name=test&completed=false HTTP/1.1" 200 OK
main  | 2025-12-22 09:26:56.083 | INFO     | servers.services.reserve:ReserveItem:16 - Received request is for reserve item: uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64' quantity=10
main  | 2025-12-22 09:26:56.083 | SUCCESS  | servers.handlers.reserve:reserve_item:12 - Reserved item: {'uuid': '5f23a419-3a68-4c6a-87a9-d14f9f021a64', 'name': 'asdf', 'instock': 3, 'reserve': 10}
main  | 2025-12-22 09:26:56.084 | DEBUG    | servers.services.reserve:ReserveItem:20 - Result reserve item: notificationType='RESERVE_NOTIFICATION_TYPE_ENUM_OK' item=Item(uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64', name='asdf', instock=3, reserve=10)
```

* Запрос информации о лояльности

```
main  | 2025-12-22 09:26:56.086 | INFO     | servers.services.loyalty:LoyaltyInfo:16 - Received request is for loyalty info: uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64' quantity=10
main  | 2025-12-22 09:26:56.086 | SUCCESS  | servers.handlers.loyalty:loyalty_info:10 - Loyalty info: {'uuid': '5f23a419-3a68-4c6a-87a9-d14f9f021a64', 'persent': 10}
main  | 2025-12-22 09:26:56.086 | DEBUG    | servers.services.loyalty:LoyaltyInfo:20 - Result loyalty info: notificationType='LOYALTY_NOTIFICATION_TYPE_ENUM_OK' loyalty=Loyalty(uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64', persent=10)
```

* Создание заказа

```
main  | 2025-12-22 09:26:56.089 | INFO     | servers.services.order:CreateOrder:25 - Received request is for create order: uuid='9841d6f7-69df-4986-b837-65c386acb41d' name='test' completed=False date='2025-12-19 09:26:34.311752Z'
main  | 2025-12-22 09:26:56.104 | SUCCESS  | servers.handlers.order:create_order:8 - Created order: [{'uuid': '9841d6f7-69df-4986-b837-65c386acb41d'}]
main  | 2025-12-22 09:26:56.104 | DEBUG    | servers.services.order:CreateOrder:29 - Result created order: notificationType='ORDER_NOTIFICATION_TYPE_ENUM_OK' order=OrderResponse(uuid='9841d6f7-69df-4986-b837-65c386acb41d', name=None, completed=False, date=None)
```

3. Исследование gRPC-сервисов

Используем утилиту командной строки [grpcurl](https://habr.com/ru/companies/vdsina/articles/563872/) для анализа:

Доступные операции:

* Просмотр обслуживаемых микросервисов

```bash
$ grpcurl -plaintext localhost:8787 list
grpc.reflection.v1alpha.ServerReflection
protos.loyalties.LoyaltyService
protos.order.OrderService
protos.warehouse.ReserveService
```

* Просмотр методов микросервиса

```bash
$ grpcurl -plaintext localhost:8787 list  protos.order.OrderService
protos.order.OrderService.CreateOrder
```

* Просмотр модели запроса

```bash
$ grpcurl -plaintext localhost:8787 describe protos.order.CreateOrderRequest
protos.order.CreateOrderRequest is a message:
message CreateOrderRequest {
  string name = 1;
  bool completed = 2;
  string date = 3;
}
```

* Создание заказа

```bash
$ grpcurl -plaintext -d '{"name":"first"}' localhost:8787 protos.order.OrderService/CreateOrder
{
  "notificationType": "ORDER_NOTIFICATION_TYPE_ENUM_OK",
  "order": {
    "uuid": "0eca9a0f-a52a-4d76-b9f8-375d3387c143"
  }
}
```

### Важные особенности и ограничения

1. Прямой вызов gRPC

По логам видно, что при прямом вызове gRPC происходит прямое резервирование без учёта бизнес-логики проверки остатков и применения лояльности.

> [!CAUTION]
> Это означает, что при прямом доступе нет гарантии атомарности операции — завершения всех шагов либо ни одного.

2. Рекомендации

Для обеспечения целостности данных и соблюдения бизнес-логики рекомендуется использовать запросы через API-шлюз (оркестратор), который обеспечивает корректную последовательность вызовов и применение всех необходимых проверок.

### Заключение

Данный прототип демонстрирует базовые принципы работы микросервисной архитектуры с использованием gRPC и Docker. Следуя описанным шагам, вы сможете запустить и исследовать работу системы, понять особенности взаимодействия микросервисов и выявить потенциальные точки роста архитектуры.

Прямой доступ к gRPC-сервисам создаёт риск частичного выполнения бизнес-процесса, что может привести к:

* Некорректным данным
* Потере информации о применённых скидках
* Резервированию недоступных товаров

Архитектурные улучшения

Для обеспечения целостности системы рекомендуется:

* Использовать только API-шлюз (оркестратор) для бизнес-операций
* Ограничить прямой доступ к gRPC-сервисам на уровне сети
* Внедрить транзакционную модель (например, Saga Pattern)
* Добавить мониторинг для отслеживания частичных сбоев

Следующие шаги эволюции:

* Разделение контейнеров для независимого масштабирования

## Решение

Разделение микросервисов по контейнерам — это архитектурное решение, обеспечивающее изоляцию сервисов, независимость в развертывании и масштабировании.

Ключевые преимущества подхода:

1. Минимизация размера контейнера. Каждый контейнер содержит только необходимые зависимости и код, что упрощает управление ресурсами и ускоряет развертывание.
2. Эффективное масштабирование. Каждый микросервис масштабируется независимо от других, обеспечивая оптимальное распределение нагрузки и рациональное использование инфраструктуры.
3. Упрощённое обновление и управление. Изменения в одном микросервисе не требуют пересоздания всех контейнеров — обновляется только затронутый сервис.
4. Гибкое управление зависимостями и версиями. Различные версии микросервисов могут существовать параллельно, не влияя на работу других компонентов системы.


![](./day1/deploy-multi.svg)

Внесённые изменения в архитектуру:

1. Прямой вызов gRPC к микросервисам заказов, резервирования и лояльности заблокирован
2. Все вызовы осуществляются только через API Gateway по REST API
3. Контейнер main декомпозирован на четыре независимых контейнера:
    * gw — микросервис-оркестратор, содержащий бизнес-логику создания заказа
    * orders service — микросервис управления заказами
    * reserve service — микросервис управления резервированием данных заказа
    * loyalty service — микросервис управления данными о лояльности

### Запуск измененного прототипа

> [!IMPORTANT]
> Предварительные условия
> 1. Репозиторий проекта склонирован
> 2. Выбрана ветка day1
> 3. Образ контейнера python3-grpc собран

1. Запуск проекта 

```
$ docker-compose -f ./docker-compose-multi.yaml up
[+] Running 4/0
 ⠿ Container gw         Created
 ⠿ Container loyalties  Created
 ⠿ Container orders     Created
 ⠿ Container reserve    Created
Attaching to gw, loyalties, orders, reserve
reserve    | 2025-12-22 12:23:20.786 | INFO     | servers.reserve:__init__:31 - Enable reflation server
reserve    | 2025-12-22 12:23:20.786 | INFO     | servers.reserve:register:37 - Register: Reserve Service
reserve    | 2025-12-22 12:23:20.786 | INFO     | servers.reserve:run:42 - *** Сервис Reserve gRPC запущен: reserve:50091 ***
loyalties  | 2025-12-22 12:23:20.833 | INFO     | servers.loyalties:__init__:31 - Enable reflation server
loyalties  | 2025-12-22 12:23:20.834 | INFO     | servers.loyalties:register:37 - Register: Loyalty Service
loyalties  | 2025-12-22 12:23:20.834 | INFO     | servers.loyalties:run:42 - *** Сервис Loyalties gRPC запущен: loyalties:50091 ***
orders     | 2025-12-22 12:23:20.952 | INFO     | servers.orders:__init__:32 - Enable reflation server
orders     | 2025-12-22 12:23:20.959 | INFO     | servers.orders:register:38 - Register: Order Service
orders     | 2025-12-22 12:23:20.960 | INFO     | servers.orders:run:44 - *** Сервис Orders gRPC запущен: orders:50091 ***
gw         | INFO:     Will watch for changes in these directories: ['/usr/src/app']
gw         | INFO:     Uvicorn running on http://0.0.0.0:1111 (Press CTRL+C to quit)
gw         | INFO:     Started reloader process [1] using StatReload
gw         | INFO:     Started server process [8]
gw         | INFO:     Waiting for application startup.
gw         | INFO:     Application startup complete.
```

По логам видно, что запустилось четыре контейнера, описанных в файле [docker-compose-multi.yaml](https://github.com/arootcom/grpc-fastapi/blob/day1/docker-compose-multi.yaml).

Скрипты для запуска контейнеров размещены в директории проекта [app/](https://github.com/arootcom/grpc-fastapi/tree/day1/app/) и соответствуют именам контейнеров:

* [gw.py](https://github.com/arootcom/grpc-fastapi/blob/day1/app/gw.py)
* [loyalties.py](https://github.com/arootcom/grpc-fastapi/blob/day1/app/loyalties.py)
* [orders.py](https://github.com/arootcom/grpc-fastapi/blob/day1/app/orders.py)
* [reserve.py](https://github.com/arootcom/grpc-fastapi/blob/day1/app/reserve.py)

### Исследование измененного прототипа

1. Просмотр запущенных контейнеров

```
$ docker ps 
CONTAINER ID   IMAGE          COMMAND                 CREATED      STATUS             PORTS                                         NAMES
bde2a383c5f7   python3-grpc   "python orders.py"      5 days ago   Up About an hour                                                 orders
18a6bd24b3a4   python3-grpc   "python loyalties.py"   5 days ago   Up About an hour                                                 loyalties
0e5972f9928e   python3-grpc   "python reserve.py"     5 days ago   Up About an hour                                                 reserve
5dc86b298da5   python3-grpc   "python gw.py"          5 days ago   Up About an hour   0.0.0.0:8080->1111/tcp, [::]:8080->1111/tcp   gw
```

Видим четыре запущенных контейнера. Порт, определённый в контейнере gw, проброшен на порт localhost, как показано на схеме выше. Порт 8080 принимает запросы по [HTTP](https://ru.wikipedia.org/wiki/HTTP).

2.  REST API: создание заказа

Используем утилиту командной строки [curl](https://ru.wikipedia.org/wiki/CURL). Сам запрос не изменился.

```
$ curl -X 'POST' 'http://localhost:8080/order?name=test&completed=false' -H 'accept: application/json'
``` 

Результат обработки запроса:

```json
{
  "notificationType": "ORDER_NOTIFICATION_TYPE_ENUM_OK",
  "order": {
    "uuid": "9841d6f7-69df-4986-b837-65c386acb41d"
  }
}
```

![](./day1/sq-curl-multi.svg)

Теперь логи и адреса вызовов изменились — каждый запрос идёт в отдельный контейнер:

Получение входящего запроса:
```
gw         | INFO:     172.20.0.1:57392 - "POST /order?name=test&completed=false HTTP/1.1" 200 OK
```

Запрос на резервирование:
```
reserve    | 2025-12-22 13:54:52.486 | INFO     | servers.services.reserve:ReserveItem:16 - Received request is for reserve item: uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64' quantity=10
reserve    | 2025-12-22 13:54:52.486 | SUCCESS  | servers.handlers.reserve:reserve_item:12 - Reserved item: {'uuid': '5f23a419-3a68-4c6a-87a9-d14f9f021a64', 'name': 'asdf', 'instock': 3, 'reserve': 10}
reserve    | 2025-12-22 13:54:52.486 | DEBUG    | servers.services.reserve:ReserveItem:20 - Result reserve item: notificationType='RESERVE_NOTIFICATION_TYPE_ENUM_OK' item=Item(uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64', name='asdf', instock=3, reserve=10)
```

Запрос информации о лояльности:
```
loyalties  | 2025-12-22 13:54:52.491 | INFO     | servers.services.loyalty:LoyaltyInfo:16 - Received request is for loyalty info: uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64' quantity=10
loyalties  | 2025-12-22 13:54:52.492 | SUCCESS  | servers.handlers.loyalty:loyalty_info:10 - Loyalty info: {'uuid': '5f23a419-3a68-4c6a-87a9-d14f9f021a64', 'persent': 10}
loyalties  | 2025-12-22 13:54:52.492 | DEBUG    | servers.services.loyalty:LoyaltyInfo:20 - Result loyalty info: notificationType='LOYALTY_NOTIFICATION_TYPE_ENUM_OK' loyalty=Loyalty(uuid='5f23a419-3a68-4c6a-87a9-d14f9f021a64', persent=10)
```

Создание заказа:
```
orders     | 2025-12-22 13:54:52.497 | INFO     | servers.services.order:CreateOrder:25 - Received request is for create order: uuid='3b2b8bb5-f488-483d-a1f1-b2771fd84149' name='test' completed=False date='2025-12-22 12:23:22.447949Z'
orders     | 2025-12-22 13:54:52.512 | SUCCESS  | servers.handlers.order:create_order:8 - Created order: [{'uuid': '3b2b8bb5-f488-483d-a1f1-b2771fd84149'}]
orders     | 2025-12-22 13:54:52.512 | DEBUG    | servers.services.order:CreateOrder:29 - Result created order: notificationType='ORDER_NOTIFICATION_TYPE_ENUM_OK' order=OrderResponse(uuid='3b2b8bb5-f488-483d-a1f1-b2771fd84149', name=None, completed=False, date=None)
```

## Обоснование

Принцип «Один микросервис — один контейнер» в микросервисной архитектуре обоснован необходимостью изоляции и переносимости микросервисов.

Этот подход позволяет:

* Разрабатывать, тестировать и масштабировать компоненты по отдельности
* Обеспечивать согласованность между средой разработки, тестовой средой и production

Ключевые преимущества:

1. Изоляция. Контейнеры работают независимо и не влияют друг на друга. Сбой в одном сервисе не приводит к падению всей системы.

2. Переносимость. Контейнеризированное приложение можно запускать в различных типах инфраструктуры:

* На «голом железе»
* В виртуальных машинах
* В облаке

...без необходимости рефакторинга для каждой среды.

3. Экономия ресурсов. Контейнеры используют ядро хостовой операционной системы без полной виртуализации оборудования, что делает их легковесными и обеспечивает экономию ресурсов по сравнению с традиционными виртуальными машинами.

## Последствия

Когда микросервисов становится много, управлять контейнерами вручную становится затруднительно. Здесь на помощь приходят оркестраторы — системы автоматизации развёртывания, масштабирования, балансировки и мониторинга контейнеров.

Например, Kubernetes обеспечивает:

* Запуск контейнеров
* Мониторинг состояния
* Автоматический перезапуск после сбоев
* Масштабирование сервисов в зависимости от нагрузки

### Преимущества

1. Простота поддержки и обновления. Команды могут работать над разными сервисами параллельно, не мешая друг другу.
2. Избирательное масштабирование. Если один компонент испытывает высокую нагрузку, можно увеличить ресурсы только для него, а не для всего приложения.
3. Лёгкость модернизации. Старые сервисы можно постепенно заменять новыми без полного переписывания кода.

### Недостатки и риски

1. Сложность тестирования. Необходимо тестировать:

* Каждый микросервис отдельно
* Взаимодействие между сервисами

Решение: внедрить автоматические интеграционные и сервисные тесты.

2. Ограничение внешних вызовов. Вызовы от внешних клиентов возможны только по REST API через API Gateway.

Решение: рассмотреть возможность добавления вызовов к gw по gRPC или альтернативного варианта коммуникации.

3. Отсутствие гарантии атомарности транзакций. Нет встроенного механизма, гарантирующего, что либо завершатся все шаги транзакции, либо ни одного.

Решение: внедрить паттерны обеспечения консистентности в распределённых системах:

* Saga Pattern (паттерн саги)
* Transactional Outbox (подход «сохрани, затем опубликуй»)
* Idempotent Operations (идемпотентные операции)

