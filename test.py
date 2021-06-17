# coding: utf-8
"""
This is to test the fortideploy.FortiDeploy class
"""
import fortideploy
import base64

ip = "10.210.35.105"
login = "admin"
password = "fortinet"

# Login
fdp = fortideploy.FortiDeploy()
fdp.login(ip, login, password)

# Backup
# content = fdp.backup()
# print(content)

# Restore
file = "36K_rules.config.cfg"
with open(file, "rb") as f:
    content = f.read()
    base64Content = base64.b64encode(content)
    fdp.debug("on")
    fdp.restore(base64Content, append=False)
    fdp.debug("off")

# Logout
fdp.logout()
