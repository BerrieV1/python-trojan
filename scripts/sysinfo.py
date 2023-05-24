import os
import subprocess
from basemodule import BaseModule
import platform
import psutil


class Sysinfo(BaseModule):
    def get_os_info(self):
        os_info = {
            "os": platform.system(),
            "version": platform.version(),
            "architecture": platform.architecture(),
            "node": platform.node(),
            "user": platform.uname(),
            "machine": platform.machine()
        }
        return os_info

    def get_cpu_info(self):
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "usage_per_cpu": psutil.cpu_percent(interval=1, percpu=True),
            "usage_total": psutil.cpu_percent(interval=1),
            "freq": psutil.cpu_freq().current
        }
        return cpu_info

    def get_ram_info(self):
        ram_info = {
            "total_memory": psutil.virtual_memory().total / (1024 ** 3),
            "available_memory": psutil.virtual_memory().available / (1024 ** 3),
            "used_memory": psutil.virtual_memory().used / (1024 ** 3),
        }
        return ram_info

    def get_disk_info(self):
        disk_info = {}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem_type": partition.fstype,
                "total_size": usage.total / (1024 ** 3),
                "used_size": usage.used / (1024 ** 3),
                "free_size": usage.free / (1024 ** 3),
                "percentage_used": usage.percent
            }
            disk_info[partition.mountpoint] = partition_info
        return disk_info

    def get_network_info(self):
        network_info = {}
        addrs = psutil.net_if_addrs()
        addresses = []

        for net, address in addrs.items():
            if net != 'lo':  # Als de netwerkinterface niet de loopbackinterface is
                for addr in address:
                    if addr.family == 2:  # IPv4
                        addresses.append(addr.address)
                network_info[net] = addresses  # Het IP adres wordt toegewezen aan een dictionary met als key de
                # netwerkinterface
        return network_info

    def run(self):
        sysinfo_dir = "../sysinfo"
        if not os.path.exists(sysinfo_dir):
            os.makedirs(sysinfo_dir)

        sysinfo_file_path = os.path.join(sysinfo_dir, "sysinfo.txt")
        with open(sysinfo_file_path, "w") as sysinfo_file:
            sysinfo_file.write(f"{str(self.get_os_info())}\n")
            sysinfo_file.write(f"{str(self.get_cpu_info())}\n")
            sysinfo_file.write(f"{str(self.get_network_info())}\n")
            sysinfo_file.write(f"{str(self.get_ram_info())}\n")
            sysinfo_file.write(f"{str(self.get_disk_info())}\n")

    def install_requirements(self):
        libraries = ["psutil"]
        for library in libraries:
            subprocess.check_call(["pip", "install", library])