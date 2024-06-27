import customtkinter as ctk
import paramiko
import time
import re
import threading

class StreamCasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StreamCaster Radio Control")
        self.geometry("400x400")

        self.ssh = None
        self.shell = None

        self.bandwidth_options = ["5", "10", "20"]

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill='both', expand=True)

        ctk.CTkLabel(self.login_frame, text="StreamCaster Login").pack(pady=12, padx=10)

        self.host_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Host")
        self.host_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.status_label = ctk.CTkLabel(self.login_frame, text="")
        self.status_label.pack(pady=12, padx=10)

    def create_control_frame(self):
        self.login_frame.pack_forget()
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=20, padx=20, fill='both', expand=True)

        ctk.CTkLabel(self.control_frame, text="Radio Control").pack(pady=12, padx=10)

        self.freq_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Frequency (MHz)")
        self.freq_entry.pack(pady=12, padx=10)

        self.set_freq_button = ctk.CTkButton(self.control_frame, text="Set Frequency", command=self.set_frequency)
        self.set_freq_button.pack(pady=12, padx=10)

        ctk.CTkLabel(self.control_frame, text="Bandwidth (MHz)").pack(pady=(12, 0), padx=10)
        self.bw_dropdown = ctk.CTkOptionMenu(self.control_frame, values=self.bandwidth_options)
        self.bw_dropdown.pack(pady=(0, 12), padx=10)

        self.set_bw_button = ctk.CTkButton(self.control_frame, text="Set Bandwidth", command=self.set_bandwidth)
        self.set_bw_button.pack(pady=12, padx=10)

        self.status_label = ctk.CTkLabel(self.control_frame, text="")
        self.status_label.pack(pady=12, padx=10)

    def login(self):
        global hostname
        hostname = self.host_entry.get()
        username = 'root'
        password = 'root'

        self.status_label.configure(text="Connecting...")
        self.login_button.configure(state="disabled")

        def connect():
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(hostname, username=username, password=password)
                self.shell = self.ssh.invoke_shell()
                time.sleep(2)
                self.shell.recv(1000)  # Clear initial output
                self.status_label.configure(text="Connected successfully!")
                self.after(1000, self.create_control_frame)
            except Exception as e:
                self.status_label.configure(text=f"Connection failed: {str(e)}")
                self.login_button.configure(state="normal")
                self.ssh = None
                self.shell = None

        threading.Thread(target=connect, daemon=True).start()

    def set_frequency(self):
        new_freq = self.freq_entry.get()
        self.status_label.configure(text="Setting frequency...")
        self.set_freq_button.configure(state="disabled")

        def send_command():
            try:
                api_command = f"api {hostname} freq '[\"{new_freq}\"]'\n"
                self.shell.send(api_command)
                time.sleep(2)
                output = ""
                while self.shell.recv_ready():
                    output += self.shell.recv(1000).decode()

                lines = output.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        if line == '[""]':
                            self.status_label.configure(text=f"Frequency set to {new_freq} MHz.")
                            break
                        elif re.match(r'\["\d+(\.\d+)?"\]', line):
                            current_freq = re.findall(r'\d+(\.\d+)?', line)[0]
                            self.status_label.configure(text=f"Current frequency: {current_freq} MHz")
                            break
                        elif "error" in line.lower():
                            self.status_label.configure(text=f"Error: {line}")
                            break
                else:
                    self.status_label.configure(text=f'Frequency set to {new_freq} MHz')
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")
            finally:
                self.set_freq_button.configure(state="normal")

        threading.Thread(target=send_command, daemon=True).start()

    def set_bandwidth(self):
        new_bw = self.bw_dropdown.get()
        self.status_label.configure(text="Setting bandwidth...")
        self.set_bw_button.configure(state="disabled")

        def send_command():
            try:
                api_command = f"api {hostname} bw '[\"{new_bw}\"]'\n"
                self.shell.send(api_command)
                time.sleep(2)
                output = ""
                while self.shell.recv_ready():
                    output += self.shell.recv(1000).decode()

                lines = output.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        if line == '[""]':
                            self.status_label.configure(text=f"Bandwidth set to {new_bw} MHz.")
                            break
                        elif re.match(r'\["\d+(\.\d+)?"\]', line):
                            current_bw = re.findall(r'\d+(\.\d+)?', line)[0]
                            self.status_label.configure(text=f"Current bandwidth: {current_bw} MHz")
                            break
                        elif "error" in line.lower():
                            self.status_label.configure(text=f"Error: {line}")
                            break
                else:
                    self.status_label.configure(text=f'Bandwidth set to {new_bw} MHz')
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")
            finally:
                self.set_bw_button.configure(state="normal")

        threading.Thread(target=send_command, daemon=True).start()

if __name__ == "__main__":
    app = StreamCasterApp()
    app.mainloop()