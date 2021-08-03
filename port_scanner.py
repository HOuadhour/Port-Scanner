import socket
import re
from common_ports import ports_and_services


def returnError(target):
  if re.match(r"^[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}$", target):
    return "Error: Invalid IP address"
  else:
    return "Error: Invalid hostname"


def checkTarget(target):
  try:
    ip = socket.getaddrinfo(target, None)[1][4][0]
    return {
        "name": ip,
        "ip": ip
    }
  except Exception as error:
    print(error)
    return returnError(target)


def parseTarget(host):
  try:
    host["name"] = socket.gethostbyaddr(host["ip"])[0]
  except:
    pass

  return host


def get_open_ports(target, port_range, verbose=False):
  open_ports = []

  # check for the target
  out = checkTarget(target)
  if type(out) is str:
    return out

  host = parseTarget(out)

  for port in range(port_range[0], port_range[1] + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((host["ip"], port))
    if result == 0:
      open_ports.append(port)
    sock.close()

  if verbose:
    text = f"Open ports for {host['name']} ({host['ip']})\n"
    if host["name"] == host["ip"]:
      text = f"Open ports for {host['ip']}\n"
    text += "PORT     SERVICE\n"
    ports = []
    for port in open_ports:
      ports.append(str(port).ljust(9) + ports_and_services.get(port, "unknown"))

    text += "\n".join(ports)
    return text
  return(open_ports)


# print(parseTarget(checkTarget("104.26.10.78")))
# print(parseTarget(checkTarget("scanme.org")))
# print(parseTarget(checkTarget("137.74.187.104")))
