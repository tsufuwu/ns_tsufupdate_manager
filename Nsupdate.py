import os
import requests
import zipfile
import threading
import webbrowser
import shutil
import subprocess
import sys
import ctypes
import time
import tkinter as tk
import re
import winreg
import ftplib
from tkinter import ttk, filedialog, messagebox, scrolledtext
from urllib.parse import urlparse, unquote
from PIL import Image, ImageTk, ImageSequence

# --- App Configuration ---
try:
    myappid = 'tsufu.switch.update.manager.pro.v103'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except: 
    pass

def resource_path(relative_path):
    """ Get absolute path to resource for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APP_VERSION = "1.0.3"
GITHUB_REPO = "tsufuwu/ns_tsufupdate_manager" 

# --- UI Colors ---
COLOR_BG = "#1e1e1e"
COLOR_CARD = "#2d2d30"
COLOR_HEADER_BG = "#3e3e42"
COLOR_FG = "#ffffff"
COLOR_ACCENT = "#007acc"
COLOR_ACCENT_HOVER = "#0098ff"
COLOR_GOLD = "#ffd700"
COLOR_SUCCESS = "#4caf50"
COLOR_WARNING = "#ff9800"
COLOR_INFO = "#17a2b8" 
COLOR_SPEED_BG = "#FF6600"    
COLOR_SPEED_HOVER = "#FF8533" 
COLOR_SPEED_PRESS = "#CC5200"
COLOR_DANGER = "#dc3545" 
COLOR_DANGER_HOVER = "#bd2130"
COLOR_PURPLE = "#9b59b6" 
COLOR_PURPLE_HOVER = "#8e44ad"

FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_TITLE = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

# --- UI Dictionary ---
UI_TEXT = {
    "VI": {
        "title": "SWITCH TSUFUPDATE MANAGER",
        "credit": "Dev by Tsufu/Phú Trần Trung Lê",
        "credit2": "Chân thành cảm ơn Group Cộng Đồng Nintendo Switch hắc ám (Admin Phong Pham)\nvì các dữ liệu cung cấp cho phần mềm này",
        "path_label": "Chọn thư mục điểm đến (Không hỗ trợ DBI (MTP)):",
        "path_tip": "Nên là thẻ nhớ (Root) nếu bạn muốn xài tính năng cập nhật tự động.\nHoặc chọn thư mục bất kì để tải file vào đó rồi chép vào thẻ nhớ sau.\n Đọc HDSD để biết cách kết nối với thẻ nhớ root",
        "btn_browse": "📁 Chọn",
        "btn_detect": "🔄 Auto",
        "btn_open": "📂 Mở thư mục",
        "btn_dl_all": "⬇️ Tải tất cả mục này",
        "btn_donate": "☕ Donate ủng hộ Dev",
        "btn_update_soft": "🔄 Cập nhật phần mềm",
        "btn_guide": "📖 Hướng dẫn sử dụng",
        "btn_ftp": "📡 FTP Transfer (Wifi)", 
        "lbl_ftp_hint": "Kết nối không dây với Switch qua Wifi:",
        "status_ready": "Sẵn sàng",
        "status_detect_ok": "Đã phát hiện thẻ nhớ/USB tại: ",
        "status_detect_fail": "Không tìm thấy ổ đĩa rời phù hợp (Switch/SD/USB).",
        "msg_confirm_dl_all": "Bạn có muốn tự động tải tất cả ứng dụng trong mục:\n'{category}' không?\n\n(Lưu ý: Sẽ bỏ qua các file dành cho PC và cần hai bước như Sigpatch, Linkalho)",
        "msg_mtp_warning": "⚠️ LƯU Ý MTP RESPONDER (DBI):\nViệc dùng MTP Responder qua DBI chỉ có tác dụng khi tải sysmod, homebrew, cheat, save...\n\nKHÔNG NÊN áp dụng cho File Hack (Atmosphere, Hekate...) vì sẽ dễ gây ra lỗi file hệ thống.\nChi tiết vui lòng đọc Hướng Dẫn Sử Dụng.",
        "cat_file": "🔥 FILE HACK & CÔNG CỤ PC",
        "cat_sysmod": "🛠️ SYSMOD HỮU ÍCH (Cần Restart)",
        "cat_homebrew": "🎮 HOMEBREW (Ứng dụng)",
        "cat_misc": "⚙️ LINH TINH (Firmware/Cheat/Save)",
        "cat_fix": "🚑 FIX LỖI NHANH (Sự cố thường gặp)",
        "cat_guide": "📚 CÁC HƯỚNG DẪN ",
        "cat_game_source": "👾 NGUỒN DOWNLOAD GAME",
        "msg_fw_done": "Đã tải và giải nén Firmware thành công vào thẻ nhớ!\n\nLƯU Ý QUAN TRỌNG:\nĐây chỉ là bước chép file. Để cập nhật máy, bạn cần mở app 'Daybreak' trên Switch để tiến hành cài đặt Firmware vừa tải.\n\nNhớ cập nhật gói My Pack hoặc Atmosphere mới nhất trước khi chạy Daybreak để tránh lỗi.",
        "ams_195_title": "Cảnh báo tương thích Atmosphere 1.9.5",
        "ams_195_msg": """⚠️ CẢNH BÁO QUAN TRỌNG VỀ FIRMWARE & HẠ CẤP

Phiên bản này tương thích tốt nhất với Tinfoil/App cũ, NHƯNG chỉ hỗ trợ Firmware < 21.0.0.
Nếu chỉ có Custom Firmware (CFW) của bạn cập nhật lên 21.0.0 thì có thể xem xét hạ cấp firmware, còn nếu bạn đã nâng cấp cả OFW lên 21.0.0 đổ lên thì buộc dùng AMS mới nhất trong gói my pack.

🔴 LƯU Ý NẾU BẠN MUỐN HẠ CẤP (DOWNGRADE) CFW:
1. Nếu chỉ có EmuNAND (CFW) lỡ lên cao: Có thể dùng Daybreak để hạ cấp.
2. CẢNH BÁO FW 21.x: Nếu đang ở FW 21, KHUYẾN NGHỊ NẾU BẠN KHÔNG CHẮC CHẮN THÌ KHÔNG NÊN HẠ, HOẶC ĐẢM BẢO ĐÃ BACK UP THẺ NHỚ. Đã có nhiều trường hợp hạ từ 21 về 20 hoặc 20 về 19 bị Semi-Brick (lỗi 2002-3005).
3. CÁCH CỨU NẾU BỊ BRICK KHI HẠ CẤP:
   - Khởi động vào chế độ Maintenance của EmuNAND.
   - Chọn dòng 2: "Initialize Console" để khôi phục lại hệ điều hành (HOS).
   (Nên Backup dữ liệu trước khi thực hiện).

👉 Bấm nút "Hướng dẫn Maintenance Mode" bên dưới để xem chi tiết.""", 
        "btn_maintenance_guide": "📖 Hướng dẫn Maintenance Mode",
        "chk_mtp_label": "Chọn vào đây nếu bạn dùng DBI (MTP)",
        "msg_mtp_alert": "Lưu ý: Chế độ này dùng cho kết nối MTP (DBI).\n\nSau khi bấm OK, hãy chọn một thư mục tạm trên máy tính để tải file về.\nSau khi tải xong, bạn hãy copy thủ công các file đó vào ổ Switch MTP.",
        "btn_hard_reset": "☢️ CHẠY RESET",
        "tip_hard_reset": "Chọn option này khi bạn đã thử nhiều cách fix mềm bên dưới vẫn không thể khắc phục. Phần mềm sẽ XÓA SẠCH thẻ nhớ (chỉ giữ lại thư mục emuMMC và các thư mục backup an toàn) và tự động tải lại gói My Pack.",
        "msg_update_virus": "Nếu cập nhật thất bại, hãy thử tắt phần mềm diệt Virus và thử lại.",
        "msg_update_manual": "Nếu phần mềm không tự khởi động lại, vui lòng mở lại file thủ công.",
        "btn_cancel": "❌ Hủy Tải (Cancel)",
        "msg_dl_success": "Đã tải và cài đặt thành công: ",
        "msg_cancelled": "Đã hủy tác vụ tải xuống và xóa file tạm.",
        "trans_title": "Chọn nguồn cài đặt Việt Hóa",
        "trans_msg_1": "Bạn muốn cài đặt từ File Nén hay Thư Mục có sẵn?",
        "trans_msg_2": "(Hệ thống thông minh sẽ tự động quét ID Game bên trong file nén/thư mục để chép vào đúng vị trí atmosphere/contents, bạn không cần phải giải nén thủ công)",
        "trans_btn_zip": "📄 File Nén (Zip/Rar/7z...)",
        "trans_btn_folder": "📂 Thư Mục (Folder)",
        "fix_theme_ok": "Đã xóa giao diện (Theme) thành công!\nNếu máy bạn bị treo logo hoặc màn hình đen, hãy khởi động lại (Reboot) máy ngay bây giờ để kiểm tra.",
        "fix_theme_fail": "Không tìm thấy thư mục Theme nào để xóa. Có thể bạn chưa cài theme hoặc đã xóa rồi.",
        "fix_mod_ok": "Đã gỡ bỏ {count} Sysmodules phổ biến (Tesla, Emuiibo...).\nMáy sẽ chạy nhẹ hơn và khắc phục được lỗi xung đột (Crash).",
        "fix_cheat_ok": "Đã xóa sạch file Cheat của {count} game.\nViệc này giúp khắc phục lỗi vào game bị văng (Crash) do cheat cũ không tương thích.",
        "fix_junk_ok": "Đã dọn sạch {count} file rác MacOS (._file).\nHekate sẽ không còn báo lỗi 'Archive Bit' khó chịu nữa.",
        "fix_wipe_warn": "CẢNH BÁO NGUY HIỂM!\n\nHành động này sẽ XÓA SẠCH thư mục 'atmosphere/contents'.\n- Mất toàn bộ Việt Hóa.\n- Mất toàn bộ Mod game.\n- Mất toàn bộ Cheat và Sysmodule.\n\nBạn có chắc chắn muốn làm điều này để sửa lỗi máy hay bị Crash không?",
        "fix_wipe_ok": "Đã xóa sạch thư mục Contents. Máy bạn đã trở về trạng thái sạch (như chưa cài mod).",
        "hard_reset_warn": "⚠️ CẢNH BÁO NGUY HIỂM (DANGER ZONE) ⚠️\n\nHành động này sẽ:\n1. XÓA SẠCH toàn bộ dữ liệu trên thẻ nhớ (Game, App, Config...).\n2. CHỈ GIỮ LẠI thư mục 'emuMMC' (Hệ điều hành ảo) và các thư mục Nintendo.\n3. Tự động tải và cài lại gói My Pack chuẩn.\n\nBạn chỉ nên dùng khi máy bị lỗi quá nặng không sửa được để cứu dữ liệu game\nBạn có CHẮC CHẮN muốn tiếp tục không?",
        "ftp_title": "Kết nối DBI FTP (Không dây)",
        "ftp_lbl_ip": "Nhập địa chỉ IP Switch (Xem trên màn hình DBI):",
        "ftp_lbl_port": "Cổng (Port - Mặc định 5000):",
        "ftp_btn_explorer": "📂 Mở thẻ nhớ (Explorer)",
        "ftp_btn_install": "🎮 Cài Game(.nsp,.xci)",
        "ftp_btn_folder": "📂 Upload Folder",
        "ftp_tip": "Hướng dẫn: Trên Switch, mở app DBI -> Chọn 'Run/Start FTP Server'.\n Chọn Browse SD Card để truy cập thẻ, chọn Install Game để cài game\n Chọn Saves để trích xuất Save game.\n Nhập dòng IP hiển thị trên màn hình Switch vào ô bên dưới (Ví dụ: 192.168.1.5)\nĐể dùng chức năng cài game nhanh, đảm bảo bạn đã chọn vào Install game trên DBI",
        "ftp_status_idle": "Trạng thái: Đang chờ lệnh...",
        "ftp_status_connecting": "Đang kết nối tới FTP...",
        "ftp_status_uploading": "Đang tải lên: {filename} ({percent}%)",
        "ftp_status_done": "✅ Đã cài xong: {filename}",
        "ftp_error": "❌ Lỗi: {error}"
    },
    "EN": {
        "title": "SWITCH TSUFUPDATE MANAGER",
        "credit": "Dev by Tsufu/Phu Tran Trung Le",
        "credit2": "Special thanks to Nintendo Switch Hacking Community Group (Admin Phong Pham)\nfor providing data for this software",
        "path_label": "Select destination folder (DBI MTP not supported):",
        "path_tip": "Should be SD Card (Root) for auto-update features.\nOr select any folder to download files there and copy manually later.",
        "btn_browse": "📁 Browse",
        "btn_detect": "🔄 Auto Detect",
        "btn_open": "📂 Open Folder",
        "btn_dl_all": "⬇️ Download All",
        "btn_donate": "☕ Donate",
        "btn_update_soft": "🔄 Update App",
        "btn_guide": "📖 User Manual",
        "btn_ftp": "📡 FTP Transfer (Wifi)",
        "lbl_ftp_hint": "Wireless connection via Wifi:",
        "status_ready": "Ready",
        "status_detect_ok": "Detected SD Card/USB at: ",
        "status_detect_fail": "Removable drive not found.",
        "msg_confirm_dl_all": "Do you want to automatically download all apps in:\n'{category}'?\n\n(Note: PC files will be skipped)",
        "msg_mtp_warning": "⚠️ MTP RESPONDER WARNING (DBI):\nUsing MTP Responder via DBI is okay for sysmods, homebrew, cheats, saves...\n\nDO NOT use it for Hack Files (Atmosphere, Hekate...) as it may cause system file errors.\nPlease read the User Manual for details.",
        "cat_file": "🔥 HACK FILES & PC TOOLS",
        "cat_sysmod": "🛠️ USEFUL SYSMODS (Restart Required)",
        "cat_homebrew": "🎮 HOMEBREW (Apps)",
        "cat_misc": "⚙️ MISC (Firmware/Cheat/Save)",
        "cat_fix": "🚑 QUICK FIX (Common Issues)",
        "cat_guide": "📚 GUIDES",
        "cat_game_source": "👾 GAME DOWNLOAD SOURCES",
        "msg_fw_done": "Firmware files copied successfully to SD card!\n\nIMPORTANT:\nThis is just a file copy. To update your system, you must open 'Daybreak' on your Switch to install this Firmware.\n\nRemember to update My Pack or Atmosphere first to avoid errors.",
        "ams_195_title": "Atmosphere 1.9.5 Compatibility Warning",
        "ams_195_msg": """⚠️ IMPORTANT FIRMWARE & DOWNGRADE WARNING

This version is best for Tinfoil/Legacy apps but ONLY supports Firmware < 21.0.0.

🔴 DOWNGRADE NOTES:
1. If only EmuNAND is updated: You can try downgrading via Daybreak.
2. FW 21.x WARNING: Downgrading from 21 to 20 often causes a Semi-Brick (Error 2002-3005). BACKUP YOUR SD CARD FIRST.
3. HOW TO FIX SEMI-BRICK:
   - Boot into EmuNAND's "Maintenance Mode".
   - Select Option 2: "Initialize Console" to restore HOS.
   (Please Backup data before proceeding).

👉 Click "Maintenance Mode Guide" below for instructions.""",
        "btn_maintenance_guide": "📖 Maintenance Mode Guide",
        "chk_mtp_label": "Check here if using DBI (MTP)",
        "msg_mtp_alert": "Note: DBI (MTP) Mode selected.\n\nAfter clicking OK, please select a temporary folder on your PC.\nThe system will download files there. You must manually copy them to the Switch MTP drive afterwards.",
        "btn_hard_reset": "☢️ HARD RESET",
        "tip_hard_reset": "Use this when other fixes fail. This will WIPE the SD Card (keeping only emuMMC) and reinstall My Pack automatically. Backup needed.",
        "msg_update_virus": "If update fails, please try disabling Anti-Virus and try again.",
        "msg_update_manual": "If the app does not restart automatically, please open the file manually.",
        "btn_cancel": "❌ Cancel Download",
        "msg_dl_success": "Download & Install Success: ",
        "msg_cancelled": "Download task cancelled. Temp files deleted.",
        "trans_title": "Install Translation Pack",
        "trans_msg_1": "Select Archive File or Folder?",
        "trans_msg_2": "(The system will automatically detect the Game ID folder inside and copy it to the correct path. No manual extraction needed)",
        "trans_btn_zip": "📄 Archive (Zip/Rar/7z...)",
        "trans_btn_folder": "📂 Folder",
        "fix_theme_ok": "Theme deleted successfully!\nIf your Switch had a black screen or boot loop, please Reboot now to verify.",
        "fix_theme_fail": "No theme folder found to delete.",
        "fix_mod_ok": "Removed {count} common sysmodules (Tesla, Emuiibo...).\nYour system should be lighter and crash less.",
        "fix_cheat_ok": "Deleted cheats for {count} games.\nThis helps fix crashes caused by incompatible cheat codes.",
        "fix_junk_ok": "Cleaned {count} MacOS junk files (._file).\nFixed 'Archive Bit' errors.",
        "fix_wipe_warn": "DANGER!\n\nThis will DELETE EVERYTHING in 'atmosphere/contents'.\n- Lose all Translations.\n- Lose all Game Mods.\n- Lose all Cheats & Sysmodules.\n\nAre you sure you want to proceed to fix crashes?",
        "fix_wipe_ok": "Wiped Contents folder. Your system is now clean (like no mods installed).",
        "hard_reset_warn": "⚠️ DANGER ZONE ⚠️\n\nThis action will:\n1. WIPE ALL DATA on SD Card (Games, Apps, Configs...).\n2. KEEP ONLY 'emuMMC' folder and Nintendo folders.\n3. Automatically download and reinstall My Pack.\n\nOnly use this for critical errors.\nAre you SURE?",
        "ftp_title": "DBI FTP Connection (Wireless)",
        "ftp_lbl_ip": "Enter Switch IP (Check on DBI screen):",
        "ftp_lbl_port": "Port (Default 5000):",
        "ftp_btn_explorer": "📂 Open SD Card (Explorer)",
        "ftp_btn_install": "🎮 Quick Install Game (.nsp/.xci)",
        "ftp_btn_folder": "📂 Upload Folder (Safe)",
        "ftp_tip": "Guide: On Switch, open DBI app -> Select 'Run FTP Server'.\nEnter the IP address shown on Switch screen below (e.g., 192.168.1.5)",
        "ftp_status_idle": "Status: Idle...",
        "ftp_status_connecting": "Connecting to FTP...",
        "ftp_status_uploading": "Uploading: {filename} ({percent}%)",
        "ftp_status_done": "✅ Install Finished: {filename}",
        "ftp_error": "❌ Error: {error}"
    }
}

# --- Data Dictionaries (Content) ---
DATA_VI = {
    "🔥 FILE HACK & CÔNG CỤ PC": [
        {"name": "Gói hack tổng hợp My Pack", "desc": "Bộ công cụ hack Switch được tùy chỉnh riêng (AIO). Bao gồm Atmosphere, Hekate và các sysmod cần thiết nhất để chạy ngay lập tức. Xem phiên bản ở dòng chữ xanh lá bên trên ", 
        "urls": {"Bước 1. Tải về file": "ACTION_MY_PACK_WARN", "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"}}, 
        {"name": "Sigpatches (Hỗ trợ game thuốc)", "desc": "Signature Patches: Thành phần quan trọng nhất để chơi game lậu. Giúp bỏ qua bước kiểm tra chữ ký số của Nintendo, cho phép cài và chạy file NSP/XCI không bản quyền.", "urls": {"Bước 1. Tải về file": "https://gbatemp.net/attachments/hekate-ams-package3-sigpatches-1-10-1p-cfw-21-1-0_v0-zip.544098/", "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"}},
        {"name": "Hekate (Bootloader)", "desc": "Trình khởi động đa năng. Dùng để Backup/Restore NAND (tránh brick máy), tạo Emunand (hệ điều hành ảo), phân vùng thẻ nhớ và khởi động vào CFW.", "urls": {"Tự động cài đặt": "https://github.com/CTCaer/hekate/releases/download/v6.4.2/hekate_ctcaer_6.4.2_Nyx_1.8.2.zip"}},
        {"name": "Atmosphere (CFW)", "desc": "Hệ điều hành tùy chỉnh (Custom Firmware) phổ biến nhất cho Switch. Đây là nền tảng cốt lõi để chạy các ứng dụng Homebrew, Mod, và game lậu.", "urls": {"Tự động cài đặt (Mới nhất)": "https://github.com/Atmosphere-NX/Atmosphere/releases/download/1.10.1/atmosphere-1.10.1-master-21c0f75a2+hbl-2.4.5+hbmenu-3.6.1.zip", "Atmosphere 1.9.5 (đọc lưu ý))": "ACTION_AMS_195" }},
        {"name": "TegraRcmGUI (Cài trên PC)", "desc": "Phần mềm chạy trên máy tính Windows. Dùng để 'kích hack' (gửi Payload) vào Switch khi máy đang ở chế độ RCM (màn hình đen).", "urls": {"Tự động cài đặt (PC)": "ACTION_RUN_PC|https://github.com/eliboa/TegraRcmGUI/releases/download/2.6/TegraRcmGUI_v2.6_Installer.msi"}},
    ],
    "🛠️ SYSMOD HỮU ÍCH (Cần Restart)": [
        {"name": "Sys-patch", "desc": "Module tự động vá lỗi hệ thống khi khởi động (fs, ldr, es). Giúp game chạy ổn định hơn, sửa lỗi khi Sigpatches chưa cập nhật kịp.", "urls": {"Bước 1. Tải về file": "https://gbatemp.net/download/sys-patch-sysmodule.39471/download", "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"}},
        {"name": "Tesla Menu (Overlay Menu)", "desc": "Menu phủ màn hình (Overlay). Cho phép bật/tắt cheat, xem thông tin máy, ép xung... ngay khi đang chơi game bằng tổ hợp phím (L + Dpad Down + R3).", "urls": {"Tự động cài đặt (Combo)": "TESLA_ACTION"}},
        {"name": "Ultrahand (Overlay mạnh mẽ)", "desc": "Một trình quản lý Overlay khác tương tự Tesla nhưng giao diện hiện đại hơn. Dùng để quản lý các plugin overlay như nghe nhạc, cheat, fps...kích hoạt bằng (ZL+ZR+DDOWN).", "urls": {"Tự động cài đặt (Combo)": "ULTRAHAND_ACTION"}},
        {"name": "Edizon Overlay (Cheat game)", "desc": "Plugin hiển thị menu Cheat đè lên màn hình game. Giúp bạn tìm kiếm giá trị, bật/tắt mã bất tử, vô hạn tiền ngay lập tức mà không cần thoát game.", "urls": {"Tự động cài đặt": "https://github.com/proferabg/EdiZon-Overlay/releases/download/v1.0.14/ovlEdiZon.ovl", "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat#cach-3-dung-edizon-overlay"}},
        {"name": "Status Monitor (FPS/Pin/Nhiệt độ)", "desc": "Công cụ giám sát phần cứng thời gian thực (Real-time). Hiển thị FPS, nhiệt độ CPU/GPU, tốc độ RAM, % Pin... ngay góc màn hình.", "urls": {"Tự động cài đặt": "https://github.com/masagrator/Status-Monitor-Overlay/releases/download/1.3.2/Status-Monitor-Overlay.zip"}},
        {"name": "emuiibo (Giả lập Amiibo)", "desc": "Giả lập tượng Amiibo ảo. Cho phép nhận quà trong game (như Zelda, Splatoon) mà không cần mua tượng thật. Sử dụng cùng với Tesla Menu.", "urls": {"Tự động cài đặt": "https://github.com/XorTroll/emuiibo/releases/download/1.1.2/emuiibo.zip"}},
        {"name": "SYS-CLK (Ép xung)", "desc": "Công cụ ép xung (Overclock) hoặc hạ xung an toàn. Giúp game nặng chạy mượt hơn (tăng FPS) hoặc tiết kiệm pin cho game nhẹ.", "urls": {"Tự động cài đặt": "https://github.com/retronx-team/sys-clk/releases/download/2.0.1/sys-clk-2.0.1-21fix.zip"}},
        {"name": "SysDVR (Stream hình ảnh qua USB)", "desc": "Truyền hình ảnh và âm thanh từ Switch sang máy tính qua cáp USB hoặc Wifi. Dùng để quay video/stream game mà không cần Capture Card đắt tiền.", "urls": {"1. Tải cho Switch": "https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR.zip", "2. Client cho PC (7z)": "ACTION_SAVE_PC|https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR-Client-Windows-x64-with-framework.7z"}},
        {"name": "Mission Control", "desc": "Cho phép kết nối các tay cầm Bluetooth của hệ máy khác (PS4, PS5, Xbox One, Wii U Pro...) với Nintendo Switch mà không cần USB Receiver.", "urls": {"Tự động cài đặt": "https://github.com/ndeadly/MissionControl/releases/download/v0.14.1/MissionControl-0.14.1-master-141b3aca.zip"}},
        {"name": "Sys-con (USB Controllers)", "desc": "Cho phép kết nối tay cầm có dây (hoặc qua USB receiver) của bên thứ 3 (Xbox 360, DualShock 3...) với Switch Dock.", "urls": {"Tự động cài đặt": "https://github.com/o0Zz/sys-con/releases/download/1.6.1/sys-con-1.6.1.zip"}},
    ],
    "🎮 HOMEBREW (Ứng dụng)": [
        {"name": "HB App Store", "desc": "Chợ ứng dụng Homebrew trực tuyến. Nơi tìm kiếm, tải xuống và cập nhật hàng trăm ứng dụng tiện ích, game homebrew trực tiếp trên Switch.", "urls": {"Tự động cài đặt": "https://github.com/fortheusers/hb-appstore/releases/download/v2.3.2/appstore.nro"}},
        {"name": "AIO Switch Updater", "desc": "Công cụ cập nhật tất cả trong một ngay trên Switch. Tự động tải và cập nhật Atmosphere, Firmware, Cheat... trực tiếp qua Wifi mà không cần PC.", "urls": {"Tự động cài đặt": "https://github.com/HamletDuFromage/aio-switch-updater/releases/download/2.23.3/aio-switch-updater.zip"}},
        {"name": "Edizon (Cheat)", "desc": "Ứng dụng quản lý Save game và Cheat code mạnh mẽ. Dùng để sao lưu save game ra thẻ nhớ hoặc kích hoạt các mã gian lận.", "urls": {"Tự động cài đặt": "https://github.com/WerWolv/EdiZon/releases/download/v3.1.0/EdiZon.nro"}},
        {"name": "Breeze (Cheat)", "desc": "Công cụ Cheat nâng cao (kế thừa Edizon). Hỗ trợ tìm kiếm giá trị bộ nhớ phức tạp hơn để tự tạo mã cheat.", "urls": {"Tự động cài đặt": "https://github.com/tomvita/Breeze-Beta/releases/download/beta99r/Breeze.zip"}},
        {"name": "Retroarch (Giả lập)", "desc": "Trình giả lập đa hệ máy 'All-in-one'. Chơi được game của NES, SNES, GBA, PS1, N64, Arcade... ngay trên Switch.", "urls": {"Truy cập Web": "https://buildbot.libretro.com/nightly/nintendo/switch/libnx/"}},
        {"name": "pEmu (Giả lập)", "desc": "Bộ sưu tập các trình giả lập (pFBA, pSNES...) được tối ưu hóa riêng cho Switch bởi Cpasjuste. Giao diện đẹp và hiệu năng tốt.", "urls": {"Truy cập Web": "https://github.com/Cpasjuste/pemu/releases/latest"}},
        {"name": "DBI (Quản lý file + Cài game)", "desc": "Công cụ 'Thần thánh' cho Switch. Hỗ trợ cài game qua cáp USB (MTP) cực nhanh, xóa file rác, quản lý file trên thẻ nhớ giao diện trực quan.", "urls": {"Tự động cài đặt": "https://github.com/rashevskyv/dbi/releases/download/854ru/DBI.nro"}},
        {"name": "Tinfoil (Shop game)", "desc": "Cửa hàng tải game miễn phí (FreeShop) nổi tiếng (cần add host). Cũng là trình quản lý file và cài đặt game giao diện đẹp mắt. Tuy nhiên không tương thích với atmosphere mới nhất nữa.", "urls": {"Truy cập Web": "https://tinfoil.io/Download#download"}},
        {"name": "Goldleaf", "desc": "Trình quản lý file và cài đặt file NSP/NSZ/XCI cơ bản, mã nguồn mở. Hỗ trợ duyệt file trên thẻ nhớ và cài game qua USB (với Quark).", "urls": {"Tự động cài đặt": "https://github.com/XorTroll/Goldleaf/releases/download/1.2.0/Goldleaf.nro"}},
        {"name": "Linkalho (Link Offline)", "desc": "Công cụ liên kết tài khoản Nintendo giả lập (Offline). Bắt buộc dùng nếu bạn chơi game yêu cầu có tài khoản Nintendo nhưng máy bị ban hoặc không muốn online.", "urls": {"Bước 1. Tải về file": "https://dlhb.gamebrew.org/switchhomebrews/linkalhonx.7z", "Bước 2. Chọn file nén để tự động chép.": "ACTION_LINKALHO_NESTED"}},
        {"name": "Combo: Theme Installer + Themezer", "desc": "Cài đặt cùng lúc 2 ứng dụng: NXThemes Installer (Quản lý/Cài theme) và Themezer-NX (Tải theme online).", "urls": {"Theme installer + Themezer": "THEME_COMBO_ACTION", "🌐 Mở trang download": "https://github.com/exelix11/SwitchThemeInjector/releases"}},
        {"name": "Battery Desync Fix (Sửa Pin ảo)", "desc": "Công cụ hiệu chỉnh lại hiển thị phần trăm pin khi bị báo sai (Pin ảo).", "urls": {"Tự động cài đặt": "https://github.com/CTCaer/battery_desync_fix_nx/releases/download/1.5.1/battery_desync_fix_v1.5.1.nro", "📖 Hướng dẫn sử dụng": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap/hieu-chuan-pin-ao"}},
    ],
    "⚙️ LINH TINH (Firmware/Cheat/Save)": [
        {"name": "Firmware (Nâng/Hạ cấp)", "desc": "Các file hệ điều hành gốc của Nintendo Switch. Cần thiết khi bạn muốn cập nhật máy lên phiên bản mới nhất bằng Daybreak.", "urls": {"Link tải tổng hợp 1": "https://darthsternie.net/switch-firmwares/", "Link tải tổng hợp 2": "https://github.com/THZoria/NX_Firmware/releases", "Hướng dẫn Update": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/cap-nhat-firmware-cho-emunand"}},
        {"name": "Cheat game (Tổng hợp)", "desc": "Kho mã Cheat do cộng đồng tổng hợp. Tải về để cập nhật các mã cheat mới nhất cho Edizon/Breeze.", "urls": {"GBAtemp": "https://gbatemp.net/threads/cheat-codes-ams-and-sx-os-add-and-request.520293/", "CheatSlips": "https://www.cheatslips.com/", "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat"}},
        {"name": "Save Game (Nguồn tải)", "desc": "Các kho lưu trữ Save game (File lưu tiến độ game) được chia sẻ bởi cộng đồng. Hữu ích khi bạn muốn chơi New Game+ hoặc mất save.", "urls": {"GBAtemp Save": "https://gbatemp.net/download/categories/game-saves.1668/", "TheTechGame": "https://www.thetechgame.com/Downloads/cid=135/nintendo-switch-game-saves.html", "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/sao-luu-va-phuc-hoi-save-game"}},
        {"name": "Việt hóa game", "desc": "Tổng hợp các bản Patch tiếng Việt cho game Switch. Cần tải về và cài đặt đúng thư mục (thường là atmosphere/contents).", "urls": {"Link tham khảo": "https://docs.google.com/spreadsheets/d/1k_8w_Eb7M6_3q1-FrtY0gYdrCokr3IGxuk-oj_u-zbw/preview"}},
    ],
    "🚑 FIX LỖI NHANH (Sự cố thường gặp)": [
        {"name": "HARD RESET (XÓA SẠCH LÀM LẠI)", "desc": "Sử dụng khi các cách fix mềm không hiệu quả. Xóa sạch thẻ nhớ (chỉ giữ emuMMC, chứa game + save game) và cài lại My Pack.", "urls": {"☢️ CHẠY RESET": "ACTION_FIX_HARD_RESET"}},
        {"name": "Cài lại gói hack My Pack (Khuyến nghị)", "desc": "Cách sửa lỗi triệt để nhất khi máy bị lỗi nặng. Hệ thống sẽ đưa bạn đến mục tải gói hack chuẩn để cài lại từ đầu.", "urls": {"🛠️ Chạy Fix": "ACTION_FIX_REINSTALL_PACK"}},
        {"name": "Gỡ bỏ Themes (Fix màn hình đen/Bootloop)", "desc": "Xóa thư mục theme (0100000000001000). Dùng khi bạn cài theme lỗi khiến máy không khởi động được hoặc bị màn hình đen sau logo Atmosphere.", "urls": {"🛠️ Chạy Fix": "ACTION_FIX_THEMES"}},
        {"name": "Gỡ bỏ các Sysmodules phổ biến", "desc": "Chỉ xóa các module chạy ngầm phổ biến (Tesla, Emuiibo, SysDVR...). Giữ lại Việt hóa và Mod game. Dùng khi máy hay bị Crash nhẹ.", "urls": {"🛠️ Chạy Fix": "ACTION_FIX_MODULES"}},
        {"name": "Xóa SẠCH thư mục Contents (Triệt để)", "desc": "CẢNH BÁO: Xóa toàn bộ folder atmosphere/contents. Sẽ mất hết Sysmod, Mod game, Việt hóa và Cheat. Dùng khi máy lỗi nặng, crash liên tục.", "urls": {"🔥 Chạy Fix": "ACTION_FIX_DELETE_ALL_CONTENTS"}},
        {"name": "Xóa file rác MacOS (Fix Archive Bit)", "desc": "Quét và xóa các file rác do MacOS tạo ra (._file, .DS_Store). Những file này thường làm Hekate không đọc được cấu hình.", "urls": {"🛠️ Chạy Fix": "ACTION_FIX_MAC_JUNK"}},
        {"name": "Xóa toàn bộ Cheats (Fix Game Crash)", "desc": "Xóa tất cả file cheat trong thư mục contents. Dùng khi vào game bị crash ngay lập tức do mã cheat cũ xung đột.", "urls": {"🛠️ Chạy Fix": "ACTION_FIX_CHEATS"}},
        {"name": "Các lỗi khác (nguồn: Cộng Đồng Nintendo Switch hắc ám)", "desc": "Tra cứu danh sách các lỗi thường gặp khác và cách khắc phục chi tiết trên Wiki của cộng đồng.", "urls": {"🌍 Xem hướng dẫn Web": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap"}}
    ],
    "📚 CÁC HƯỚNG DẪN (nguồn: Cộng Đồng Nintendo Switch hắc ám)": [
        {"name": "Hướng dẫn căn bản ", "desc": "Các kiến thức nhập môn cần thiết: Phân biệt đời máy, thuật ngữ hack, hướng dẫn sử dụng cơ bản cho người mới bắt đầu.", "urls": {"🌍 Truy cập Web": "https://nsw.gitbook.io/guide/huong-dan-can-ban/"}},
        {"name": "Hướng dẫn nâng cao ", "desc": "Tổng hợp các bài viết chuyên sâu: Tạo EmuMMC, Ẩn số seri (Incognito), Phân vùng thẻ nhớ, Sao lưu Nand...", "urls": {"🌍 Truy cập Web": "https://nsw.gitbook.io/guide/huong-dan-nang-cao"}}
    ],
    "👾 NGUỒN DOWNLOAD GAME": [
        {"name": "Website tải game Switch", "desc": "Kho game Switch phong phú, cập nhật thường xuyên.", "urls": {"Link tham khảo": "https://rebrand.ly/tsufurom"}}
    ]
}

DATA_EN = {
    "🔥 HACK FILES & PC TOOLS": [
        {"name": "My Pack AIO Custom", "desc": "Customized Switch Hack Toolkit (AIO). Includes Atmosphere, Hekate, and essential sysmods for immediate use. Check version in green text above.", 
        "urls": {"Step 1. Download file": "ACTION_MY_PACK_WARN", "Step 2. Select ZIP to auto-copy": "ACTION_PICK_ZIP"}}, 
        {"name": "Sigpatches (For pirated games)", "desc": "Signature Patches: Most important for pirated games. Bypasses Nintendo signature checks, allowing unsigned NSP/XCI installation.", "urls": {"Step 1. Download file": "https://gbatemp.net/attachments/hekate-ams-package3-sigpatches-1-10-1p-cfw-21-1-0_v0-zip.544098/", "Step 2. Select ZIP to auto-copy": "ACTION_PICK_ZIP"}},
        {"name": "Hekate (Bootloader)", "desc": "Multi-purpose bootloader. Used for Backup/Restore NAND, creating EmuNAND, partitioning SD card, and booting into CFW.", "urls": {"Auto Install": "https://github.com/CTCaer/hekate/releases/download/v6.4.2/hekate_ctcaer_6.4.2_Nyx_1.8.2.zip"}},
        {"name": "Atmosphere (CFW)", "desc": "Most popular Custom Firmware for Switch. Core platform for Homebrew, Mods, and pirated games.", "urls": {"Auto Install (Latest)": "https://github.com/Atmosphere-NX/Atmosphere/releases/download/1.10.1/atmosphere-1.10.1-master-21c0f75a2+hbl-2.4.5+hbmenu-3.6.1.zip", "Atmosphere 1.9.5 (Read Note)": "ACTION_AMS_195" }},
        {"name": "TegraRcmGUI (PC Installer)", "desc": "Windows PC software. Used to inject Payload into Switch when in RCM mode (black screen).", "urls": {"Auto Install (PC)": "ACTION_RUN_PC|https://github.com/eliboa/TegraRcmGUI/releases/download/2.6/TegraRcmGUI_v2.6_Installer.msi"}},
    ],
    "🛠️ USEFUL SYSMODS (Restart Required)": [
        {"name": "Sys-patch", "desc": "Auto-patches system modules on boot (fs, ldr, es). Helps games run stably if Sigpatches are outdated.", "urls": {"Step 1. Download file": "https://gbatemp.net/download/sys-patch-sysmodule.39471/download", "Step 2. Select ZIP to auto-copy": "ACTION_PICK_ZIP"}},
        {"name": "Tesla Menu (Overlay Menu)", "desc": "Overlay Menu. Toggle cheats, view system info, overclock... while in-game using combo (L + Dpad Down + R3).", "urls": {"Auto Install (Combo)": "TESLA_ACTION"}},
        {"name": "Ultrahand (Powerful Overlay)", "desc": "Modern overlay manager similar to Tesla. Manages plugins like music, cheats, fps... activate with (ZL+ZR+DDOWN).", "urls": {"Auto Install (Combo)": "ULTRAHAND_ACTION"}},
        {"name": "Edizon Overlay (Game Cheats)", "desc": "Cheat menu overlay. Search values, toggle cheats, infinite money instantly without exiting game.", "urls": {"Auto Install": "https://github.com/proferabg/EdiZon-Overlay/releases/download/v1.0.14/ovlEdiZon.ovl", "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat#cach-3-dung-edizon-overlay"}},
        {"name": "Status Monitor (FPS/Battery/Temp)", "desc": "Real-time hardware monitor. Shows FPS, CPU/GPU temp, RAM speed, Battery %... on screen corner.", "urls": {"Auto Install": "https://github.com/masagrator/Status-Monitor-Overlay/releases/download/1.3.2/Status-Monitor-Overlay.zip"}},
        {"name": "emuiibo (Amiibo Emulation)", "desc": "Virtual Amiibo emulator. Get in-game rewards (Zelda, Splatoon) without real figures. Use with Tesla Menu.", "urls": {"Auto Install": "https://github.com/XorTroll/emuiibo/releases/download/1.1.2/emuiibo.zip"}},
        {"name": "SYS-CLK (Overclock)", "desc": "Safe Overclock/Underclock tool. Improves performance for heavy games (fps boost) or saves battery for light games.", "urls": {"Auto Install": "https://github.com/retronx-team/sys-clk/releases/download/2.0.1/sys-clk-2.0.1-21fix.zip"}},
        {"name": "SysDVR (Stream via USB)", "desc": "Stream Audio/Video from Switch to PC via USB/Wifi. Record/Stream games without expensive Capture Card.", "urls": {"1. Switch App": "https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR.zip", "2. PC Client (7z)": "ACTION_SAVE_PC|https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR-Client-Windows-x64-with-framework.7z"}},
        {"name": "Mission Control", "desc": "Connect Bluetooth controllers from other consoles (PS4, PS5, Xbox One, Wii U Pro...) to Switch without USB Receiver.", "urls": {"Auto Install": "https://github.com/ndeadly/MissionControl/releases/download/v0.14.1/MissionControl-0.14.1-master-141b3aca.zip"}},
        {"name": "Sys-con (USB Controllers)", "desc": "Connect wired 3rd party controllers (Xbox 360, DualShock 3...) to Switch Dock.", "urls": {"Auto Install": "https://github.com/o0Zz/sys-con/releases/download/1.6.1/sys-con-1.6.1.zip"}},
    ],
    "🎮 HOMEBREW (Apps)": [
        {"name": "HB App Store", "desc": "Online Homebrew Store. Search, download, and update hundreds of utility apps and homebrew games directly on Switch.", "urls": {"Auto Install": "https://github.com/fortheusers/hb-appstore/releases/download/v2.3.2/appstore.nro"}},
        {"name": "AIO Switch Updater", "desc": "All-in-one updater on Switch. Update Atmosphere, Firmware, Cheats... via Wifi without PC.", "urls": {"Auto Install": "https://github.com/HamletDuFromage/aio-switch-updater/releases/download/2.23.3/aio-switch-updater.zip"}},
        {"name": "Edizon (Cheat Manager)", "desc": "Powerful Save game and Cheat code manager. Backup saves to SD or activate cheat codes.", "urls": {"Auto Install": "https://github.com/WerWolv/EdiZon/releases/download/v3.1.0/EdiZon.nro"}},
        {"name": "Breeze (Cheat)", "desc": "Advanced Cheat tool (Edizon successor). Supports complex memory search for creating own cheats.", "urls": {"Auto Install": "https://github.com/tomvita/Breeze-Beta/releases/download/beta99r/Breeze.zip"}},
        {"name": "Retroarch (Emulator)", "desc": "All-in-one emulator. Play NES, SNES, GBA, PS1, N64, Arcade... games on Switch.", "urls": {"Web Access": "https://buildbot.libretro.com/nightly/nintendo/switch/libnx/"}},
        {"name": "pEmu (Emulator)", "desc": "Collection of optimized emulators (pFBA, pSNES...) for Switch by Cpasjuste. Great UI and performance.", "urls": {"Web Access": "https://github.com/Cpasjuste/pemu/releases/latest"}},
        {"name": "DBI (File Manager + Installer)", "desc": "Ultimate tool for Switch. Fast USB Game Install (MTP), clean junk files, manage SD files with intuitive UI.", "urls": {"Auto Install": "https://github.com/rashevskyv/dbi/releases/download/854ru/DBI.nro"}},
        {"name": "Tinfoil (Game Shop)", "desc": "Famous FreeShop (needs host). Also a file manager and game installer with nice UI. (Not compatible with latest Atmosphere).", "urls": {"Web Access": "https://tinfoil.io/Download#download"}},
        {"name": "Goldleaf", "desc": "Basic file manager and NSP/NSZ/XCI installer. Open Source. Browse SD files and install via USB (with Quark).", "urls": {"Auto Install": "https://github.com/XorTroll/Goldleaf/releases/download/1.2.0/Goldleaf.nro"}},
        {"name": "Linkalho (Offline Link)", "desc": "Links fake Nintendo Account (Offline). Required for games needing Nintendo Account if banned or offline.", "urls": {"Step 1. Download file": "https://dlhb.gamebrew.org/switchhomebrews/linkalhonx.7z", "Step 2. Select ZIP to auto-copy": "ACTION_LINKALHO_NESTED"}},
        {"name": "Combo: Theme Installer + Themezer", "desc": "Installs both: NXThemes Installer (Manage/Install themes) and Themezer-NX (Download themes online).", "urls": {"Theme installer + Themezer": "THEME_COMBO_ACTION", "🌐 Open Download Page": "https://github.com/exelix11/SwitchThemeInjector/releases"}},
        {"name": "Battery Desync Fix", "desc": "Tool to calibrate battery percentage when it shows incorrect values.", "urls": {"Auto Install": "https://github.com/CTCaer/battery_desync_fix_nx/releases/download/1.5.1/battery_desync_fix_v1.5.1.nro", "📖 Guide": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap/hieu-chuan-pin-ao"}},
    ],
    "⚙️ MISC (Firmware/Cheat/Save)": [
        {"name": "Firmware (Upgrade/Downgrade)", "desc": "Original Nintendo Switch OS files. Required when updating system using Daybreak.", "urls": {"Download Link 1": "https://darthsternie.net/switch-firmwares/", "Download Link 2": "https://github.com/THZoria/NX_Firmware/releases", "Update Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/cap-nhat-firmware-cho-emunand"}},
        {"name": "Game Cheats (AIO)", "desc": "Community cheat database. Download to update latest cheats for Edizon/Breeze.", "urls": {"GBAtemp": "https://gbatemp.net/threads/cheat-codes-ams-and-sx-os-add-and-request.520293/", "CheatSlips": "https://www.cheatslips.com/", "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat"}},
        {"name": "Save Game (Source)", "desc": "Save game repositories shared by community. Useful for New Game+ or lost saves.", "urls": {"GBAtemp Save": "https://gbatemp.net/download/categories/game-saves.1668/", "TheTechGame": "https://www.thetechgame.com/Downloads/cid=135/nintendo-switch-game-saves.html", "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/sao-luu-va-phuc-hoi-save-game"}},
        {"name": "Game Translation (Vietnamese)", "desc": "Collection of Vietnamese Patches for Switch games. Download and install to correct folder (usually atmosphere/contents).", "urls": {"Reference Link": "https://docs.google.com/spreadsheets/d/1k_8w_Eb7M6_3q1-FrtY0gYdrCokr3IGxuk-oj_u-zbw/preview"}},
    ],
    "🚑 QUICK FIX (Common Issues)": [
        {"name": "HARD RESET (WIPE & REINSTALL)", "desc": "Use when soft fixes fail. Wipes SD Card (keeps emuMMC) and reinstalls My Pack.", "urls": {"☢️ RUN RESET": "ACTION_FIX_HARD_RESET"}},
        {"name": "Reinstall My Pack (Recommended)", "desc": "Best way to fix severe errors. System will guide you to download the standard hack pack to reinstall.", "urls": {"🛠️ Run Fix": "ACTION_FIX_REINSTALL_PACK"}},
        {"name": "Remove Themes (Fix Black Screen)", "desc": "Delete theme folder (0100000000001000). Use when theme causes boot failure or black screen.", "urls": {"🛠️ Run Fix": "ACTION_FIX_THEMES"}},
        {"name": "Remove Common Sysmodules", "desc": "Only delete background modules (Tesla, Emuiibo, SysDVR...). Keep Translations and Game Mods. Use when crashing.", "urls": {"🛠️ Run Fix": "ACTION_FIX_MODULES"}},
        {"name": "WIPE Contents Folder (Extreme)", "desc": "WARNING: Delete entire atmosphere/contents folder. Will lose all Sysmods, Mods, Translations, and Cheats. Use for severe crashes.", "urls": {"🔥 Wipe & Reset": "ACTION_FIX_DELETE_ALL_CONTENTS"}},
        {"name": "Remove MacOS Junk (Fix Archive Bit)", "desc": "Scan and delete MacOS junk files (._file, .DS_Store). These often cause Hekate config errors.", "urls": {"🛠️ Run Fix": "ACTION_FIX_MAC_JUNK"}},
        {"name": "Delete All Cheats (Fix Game Crash)", "desc": "Delete all cheat files in contents. Use when game crashes immediately due to old cheat conflicts.", "urls": {"🛠️ Run Fix": "ACTION_FIX_CHEATS"}},
        {"name": "Other Errors (Source: Community)", "desc": "Lookup other common errors and detailed fixes on Community Wiki.\n(Note: This website is in Vietnamese only. Please use Google Translate or AI to translate)", "urls": {"🌍 View Guide": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap"}}
    ],
    "📚 GUIDES (Source: Nintendo Switch Community)": [
        {"name": "Basic Guide", "desc": "Essential knowledge: Distinguish Switch models, hack terminology, basic usage.\n(Note: This website is in Vietnamese only. Please use Google Translate or AI to translate)", "urls": {"🌍 Web Access": "https://nsw.gitbook.io/guide/huong-dan-can-ban/"}},
        {"name": "Advanced Guide", "desc": "In-depth articles: Create EmuMMC, Incognito, Partition SD, Backup Nand...\n(Note: This website is in Vietnamese only. Please use Google Translate or AI to translate)", "urls": {"🌍 Web Access": "https://nsw.gitbook.io/guide/huong-dan-nang-cao"}}
    ],
    "👾 GAME DOWNLOAD SOURCES": [
        {"name": "Switch Game Website", "desc": "Rich Switch game library, frequently updated.", "urls": {"Reference Link": "https://rebrand.ly/tsufurom"}}
    ]
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://gbatemp.net'
}

# --- ToolTip Class ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(300, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        frame = tk.Frame(tw, background="#ffffe0", relief='solid', borderwidth=1)
        frame.pack()

        label = tk.Label(frame, text=self.text, justify='left',
                       background="#ffffe0", foreground="#333",
                       font=("Segoe UI", 9), wraplength=400)
        label.pack(padx=5, pady=2)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class SwitchToolApp:
    # --- Registry Settings ---
    def load_saved_language(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\TsufuSwitchManager", 0, winreg.KEY_READ)
            lang, _ = winreg.QueryValueEx(key, "Language")
            winreg.CloseKey(key)
            return lang
        except:
            return None

    def save_language(self, lang):
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\TsufuSwitchManager")
            winreg.SetValueEx(key, "Language", 0, winreg.REG_SZ, lang)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry error: {e}")
            
    def load_ftp_ip(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\TsufuSwitchManager", 0, winreg.KEY_READ)
            ip, _ = winreg.QueryValueEx(key, "LastFTP_IP")
            winreg.CloseKey(key)
            return ip
        except:
            return "192.168.1." # Default

    def save_ftp_ip(self, ip):
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\TsufuSwitchManager")
            winreg.SetValueEx(key, "LastFTP_IP", 0, winreg.REG_SZ, ip)
            winreg.CloseKey(key)
        except: pass

    # --- FTP Keep-Alive ---
    def ftp_keep_alive_loop(self, ip, port):
        self.keep_alive_running = True
        try:
            ftp_alive = ftplib.FTP()
            ftp_alive.connect(ip, int(port), timeout=10)
            ftp_alive.login()
            
            while self.keep_alive_running:
                try:
                    ftp_alive.voidcmd("NOOP")
                    for _ in range(15): 
                        if not self.keep_alive_running: break
                        time.sleep(1)
                except Exception:
                    break
            
            try: ftp_alive.quit()
            except: pass
            
        except Exception as e:
            print(f"Keep-alive failed: {e}")
        finally:
            self.keep_alive_running = False

    def ask_language_first_time(self):
        lang_win = tk.Toplevel(self.root)
        lang_win.title("Select Language")
        lang_win.geometry("300x150")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - 150
        y = (screen_height // 2) - 75
        lang_win.geometry(f"+{x}+{y}")
        
        lang_win.configure(bg="#2d2d30")
        lang_win.transient(self.root)
        lang_win.grab_set()
        
        lbl = tk.Label(lang_win, text="Please select your language:\nVui lòng chọn ngôn ngữ:", 
                       fg="white", bg="#2d2d30", font=("Segoe UI", 10))
        lbl.pack(pady=20)

        def set_vi():
            self.lang_code = "VI"
            self.save_language("VI")
            lang_win.destroy()

        def set_en():
            self.lang_code = "EN"
            self.save_language("EN")
            lang_win.destroy()

        btn_frame = tk.Frame(lang_win, bg="#2d2d30")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Tiếng Việt 🇻🇳", command=set_vi, width=12, bg="#4caf50", fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="English 🇺🇸", command=set_en, width=12, bg="#007acc", fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=10)

        self.root.wait_window(lang_win)

    def __init__(self, root):
        self.root = root
        saved_lang = self.load_saved_language()
        if saved_lang:
            self.lang_code = saved_lang
        else:
            self.lang_code = "VI"
            self.ask_language_first_time()
            self.cancel_flag = False
        self.cancel_flag = False
        
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except: pass

        self.setup_window()
        self.dest_path = tk.StringVar(value=os.getcwd())
        self.is_mtp_mode = tk.BooleanVar(value=False)
        
        self.configure_styles()
        self.root.configure(bg=COLOR_BG)
        
        self.is_app_ready = False 
        self.keep_alive_running = False
        
        self.show_loading_screen()

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        app_width = 1100  
        app_height = screen_height - 110 
        x = int((screen_width / 2) - (app_width / 2))
        y = 5 
        self.root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        self.update_title()

    def update_title(self):
        self.root.title(f"{UI_TEXT[self.lang_code]['title']} (v{APP_VERSION})")
    
    def confirm_my_pack_download(self):
        msg = (
            "⚠️ LƯU Ý QUAN TRỌNG VỀ TƯƠNG THÍCH ⚠️\n\n"
            "• Gói hack này hỗ trợ Firmware tối đa 21.1.0 và tương thích mọi FW hiện tại.\n"
            "• TUY NHIÊN: Do chạy nhân Atmosphere mới nhất, một số Homebrew & Sysmodule cũ "
            "(đặc biệt là Tinfoil) có thể KHÔNG HOẠT ĐỘNG.\n\n"
            "💡 GIẢI PHÁP (Nếu bạn đang ở FW < 21.0.0 và cần dùng Tinfoil/App cũ):\n"
            "1. Cài đặt My Pack này như bình thường.\n"
            "2. Sau đó, tìm và cài đè thêm mục 'Atmosphere 1.9.5' ở bên dưới.\n"
            "(Hoặc tải lẻ từng phần: Hekate + Sigpatches + Atmosphere 1.9.5 thay vì dùng My Pack).\n\n"
            "Bạn có ĐÃ HIỂU và muốn tiếp tục tải về không?"
        )
        
        if messagebox.askokcancel("Xác nhận tải My Pack", msg, icon='warning'):
            webbrowser.open("https://rebrand.ly/mypack")

    def configure_styles(self):
        style = ttk.Style()
        try: style.theme_use('clam') 
        except: pass

        style.configure(".", background=COLOR_BG, foreground=COLOR_FG, font=FONT_NORMAL)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_FG)
        style.configure("Card.TFrame", background=COLOR_CARD, relief="flat")
        style.configure("TCheckbutton", background=COLOR_BG, foreground=COLOR_FG, font=FONT_SMALL)
        
        style.configure("Section.TLabel", 
                        font=FONT_HEADER, 
                        foreground=COLOR_GOLD, 
                        background=COLOR_HEADER_BG, 
                        padding=10)
        
        style.configure("TEntry", fieldbackground=COLOR_CARD, foreground=COLOR_FG, borderwidth=0)
        
        style.configure("TButton", 
                        background=COLOR_CARD, foreground=COLOR_FG, 
                        borderwidth=1, focuscolor=COLOR_ACCENT, font=("Segoe UI", 9))
        style.map("TButton", 
                  background=[('active', "#3e3e42"), ('pressed', "#007acc")],
                  foreground=[('active', 'white')])

        style.configure("Accent.TButton", 
                        background=COLOR_ACCENT, foreground="white", 
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Accent.TButton", 
                  background=[('active', COLOR_ACCENT_HOVER), ('pressed', "#003e66")])

        style.configure("Gold.TButton", 
                        background=COLOR_GOLD, foreground="#333333", 
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Gold.TButton", 
                  background=[('active', "#ffea70"), ('pressed', "#ccac00")])

        style.configure("Web.TButton", 
                        background="#333333", foreground="#aaaaaa", 
                        font=("Segoe UI", 9), borderwidth=0)
        style.map("Web.TButton", background=[('active', "#444444")])
        style.configure("Smart.TButton", 
                        background=COLOR_SPEED_BG, foreground="white", 
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Smart.TButton", 
                  background=[('active', COLOR_SPEED_HOVER), ('pressed', COLOR_SPEED_PRESS)])
        
        style.configure("DownloadAll.TButton", 
                        background=COLOR_SUCCESS, foreground="white", 
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("DownloadAll.TButton", background=[('active', "#45a049")])
        
        style.configure("Danger.TButton", 
                        background=COLOR_DANGER, foreground="white", 
                        font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Danger.TButton", 
                  background=[('active', COLOR_DANGER_HOVER), ('pressed', "#a71d2a")])
        
        style.configure("Lang.TButton", 
                        background="#555555", foreground="white", 
                        font=("Segoe UI", 8, "bold"), borderwidth=0)
        style.configure("FTP.TButton", 
                        background=COLOR_PURPLE, foreground="white", 
                        font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("FTP.TButton", 
                  background=[('active', COLOR_PURPLE_HOVER), ('pressed', "#6c3483")])

    # --- Initialization Tasks ---
    def run_init_tasks(self):
        self.auto_detect_drive()
        try:
            load = Image.open(resource_path("logo.png"))
            target_height = 140 
            aspect_ratio = load.width / load.height
            target_width = int(target_height * aspect_ratio)
            self.preloaded_logo_image = load.resize((target_width, target_height), Image.Resampling.LANCZOS)
        except:
            self.preloaded_logo_image = None
        time.sleep(1.5) 
        self.is_app_ready = True

    # --- Loading Screen ---
    def show_loading_screen(self):
        self.loading_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        center_frame = tk.Frame(self.loading_frame, bg=COLOR_BG)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.loading_frames = [] 
        try:
            im = Image.open(resource_path("loading.gif"))
            for frame in ImageSequence.Iterator(im):
                self.loading_frames.append(ImageTk.PhotoImage(frame.copy()))
        except:
            pass 

        self.loading_label = tk.Label(center_frame, bg=COLOR_BG, bd=0)
        self.loading_label.pack(pady=(0, 20))

        if self.lang_code == "VI":
            loading_txt = "✨ Đang thực hiện ma thuật hắc ám, vui lòng đợi..."
        else:
            loading_txt = "✨ Performing dark magic, please wait..."
            
        tk.Label(center_frame, 
                 text=loading_txt, 
                 font=("Segoe UI", 14, "bold"),  
                 fg=COLOR_GOLD,                  
                 bg=COLOR_BG).pack(pady=(10, 0))

        threading.Thread(target=self.run_init_tasks, daemon=True).start()
        self.update_loading_animation(0)

    def update_loading_animation(self, frame_index):
        if not hasattr(self, 'loading_frame') or not self.loading_frame.winfo_exists():
            return

        if self.is_app_ready: 
            self.finish_loading() 
            return

        if self.loading_frames:
            self.loading_label.config(image=self.loading_frames[frame_index])
            next_index = (frame_index + 1) % len(self.loading_frames)
        else:
            next_index = 0

        self.root.after(30, self.update_loading_animation, next_index)

    def finish_loading(self):
        if hasattr(self, 'loading_frame') and self.loading_frame.winfo_exists():
            self.loading_frame.destroy() 
            self.setup_ui() 
            self.check_for_updates()
    
    def toggle_language(self):
        if self.lang_code == "VI":
            self.lang_code = "EN"
        else:
            self.lang_code = "VI"
        
        self.update_title()
        self.refresh_ui()

    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def show_user_guide(self):
        guide_win = tk.Toplevel(self.root)
        guide_win.title("Hướng dẫn sử dụng / User Manual")
        guide_win.geometry("600x500")
        guide_win.configure(bg=COLOR_BG)

        tk.Label(guide_win, text="HƯỚNG DẪN SỬ DỤNG", font=FONT_HEADER, bg=COLOR_BG, fg=COLOR_GOLD).pack(pady=10)

        text_area = scrolledtext.ScrolledText(guide_win, width=70, height=25, font=("Segoe UI", 10), bg=COLOR_CARD, fg="white", padx=10, pady=10, relief="flat")
        text_area.pack(fill="both", expand=True, padx=10, pady=5)

        guide_content = """...""" # Kept brief for brevity
        text_area.insert(tk.END, guide_content)
        text_area.config(state=tk.DISABLED) 

    def setup_ui(self):
        text_db = UI_TEXT[self.lang_code]
        if self.lang_code == "VI":
            data_db = DATA_VI
        else:
            data_db = DATA_EN

        top_frame = tk.Frame(self.root, bg=COLOR_BG, pady=10, padx=20)
        top_frame.pack(fill="x", side="top")
        
        left_info = tk.Frame(top_frame, bg=COLOR_BG)
        left_info.pack(side="left", fill="both", expand=True)

        lbl_title = tk.Label(left_info, text=text_db["title"], font=("Segoe UI", 20, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT)
        lbl_title.pack(side="top", anchor="w")

        lbl_credit = tk.Label(left_info, text=text_db["credit"], font=("Segoe UI", 10, "italic"), bg=COLOR_BG, fg="#dddddd")
        lbl_credit.pack(side="top", anchor="w")
        
        lbl_credit_2 = tk.Label(left_info, text=text_db["credit2"],
                                font=("Segoe UI", 9, "italic"), bg=COLOR_BG, fg="#dddddd", justify="left")
        lbl_credit_2.pack(side="top", anchor="w", pady=(2, 0))
       
        ver_info_text = f"✨ Update {APP_VERSION} (25/12/2025): Hekate v6.4.2 | Atmosphere 1.10.1 | Sigpatches v1.10.1p"
        lbl_version_info = tk.Label(left_info, text=ver_info_text,
                                    font=("Segoe UI", 9, "bold"), bg=COLOR_BG, fg=COLOR_SUCCESS, justify="left")
        lbl_version_info.pack(side="top", anchor="w", pady=(5, 0))

        right_info = tk.Frame(top_frame, bg=COLOR_BG)
        right_info.pack(side="right", anchor="ne", fill="y")
        
        btn_container = tk.Frame(right_info, bg=COLOR_BG)
        btn_container.pack(side="top", anchor="e")

        btn_update_soft = ttk.Button(btn_container, text=text_db["btn_update_soft"], style="TButton",
                                     command=self.check_for_updates)
        btn_update_soft.pack(side="top", anchor="e", pady=2, fill="x")

        btn_donate_header = tk.Button(btn_container, text=text_db["btn_donate"], bg="#FFD700", fg="black", font=("Segoe UI", 9, "bold"), relief="flat",
                                      activebackground="#ffcc00",
                                      command=lambda: webbrowser.open("https://tsufu.gitbook.io/donate/"))
        btn_donate_header.pack(side="top", anchor="e", pady=2, fill="x")

        sub_btn_frame = tk.Frame(btn_container, bg=COLOR_BG)
        sub_btn_frame.pack(side="top", anchor="e", pady=2)

        btn_guide = ttk.Button(sub_btn_frame, text=text_db["btn_guide"], style="TButton", width=18,
                               command=self.show_user_guide)
        btn_guide.pack(side="right", padx=2)

        lang_text = "Language: VI" if self.lang_code == "VI" else "Language: EN"
        btn_lang = ttk.Button(sub_btn_frame, text=lang_text, style="Lang.TButton", width=12, command=self.toggle_language)
        btn_lang.pack(side="right", padx=2)

        try:
            if hasattr(self, 'preloaded_logo_image') and self.preloaded_logo_image:
                 self.logo_img = ImageTk.PhotoImage(self.preloaded_logo_image)
            else:
                load = Image.open(resource_path("logo.png"))
                target_height = 100
                aspect_ratio = load.width / load.height
                target_width = int(target_height * aspect_ratio)
                render = load.resize((target_width, target_height), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(render)

            self.logo_label = tk.Label(right_info, image=self.logo_img, bg=COLOR_BG, bd=0)
            self.logo_label.pack(side="top", anchor="e", pady=5)
        except Exception as e:
            pass

        path_frame = tk.Frame(self.root, bg=COLOR_BG, pady=5, padx=20)
        path_frame.pack(fill="x", side="top") 
        
        path_lbl_container = tk.Frame(path_frame, bg=COLOR_BG)
        path_lbl_container.pack(side="left")

        tk.Label(path_lbl_container, text=text_db["path_label"], bg=COLOR_BG, fg="#dddddd", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        lbl_path_help = tk.Label(path_lbl_container, text="❓", font=("Segoe UI", 10), bg=COLOR_BG, fg=COLOR_INFO, cursor="hand2")
        lbl_path_help.pack(side="left", padx=5)
        ToolTip(lbl_path_help, text_db["path_tip"])

        entry_path = tk.Entry(path_frame, textvariable=self.dest_path, bg=COLOR_CARD, fg="white", insertbackground="white", relief="flat", font=("Consolas", 11))
        entry_path.pack(side="left", fill="x", expand=True, padx=10, ipady=5)
        
        ttk.Button(path_frame, text=text_db["btn_browse"], command=self.browse_folder).pack(side="left", padx=2)
        ttk.Button(path_frame, text=text_db["btn_detect"], command=lambda: threading.Thread(target=self.auto_detect_drive, daemon=True).start()).pack(side="left", padx=2)
        ttk.Button(path_frame, text=text_db["btn_open"], command=self.open_root_folder).pack(side="left", padx=2)
        
        # --- FTP Section ---
        ftp_frame = tk.Frame(self.root, bg=COLOR_BG, pady=2, padx=20)
        ftp_frame.pack(fill="x", side="top")

        tk.Label(ftp_frame, text=text_db["lbl_ftp_hint"], 
                 bg=COLOR_BG, fg=COLOR_GOLD, font=("Segoe UI", 10, "bold")).pack(side="left")

        btn_ftp = ttk.Button(ftp_frame, text=text_db.get("btn_ftp", "📡 FTP Transfer (Wifi)"), 
                             style="FTP.TButton", 
                             command=self.open_ftp_window, width=25)
        btn_ftp.pack(side="left", padx=10)

        mtp_frame = tk.Frame(self.root, bg=COLOR_BG, padx=20)
        mtp_frame.pack(fill="x", side="top")
        
        def on_mtp_check():
            if self.is_mtp_mode.get():
                messagebox.showwarning("MTP Warning", text_db["msg_mtp_alert"])
                self.browse_folder()
        
        chk_mtp = ttk.Checkbutton(mtp_frame, text=text_db["chk_mtp_label"], variable=self.is_mtp_mode, 
                                  command=on_mtp_check, style="TCheckbutton")
        chk_mtp.pack(side="left")

        container = tk.Frame(self.root, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=10, pady=(5, 0))
        
        self.canvas = tk.Canvas(container, highlightthickness=0, bg=COLOR_BG)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        self.scroll_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        categories = data_db.keys()
        
        for cat in categories:
            items = data_db[cat]
            header_frame = tk.Frame(self.scroll_frame, bg=COLOR_HEADER_BG, pady=5)
            header_frame.pack(fill="x", pady=(15, 5), padx=5) 
            
            tk.Label(header_frame, text=cat, font=FONT_HEADER, bg=COLOR_HEADER_BG, fg=COLOR_GOLD, anchor="w").pack(side="left", padx=10)
            
            if "SYSMOD" in cat or "HOMEBREW" in cat:
                btn_dl_all = ttk.Button(header_frame, text=text_db["btn_dl_all"], style="DownloadAll.TButton",
                                        command=lambda c=cat: self.download_category_all(c))
                btn_dl_all.pack(side="right", padx=10)
            
            tk.Frame(header_frame, bg=COLOR_GOLD, height=2).pack(side="bottom", fill="x")

            for item in items:
                self.create_item_card(self.scroll_frame, item)

        bot = tk.Frame(self.root, bg=COLOR_CARD, pady=10, padx=20)
        bot.pack(fill="x", side="bottom")
        
        self.progress_var = tk.DoubleVar()
        style_prog = ttk.Style()
        style_prog.configure("Horizontal.TProgressbar", background=COLOR_SUCCESS, troughcolor=COLOR_BG, borderwidth=0)
        self.progress_bar = ttk.Progressbar(bot, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=5)
        
        info_line = tk.Frame(bot, bg=COLOR_CARD)
        info_line.pack(fill="x")
        
        self.status_label = tk.Label(info_line, text=text_db["status_ready"], bg=COLOR_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
        self.status_label.pack(side="left")

        btn_cancel = ttk.Button(info_line, text=text_db.get("btn_cancel", "Cancel"), style="Danger.TButton", 
                                command=self.cancel_download)
        btn_cancel.pack(side="left", padx=10)
        
        btn_bug_report = tk.Button(info_line, text="🐞 Góp ý & báo lỗi (Bug&Report)", 
                                   font=("Segoe UI", 9, "bold"), 
                                   bg=COLOR_CARD, fg="#E06C75", 
                                   activebackground="#3e3e42", activeforeground="#ff5555",
                                   bd=0, cursor="hand2",
                                   command=lambda: webbrowser.open("https://rebrand.ly/bugrp"))
        btn_bug_report.pack(side="right")

    def check_for_updates(self):
        threading.Thread(target=self._process_check_update, daemon=True).start()

    def _process_check_update(self):
        self.status_label.config(text="Checking for updates...", fg=COLOR_INFO)
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        try:
            r = requests.get(api_url, timeout=None)
            if r.status_code == 200:
                data = r.json()
                latest_tag = data.get("tag_name", "v0.0.0")
                download_url = ""
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                if latest_tag != f"v{APP_VERSION}" and latest_tag > f"v{APP_VERSION}":
                    msg = f"Đã có phiên bản mới: {latest_tag}\nBạn có muốn cập nhật ngay không?"
                    if messagebox.askyesno("Update Available", msg):
                        if download_url:
                            self.perform_update_download(download_url)
                        else:
                            messagebox.showerror("Error", "Không tìm thấy file tải xuống trong bản phát hành.")
                            webbrowser.open(data["html_url"])
                else:
                    messagebox.showinfo("Update", f"Bạn đang dùng phiên bản mới nhất (v{APP_VERSION}).")
            else:
                messagebox.showerror("Error", "Không thể kiểm tra cập nhật (Repo chưa public hoặc lỗi mạng).")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi kiểm tra cập nhật: {e}")
        self.status_label.config(text="Ready", fg=COLOR_ACCENT)

    def perform_update_download(self, url):
        self.status_label.config(text="Downloading update...", fg=COLOR_WARNING)
        try:
            r = requests.get(url, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            new_exe_name = "SwitchManager_New.exe"
            with open(new_exe_name, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        self.progress_var.set((downloaded / total_size) * 100)
            
            self.status_label.config(text="Installing update...", fg=COLOR_SUCCESS)
            current_exe = sys.executable
            bat_script = f"""
@echo off
timeout /t 3 /nobreak
move /y "{current_exe}" "{current_exe}.old"
move /y "{new_exe_name}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
            with open("update_script.bat", "w") as bat:
                bat.write(bat_script)
            
            text_db = UI_TEXT[self.lang_code]
            messagebox.showinfo("Update", text_db.get("msg_update_manual", "Restarting..."))
            subprocess.Popen("update_script.bat", shell=True)
            self.root.quit()
        except Exception as e:
            text_db = UI_TEXT[self.lang_code]
            full_msg = f"Lỗi cập nhật: {e}\n\n{text_db['msg_update_virus']}"
            messagebox.showerror("Update Error", full_msg)

    def create_item_card(self, parent, item):
        card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        card.pack(fill="x", pady=4, padx=10)
        
        name_frame = tk.Frame(card, bg=COLOR_CARD)
        name_frame.pack(side="left", fill="x", expand=True)
        
        label_fg = "white"
        if "HARD RESET" in item["name"].upper():
            label_fg = COLOR_DANGER
            
        lbl_name = tk.Label(name_frame, text=item["name"], font=FONT_TITLE, bg=COLOR_CARD, fg=label_fg, anchor="w")
        lbl_name.pack(side="left")
        
        lbl_info = tk.Label(name_frame, text="❓", font=("Segoe UI", 10), bg=COLOR_CARD, fg=COLOR_INFO, cursor="hand2")
        lbl_info.pack(side="left", padx=5)
        
        ToolTip(lbl_info, item.get("desc", ""))
        
        btn_box = ttk.Frame(card, style="Card.TFrame")
        btn_box.pack(side="right")

        if "Việt hóa game" in item["name"] or "Game Translation" in item["name"]:
            txt = "⚡ Auto Install" if self.lang_code == "EN" else "⚡ Cài đặt thông minh"
            ttk.Button(btn_box, text=txt, style="Smart.TButton", command=self.install_translation_pack).pack(side="left", padx=4)
        if "Firmware" in item["name"]:
            txt = "⚡ Auto Install" if self.lang_code == "EN" else "⚡Chọn file nén để tự động chép."
            ttk.Button(btn_box, text=txt, command=self.install_firmware_local).pack(side="left", padx=4)

        has_manual_web_link = False

        for lbl, url in item["urls"].items():
            if url == "TESLA_ACTION": 
                cmd = self.install_tesla_combo
            elif url == "ULTRAHAND_ACTION": 
                cmd = self.install_ultrahand_combo
            elif url == "ACTION_LINKALHO_NESTED":
                cmd = self.install_linkalho_special
            elif url == "ACTION_PICK_ZIP":
                cmd = lambda n=item["name"]: self.install_local_zip_generic(n)
            elif url == "ACTION_AMS_195":
                cmd = self.install_ams_195_logic
            elif url == "THEME_COMBO_ACTION":
                cmd = self.install_theme_combo
            elif url.startswith("ACTION_SAVE_PC|"):
                actual_url = url.split("|")[1]
                cmd = lambda u=actual_url: self.download_pc_file_generic(u)
            elif url.startswith("ACTION_RUN_PC|"):
                actual_url = url.split("|")[1]
                cmd = lambda u=actual_url, n=item["name"]: self.process_run_pc(u, n)
            elif url.startswith("ACTION_FIX_"):
                cmd = lambda u=url: self.run_fix_task(u)
            elif url == "ACTION_MY_PACK_WARN":
                cmd = self.confirm_my_pack_download
            else: 
                cmd = lambda u=url, n=item["name"], l=lbl: self.process_action(u, n, l)

            display_text = lbl
            is_web = "Web" in lbl or "Link" in lbl or "Hướng dẫn" in lbl or "Guide" in lbl or "GBAtemp" in lbl or "Cộng Đồng" in lbl or "TheTechGame" in lbl or "CheatSlips" in lbl or "Link tham khảo" in lbl
            
            if "Bước 1" in lbl or "Step 1" in lbl:
                 is_web = True

            btn_width = None
            if "Fix" in url: 
                display_text = lbl
            
            if url == "ACTION_FIX_HARD_RESET":
                 btn_style = "Danger.TButton"
            elif "Fix" in url:
                 btn_style = "Accent.TButton"
            elif url == "ACTION_AMS_195":
                display_text = "✨ " + lbl
                btn_style = "Gold.TButton"
            elif url == "THEME_COMBO_ACTION":
                display_text = "⚡ " + lbl
                btn_style = "Accent.TButton"
            elif "Tự động" in lbl or "Auto" in lbl or "Tải" in lbl or "Download" in lbl or "Chọn" in lbl or "Pick" in lbl:
                display_text = "⚡ " + lbl
                btn_style = "Accent.TButton"
            else:
                btn_style = "TButton"
            
            if "Bước 1" in lbl or "Step 1" in lbl:
                display_text = "⬇️ " + lbl
                btn_style = "Accent.TButton"
            elif is_web:
                btn_style = "Web.TButton"
                has_manual_web_link = True 

            btn = ttk.Button(btn_box, text=display_text, style=btn_style, command=cmd)
            padx_val = 2
            if "Fix" in url: padx_val = 5
                
            btn.pack(side="left", padx=padx_val)
            if "HARD RESET" in lbl:
                ToolTip(btn, UI_TEXT[self.lang_code]["tip_hard_reset"])

        detected_source_url = None
        for u in item["urls"].values():
            if "github.com" in u and "/releases/download/" in u:
                detected_source_url = u.split("/releases/download/")[0] + "/releases"
                break
            elif "github.com" in u and "ACTION" not in u and ".zip" not in u and ".nro" not in u:
                 detected_source_url = u
                 break

        if detected_source_url:
            txt_dl_page = "🌐 Download Page" if self.lang_code == "EN" else "🌐 Mở trang download"
            is_duplicate = False
            for existing_url in item["urls"].values():
                if existing_url == detected_source_url:
                    is_duplicate = True
            
            if not is_duplicate:
                ttk.Button(btn_box, text=txt_dl_page, style="Web.TButton", 
                           command=lambda u=detected_source_url: webbrowser.open(u)).pack(side="left", padx=2)
       
    def install_ams_195_logic(self):
        text_db = UI_TEXT[self.lang_code]
        dialog = tk.Toplevel(self.root)
        dialog.title(text_db["ams_195_title"])
        dialog.geometry("600x550")
        dialog.configure(bg=COLOR_CARD)
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 275
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(dialog, text="⚠️ ATTENTION / CHÚ Ý", font=("Segoe UI", 14, "bold"), fg=COLOR_GOLD, bg=COLOR_CARD).pack(pady=10)
        msg_frame = tk.Frame(dialog, bg=COLOR_CARD, padx=10)
        msg_frame.pack(fill="both", expand=True)
        st = scrolledtext.ScrolledText(msg_frame, height=18, font=("Segoe UI", 10), bg="#1e1e1e", fg="white", relief="flat")
        st.pack(fill="both", expand=True)
        st.insert(tk.END, text_db["ams_195_msg"])
        st.config(state=tk.DISABLED)
        
        guide_url = "https://nsw.gitbook.io/guide/cac-loi-thuong-gap/xoa-thong-bao-update-firmware"
        btn_guide = ttk.Button(dialog, text=text_db["btn_maintenance_guide"], style="TButton", 
                               command=lambda: webbrowser.open(guide_url))
        btn_guide.pack(pady=10)
        
        btn_frame = tk.Frame(dialog, bg=COLOR_CARD, pady=10)
        btn_frame.pack(fill="x", side="bottom")
        
        def on_confirm():
            dialog.destroy()
            url = "https://github.com/Atmosphere-NX/Atmosphere/releases/download/1.9.5/atmosphere-1.9.5-master-de9b02007+hbl-2.4.4+hbmenu-3.6.0.zip"
            threading.Thread(target=self.download_task, args=("Atmosphere 1.9.5", url), daemon=True).start()
            
        def on_cancel():
            dialog.destroy()

        ttk.Button(btn_frame, text="✅ OK, Download & Install", style="Accent.TButton", command=on_confirm).pack(side="right", padx=20)
        ttk.Button(btn_frame, text="❌ Cancel", style="TButton", command=on_cancel).pack(side="right", padx=10)

    def browse_folder(self):
        d = filedialog.askdirectory()
        if d: 
            self.dest_path.set(d)

    def download_category_all(self, category_name):
        data_db = DATA_VI if self.lang_code == "VI" else DATA_EN
        text_db = UI_TEXT[self.lang_code]
        items = data_db.get(category_name, [])
        if not items: return
        
        msg = text_db["msg_confirm_dl_all"].format(category=category_name)
        if not messagebox.askyesno("Confirm", msg):
            return

        self.cancel_flag = False
        threading.Thread(target=self.process_download_all, args=(items,), daemon=True).start()

    def cancel_download(self):
        self.cancel_flag = True
        self.status_label.config(text=UI_TEXT[self.lang_code]["msg_cancelled"], fg=COLOR_WARNING)

    def process_download_all(self, items):
        count = 0
        for item in items:
            if self.cancel_flag: break
            for label, url in item["urls"].items():
                if self.cancel_flag: break
                
                if "PC" in label or "Client" in label or "Web" in label or "Guide" in label or "Link" in label or "Hướng dẫn" in label:
                    continue
                if "Bước 1" in label or "Step 1" in label or "Bước 2" in label or "Step 2" in label:
                    continue
                if "ACTION_SAVE_PC" in url or "ACTION_PICK_ZIP" in url or "ACTION_FIX" in url:
                    continue
                if "ACTION_AMS_195" in url:
                    continue
                
                if url == "THEME_COMBO_ACTION":
                    self.root.after(0, lambda: self.status_label.config(text=f"Auto: Theme Combo...", fg=COLOR_INFO))
                    self.run_theme_combo_thread(self.dest_path.get(), is_batch=True)
                    count += 1
                    time.sleep(1)
                    continue

                if url == "TESLA_ACTION":
                    self.root.after(0, lambda: self.status_label.config(text=f"Auto: Tesla Combo...", fg=COLOR_INFO))
                    self.run_tesla_thread(self.dest_path.get(), is_batch=True)
                    count += 1
                    continue
                elif url == "ULTRAHAND_ACTION":
                    self.root.after(0, lambda: self.status_label.config(text=f"Auto: Ultrahand Combo...", fg=COLOR_INFO))
                    self.run_ultrahand_thread(self.dest_path.get(), is_batch=True)
                    count += 1
                    continue
                
                self.download_task(item["name"], url, silent_success=False, is_batch=True)
                count += 1
                time.sleep(1)

        if not self.cancel_flag:
            self.root.after(0, lambda: messagebox.showinfo("Done", f"Finished {count} tasks."))
        else:
            self.root.after(0, lambda: messagebox.showinfo("Cancelled", "Download queue cancelled."))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def auto_detect_drive(self):
        text_db = UI_TEXT[self.lang_code]
        found_drive = None
        
        if sys.platform == 'win32':
            letters = "EFGHIJKLMNOPQRSTUVWXYZ" # Skip C, D
            for letter in letters:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        dtype = ctypes.windll.kernel32.GetDriveTypeW(drive)
                        if dtype == 2: # Removable
                            vol_name_buf = ctypes.create_unicode_buffer(1024)
                            ctypes.windll.kernel32.GetVolumeInformationW(
                                ctypes.c_wchar_p(drive),
                                vol_name_buf,
                                ctypes.sizeof(vol_name_buf),
                                None, None, None, None, 0
                            )
                            vol_label = vol_name_buf.value.upper()
                            
                            if any(k in vol_label for k in ["SWITCH", "SD", "NO NAME", "HEKATE", "BOOT", "ATMOSPHERE"]):
                                found_drive = drive
                                break
                            
                            if not found_drive: 
                                found_drive = drive
                    except: pass
        
        if found_drive:
            self.root.after(0, lambda: self.dest_path.set(found_drive))
            self.root.after(0, lambda: self.status_label.config(text=f"{text_db['status_detect_ok']}{found_drive}", fg=COLOR_SUCCESS))
        else:
            self.root.after(0, lambda: self.status_label.config(text=text_db['status_detect_fail'], fg=COLOR_WARNING))

    def download_pc_file_generic(self, url):
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))
        if not filename: filename = "downloaded_file"
        
        ext = os.path.splitext(filename)[1]
        file_types = [("All Files", "*.*")]
        if ext == ".msi": file_types.insert(0, ("Installer", "*.msi"))
        if ext == ".7z": file_types.insert(0, ("7z Archive", "*.7z"))

        save_path = filedialog.asksaveasfilename(
            title="Save file",
            defaultextension=ext,
            filetypes=file_types,
            initialfile=filename
        )
        
        if save_path:
            self.cancel_flag = False
            threading.Thread(target=self.download_task, args=("File PC", url), kwargs={'custom_save_path': save_path}, daemon=True).start()

    def process_run_pc(self, url, name):
        if not messagebox.askyesno("Xác nhận cài đặt", f"Bạn có muốn tải và TỰ ĐỘNG CHẠY file cài đặt cho {name} không?"):
            return
        filename = "TegraRcmGUI_Installer.msi" 
        temp_dir = os.environ.get('TEMP', os.getcwd())
        save_path = os.path.join(temp_dir, filename)
        self.cancel_flag = False
        threading.Thread(target=self.download_task, 
                         args=(name, url), 
                         kwargs={'custom_save_path': save_path, 'auto_run': True}, 
                         daemon=True).start()

    def open_root_folder(self):
        path = self.dest_path.get()
        if os.path.exists(path):
            if sys.platform == 'win32': os.startfile(path)
            elif sys.platform == 'darwin': subprocess.Popen(['open', path])
            else: subprocess.Popen(['xdg-open', path])
        else:
            messagebox.showerror("Error", "Path not found!")

    def process_action(self, url, name, label):
        if "Web" in label or "Link" in label or "Guide" in label or "Hướng dẫn" in label:
            webbrowser.open(url)
            self.status_label.config(text=f"Open Web: {name}", fg=COLOR_ACCENT)
            return
        
        if "Bước 1" in label or "Step 1" in label:
             webbrowser.open(url)
             self.status_label.config(text=f"Open Download: {name}", fg=COLOR_ACCENT)
             return

        web_keywords = ["tinfoil.io", "cheatslips", "gbatemp", "thetechgame", "nswgame"]
        for kw in web_keywords:
            if kw in url:
                if messagebox.askyesno("Confirm", f"Open web browser for {name}?"):
                    webbrowser.open(url)
                    return
        
        self.cancel_flag = False
        threading.Thread(target=self.download_task, args=(name, url), daemon=True).start()

    def install_tesla_combo(self):
        root_path = self.dest_path.get()
        self.cancel_flag = False
        threading.Thread(target=self.run_tesla_thread, args=(root_path,), daemon=True).start()

    def run_tesla_thread(self, root_path, is_batch=False):
        url1 = "https://github.com/ppkantorski/nx-ovlloader/releases/download/v2.0.0/nx-ovlloader+.zip"
        self.download_task("Tesla Loader", url1, silent_success=True, is_batch=is_batch)
        url2 = "https://github.com/WerWolv/Tesla-Menu/releases/download/v1.2.3/ovlmenu.zip"
        self.download_task("Tesla Menu UI", url2, is_batch=is_batch)

    def install_ultrahand_combo(self):
        root_path = self.dest_path.get()
        self.cancel_flag = False
        threading.Thread(target=self.run_ultrahand_thread, args=(root_path,), daemon=True).start()

    def run_ultrahand_thread(self, root_path, is_batch=False):
        url1 = "https://github.com/ppkantorski/nx-ovlloader/releases/download/v2.0.0/nx-ovlloader+.zip"
        self.download_task("Ultrahand Loader", url1, silent_success=True, is_batch=is_batch)
        url2 = "https://github.com/ppkantorski/Ultrahand-Overlay/releases/latest/download/ovlmenu.ovl"
        self.download_task("Ultrahand Overlay", url2, is_batch=is_batch)

    def install_theme_combo(self):
        root_path = self.dest_path.get()
        self.cancel_flag = False
        threading.Thread(target=self.run_theme_combo_thread, args=(root_path,), daemon=True).start()

    def run_theme_combo_thread(self, root_path, is_batch=False):
        url1 = "https://github.com/exelix11/SwitchThemeInjector/releases/download/v4.8.3/NXThemesInstaller.nro"
        self.download_task("NXThemes Installer", url1, silent_success=True, is_batch=is_batch)
        url2 = "https://github.com/suchmememanyskill/themezer-nx/releases/download/2.0.3/themezer-nx.nro"
        self.download_task("Themezer-NX", url2, is_batch=is_batch)

    def download_task(self, name, url, silent_success=False, custom_save_path=None, auto_run=False, is_batch=False):
        try:
            if custom_save_path:
                save_path = custom_save_path
            else:
                # Always download to dest_path
                root_path = self.dest_path.get()
                if not os.path.exists(root_path): os.makedirs(root_path)

            self.root.after(0, lambda: self.status_label.config(text=f"Connecting: {name}...", fg=COLOR_ACCENT))
            
            try:
                r = requests.get(url, stream=True, allow_redirects=True, timeout=30, headers=HEADERS)
                if r.status_code == 403:
                    self.root.after(0, lambda: messagebox.showinfo("Info", f"Server blocked auto-download.\nOpening browser..."))
                    webbrowser.open(url)
                    return
                r.raise_for_status()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showinfo("Net Error", f"Cannot download.\nOpening browser..."))
                webbrowser.open(url)
                return

            total_size = int(r.headers.get('content-length', 0))
            
            if not custom_save_path:
                parsed_url = urlparse(r.url)
                filename = unquote(os.path.basename(parsed_url.path))
                if not filename or "." not in filename: 
                    if "Content-Disposition" in r.headers:
                        import re
                        fname = re.findall("filename=\"?([^\";]+)\"?", r.headers["Content-Disposition"])
                        if fname: filename = fname[0]
                    else:
                        filename = f"{name.replace(' ', '_')}.zip" 

                is_zip = filename.lower().endswith(".zip")
                is_nro = filename.lower().endswith(".nro")
                is_ovl = filename.lower().endswith(".ovl")

                if is_nro: save_path = os.path.join(root_path, "switch", filename)
                elif is_ovl: save_path = os.path.join(root_path, "switch", ".overlays", filename)
                elif is_zip: save_path = os.path.join(root_path, "temp_download.zip")
                else: save_path = os.path.join(root_path, filename)

                if not os.path.exists(os.path.dirname(save_path)): os.makedirs(os.path.dirname(save_path))
            else:
                is_zip = save_path.lower().endswith(".zip")
                root_path = os.path.dirname(save_path)

            downloaded = 0
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if self.cancel_flag:
                        f.close()
                        try: os.remove(save_path)
                        except: pass
                        self.root.after(0, lambda: self.status_label.config(text="Cancelled", fg=COLOR_WARNING))
                        return
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        self.progress_var.set((downloaded / total_size) * 100)

            msg = ""
            if custom_save_path:
                msg = f"Downloaded: {os.path.basename(save_path)}"
                if auto_run:
                    self.root.after(0, lambda: self.status_label.config(text=f"Opening installer...", fg=COLOR_SUCCESS))
                    try:
                        os.startfile(save_path)
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Error", f"Cannot open: {e}"))
            elif is_zip:
                if "emuiibo" in name.lower():
                    self.root.after(0, lambda: self.status_label.config(text=f"Installing emuiibo...", fg=COLOR_WARNING))
                    try:
                        with zipfile.ZipFile(save_path, 'r') as z:
                            temp_extract = os.path.join(root_path, "temp_emuiibo")
                            z.extractall(temp_extract)
                            sdout_path = os.path.join(temp_extract, "SdOut")
                            if os.path.exists(sdout_path):
                                self.copy_tree_custom(sdout_path, root_path)
                                msg = "Installed emuiibo (SdOut)."
                            else:
                                self.copy_tree_custom(temp_extract, root_path)
                                msg = "Installed emuiibo."
                            shutil.rmtree(temp_extract)
                        os.remove(save_path)
                    except Exception as e: msg = f"Error: {e}"
                else:
                    self.root.after(0, lambda: self.status_label.config(text=f"Extracting...", fg=COLOR_WARNING))
                    try:
                        with zipfile.ZipFile(save_path, 'r') as z: z.extractall(root_path)
                        os.remove(save_path)
                        msg = f"Extracted {name}"
                    except zipfile.BadZipFile:
                        webbrowser.open(url)
                        return
            else: msg = f"Downloaded {os.path.basename(save_path)}."

            self.root.after(0, lambda: self.status_label.config(text=f"Success: {name}", fg=COLOR_SUCCESS))
            
            if not is_batch and not silent_success:
                 success_msg = UI_TEXT[self.lang_code]["msg_dl_success"] + name
                 self.root.after(0, lambda: messagebox.showinfo("Success", success_msg))

        except Exception as e:
            if not self.cancel_flag:
                self.root.after(0, lambda: self.status_label.config(text="Error!", fg="red"))
                messagebox.showerror("Error", f"Detail: {str(e)}")

    def install_local_zip_generic(self, label_name):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        
        file_path = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.zip *.rar *.7z")])
        
        if file_path: threading.Thread(target=self.extract_simple, args=(file_path, root_path, label_name), daemon=True).start()
    
    def install_firmware_local(self):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        file_path = filedialog.askopenfilename(filetypes=[("Zip", "*.zip")])
        if file_path:
            dest = os.path.join(root_path, "firmware")
            if not os.path.exists(dest): os.makedirs(dest)
            threading.Thread(target=self.extract_simple, args=(file_path, dest, "Firmware"), daemon=True).start()

    def extract_simple(self, file_path, target_dir, label):
        try:
            self.root.after(0, lambda: self.status_label.config(text=f"Installing {label}...", fg=COLOR_WARNING))
            
            extracted_ok = False
            f_lower = file_path.lower()

            if f_lower.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as z: z.extractall(target_dir)
                extracted_ok = True

            elif f_lower.endswith((".7z", ".rar")):
                extracted_ok = self.extract_archive_external(file_path, target_dir)
                
                if not extracted_ok:
                    if f_lower.endswith(".7z"):
                        try:
                            import py7zr
                            with py7zr.SevenZipFile(file_path, mode='r') as z: z.extractall(path=target_dir)
                            extracted_ok = True
                        except: pass
                    elif f_lower.endswith(".rar"):
                        try:
                            import rarfile
                            r = rarfile.RarFile(file_path)
                            r.extractall(target_dir)
                            extracted_ok = True
                        except: pass

            if not extracted_ok:
                raise Exception("Cannot extract. Please install WinRAR or 7-Zip!")

            self.root.after(0, lambda: self.status_label.config(text=f"Done {label}", fg=COLOR_SUCCESS))
            
            if label == "Firmware":
                 msg = UI_TEXT[self.lang_code]["msg_fw_done"]
                 messagebox.showinfo("Attention", msg)
            else:
                 messagebox.showinfo("Success", f"Installed {label}")

        except Exception as e: messagebox.showerror("Error", str(e))
    
    def install_linkalho_special(self):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        file_path = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.zip *.rar *.7z")])
        if file_path: 
            threading.Thread(target=self.process_linkalho_task, args=(file_path, root_path), daemon=True).start()

    def process_linkalho_task(self, source_file, root_path):
        try:
            self.root.after(0, lambda: self.status_label.config(text="Processing Linkalho...", fg=COLOR_WARNING))
            
            temp_outer = os.path.join(root_path, "temp_linkalho_outer")
            temp_inner = os.path.join(root_path, "temp_linkalho_inner")
            if os.path.exists(temp_outer): shutil.rmtree(temp_outer)
            if os.path.exists(temp_inner): shutil.rmtree(temp_inner)
            os.makedirs(temp_outer)
            os.makedirs(temp_inner)

            if not self.helper_extract_any(source_file, temp_outer):
                 raise Exception("Cannot extract outer archive.")

            inner_archive = None
            for root, dirs, files in os.walk(temp_outer):
                for f in files:
                    if "linkalho" in f.lower() and f.lower().endswith((".zip", ".rar", ".7z")):
                        inner_archive = os.path.join(root, f)
                        break
                if inner_archive: break
            
            if not inner_archive:
                raise Exception("Inner Linkalho archive not found.")

            if not self.helper_extract_any(inner_archive, temp_inner):
                 raise Exception("Cannot extract inner archive.")

            nro_found = False
            switch_dir = os.path.join(root_path, "switch")
            if not os.path.exists(switch_dir): os.makedirs(switch_dir)

            for root, dirs, files in os.walk(temp_inner):
                for f in files:
                    if f.lower().endswith(".nro"):
                        src_nro = os.path.join(root, f)
                        shutil.copy2(src_nro, switch_dir)
                        nro_found = True
            
            try:
                shutil.rmtree(temp_outer)
                shutil.rmtree(temp_inner)
            except: pass

            if nro_found:
                self.root.after(0, lambda: self.status_label.config(text="Installed Linkalho!", fg=COLOR_SUCCESS))
                messagebox.showinfo("Success", "Installed Linkalho (.nro) to /switch/ folder.")
            else:
                raise Exception("No .nro file found.")

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error", fg="red"))
            messagebox.showerror("Error", str(e))

    def helper_extract_any(self, file_path, target_dir):
        f_lower = file_path.lower()
        extracted = False
        
        if self.extract_archive_external(file_path, target_dir):
            return True

        if f_lower.endswith(".zip"):
            try:
                with zipfile.ZipFile(file_path, 'r') as z: z.extractall(target_dir)
                extracted = True
            except: pass
        elif f_lower.endswith(".7z"):
            try:
                import py7zr
                with py7zr.SevenZipFile(file_path, mode='r') as z: z.extractall(path=target_dir)
                extracted = True
            except: pass
        elif f_lower.endswith(".rar"):
            try:
                import rarfile
                r = rarfile.RarFile(file_path)
                r.extractall(target_dir)
                extracted = True
            except: pass
            
        return extracted

    def install_translation_pack(self):
        root_path = self.dest_path.get()
        text_db = UI_TEXT[self.lang_code]
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        
        win = tk.Toplevel(self.root)
        win.title(text_db.get("trans_title", "Install Translation"))
        
        win.geometry("500x220") 
        win.configure(bg=COLOR_CARD)
        
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 110
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text=text_db.get("trans_msg_1"), bg=COLOR_CARD, fg="white", font=("Segoe UI", 11)).pack(pady=(20, 5))
        
        tk.Label(win, text=text_db.get("trans_msg_2"), 
                 bg=COLOR_CARD, fg="#aaaaaa", font=("Segoe UI", 9, "italic"), wraplength=480).pack(pady=(0, 10))
        
        btn_frame = tk.Frame(win, bg=COLOR_CARD)
        btn_frame.pack(pady=10)

        def on_zip():
            win.destroy()
            f = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.zip *.rar *.7z")])
            if f: threading.Thread(target=self.process_translation_task, args=(f, root_path, "file"), daemon=True).start()
            
        def on_folder():
            win.destroy()
            d = filedialog.askdirectory()
            if d: threading.Thread(target=self.process_translation_task, args=(d, root_path, "folder"), daemon=True).start()

        ttk.Button(btn_frame, text=text_db.get("trans_btn_zip"), command=on_zip).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=text_db.get("trans_btn_folder"), command=on_folder).pack(side="left", padx=10)

    def extract_archive_external(self, source_file, dest_dir):
        """Use WinRAR or 7-Zip"""
        seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
        winrar_path = r"C:\Program Files\WinRAR\WinRAR.exe"
        cmd = None
        if os.path.exists(seven_zip_path):
            cmd = [seven_zip_path, "x", source_file, f"-o{dest_dir}", "-y"]
        elif os.path.exists(winrar_path):
            cmd = [winrar_path, "x", "-ibck", source_file, dest_dir + "\\"]
        
        if cmd:
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.run(cmd, check=True, startupinfo=startupinfo)
                return True
            except subprocess.CalledProcessError as e:
                print(f"External extract failed: {e}")
                return False
        return False

    def process_translation_task(self, source, root_path, source_type):
        try:
            self.root.after(0, lambda: self.status_label.config(text="Processing Translation...", fg=COLOR_WARNING))
            
            def is_game_id_strict(name):
                return bool(re.match(r'^0100[0-9A-Fa-f]{12}$', name))

            input_name = os.path.basename(os.path.normpath(source))
            if source_type == "file":
                input_name = os.path.splitext(input_name)[0]

            search_path = source
            temp_dir = ""

            if source_type == "file":
                temp_dir = os.path.join(root_path, "temp_translation_extract")
                if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
                os.makedirs(temp_dir)

                extracted_ok = False
                if source.lower().endswith((".7z", ".rar")):
                    extracted_ok = self.extract_archive_external(source, temp_dir)
                
                if not extracted_ok:
                    if source.lower().endswith(".zip"):
                        with zipfile.ZipFile(source, 'r') as z: z.extractall(temp_dir)
                    elif source.lower().endswith(".7z"):
                        import py7zr
                        with py7zr.SevenZipFile(source, mode='r') as z: z.extractall(path=temp_dir)
                    elif source.lower().endswith(".rar"):
                        import rarfile
                        r = rarfile.RarFile(source)
                        r.extractall(temp_dir)
                search_path = temp_dir

            contents_dir = os.path.join(root_path, "atmosphere", "contents")
            if not os.path.exists(contents_dir): os.makedirs(contents_dir)
            
            found_count = 0

            if is_game_id_strict(input_name):
                dest_game_path = os.path.join(contents_dir, input_name)
                
                if source_type == "folder":
                    if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                    shutil.copytree(source, dest_game_path, dirs_exist_ok=True)
                    found_count = 1
                else: 
                    nested_path = os.path.join(temp_dir, input_name)
                    if os.path.exists(nested_path) and os.path.isdir(nested_path):
                        if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                        shutil.copytree(nested_path, dest_game_path, dirs_exist_ok=True)
                        found_count = 1
                    else:
                        if not os.path.exists(dest_game_path): os.makedirs(dest_game_path)
                        self.copy_tree_custom(temp_dir, dest_game_path)
                        found_count = 1
            else:
                for root, dirs, files in os.walk(search_path):
                    for dirname in dirs[:]:
                        if is_game_id_strict(dirname):
                            src_game_path = os.path.join(root, dirname)
                            dest_game_path = os.path.join(contents_dir, dirname)
                            if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                            shutil.copytree(src_game_path, dest_game_path, dirs_exist_ok=True)
                            found_count += 1
                            dirs.remove(dirname)

            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            if found_count > 0:
                self.root.after(0, lambda: self.status_label.config(text=f"Installed {found_count} translations!", fg=COLOR_SUCCESS))
                messagebox.showinfo("Success", f"Đã cài đặt thành công {found_count} gói Việt Hóa.\nHãy vào game để kiểm tra!")
            else:
                self.root.after(0, lambda: self.status_label.config(text="No translation found.", fg=COLOR_WARNING))
                messagebox.showwarning("Failed", "Không tìm thấy nội dung Việt Hóa hợp lệ.\nHệ thống tự động quét nhưng không thấy thư mục ID Game (0100...) nào.")

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error", fg="red"))
            messagebox.showerror("Error", str(e))

    def copy_tree_custom(self, src, dst):
        if not os.path.exists(dst): os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s): self.copy_tree_custom(s, d)
            else: shutil.copy2(s, d)

    def run_fix_task(self, fix_type):
        root_path = self.dest_path.get()
        text_db = UI_TEXT[self.lang_code]
        if not os.path.exists(root_path):
            messagebox.showerror("Error", "Select SD Root first!")
            return

        if fix_type == "ACTION_FIX_REINSTALL_PACK":
            msg = "Reinstalling AIO Pack."
            messagebox.showinfo("Reinstall Pack", msg)
            self.canvas.yview_moveto(0) 
            return

        # --- Hard Reset Logic ---
        if fix_type == "ACTION_FIX_HARD_RESET":
            warn_msg = text_db.get("hard_reset_warn")
            if not messagebox.askyesno("Confirm Hard Reset", warn_msg, icon='warning'):
                return
            
            try:
                self.root.after(0, lambda: self.status_label.config(text="HARD RESET: Deleting files...", fg=COLOR_DANGER))
                items = os.listdir(root_path)
                deleted_count = 0
                for item in items:
                    if "emummc" in item.lower(): continue 
                    
                    full_path = os.path.join(root_path, item)
                    try:
                        if os.path.isdir(full_path): shutil.rmtree(full_path)
                        else: os.remove(full_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Cannot delete {item}: {e}")
                
                msg_done = f"Deleted {deleted_count} items. Installing My Pack..."
                self.root.after(0, lambda: self.status_label.config(text=msg_done, fg=COLOR_SUCCESS))
                
                my_pack_url = "https://rebrand.ly/mypack"
                webbrowser.open(my_pack_url)
                
                msg_next = "SD Card Cleaned. Please pick the My Pack zip to install."
                if self.lang_code == "VI":
                    msg_next = "Đã dọn sạch thẻ nhớ. Vui lòng chọn file My Pack vừa tải để cài đặt."

                messagebox.showinfo("Hard Reset Step 1 Done", msg_next)
                self.install_local_zip_generic("My Pack (Clean Install)")
            except Exception as e:
                messagebox.showerror("Reset Error", str(e))
            return

        # --- Soft Fixes ---
        if not messagebox.askyesno("Confirm", text_db.get("fix_wipe_warn") if fix_type == "ACTION_FIX_DELETE_ALL_CONTENTS" else "Modify/Delete files on SD card?"):
            return

        try:
            msg = "Done!"
            atm_contents = os.path.join(root_path, "atmosphere", "contents")
            
            if fix_type == "ACTION_FIX_THEMES":
                theme_id = "0100000000001000"
                target = os.path.join(atm_contents, theme_id)
                if os.path.exists(target):
                    shutil.rmtree(target)
                    msg = text_db.get("fix_theme_ok")
                else:
                    msg = text_db.get("fix_theme_fail")

            elif fix_type == "ACTION_FIX_DELETE_ALL_CONTENTS":
                if os.path.exists(atm_contents):
                    shutil.rmtree(atm_contents)
                    os.makedirs(atm_contents)
                    msg = text_db.get("fix_wipe_ok")
                else:
                    os.makedirs(atm_contents)
                    msg = text_db.get("fix_wipe_ok")

            elif fix_type == "ACTION_FIX_MODULES":
                common_modules = [
                    "420000000007E51A", "01000000000000352", "00FF0000636C6BFF", 
                    "0000000000534C56", "420000000000000B", "010000000000000D"
                ]
                deleted_count = 0
                if os.path.exists(atm_contents):
                    for item in os.listdir(atm_contents):
                        if item.upper() in common_modules or item in common_modules:
                            shutil.rmtree(os.path.join(atm_contents, item))
                            deleted_count += 1
                msg = text_db.get("fix_mod_ok").format(count=deleted_count)

            elif fix_type == "ACTION_FIX_CHEATS":
                deleted_count = 0
                if os.path.exists(atm_contents):
                    for game_id in os.listdir(atm_contents):
                        cheat_path = os.path.join(atm_contents, game_id, "cheats")
                        if os.path.exists(cheat_path):
                            shutil.rmtree(cheat_path)
                            deleted_count += 1
                msg = text_db.get("fix_cheat_ok").format(count=deleted_count)

            elif fix_type == "ACTION_FIX_MAC_JUNK":
                deleted_count = 0
                for root, dirs, files in os.walk(root_path):
                    for file in files:
                        if file.startswith("._") or file == ".DS_Store":
                            try:
                                os.remove(os.path.join(root, file))
                                deleted_count += 1
                            except: pass
                msg = text_db.get("fix_junk_ok").format(count=deleted_count)

            messagebox.showinfo("Result", msg)

        except Exception as e:
            messagebox.showerror("Fix Error", str(e))

    # --- FTP Features ---
    def open_ftp_window(self):
        text_db = UI_TEXT[self.lang_code]
        win = tk.Toplevel(self.root)
        win.title(text_db.get("ftp_title"))
        win.geometry("500x500")
        win.configure(bg=COLOR_CARD)
        
        # Center Window
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 175
        win.geometry(f"+{x}+{y}")
        
        # Header
        tk.Label(win, text=text_db.get("ftp_title").upper(), font=("Segoe UI", 12, "bold"), 
                 bg=COLOR_CARD, fg=COLOR_GOLD).pack(pady=10)

        # Help Tip
        tk.Label(win, text=text_db.get("ftp_tip"), bg=COLOR_CARD, fg="#cccccc", font=("Segoe UI", 9, "italic"), justify="center").pack(pady=5)

        # Input Frame
        input_frame = tk.Frame(win, bg=COLOR_CARD)
        input_frame.pack(pady=10)

        # IP Input
        tk.Label(input_frame, text=text_db.get("ftp_lbl_ip"), bg=COLOR_CARD, fg="white").grid(row=0, column=0, padx=5, sticky="e")
        ip_entry = tk.Entry(input_frame, font=("Consolas", 11), width=15)
        saved_ip = self.load_ftp_ip()
        ip_entry.insert(0, saved_ip)
        ip_entry.grid(row=0, column=1, padx=5)

        # Port Input
        tk.Label(input_frame, text=text_db.get("ftp_lbl_port"), bg=COLOR_CARD, fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        port_entry = tk.Entry(input_frame, font=("Consolas", 11), width=6)
        port_entry.insert(0, "5000")
        port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Status Label inside Window
        lbl_ftp_status = tk.Label(win, text=text_db.get("ftp_status_idle"), bg=COLOR_CARD, fg=COLOR_INFO, font=("Segoe UI", 9))
        lbl_ftp_status.pack(pady=5)
        
        # Progress Bar inside Window
        ftp_progress = ttk.Progressbar(win, orient="horizontal", length=400, mode="determinate")
        ftp_progress.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(win, bg=COLOR_CARD)
        btn_frame.pack(pady=15)
            

        def run_explorer():
            ip = ip_entry.get().strip()
            port = port_entry.get().strip()
            if not ip: return messagebox.showwarning("IP Error", "Please enter IP Address")
            self.open_ftp_explorer(ip, port)

        def run_install():
            ip = ip_entry.get().strip()
            port = port_entry.get().strip()
            if not ip: return messagebox.showwarning("IP Error", "Please enter IP Address")
            self.save_ftp_ip(ip)
            
            file_types = [
                ("All Supported", "*.nsp *.xci *.nsz *.xcz *.zip *.rar *.7z"),
                ("Game Files", "*.nsp *.xci *.nsz *.xcz"),
                ("Archives", "*.zip *.rar *.7z")
            ]
            files = filedialog.askopenfilenames(filetypes=file_types)
            if files:
                 threading.Thread(target=self.ftp_install_game_thread, args=(ip, port, files, lbl_ftp_status, ftp_progress), daemon=True).start()

        def run_upload_folder():
            ip = ip_entry.get().strip()
            port = port_entry.get().strip()
            if not ip: return messagebox.showwarning("IP Error", "Please enter IP Address")
            self.save_ftp_ip(ip)
            
            folder_path = filedialog.askdirectory(title="Select Folder to Upload")
            if folder_path:
                threading.Thread(target=self.ftp_upload_folder_thread, args=(ip, port, folder_path, lbl_ftp_status, ftp_progress), daemon=True).start()

        # --- GIAO DIỆN MỚI: CHIA LÀM 2 HÀNG ---
        # Hàng 1: Explorer + Install Game
        row1 = tk.Frame(btn_frame, bg=COLOR_CARD)
        row1.pack(side="top", pady=5)
        
        ttk.Button(row1, text=text_db.get("ftp_btn_explorer"), style="Smart.TButton", command=run_explorer).pack(side="left", padx=5)
        
        ttk.Button(row1, text=text_db.get("ftp_btn_install"), style="Accent.TButton", command=run_install).pack(side="left", padx=5)

        # Hàng 2: Upload Folder (Nút to nằm dưới)
        row2 = tk.Frame(btn_frame, bg=COLOR_CARD)
        row2.pack(side="top", pady=5)
        
        ttk.Button(row2, text=text_db.get("ftp_btn_folder", "📂 Upload Folder"), style="FTP.TButton", width=35, command=run_upload_folder).pack(side="left", padx=5)

    def open_ftp_explorer(self, ip, port):
        url = f"ftp://{ip}:{port}/"
        try:
            if sys.platform == 'win32':
                subprocess.Popen(['explorer.exe', url])
            else:
                webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open Explorer: {e}")

        # Activate Keep-Alive
        if not self.keep_alive_running:
            threading.Thread(target=self.ftp_keep_alive_loop, args=(ip, port), daemon=True).start()
            self.status_label.config(text="FTP Keep-Alive: ON", fg=COLOR_SUCCESS)

    def ftp_install_game_thread(self, ip, port, file_paths, lbl_status, pbar):
        text_db = UI_TEXT[self.lang_code]
        temp_extract_dir = os.path.join(os.getcwd(), "temp_ftp_game_extract")
        
        try:
            lbl_status.config(text=text_db.get("ftp_status_connecting"), fg=COLOR_WARNING)
            
            ftp = ftplib.FTP()
            ftp.connect(ip, int(port), timeout=None) 
            ftp.login() 
            ftp.set_pasv(True)

            try:
                ftp.cwd('MicroSD Install')
            except:
                pass
            
            def upload_single_file(path_to_file):
                filename = os.path.basename(path_to_file)
                filesize = os.path.getsize(path_to_file)
                
                lbl_status.config(text=text_db.get("ftp_status_uploading").format(filename=filename, percent="0"), fg=COLOR_ACCENT)
                pbar['value'] = 0
                
                uploaded_bytes = 0
                
                def callback(data):
                    nonlocal uploaded_bytes
                    uploaded_bytes += len(data)
                    percent = int((uploaded_bytes / filesize) * 100)
                    pbar['value'] = percent
                    
                    if percent >= 100:
                         lbl_status.config(text=f"⏳ Finalizing (Writing to SD)...", fg=COLOR_GOLD)
                    elif percent % 5 == 0: 
                         lbl_status.config(text=text_db.get("ftp_status_uploading").format(filename=filename, percent=str(percent)))

                try:
                    with open(path_to_file, 'rb') as f:
                        ftp.storbinary(f'STOR {filename}', f, 131072, callback)
                    
                    lbl_status.config(text=text_db.get("ftp_status_done").format(filename=filename), fg=COLOR_SUCCESS)

                except ftplib.all_errors as e:
                    err_msg = str(e)
                    # Ignore 426 as it implies successful install/close by DBI
                    if "426" in err_msg or "Connection closed" in err_msg:
                        lbl_status.config(text=text_db.get("ftp_status_done").format(filename=filename), fg=COLOR_SUCCESS)
                        pbar['value'] = 100
                    else:
                        raise e 
                
                time.sleep(0.5)

            total_processed = 0

            for file_path in file_paths:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext in ['.zip', '.rar', '.7z']:
                    lbl_status.config(text=f"Extracting: {os.path.basename(file_path)}...", fg=COLOR_INFO)
                    if os.path.exists(temp_extract_dir): shutil.rmtree(temp_extract_dir)
                    os.makedirs(temp_extract_dir)
                    
                    if self.helper_extract_any(file_path, temp_extract_dir):
                        found_game_in_zip = False
                        for root, dirs, files in os.walk(temp_extract_dir):
                            for f in files:
                                if f.lower().endswith(('.nsp', '.xci', '.nsz', '.xcz')):
                                    full_path = os.path.join(root, f)
                                    upload_single_file(full_path)
                                    total_processed += 1
                                    found_game_in_zip = True
                        if not found_game_in_zip: print(f"No game files found in {file_path}")
                    else:
                        lbl_status.config(text=f"Extraction Error: {os.path.basename(file_path)}", fg=COLOR_DANGER)
                        time.sleep(2)
                    if os.path.exists(temp_extract_dir): shutil.rmtree(temp_extract_dir)

                elif ext in ['.nsp', '.xci', '.nsz', '.xcz']:
                    upload_single_file(file_path)
                    total_processed += 1

            ftp.quit()
            
            if os.path.exists(temp_extract_dir): shutil.rmtree(temp_extract_dir)

            msg = f"Finished!\nInstalled {total_processed} files."
            messagebox.showinfo("FTP Finished", msg)
            lbl_status.config(text=text_db.get("ftp_status_idle"), fg=COLOR_INFO)
            pbar['value'] = 0

        except Exception as e:
            if os.path.exists(temp_extract_dir): shutil.rmtree(temp_extract_dir)
            lbl_status.config(text=text_db.get("ftp_error").format(error=str(e)), fg=COLOR_DANGER)
            messagebox.showerror("FTP Error", f"Error: {str(e)}")

    def ftp_upload_folder_thread(self, ip, port, local_folder_path, lbl_status, pbar):
        # 1. DỌN DẸP
        self.keep_alive_running = False 
        import gc
        gc.collect()
        time.sleep(1)
        
        text_db = UI_TEXT[self.lang_code]
        folder_name = os.path.basename(local_folder_path)
        
        # 2. QUÉT VÀ SẮP XẾP FILE
        try: lbl_status.config(text="Đang quét file...", fg=COLOR_INFO)
        except: return

        upload_queue = []
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_path = os.path.join(root, file)
                try: f_size = os.path.getsize(local_path)
                except: f_size = 0
                
                relative_path = os.path.relpath(local_path, local_folder_path)
                remote_path = f"{folder_name}/{relative_path}".replace("\\", "/")
                upload_queue.append((local_path, remote_path, f_size))

        total_files = len(upload_queue)
        if total_files == 0: return

        # Sắp xếp file bé -> lớn (để file hệ thống chạy trước)
        upload_queue.sort(key=lambda x: x[2])

        # 3. HÀM UPLOAD ĐƠN LẺ (CÓ TRICK ĐỔI TÊN)
        def upload_one_file_session(local_file, remote_file_path):
            ftp = ftplib.FTP()
            try:
                # Timeout: Kết nối 20s, truyền dữ liệu 120s (chống disconnect)
                ftp.connect(ip, int(port), timeout=20)
                ftp.login()
                ftp.set_pasv(True)
                ftp.sock.settimeout(120.0) 
                
                remote_dir = os.path.dirname(remote_file_path)
                filename = os.path.basename(remote_file_path)
                
                # Tạo folder cha (Làm nhanh, bỏ qua lỗi nếu đã có)
                parts = remote_dir.split('/')
                current = ""
                for part in parts:
                    if not part: continue
                    current += f"/{part}"
                    try: ftp.mkd(current)
                    except: pass
                
                try: ftp.cwd(f"/{remote_dir}")
                except: pass
                
                # Check Resume
                local_size = os.path.getsize(local_file)
                try:
                    remote_size = ftp.size(filename)
                    if remote_size == local_size:
                        ftp.quit()
                        return "SKIPPED"
                except: pass

                # --- CHIẾN THUẬT ĐÁNH LỪA (RENAME TRICK) ---
                # Nếu là file .cnmt.nca, đổi tên thành .tmp_bypass để upload
                # Switch sẽ tưởng là rác và KHÔNG dùng CPU để xử lý -> Nhanh & Mượt
                use_trick = "cnmt.nca" in filename.lower()
                
                upload_filename = filename
                if use_trick:
                    upload_filename = filename + ".tmp_bypass"

                # Upload file (với tên thật hoặc tên giả)
                with open(local_file, 'rb') as f:
                    ftp.storbinary(f'STOR {upload_filename}', f, blocksize=32768)
                
                # Nếu nãy dùng tên giả, giờ đổi lại tên thật (Chỉ tốn 0.01s)
                if use_trick:
                    try:
                        # Xóa file gốc nếu tồn tại (để rename đè lên)
                        try: ftp.delete(filename)
                        except: pass
                        
                        # Đổi tên: .tmp_bypass -> .cnmt.nca
                        ftp.rename(upload_filename, filename)
                    except Exception as e:
                        print(f"Lỗi đổi tên: {e}")
                        raise e # Lỗi đổi tên coi như lỗi upload

                try: ftp.quit()
                except: ftp.close()
                return "UPLOADED"

            except Exception as e:
                try: ftp.close()
                except: pass
                raise e 

        # 4. VÒNG LẶP CHÍNH
        processed_count = 0
        success_count = 0
        
        for local, remote, size in upload_queue:
            # Kiểm tra cửa sổ còn sống không
            try: pbar.winfo_exists()
            except tk.TclError: return

            filename_only = os.path.basename(remote)
            size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
            
            retry_max = 3
            
            for attempt in range(retry_max):
                try:
                    lbl_status.config(text=f"Up ({processed_count + 1}/{total_files}): {filename_only} ({size_str})", fg=COLOR_ACCENT)
                    try: pbar.update()
                    except: pass
                    
                    result = upload_one_file_session(local, remote)
                    
                    if result == "SKIPPED":
                        try: lbl_status.config(text=f"Đã có: {filename_only}", fg=COLOR_INFO)
                        except: pass
                        # Skip thì chạy cực nhanh (sleep cực ngắn)
                        time.sleep(0.01) 
                    else:
                        # Upload mới thành công
                        success_count += 1
                        # Đã dùng trick rename nên không cần nghỉ 5s nữa
                        # Nghỉ nhẹ 1.5s là đủ an toàn
                        time.sleep(1.5) 
                    
                    break 
                    
                except Exception as e:
                    print(f"Lỗi {filename_only}: {e}")
                    try: lbl_status.config(text=f"Lỗi mạng. Thử lại {attempt+1}...", fg=COLOR_DANGER)
                    except: pass
                    # Nếu lỗi thật sự thì nghỉ 3s để hồi mạng
                    time.sleep(3) 
            
            processed_count += 1
            percent = int((processed_count / total_files) * 100)
            try: pbar['value'] = percent
            except: return

        try:
            lbl_status.config(text=f"✅ Hoàn tất! (Mới: {success_count})", fg=COLOR_SUCCESS)
            messagebox.showinfo("Thành công", f"Đã chép xong {total_files} file!")
            pbar['value'] = 0
        except: pass
if __name__ == "__main__":
    root = tk.Tk()
    app = SwitchToolApp(root)
    root.mainloop()