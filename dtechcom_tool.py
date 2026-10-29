import os
import sys
import threading
import subprocess
import shutil
import psutil
import customtkinter as ctk

# Cấu hình giao diện CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ==================== CORE: HỆ THỐNG & TỐI ƯU ====================
def run_cmd(cmd: str):
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

def clean_junk_files(log_func):
    log_func("Đang quét và xóa rác hệ thống (Temp, Prefetch)...")
    cmd = 'del /q /f /s "%TEMP%\*" & del /q /f /s "C:\\Windows\\Temp\*"'
    run_cmd(cmd)
    log_func("✅ Đã dọn dẹp xong bộ nhớ tạm!")

def convert_mbr_to_gpt(log_func):
    log_func("Đang kiểm tra khả năng chuyển MBR -> GPT...")
    res = subprocess.run("mbr2gpt /validate /allowFullOS", shell=True, capture_output=True, text=True)
    if "Validation completed successfully" in res.stdout:
        log_func("Tiến hành chuyển đổi đĩa sang GPT...")
        run_cmd("mbr2gpt /convert /allowFullOS")
        log_func("✅ Đã chuyển đổi sang GPT thành công!")
    else:
        log_func("❌ Đĩa không đủ điều kiện chuyển đổi trực tiếp.")

def enable_ultimate_performance(log_func):
    log_func("Đang mở khóa Ultimate Performance Power Plan...")
    run_cmd("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61")
    log_func("✅ Đã kích hoạt Ultimate Performance!")

def get_hw_usage():
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent
    }

# ==================== CORE: MÁY IN & MẠNG LAN ====================
def run_ps(cmd: str) -> str:
    result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def fix_printer_errors(log_func):
    log_func("Đang áp dụng Regkey fix lỗi máy in 0x0000011b & 0x00000709...")
    cmd = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Print" /v RpcAuthnLevelPrivacyEnabled /t REG_DWORD /d 0 /f'
    run_ps(cmd)
    run_ps("net stop spooler; net start spooler")
    log_func("✅ Fix lỗi máy in hoàn tất! Đã khởi động lại Print Spooler.")

def clear_print_spooler(log_func):
    log_func("Đang dọn dẹp hàng chờ in...")
    cmd = 'Stop-Service spooler; Remove-Item -Path "$env:SystemRoot\\System32\\spool\\PRINTERS\\*" -Force; Start-Service spooler'
    run_ps(cmd)
    log_func("✅ Đã dọn sạch hàng chờ in!")

def setup_lan_server_folders(base_path: str, pc_list: list, log_func):
    log_func(f"Đang thiết lập Máy Chủ LAN tại: {base_path}...")
    run_ps('Set-NetFirewallRule -DisplayGroup "File and Printer Sharing" -Enabled True')
    
    public_dir = os.path.join(base_path, "Public")
    os.makedirs(public_dir, exist_ok=True)
    run_ps(f'New-SmbShare -Name "Public" -Path "{public_dir}" -FullAccess "Everyone" -ErrorAction SilentlyContinue')
    log_func(" -> Đã tạo & chia sẻ thư mục Public (Everyone Access)")

    for pc in pc_list:
        p_dir = os.path.join(base_path, pc)
        os.makedirs(p_dir, exist_ok=True)
        cmd_acl = f'icacls "{p_dir}" /inheritance:r /grant:r "SYSTEM":(OI)(CI)F "Administrators":(OI)(CI)F "{pc}":(OI)(CI)M'
        run_ps(cmd_acl)
        run_ps(f'New-SmbShare -Name "{pc}_Data" -Path "{p_dir}" -ChangeAccess "{pc}" -ErrorAction SilentlyContinue')
        log_func(f" -> Đã phân quyền riêng cho {pc} tại {p_dir}")

    log_func("✅ Hoàn tất cấu hình File Server & Phân quyền LAN!")

# ==================== CORE: SAO LƯU DỮ LIỆU ====================
def backup_zalo_data(destination_dir: str, log_func):
    log_func("Đang sao lưu dữ liệu Zalo...")
    zalo_path = os.path.expandvars(r"%APPDATA%\ZaloData")
    if os.path.exists(zalo_path):
        target = os.path.join(destination_dir, "ZaloData_Backup")
        shutil.copytree(zalo_path, target, dirs_exist_ok=True)
        log_func(f"✅ Đã sao lưu ZaloData vào: {target}")
    else:
        log_func("⚠️ Không tìm thấy dữ liệu Zalo trên máy.")

def backup_wifi_passwords(destination_dir: str, log_func):
    log_func("Đang xuất danh sách mật khẩu Wi-Fi...")
    target = os.path.join(destination_dir, "WiFi_Profiles")
    os.makedirs(target, exist_ok=True)
    subprocess.run(f'netsh wlan export profile folder="{target}" key=clear', shell=True, capture_output=True)
    log_func(f"✅ Đã lưu cấu hình Wi-Fi vào: {target}")

# ==================== MAIN GUI (GIAO DIỆN CHÍNH) ====================
class DTechComApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DTechCom Tool v1.0 - All-In-One Technical Suite")
        self.geometry("1100 x 680")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="DTECHCOM TOOL", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        
        ctk.CTkButton(self.sidebar, text="🖥️ Hệ Thống & Tối Ưu", command=self.show_sys_tab).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="🖨️ Máy In & Mạng LAN", command=self.show_net_tab).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="💾 Sao Lưu & Dữ Liệu", command=self.show_bak_tab).grid(row=3, column=0, padx=20, pady=10)

        self.lbl_hw_info = ctk.CTkLabel(self.sidebar, text="CPU: --% | RAM: --%", font=ctk.CTkFont(size=12))
        self.lbl_hw_info.grid(row=7, column=0, padx=20, pady=10)

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.log_box = ctk.CTkTextbox(self.main_frame, height=180)
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.content_view = ctk.CTkScrollableFrame(self.main_frame)
        self.content_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.show_sys_tab()
        self.start_hw_monitor()

    def log(self, message: str):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def run_thread(self, func, *args):
        threading.Thread(target=func, args=args, daemon=True).start()

    def clear_content(self):
        for widget in self.content_view.winfo_children():
            widget.destroy()

    def show_sys_tab(self):
        self.clear_content()
        ctk.CTkLabel(self.content_view, text="Công Cụ Tối Ưu & Hệ Thống", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)
        ctk.CTkButton(self.content_view, text="Dọn Dẹp Rác Ổ C & Temp", command=lambda: self.run_thread(clean_junk_files, self.log)).pack(fill="x", pady=5)
        ctk.CTkButton(self.content_view, text="Chuyển Ổ Đĩa MBR Sang GPT (No Data Loss)", command=lambda: self.run_thread(convert_mbr_to_gpt, self.log)).pack(fill="x", pady=5)
        ctk.CTkButton(self.content_view, text="Bật Chế Độ Ultimate Performance", command=lambda: self.run_thread(enable_ultimate_performance, self.log)).pack(fill="x", pady=5)

    def show_net_tab(self):
        self.clear_content()
        ctk.CTkLabel(self.content_view, text="Quản Lý Máy In & Cấu Hình Máy Chủ LAN", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)
        ctk.CTkButton(self.content_view, text="Fix Lỗi In Mạng 0x0000011b & 0x00000709", command=lambda: self.run_thread(fix_printer_errors, self.log)).pack(fill="x", pady=5)
        ctk.CTkButton(self.content_view, text="Clear & Restart Spooler", command=lambda: self.run_thread(clear_print_spooler, self.log)).pack(fill="x", pady=5)
        ctk.CTkButton(self.content_view, text="Setup Trọn Gói Thư Mục Chia Sẻ (Private/Public ACLs)",
                      command=lambda: self.run_thread(setup_lan_server_folders, "D:\\OfficeData", ["PC2", "PC3", "PC4"], self.log)).pack(fill="x", pady=5)

    def show_bak_tab(self):
        self.clear_content()
        ctk.CTkLabel(self.content_view, text="Sao Lưu Dữ Liệu & Ứng Dụng", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)
        ctk.CTkButton(self.content_view, text="Backup Profile Zalo (Lịch sử Chat & File)", command=lambda: self.run_thread(backup_zalo_data, "D:\\Backups", self.log)).pack(fill="x", pady=5)
        ctk.CTkButton(self.content_view, text="Export Toàn Bộ Wi-Fi Passwords", command=lambda: self.run_thread(backup_wifi_passwords, "D:\\Backups", self.log)).pack(fill="x", pady=5)

    def start_hw_monitor(self):
        def update_stats():
            usage = get_hw_usage()
            self.lbl_hw_info.configure(text=f"CPU: {usage['cpu']}% | RAM: {usage['ram']}%")
            self.after(3000, update_stats)
        update_stats()

if __name__ == "__main__":
    app = DTechComApp()
    app.mainloop()
