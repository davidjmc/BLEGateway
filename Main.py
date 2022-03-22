import socket

_env = {}
with open("env.ini", "r") as file:
    for line in file:
        
        if line.strip() == '':
            continue

        [key, value] = [p.strip for p in line.split("=")]
        _env[key] = value

ipAddress = socket.gethostbyname(socket.gethostname())

from Amot import AmotRuntime
from Gateway import Gateway

AmotRuntime.setInstanceWith(ipAddress, _env)
AmotRuntime.getInstance().main(Gateway())
