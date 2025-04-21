import tkinter as tk
from tkinter import ttk
import subprocess
import random
import re


def generate_insane_mac():
    """Generate a valid but totally chaotic MAC address."""
    mac_bytes = [random.randint(0x00, 0xFF) for _ in range(6)]
    # Force locally administered and unicast
    mac_bytes[0] = (mac_bytes[0] | 0x02) & 0xFE

    formats = [
        lambda b: ':'.join(f"{x:02x}" for x in b),
        lambda b: '-'.join(f"{x:02X}" for x in b),
        lambda b: ''.join(f"{x:02x}" for x in b),
        lambda b: ':'.join(f"{x:02X}" for x in b),
        lambda b: '-'.join(f"{x:02x}" for x in b),
        lambda b: ':'.join(f"{x:02x}" if i % 2 == 0 else f"{x:02X}" for i, x in enumerate(b))
    ]

    if random.choice([True, False]):
        mac_bytes.reverse()

    return random.choice(formats)(mac_bytes)


def get_current_mac(interface):
    try:
        out = subprocess.check_output(["ifconfig", interface]).decode()
        match = re.search(r"ether (\S+)", out)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error getting current MAC: {e}")
    return None


def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def try_method(cmd_list, interface, new_mac, method_name, password):
    print(f"Trying {method_name} with MAC: {new_mac}")
    for cmd in cmd_list:
        formatted_cmd = cmd.format(password=password, iface=interface, mac=new_mac)
        full_cmd = f'echo "{password}" | sudo -S {formatted_cmd}'
        run_cmd(full_cmd)

    actual_mac = get_current_mac(interface)
    if actual_mac and actual_mac.lower().replace('-', ':') == new_mac.lower().replace('-', ':'):
        print(f"{method_name}: Worked!")
        return True
    else:
        print(f"{method_name}: Didn't work.")
        return False


class MacSpooferApp:
    def __init__(self, master):
        self.master = master
        self.master.title("💀 INSANE MAC SPOOFER 💀")
        self.master.geometry("350x230")
        self.interface = "en0"  # Change this to your actual interface

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="Admin Password:").pack(pady=(10, 0))
        self.password_entry = ttk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.change_btn = ttk.Button(self.master, text="💥 Spoof MAC Insanely 💥", command=self.spoof_mac)
        self.change_btn.pack(pady=15)

        self.status_label = ttk.Label(self.master, text="Status: Waiting")
        self.status_label.pack(pady=5)

        self.mac_display = ttk.Label(self.master, text="New MAC: -")
        self.mac_display.pack(pady=5)

    def spoof_mac(self):
        password = self.password_entry.get()
        new_mac = generate_insane_mac()

        methods = [
            {
                "name": "Method 1",
                "cmds": [
                    "ifconfig {iface} down",
                    "ifconfig {iface} ether {mac}",
                    "ifconfig {iface} up"
                ]
            },
            {
                "name": "Method 2",
                "cmds": [
                    "networksetup -setairportpower {iface} off",
                    "ifconfig {iface} ether {mac}",
                    "networksetup -setairportpower {iface} on"
                ]
            },
            {
                "name": "Method 3",
                "cmds": [
                    "ifconfig {iface} down",
                    "ifconfig {iface} hw ether {mac}",
                    "ifconfig {iface} up"
                ]
            },
            {
                "name": "Method 4",
                "cmds": [
                    "ifconfig {iface} down",
                    "ip link set dev {iface} address {mac}",
                    "ifconfig {iface} up"
                ]
            },
            {
                "name": "Method 5",
                "cmds": [
                    "ifconfig {iface} down",
                    "sudo ipconfig set {iface} DHCP",
                    "ifconfig {iface} ether {mac}",
                    "ifconfig {iface} up"
                ]
            },
            {
                "name": "Method 6",
                "cmds": [
                    "ifconfig {iface} down",
                    "networksetup -sethardwareaddress {iface} {mac}",
                    "ifconfig {iface} up"
                ]
            },
        ]

        success = False
        for method in methods:
            self.status_label.config(text=f"Trying {method['name']}...")
            self.master.update()
            success = try_method(method['cmds'], self.interface, new_mac, method['name'], password)
            if success:
                self.status_label.config(text=f"{method['name']} succeeded!")
                self.mac_display.config(text=f"New MAC: {new_mac}")
                return

        self.status_label.config(text="All methods failed.")
        self.mac_display.config(text="New MAC: -")


if __name__ == "__main__":
    root = tk.Tk()
    app = MacSpooferApp(root)
    root.mainloop()
