# grpc-fastapi

# Подсказки

1. Собрать образ

```
$ docker build -t python3-grpc .
```

2. Генерация gRPC код для Python

```
$ docker exec -it orders-api bash
# python3 -m grpc_tools.protoc --python_out=./protos/order --grpc_python_out=./protos/order --pyi_out=./protos/order --proto_path=./protos/ ./protos/order.proto
```

3. Запуск окружения все в одном конейнере

```
$ docker-compose up -d
```

4. Запуск окрежения каждый сикросервис в отдельном контейнере

```
$ docker-compose -f docker-compose-multi.yaml up
```

5. Запрос создать заказ

```
curl -X 'POST' 'http://localhost:8080/order?name=test&completed=false' -H 'accept: application/json'
```

# Материалы

* [https://github.com/0xN1ck/grpc_example/](https://github.com/0xN1ck/grpc_example/)
* [https://grpc.io/docs/languages/python/quickstart/](https://grpc.io/docs/languages/python/quickstart/)
* [https://habr.com/ru/companies/wunderfund/articles/700474/](https://habr.com/ru/companies/wunderfund/articles/700474/)
* [https://habr.com/ru/articles/894766/?ysclid=mj30m3o7vq394437717](Принцип каскадного снижения связанности)

