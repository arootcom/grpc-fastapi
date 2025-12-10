# grpc-fastapi

* [https://github.com/0xN1ck/grpc_example/](https://github.com/0xN1ck/grpc_example/)
* [https://grpc.io/docs/languages/python/quickstart/](https://grpc.io/docs/languages/python/quickstart/)


```
$ docker build -t python3-grpc .
$ docker-compose up -d
$ docker exec -it orders-api bash
# python3 -m grpc_tools.protoc --python_out=./protos/order --grpc_python_out=./protos/order --pyi_out=./protos/order --proto_path=./protos/ ./protos/order.proto
```

```
curl -X 'POST' 'http://localhost:8080/order?name=test&completed=false' -H 'accept: application/json'
```

