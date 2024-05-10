import tkinter as tk     #toolkit for GUI
from tkinter import scrolledtext
import psutil     #for system information
import platform  #for OS data
from datetime import datetime
import cpuinfo
import socket
import uuid
import re


# function for get convert data to byte for human readable
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_information():
    info = {}
    uname = platform.uname()
    info["System Information"] = f"System: {uname.system}\n" \
                                 f"Node Name: {uname.node}\n" \
                                 f"Release: {uname.release}\n" \
                                 f"Version: {uname.version}\n" \
                                 f"Machine: {uname.machine}\n" \
                                 f"Processor: {uname.processor}\n" \
                                 f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n" \
                                 f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n" \
                                 f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n"

    boot_time_timestamp = psutil.boot_time()                           
    bt = datetime.fromtimestamp(boot_time_timestamp)
    info["Boot Time"] = f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n"

    info["CPU Info"] = f"Physical cores: {psutil.cpu_count(logical=False)}\n" \
                       f"Total cores: {psutil.cpu_count(logical=True)}\n"
    cpufreq = psutil.cpu_freq()
    info["CPU Info"] += f"Max Frequency: {cpufreq.max:.2f}Mhz\n" \
                        f"Min Frequency: {cpufreq.min:.2f}Mhz\n" \
                        f"Current Frequency: {cpufreq.current:.2f}Mhz\n" \
                        "CPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info["CPU Info"] += f"Core {i}: {percentage}%\n"
    info["CPU Info"] += f"Total CPU Usage: {psutil.cpu_percent()}%\n"

    svmem = psutil.virtual_memory()
    info["Memory Information"] = f"Total: {get_size(svmem.total)}\n" \
                                  f"Available: {get_size(svmem.available)}\n" \
                                  f"Used: {get_size(svmem.used)}\n" \
                                  f"Percentage: {svmem.percent}%\n"

    swap = psutil.swap_memory()
    info["SWAP"] = f"Total: {get_size(swap.total)}\n" \
                   f"Free: {get_size(swap.free)}\n" \
                   f"Used: {get_size(swap.used)}\n" \
                   f"Percentage: {swap.percent}%\n"

    partitions = psutil.disk_partitions()
    info["Disk Information"] = ""
    for partition in partitions:
        info["Disk Information"] += f"=== Device: {partition.device} ===\n" \
                                    f"  Mountpoint: {partition.mountpoint}\n" \
                                    f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        info["Disk Information"] += f"  Total Size: {get_size(partition_usage.total)}\n" \
                                    f"  Used: {get_size(partition_usage.used)}\n" \
                                    f"  Free: {get_size(partition_usage.free)}\n" \
                                    f"  Percentage: {partition_usage.percent}%\n"
    disk_io = psutil.disk_io_counters()
    info["Disk Information"] += f"Total read: {get_size(disk_io.read_bytes)}\n" \
                                f"Total write: {get_size(disk_io.write_bytes)}\n"

    info["Network Information"] = ""
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            info["Network Information"] += f"=== Interface: {interface_name} ===\n"
            if str(address.family) == 'AddressFamily.AF_INET':
                info["Network Information"] += f"  IP Address: {address.address}\n" \
                                               f"  Netmask: {address.netmask}\n" \
                                               f"  Broadcast IP: {address.broadcast}\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info["Network Information"] += f"  MAC Address: {address.address}\n" \
                                               f"  Netmask: {address.netmask}\n" \
                                               f"  Broadcast MAC: {address.broadcast}\n"
    net_io = psutil.net_io_counters()
    info["Network Information"] += f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n" \
                                   f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n"

    return info

def display_system_information():
    # Create the main application window
    root = tk.Tk()
    root.title("System Information")

    def change_button_color(button):
        button.config(bg="green")

    # Function to update the text area with specific system information
    def update_text_area(category, button):
        for btn in buttons:
            btn.config(bg="SystemButtonFace")  # Reset other buttons' color
        change_button_color(button)  # Change the clicked button's color
        text_area.configure(state="normal")
        text_area.delete(1.0, tk.END)  # Clear previous content
        text_area.insert(tk.END, system_info[category])  # Insert new content
        text_area.configure(state="disabled")

    # Function to save all text data to a file
    def save_all_text_data():
        def save():
            with open("system_information.txt", "w") as file:
                file.write(text_area.get(1.0, tk.END))
        root.after(100, save)  # Schedule the save function to be called after 100ms

    # Create a scrolled text widget to display the system information
    text_area = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
    text_area.pack(expand=True, fill="both")

    # Create buttons for each category of information
    system_info = get_system_information()
    buttons = []
    for category in system_info.keys():
        button = tk.Button(root, text=category)
        button.config(command=lambda c=category, btn=button: update_text_area(c, button))
        button.pack(side="left", padx=5, pady=5)
        buttons.append(button)

    # Create a button to save all text data
    save_button = tk.Button(root, text="Save All", command=save_all_text_data)
    save_button.pack(side="right", padx=5, pady=5)

    # Disable editing initially
    text_area.configure(state="disabled")

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    display_system_information()
