import threading
import socket

lock = threading.Lock()

class DeviceScan:
    routers = []

    def __init__(self, start_ip, end_ip):
        self.start_ip = start_ip
        self.end_ip = end_ip
        start_index = self.get_last_ip(start_ip)
        end_index = self.get_last_ip(end_ip)
        if start_index is not None and end_index is not None:
            self.scan(int(start_index), int(end_index))

    def get_last_ip(self, ip):
        if ip is not None and len(ip) > 0:
            ips = ip.split(".")
            if len(ips) == 4:
                return ips[3]
            else:
                return None
        else:
            return None

    def check_ip(self, new_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        s.settimeout(1)
        PORT = 5555
        result = s.connect_ex((new_ip, PORT))
        if result == 0:
            lock.acquire()  # get lock
            self.routers.append(new_ip)
            lock.release()

    def scan(self, start_index, end_index):
        local_ip = socket.gethostbyname_ex(socket.gethostname())
        all_threads = []
        for ip in local_ip[2]:
            for i in range(start_index, end_index):
                array = ip.split(".")  # split ip for dot
                array[3] = str(i)
                new_ip = '.'.join(array)
                t = threading.Thread(target=self.check_ip, args=(new_ip,))
                t.start()
                all_threads.append(t)
            for t in all_threads:
                t.join()

    def get_ips(self):
        return self.routers


result = DeviceScan('192.168.31.1', '192.168.31.255').get_ips()
print(result)
