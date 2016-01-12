# Bequeather Client - Python

## Usage
```python
from client import Client

ip, port = "127.0.0.1", 666

c = Client().connect(ip, port).callRoutine('RoutineName', 'functionName')

print("Header: {}".format(c.getResponse()))
print("Response: {}".format(c.getResponse()))
```
