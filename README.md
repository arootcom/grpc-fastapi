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
# python3 -m grpc_tools.protoc --python_out=./protos/reserve --grpc_python_out=./protos/reserve --pyi_out=./protos/reserve --proto_path=./protos/ ./protos/reserve.proto
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

6. gRPC запрос

Установить grpcurl (пример для Kubuntu)

```
# sudo apt update
# sudo apt install snapd
# sudo snap install grpcurl --edge
```

```
$ grpcurl -plaintext localhost:8787 list
$ grpcurl -plaintext localhost:8787 list  protos.order.OrderService
$ grpcurl -plaintext -d '{"name":"first"}' localhost:8787 protos.order.OrderService/CreateOrder
```

# Материалы

* [gRPC ecample](https://github.com/0xN1ck/grpc_example/)
* [gRPC: Quick start](https://grpc.io/docs/languages/python/quickstart/)
* [gRPC: Guides](https://grpc.io/docs/guides/)
* [Полное руководство по модулю asyncio в Python. Часть 1](https://habr.com/ru/companies/wunderfund/articles/700474/)
* [Принцип каскадного снижения связанности](https://habr.com/ru/articles/894766/?ysclid=mj30m3o7vq394437717)
* [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
* [Language Guide (proto 3)](https://protobuf.dev/programming-guides/proto3/)
* [gRPCurl — curl для gRPC-серверов](https://habr.com/ru/companies/vdsina/articles/563872/)
