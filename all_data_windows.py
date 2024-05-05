import tkinter as tk
from tkinter import scrolledtext
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_information():
    info = ""
    info += "="*40 + " System Information " + "="*40 + "\n"
    uname = platform.uname()
    info += f"System: {uname.system}\n"
    info += f"Node Name: {uname.node}\n"
    info += f"Release: {uname.release}\n"
    info += f"Version: {uname.version}\n"
    info += f"Machine: {uname.machine}\n"
    info += f"Processor: {uname.processor}\n"
    info += f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n"
    info += f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n"
    info += f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n"

    # Boot Time
    info += "="*40 + " Boot Time " + "="*40 + "\n"
    boot_time_timestamp = psutil.boot_time()                           
    bt = datetime.fromtimestamp(boot_time_timestamp)
    info += f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n"

    # CPU Information
    info += "="*40 + " CPU Info " + "="*40 + "\n"
    info += f"Physical cores: {psutil.cpu_count(logical=False)}\n"
    info += f"Total cores: {psutil.cpu_count(logical=True)}\n"
    cpufreq = psutil.cpu_freq()
    info += f"Max Frequency: {cpufreq.max:.2f}Mhz\n"
    info += f"Min Frequency: {cpufreq.min:.2f}Mhz\n"
    info += f"Current Frequency: {cpufreq.current:.2f}Mhz\n"
    info += "CPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info += f"Core {i}: {percentage}%\n"
    info += f"Total CPU Usage: {psutil.cpu_percent()}%\n"

    # Memory Information
    info += "="*40 + " Memory Information " + "="*40 + "\n"
    svmem = psutil.virtual_memory()
    info += f"Total: {get_size(svmem.total)}\n"
    info += f"Available: {get_size(svmem.available)}\n"
    info += f"Used: {get_size(svmem.used)}\n"
    info += f"Percentage: {svmem.percent}%\n"

    info += "="*20 + " SWAP " + "="*20 + "\n"
    swap = psutil.swap_memory()
    info += f"Total: {get_size(swap.total)}\n"
    info += f"Free: {get_size(swap.free)}\n"
    info += f"Used: {get_size(swap.used)}\n"
    info += f"Percentage: {swap.percent}%\n"

    # Disk Information
    info += "="*40 + " Disk Information " + "="*40 + "\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        info += f"=== Device: {partition.device} ===\n"
        info += f"  Mountpoint: {partition.mountpoint}\n"
        info += f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        info += f"  Total Size: {get_size(partition_usage.total)}\n"
        info += f"  Used: {get_size(partition_usage.used)}\n"
        info += f"  Free: {get_size(partition_usage.free)}\n"
        info += f"  Percentage: {partition_usage.percent}%\n"
    disk_io = psutil.disk_io_counters()
    info += f"Total read: {get_size(disk_io.read_bytes)}\n"
    info += f"Total write: {get_size(disk_io.write_bytes)}\n"

    # Network Information
    info += "="*40 + " Network Information " + "="*40 + "\n"
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            info += f"=== Interface: {interface_name} ===\n"
            if str(address.family) == 'AddressFamily.AF_INET':
                info += f"  IP Address: {address.address}\n"
                info += f"  Netmask: {address.netmask}\n"
                info += f"  Broadcast IP: {address.broadcast}\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info += f"  MAC Address: {address.address}\n"
                info += f"  Netmask: {address.netmask}\n"
                info += f"  Broadcast MAC: {address.broadcast}\n"
    net_io = psutil.net_io_counters()
    info += f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n"
    info += f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n"

    return info

def display_system_information():
    system_info = get_system_information()

    # Create the main application window
    root = tk.Tk()
    root.title("System Information")

    # Create a scrolled text widget to display the system information
    text_area = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
    text_area.pack(expand=True, fill="both")

    # Insert the system information into the text area
    text_area.insert(tk.END, system_info)

    # Disable editing
    text_area.configure(state="disabled")

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    display_system_information()
