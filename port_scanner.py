import socket
import subprocess
import re
from common_ports import ports_and_services


def returnError(target):
  if re.match(r"^[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}$", target):
    return "Error: Invalid IP address"
  else:
    return "Error: Invalid hostname"


def checkTarget(target):
  try:
    out = subprocess.check_output(f"ping -c1 {target}", timeout=2, shell=True).decode()
    if "1 received" in out:
      out = re.findall(r"from (.+):", out)
      return out[0].split(" ")
    else:
      return returnError(target)
  except Exception as error:
    print(error)
    return returnError(target)


def parseTarget(target):
  host = {}
  if len(target) == 1:
    host["name"] = target[0]
    host["ip"] = target[0]
  elif len(target) == 2:
    host["name"] = target[0]
    host["ip"] = target[1][1:-1]

  if host["name"] == host["ip"]:
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
