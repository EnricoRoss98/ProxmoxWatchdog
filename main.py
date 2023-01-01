from proxmoxer import ProxmoxAPI
import func_timeout
import time
import urllib3
import requests
from ping3 import ping

urllib3.disable_warnings()
url = None
ip = None

ip_vmid_list = {
    # "ScreenName": ["URL_to_check_if_VM_responds", "VM_ID", "VM_IP_address"]
    'OPNsense': ["https://192.168.12.1/", '100', "192.168.12.1"],
    'OMV': ["https://192.168.12.100:9001/", '101', "192.168.12.100"],
    'DockerVM': ["https://192.168.12.11:9001/", '102', "192.168.12.11"],
    'AlpineDMZ': ["https://192.168.1.99:9001/", '103', "192.168.1.99"]
}

# EDIT THIS
proxmox = ProxmoxAPI("192.168.12.10", user="root@pam", password="root_password", verify_ssl=False)


def request_page():
    global url
    return requests.get(url, verify=False).status_code


def ping_ip():
    global ip
    return ping(ip)


for vm in ip_vmid_list:
    url = ip_vmid_list[vm][0]
    ip = ip_vmid_list[vm][2]

    down = False

    status = proxmox.get('/api2/json/nodes/proxmox/qemu/' + ip_vmid_list[vm][1] + '/status/current')["status"]
    if status == "stopped":
        continue

    for ct in range(2):
        try:
            status_code = func_timeout.func_timeout(10, request_page)
            break
        except:
            # print(f'The page ' + url + ' is unreachable!')
            down = True
            time.sleep(1)

    if down:
        proxmox.post('/api2/json/nodes/proxmox/qemu/' + ip_vmid_list[vm][1] + '/status/stop')
        time.sleep(10)
        proxmox.post('/api2/json/nodes/proxmox/qemu/' + ip_vmid_list[vm][1] + '/status/start')
        print(vm + " RESTARTED at " + str(time.asctime()) + "\n")
