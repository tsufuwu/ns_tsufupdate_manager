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
from tkinter import ttk, filedialog, messagebox, scrolledtext
from urllib.parse import urlparse, unquote
from PIL import Image, ImageTk, ImageSequence

# --- HÀM QUAN TRỌNG: TÌM ĐƯỜNG DẪN TÀI NGUYÊN (FIX LỖI MẤT ICON/GIF) ---
def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối tới tài nguyên, dùng cho cả Dev và PyInstaller """
    try:
        # PyInstaller tạo ra thư mục tạm này
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CẤU HÌNH PHẦN MỀM & UPDATE ---
APP_VERSION = "1.0.0"  # Đã sửa về 1.0.0 theo yêu cầu
GITHUB_REPO = "tsufuwu/ns_tsufupdate_manager" 

# --- CẤU HÌNH MÀU SẮC ---
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

FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_TITLE = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

# --- TỪ ĐIỂN UI ---
UI_TEXT = {
    "VI": {
        "title": "SWITCH TSUFUPDATE MANAGER",
        "credit": "Dev by Tsufu/Phú Trần Trung Lê",
        "credit2": "Chân thành cảm ơn Group Cộng Đồng Nintendo Switch hắc ám (Admin Phong Pham)\nvì các dữ liệu cung cấp cho phần mềm này",
        "path_label": "Thẻ nhớ (Root):",
        "btn_browse": "📁 Chọn",
        "btn_detect": "🔄 Auto",
        "btn_open": "📂 Mở thư mục",
        "btn_dl_all": "⬇️ Tải tất cả mục này",
        "btn_donate": "☕ Donate ủng hộ Dev",
        "btn_update_soft": "🔄 Cập nhật phần mềm",
        "btn_guide": "📖 Hướng dẫn sử dụng",
        "status_ready": "Sẵn sàng",
        "status_detect_ok": "Đã phát hiện thẻ nhớ/USB tại: ",
        "status_detect_fail": "Không tìm thấy ổ đĩa rời. Vui lòng chọn thủ công.",
        "msg_confirm_dl_all": "Bạn có muốn tự động tải tất cả ứng dụng trong mục:\n'{category}' không?\n\n(Lưu ý: Sẽ bỏ qua các file dành cho PC và cần hai bước như Sigpatch, Linkalho)",
        "cat_file": "🔥 FILE HACK & CÔNG CỤ PC",
        "cat_sysmod": "🛠️ SYSMOD HỮU ÍCH (Cần Restart)",
        "cat_homebrew": "🎮 HOMEBREW (Ứng dụng)",
        "cat_misc": "⚙️ LINH TINH (Firmware/Cheat/Save)",
        "cat_fix": "🚑 FIX LỖI NHANH (Sự cố thường gặp)",
        "cat_guide": "📚 CÁC HƯỚNG DẪN ",
        "cat_game_source": "👾 NGUỒN DOWNLOAD GAME",
        "msg_fw_done": "Đã chép file Firmware thành công vào thẻ nhớ, nhưng chưa xong, bạn cần xem hướng dẫn update Firmware ở nút bên cạnh để hoàn thành. Nhớ cập nhật gói my pack ở đầu phần mềm"
    },
    "EN": {
        "title": "SWITCH TSUFUPDATE MANAGER",
        "credit": "Dev by Tsufu/Phu Tran Trung Le",
        "credit2": "Special thanks to Nintendo Switch Hacking Community Group (Admin Phong Pham)\nfor providing data for this software",
        "path_label": "SD Card (Root):",
        "btn_browse": "📁 Browse",
        "btn_detect": "🔄 Auto Detect",
        "btn_open": "📂 Open Folder",
        "btn_dl_all": "⬇️ Download All",
        "btn_donate": "☕ Donate",
        "btn_update_soft": "🔄 Update App",
        "btn_guide": "📖 User Manual",
        "status_ready": "Ready",
        "status_detect_ok": "Detected SD Card/USB at: ",
        "status_detect_fail": "Removable drive not found. Please select manually.",
        "msg_confirm_dl_all": "Do you want to automatically download all apps in:\n'{category}'?\n\n(Note: PC files will be skipped)",
        "cat_file": "🔥 HACK FILES & PC TOOLS",
        "cat_sysmod": "🛠️ USEFUL SYSMODS (Restart Required)",
        "cat_homebrew": "🎮 HOMEBREW (Apps)",
        "cat_misc": "⚙️ MISC (Firmware/Cheat/Save)",
        "cat_fix": "🚑 QUICK FIX (Common Issues)",
        "cat_guide": "📚 GUIDES",
        "cat_game_source": "👾 GAME DOWNLOAD SOURCES",
        "msg_fw_done": "Firmware files copied successfully to SD card. You need to use Daybreak to apply the update. Remember to update My Pack first."
    }
}

DATA_VI = {
    "🔥 FILE HACK & CÔNG CỤ PC": [
        {
            "name": "Gói hack tổng hợp My Pack", 
            "desc": "Bộ công cụ hack Switch được tùy chỉnh riêng (AIO). Bao gồm Atmosphere, Hekate và các sysmod cần thiết nhất để chạy ngay lập tức.",
            "urls": {
                "Bước 1. Tải về file": "https://rebrand.ly/mypack",
                "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"
            }
        }, 
        {
            "name": "Sigpatches (Hỗ trợ game thuốc)", 
            "desc": "Signature Patches: Thành phần quan trọng nhất để chơi game lậu. Giúp bỏ qua bước kiểm tra chữ ký số của Nintendo, cho phép cài và chạy file NSP/XCI không bản quyền.",
            "urls": {
                "Bước 1. Tải về file": "https://gbatemp.net/attachments/hekate-ams-package3-sigpatches-1-10-1p-cfw-21-1-0_v0-zip.544098/",
                "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"
            }
        },
        {
            "name": "Hekate (Bootloader)", 
            "desc": "Trình khởi động đa năng. Dùng để Backup/Restore NAND (tránh brick máy), tạo Emunand (hệ điều hành ảo), phân vùng thẻ nhớ và khởi động vào CFW.",
            "urls": {"Tự động cài đặt": "https://github.com/CTCaer/hekate/releases/download/v6.4.2/hekate_ctcaer_6.4.2_Nyx_1.8.2.zip"}
        },
        {
            "name": "Atmosphere (CFW)", 
            "desc": "Hệ điều hành tùy chỉnh (Custom Firmware) phổ biến nhất cho Switch. Đây là nền tảng cốt lõi để chạy các ứng dụng Homebrew, Mod, và game lậu.",
            "urls": {"Tự động cài đặt": "https://github.com/Atmosphere-NX/Atmosphere/releases/download/1.10.1/atmosphere-1.10.1-master-21c0f75a2+hbl-2.4.5+hbmenu-3.6.1.zip"}
        },
        {
            "name": "TegraRcmGUI (Cài trên PC)", 
            "desc": "Phần mềm chạy trên máy tính Windows. Dùng để 'kích hack' (gửi Payload) vào Switch khi máy đang ở chế độ RCM (màn hình đen).",
            "urls": {"Tự động cài đặt (PC)": "ACTION_RUN_PC|https://github.com/eliboa/TegraRcmGUI/releases/download/2.6/TegraRcmGUI_v2.6_Installer.msi"}
        },
    ],
    "🛠️ SYSMOD HỮU ÍCH (Cần Restart)": [
        {
            "name": "Sys-patch", 
            "desc": "Module tự động vá lỗi hệ thống khi khởi động (fs, ldr, es). Giúp game chạy ổn định hơn, sửa lỗi khi Sigpatches chưa cập nhật kịp.",
            "urls": {
                "Bước 1. Tải về file": "https://gbatemp.net/download/sys-patch-sysmodule.39471/download",
                "Bước 2. Chọn file nén để tự động chép.": "ACTION_PICK_ZIP"
            }
        },
        {
            "name": "Tesla Menu (Overlay Menu)", 
            "desc": "Menu phủ màn hình (Overlay). Cho phép bật/tắt cheat, xem thông tin máy, ép xung... ngay khi đang chơi game bằng tổ hợp phím (L + Dpad Down + R3).",
            "urls": {"Tự động cài đặt (Combo)": "TESLA_ACTION"}
        },
        {
            "name": "Ultrahand (Overlay mạnh mẽ)", 
            "desc": "Một trình quản lý Overlay khác tương tự Tesla nhưng giao diện hiện đại hơn. Dùng để quản lý các plugin overlay như nghe nhạc, cheat, fps...kích hoạt bằng (ZL+ZR+DDOWN )",
            "urls": {"Tự động cài đặt (Combo)": "ULTRAHAND_ACTION"}
        },
        {
            "name": "Edizon Overlay (Cheat game)", 
            "desc": "Plugin hiển thị menu Cheat đè lên màn hình game. Giúp bạn tìm kiếm giá trị, bật/tắt mã bất tử, vô hạn tiền ngay lập tức mà không cần thoát game.",
            "urls": {"Tự động cài đặt": "https://github.com/proferabg/EdiZon-Overlay/releases/download/v1.0.14/ovlEdiZon.ovl", "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat#cach-3-dung-edizon-overlay"}
        },
        {
            "name": "Status Monitor (FPS/Pin/Nhiệt độ)", 
            "desc": "Công cụ giám sát phần cứng thời gian thực (Real-time). Hiển thị FPS, nhiệt độ CPU/GPU, tốc độ RAM, % Pin... ngay góc màn hình.",
            "urls": {"Tự động cài đặt": "https://github.com/masagrator/Status-Monitor-Overlay/releases/download/1.3.2/Status-Monitor-Overlay.zip"}
        },
        {
            "name": "emuiibo (Giả lập Amiibo)", 
            "desc": "Giả lập tượng Amiibo ảo. Cho phép nhận quà trong game (như Zelda, Splatoon) mà không cần mua tượng thật. Sử dụng cùng với Tesla Menu.",
            "urls": {"Tự động cài đặt": "https://github.com/XorTroll/emuiibo/releases/download/1.1.2/emuiibo.zip"}
        },
        {
            "name": "SYS-CLK (Ép xung)", 
            "desc": "Công cụ ép xung (Overclock) hoặc hạ xung an toàn. Giúp game nặng chạy mượt hơn (tăng FPS) hoặc tiết kiệm pin cho game nhẹ.",
            "urls": {"Tự động cài đặt": "https://github.com/retronx-team/sys-clk/releases/download/2.0.1/sys-clk-2.0.1-21fix.zip"}
        },
        {
            "name": "SysDVR (Stream hình ảnh qua USB)", 
            "desc": "Truyền hình ảnh và âm thanh từ Switch sang máy tính qua cáp USB hoặc Wifi. Dùng để quay video/stream game mà không cần Capture Card đắt tiền.",
            "urls": {"1. Tải cho Switch": "https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR.zip", "2. Client cho PC (7z)": "ACTION_SAVE_PC|https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR-Client-Windows-x64-with-framework.7z"}
        },
        {
            "name": "Mission Control", 
            "desc": "Cho phép kết nối các tay cầm Bluetooth của hệ máy khác (PS4, PS5, Xbox One, Wii U Pro...) với Nintendo Switch mà không cần USB Receiver.",
            "urls": {"Tự động cài đặt": "https://github.com/ndeadly/MissionControl/releases/download/v0.14.1/MissionControl-0.14.1-master-141b3aca.zip"}
        },
        {
            "name": "Sys-con (USB Controllers)", 
            "desc": "Connect wired controllers (or via USB receiver) from 3rd parties (Xbox 360, DualShock 3...) to Switch Dock.",
            "urls": {"Tự động cài đặt": "https://github.com/o0Zz/sys-con/releases/download/1.6.1/sys-con-1.6.1.zip"}
        },
    ],
    "🎮 HOMEBREW (Ứng dụng)": [
        {
            "name": "HB App Store", 
            "desc": "Chợ ứng dụng Homebrew trực tuyến. Nơi tìm kiếm, tải xuống và cập nhật hàng trăm ứng dụng tiện ích, game homebrew trực tiếp trên Switch.",
            "urls": {"Tự động cài đặt": "https://github.com/fortheusers/hb-appstore/releases/download/v2.3.2/appstore.nro"}
        },
        {
            "name": "Edizon (Cheat)", 
            "desc": "Ứng dụng quản lý Save game và Cheat code mạnh mẽ. Dùng để sao lưu save game ra thẻ nhớ hoặc kích hoạt các mã gian lận.",
            "urls": {"Tự động cài đặt": "https://github.com/WerWolv/EdiZon/releases/download/v3.1.0/EdiZon.nro"}
        },
        {
            "name": "Breeze (Cheat)", 
            "desc": "Công cụ Cheat nâng cao (kế thừa Edizon). Hỗ trợ tìm kiếm giá trị bộ nhớ phức tạp hơn để tự tạo mã cheat.",
            "urls": {"Tự động cài đặt": "https://github.com/tomvita/Breeze-Beta/releases/download/beta99r/Breeze.zip"}
        },
        {
            "name": "Retroarch (Giả lập)", 
            "desc": "Trình giả lập đa hệ máy 'All-in-one'. Chơi được game của NES, SNES, GBA, PS1, N64, Arcade... ngay trên Switch.",
            "urls": {"Truy cập Web": "https://buildbot.libretro.com/nightly/nintendo/switch/libnx/"}
        },
        {
            "name": "pEmu (Giả lập)", 
            "desc": "Bộ sưu tập các trình giả lập (pFBA, pSNES...) được tối ưu hóa riêng cho Switch bởi Cpasjuste. Giao diện đẹp và hiệu năng tốt.",
            "urls": {"Truy cập Web": "https://github.com/Cpasjuste/pemu/releases/latest"}
        },
        {
            "name": "DBI (Quản lý file + Cài game)", 
            "desc": "Công cụ 'Thần thánh' cho Switch. Hỗ trợ cài game qua cáp USB (MTP) cực nhanh, xóa file rác, quản lý file trên thẻ nhớ giao diện trực quan.",
            "urls": {"Tự động cài đặt": "https://github.com/rashevskyv/dbi/releases/download/854ru/DBI.nro"}
        },
        {
            "name": "Tinfoil (Shop game)", 
            "desc": "Cửa hàng tải game miễn phí (FreeShop) nổi tiếng (cần add host). Cũng là trình quản lý file và cài đặt game giao diện đẹp mắt. Tuy nhiên không tương thích với atmosphere mới nhất nữa, bạn hãy chọn mở trang download atmosphere, tải bản 1.9.5 đổ xuống với điều kiện OFW lẫn CFW <21.0.0 thì mới sử dụng được",
            "urls": {"Truy cập Web": "https://tinfoil.io/Download#download"}
        },
        {
            "name": "Goldleaf", 
            "desc": "Trình quản lý file và cài đặt file NSP/NSZ/XCI cơ bản, mã nguồn mở. Hỗ trợ duyệt file trên thẻ nhớ và cài game qua USB (với Quark).",
            "urls": {"Tự động cài đặt": "https://github.com/XorTroll/Goldleaf/releases/download/1.2.0/Goldleaf.nro"}
        },
        {
            "name": "Linkalho (Link Offline)", 
            "desc": "Công cụ liên kết tài khoản Nintendo giả lập (Offline). Bắt buộc dùng nếu bạn chơi game yêu cầu có tài khoản Nintendo nhưng máy bị ban hoặc không muốn online.",
            "urls": {
                "Bước 1. Tải về file": "https://dlhb.gamebrew.org/switchhomebrews/linkalhonx.7z",
                "Bước 2. Chọn file nén để tự động chép.": "ACTION_LINKALHO_NESTED"
            }
        },
    ],
    "⚙️ LINH TINH (Firmware/Cheat/Save)": [
        {
            "name": "Firmware (Nâng/Hạ cấp)", 
            "desc": "Các file hệ điều hành gốc của Nintendo Switch. Cần thiết khi bạn muốn cập nhật máy lên phiên bản mới nhất bằng Daybreak.",
            "urls": {
                "Link tải tổng hợp 1": "https://darthsternie.net/switch-firmwares/", 
                "Link tải tổng hợp 2": "https://github.com/THZoria/NX_Firmware/releases",
                "Hướng dẫn Update": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/cap-nhat-firmware-cho-emunand"
            }
        },
        {
            "name": "Cheat game (Tổng hợp)", 
            "desc": "Kho mã Cheat do cộng đồng tổng hợp. Tải về để cập nhật các mã cheat mới nhất cho Edizon/Breeze.",
            "urls": {
                "GBAtemp": "https://gbatemp.net/threads/cheat-codes-ams-and-sx-os-add-and-request.520293/",
                "CheatSlips": "https://www.cheatslips.com/",
                "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat"
            }
        },
        {
            "name": "Save Game (Nguồn tải)", 
            "desc": "Các kho lưu trữ Save game (File lưu tiến độ game) được chia sẻ bởi cộng đồng. Hữu ích khi bạn muốn chơi New Game+ hoặc mất save.",
            "urls": {
                "GBAtemp Save": "https://gbatemp.net/download/categories/game-saves.1668/",
                "TheTechGame": "https://www.thetechgame.com/Downloads/cid=135/nintendo-switch-game-saves.html",
                "Hướng dẫn": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/sao-luu-va-phuc-hoi-save-game"
            }
        },
        {
            "name": "Việt hóa game", 
            "desc": "Tổng hợp các bản Patch tiếng Việt cho game Switch. Cần tải về và cài đặt đúng thư mục (thường là atmosphere/contents).",
            "urls": {"Link tham khảo": "https://docs.google.com/spreadsheets/d/1k_8w_Eb7M6_3q1-FrtY0gYdrCokr3IGxuk-oj_u-zbw/preview"}
        },
    ],
    "🚑 FIX LỖI NHANH (Sự cố thường gặp)": [
        {
            "name": "Cài lại gói hack My Pack (Khuyến nghị)", 
            "desc": "Cách sửa lỗi triệt để nhất khi máy bị lỗi nặng. Hệ thống sẽ đưa bạn đến mục tải gói hack chuẩn để cài lại từ đầu.",
            "urls": {"🛠️ Chạy Fix": "ACTION_FIX_REINSTALL_PACK"}
        },
        {
            "name": "Gỡ bỏ Themes (Fix màn hình đen/Bootloop)", 
            "desc": "Xóa thư mục theme (0100000000001000). Dùng khi bạn cài theme lỗi khiến máy không khởi động được hoặc bị màn hình đen sau logo Atmosphere.",
            "urls": {"🛠️ Chạy Fix": "ACTION_FIX_THEMES"}
        },
        {
            "name": "Gỡ bỏ các Sysmodules phổ biến", 
            "desc": "Chỉ xóa các module chạy ngầm phổ biến (Tesla, Emuiibo, SysDVR...). Giữ lại Việt hóa và Mod game. Dùng khi máy hay bị Crash nhẹ.",
            "urls": {"🛠️ Chạy Fix": "ACTION_FIX_MODULES"}
        },
        {
            "name": "Xóa SẠCH thư mục Contents (Triệt để)", 
            "desc": "CẢNH BÁO: Xóa toàn bộ folder atmosphere/contents. Sẽ mất hết Sysmod, Mod game, Việt hóa và Cheat. Dùng khi máy lỗi nặng, crash liên tục.",
            "urls": {"🔥 Chạy Fix": "ACTION_FIX_DELETE_ALL_CONTENTS"}
        },
        {
            "name": "Xóa file rác MacOS (Fix Archive Bit)", 
            "desc": "Quét và xóa các file rác do MacOS tạo ra (._file, .DS_Store). Những file này thường làm Hekate không đọc được cấu hình.",
            "urls": {"🛠️ Chạy Fix": "ACTION_FIX_MAC_JUNK"}
        },
        {
            "name": "Xóa toàn bộ Cheats (Fix Game Crash)", 
            "desc": "Xóa tất cả file cheat trong thư mục contents. Dùng khi vào game bị crash ngay lập tức do mã cheat cũ xung đột.",
            "urls": {"🛠️ Chạy Fix": "ACTION_FIX_CHEATS"}
        },
        {
            "name": "Các lỗi khác (nguồn: Cộng Đồng Nintendo Switch hắc ám)", 
            "desc": "Tra cứu danh sách các lỗi thường gặp khác và cách khắc phục chi tiết trên Wiki của cộng đồng.",
            "urls": {"🌍 Xem hướng dẫn Web": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap"}
        }
    ],
    "📚 CÁC HƯỚNG DẪN (nguồn: Cộng Đồng Nintendo Switch hắc ám)": [
        {
            "name": "Hướng dẫn căn bản ", 
            "desc": "Các kiến thức nhập môn cần thiết: Phân biệt đời máy, thuật ngữ hack, hướng dẫn sử dụng cơ bản cho người mới bắt đầu.",
            "urls": {"🌍 Truy cập Web": "https://nsw.gitbook.io/guide/huong-dan-can-ban/"}
        },
         {
            "name": "Hướng dẫn nâng cao ", 
            "desc": "Tổng hợp các bài viết chuyên sâu: Tạo EmuMMC, Ẩn số seri (Incognito), Phân vùng thẻ nhớ, Sao lưu Nand...",
            "urls": {"🌍 Truy cập Web": "https://nsw.gitbook.io/guide/huong-dan-nang-cao"}
        },
    ],
    "👾 NGUỒN DOWNLOAD GAME": [
        {
            "name": "Website tải game Switch",
            "desc": "Kho game Switch phong phú, cập nhật thường xuyên.",
            "urls": {"Link tham khảo": "https://rebrand.ly/tsufurom"}
        }
    ]
}

# --- DỮ LIỆU DỊCH (ENGLISH) ---
DATA_EN = {
    "🔥 HACK FILES & PC TOOLS": [
        {
            "name": "My Pack AIO Hack", 
            "desc": "Custom Switch hack toolkit (AIO). Includes Atmosphere, Hekate, and essential sysmods to run immediately.",
            "urls": {
                "Step 1. Download file": "https://rebrand.ly/mypack",
                "Step 2. Pick Zip to Auto Install": "ACTION_PICK_ZIP"
            }
        }, 
        {
            "name": "Sigpatches (Piracy Support)", 
            "desc": "Signature Patches: Essential for playing pirated games. Bypasses Nintendo's signature check, allowing NSP/XCI installation.",
            "urls": {
                "Step 1. Download file": "https://gbatemp.net/attachments/hekate-ams-package3-sigpatches-1-10-1p-cfw-21-1-0_v0-zip.544098/",
                "Step 2. Pick Zip to Auto Install": "ACTION_PICK_ZIP"
            }
        },
        {
            "name": "Hekate (Bootloader)", 
            "desc": "All-in-one bootloader. Used for Backup/Restore NAND, Create Emunand, Partition SD Card, and boot into CFW.",
            "urls": {"Auto Install": "https://github.com/CTCaer/hekate/releases/download/v6.4.2/hekate_ctcaer_6.4.2_Nyx_1.8.2.zip"}
        },
        {
            "name": "Atmosphere (CFW)", 
            "desc": "Most popular Custom Firmware for Switch. Core platform for running Homebrew, Mods, and Pirated games.",
            "urls": {"Auto Install": "https://github.com/Atmosphere-NX/Atmosphere/releases/download/1.10.1/atmosphere-1.10.1-master-21c0f75a2+hbl-2.4.5+hbmenu-3.6.1.zip"}
        },
        {
            "name": "TegraRcmGUI (PC App)", 
            "desc": "Windows PC Software. Used to inject Payload into Switch when in RCM mode (black screen).",
            "urls": {"Auto Install (PC)": "ACTION_RUN_PC|https://github.com/eliboa/TegraRcmGUI/releases/download/2.6/TegraRcmGUI_v2.6_Installer.msi"}
        },
    ],
    "🛠️ USEFUL SYSMODS (Restart Required)": [
        {
            "name": "Sys-patch", 
            "desc": "Module to automatically patch system errors on boot (fs, ldr, es). Helps games run more stable.",
            "urls": {
                "Step 1. Download file": "https://gbatemp.net/download/sys-patch-sysmodule.39471/download",
                "Step 2. Pick Zip to Auto Install": "ACTION_PICK_ZIP"
            }
        },
        {
            "name": "Tesla Menu (Overlay Menu)", 
            "desc": "Overlay Menu. Allows toggling cheats, viewing system info, overclocking... while playing games (Combo: L + Dpad Down + R3).",
            "urls": {"Auto Install (Combo)": "TESLA_ACTION"}
        },
        {
            "name": "Ultrahand (Overlay Manager)", 
            "desc": "Another Overlay manager similar to Tesla but with a modern UI.",
            "urls": {"Auto Install (Combo)": "ULTRAHAND_ACTION"}
        },
        {
            "name": "Edizon Overlay (Cheat game)", 
            "desc": "Plugin to display Cheat menu over the game. Search values, toggle cheats, infinite money without quitting game.",
            "urls": {"Auto Install": "https://github.com/proferabg/EdiZon-Overlay/releases/download/v1.0.14/ovlEdiZon.ovl", "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat#cach-3-dung-edizon-overlay"}
        },
        {
            "name": "Status Monitor (FPS/Battery/Temp)", 
            "desc": "Real-time hardware monitor. Displays FPS, CPU/GPU Temp, RAM speed, Battery %...",
            "urls": {"Auto Install": "https://github.com/masagrator/Status-Monitor-Overlay/releases/download/1.3.2/Status-Monitor-Overlay.zip"}
        },
        {
            "name": "emuiibo (Amiibo Emulator)", 
            "desc": "Virtual Amiibo emulator. Get in-game rewards (Zelda, Splatoon) without real figures. Used with Tesla Menu.",
            "urls": {"Auto Install": "https://github.com/XorTroll/emuiibo/releases/download/1.1.2/emuiibo.zip"}
        },
        {
            "name": "SYS-CLK (Overclock)", 
            "desc": "Overclock or Underclock tool. Helps heavy games run smoother (higher FPS) or save battery.",
            "urls": {"Auto Install": "https://github.com/retronx-team/sys-clk/releases/download/2.0.1/sys-clk-2.0.1-21fix.zip"}
        },
        {
            "name": "SysDVR (Stream via USB)", 
            "desc": "Stream video and audio from Switch to PC via USB or Wifi. Record/Stream without Capture Card.",
            "urls": {"1. Download for Switch": "https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR.zip", "2. Client for PC (7z)": "ACTION_SAVE_PC|https://github.com/exelix11/SysDVR/releases/download/v6.2.2/SysDVR-Client-Windows-x64-with-framework.7z"}
        },
        {
            "name": "Mission Control", 
            "desc": "Connect Bluetooth controllers from other systems (PS4, PS5, Xbox One, Wii U Pro...) to Switch without USB Receiver.",
            "urls": {"Auto Install": "https://github.com/ndeadly/MissionControl/releases/download/v0.14.1/MissionControl-0.14.1-master-141b3aca.zip"}
        },
        {
            "name": "Sys-con (USB Controllers)", 
            "desc": "Connect wired controllers (or via USB receiver) from 3rd parties (Xbox 360, DualShock 3...) to Switch Dock.",
            "urls": {"Auto Install": "https://github.com/o0Zz/sys-con/releases/download/1.6.1/sys-con-1.6.1.zip"}
        },
    ],
    "🎮 HOMEBREW (Apps)": [
        {
            "name": "HB App Store", 
            "desc": "Online Homebrew App Store. Search, download, and update hundreds of utilities and homebrew games.",
            "urls": {"Auto Install": "https://github.com/fortheusers/hb-appstore/releases/download/v2.3.2/appstore.nro"}
        },
        {
            "name": "Edizon (Cheat)", 
            "desc": "Save game manager and Cheat code tool. Backup save files or activate cheat codes.",
            "urls": {"Auto Install": "https://github.com/WerWolv/EdiZon/releases/download/v3.1.0/EdiZon.nro"}
        },
        {
            "name": "Breeze (Cheat)", 
            "desc": "Advanced Cheat tool (Successor to Edizon). Supports searching complex memory values.",
            "urls": {"Auto Install": "https://github.com/tomvita/Breeze-Beta/releases/download/beta99r/Breeze.zip"}
        },
        {
            "name": "Retroarch (Emulator)", 
            "desc": "All-in-one emulator. Play NES, SNES, GBA, PS1, N64, Arcade... on Switch.",
            "urls": {"Open Web": "https://buildbot.libretro.com/nightly/nintendo/switch/libnx/"}
        },
        {
            "name": "pEmu (Emulator)", 
            "desc": "Collection of optimized emulators (pFBA, pSNES...) by Cpasjuste. Nice UI and good performance.",
            "urls": {"Open Web": "https://github.com/Cpasjuste/pemu/releases/latest"}
        },
        {
            "name": "DBI (File Manager + Installer)", 
            "desc": "God-tier tool for Switch. Install games via USB (MTP), clean junk files, manage SD card files.",
            "urls": {"Auto Install": "https://github.com/rashevskyv/dbi/releases/download/854ru/DBI.nro"}
        },
        {
            "name": "Tinfoil (Game Shop)", 
            "desc": "Famous FreeShop (needs host). Also a beautiful file manager and game installer.",
            "urls": {"Open Web": "https://tinfoil.io/Download#download"}
        },
        {
            "name": "Goldleaf", 
            "desc": "Open source file manager and NSP/NSZ/XCI installer. Browse SD card and install via USB (with Quark).",
            "urls": {"Auto Install": "https://github.com/XorTroll/Goldleaf/releases/download/1.2.0/Goldleaf.nro"}
        },
        {
            "name": "Linkalho (Offline Account)", 
            "desc": "Link fake Nintendo account (Offline). Required if game asks for Nintendo account but you are banned or offline.",
            "urls": {
                "Step 1. Download file": "https://dlhb.gamebrew.org/switchhomebrews/linkalhonx.7z",
                "Step 2. Pick Zip to Auto Install": "ACTION_LINKALHO_NESTED"
            }
        },
    ],
    "⚙️ MISC (Firmware/Cheat/Save)": [
        {
            "name": "Firmware (Up/Downgrade)", 
            "desc": "Original Nintendo Switch Firmware files. Needed when updating system using Daybreak.",
            "urls": {
                "Link Collection 1": "https://darthsternie.net/switch-firmwares/", 
                "Link Collection 2": "https://github.com/THZoria/NX_Firmware/releases",
                "Update Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/cap-nhat-firmware-cho-emunand"
            }
        },
        {
            "name": "Cheat game (Database)", 
            "desc": "Cheat codes collected by community. Download to update latest cheats for Edizon/Breeze.",
            "urls": {
                "GBAtemp": "https://gbatemp.net/threads/cheat-codes-ams-and-sx-os-add-and-request.520293/",
                "CheatSlips": "https://www.cheatslips.com/",
                "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/su-dung-cheat"
            }
        },
        {
            "name": "Save Game (Database)", 
            "desc": "Save game files shared by community. Useful for New Game+ or lost saves.",
            "urls": {
                "GBAtemp Save": "https://gbatemp.net/download/categories/game-saves.1668/",
                "TheTechGame": "https://www.thetechgame.com/Downloads/cid=135/nintendo-switch-game-saves.html",
                "Guide": "https://nsw.gitbook.io/guide/huong-dan-nang-cao/sao-luu-va-phuc-hoi-save-game"
            }
        },
        {
            "name": "Game Translation", 
            "desc": "Vietnamese patches for Switch games. Download and install to correct folder (usually atmosphere/contents).",
            "urls": {"Reference Link": "https://docs.google.com/spreadsheets/d/1k_8w_Eb7M6_3q1-FrtY0gYdrCokr3IGxuk-oj_u-zbw/preview"}
        },
    ],
    "🚑 QUICK FIX (Common Issues)": [
        {
            "name": "Reinstall My Pack (Recommended)", 
            "desc": "Best way to fix severe errors. System will guide you to download the standard hack pack to reinstall.",
            "urls": {"🛠️ Run Fix": "ACTION_FIX_REINSTALL_PACK"}
        },
        {
            "name": "Remove Themes (Fix Black Screen)", 
            "desc": "Delete theme folder (0100000000001000). Use when theme causes boot failure or black screen.",
            "urls": {"🛠️ Run Fix": "ACTION_FIX_THEMES"}
        },
        {
            "name": "Remove Common Sysmodules", 
            "desc": "Only delete background modules (Tesla, Emuiibo, SysDVR...). Keep Translations and Game Mods. Use when crashing.",
            "urls": {"🛠️ Run Fix": "ACTION_FIX_MODULES"}
        },
        {
            "name": "WIPE Contents Folder (Extreme)", 
            "desc": "WARNING: Delete entire atmosphere/contents folder. Will lose all Sysmods, Mods, Translations, and Cheats. Use for severe crashes.",
            "urls": {"🔥 Wipe & Reset": "ACTION_FIX_DELETE_ALL_CONTENTS"}
        },
        {
            "name": "Remove MacOS Junk (Fix Archive Bit)", 
            "desc": "Scan and delete MacOS junk files (._file, .DS_Store). These often cause Hekate config errors.",
            "urls": {"🛠️ Run Fix": "ACTION_FIX_MAC_JUNK"}
        },
        {
            "name": "Delete All Cheats (Fix Game Crash)", 
            "desc": "Delete all cheat files in contents. Use when game crashes immediately due to old cheat conflicts.",
            "urls": {"🛠️ Run Fix": "ACTION_FIX_CHEATS"}
        },
        {
            "name": "Other Errors (Source: Community)", 
            "desc": "Lookup other common errors and detailed fixes on Community Wiki.",
            "urls": {"🌍 View Guide": "https://nsw.gitbook.io/guide/cac-loi-thuong-gap"}
        }
    ],
    "📚 GUIDES (Source: Nintendo Switch Community)": [
         {
            "name": "Advanced Guides", 
            "desc": "In-depth articles: Create EmuMMC, Incognito, Partition SD, Backup Nand...",
            "urls": {"🌍 Open Web": "https://nsw.gitbook.io/guide/huong-dan-nang-cao"}
        },
        {
            "name": "Basic Guides (For Beginners)", 
            "desc": "Essential knowledge: Switch revisions, hacking terminology, basic usage guides for beginners.",
            "urls": {"🌍 Open Web": "https://nsw.gitbook.io/guide/huong-dan-can-ban/"}
        }
    ],
    "👾 GAME DOWNLOAD SOURCES": [
        {
            "name": "Switch Game Download Site",
            "desc": "Large library of Switch games, updated frequently.",
            "urls": {"Link": "https://rebrand.ly/tsufurom"}
        }
    ]
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://gbatemp.net'
}

# --- CLASS TOOLTIP ---
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
                       font=("Segoe UI", 9), wraplength=300)
        label.pack(padx=5, pady=2)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class SwitchToolApp:
    def __init__(self, root):
        self.root = root
        self.lang_code = "VI" # Mặc định tiếng Việt
        
        # --- THIẾT LẬP ICON WINDOWS TASKBAR ---
        try:
            myappid = 'mycompany.switch.update.manager.pro'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except: pass

        self.setup_window()
        self.dest_path = tk.StringVar(value=os.getcwd())
        
        self.configure_styles()
        self.root.configure(bg=COLOR_BG)
        
        self.is_app_ready = False # Cờ báo hiệu tải xong

        # --- LOADING SCREEN ĐƯỢC GỌI Ở ĐÂY ---
        self.show_loading_screen()
        # -------------------------------------

    def center_window(self, width=1000, height=1000):
        # Hàm căn giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_window(self):
        # Icon App
        # [SỬA] Dùng resource_path để tìm đúng icon khi chạy file exe
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except: pass
        
        # --- CẬP NHẬT GIAO DIỆN KHÔNG BỊ CHE ---
        
        # 1. Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 2. Thiết lập kích thước App
        app_width = 1100  # Chiều ngang cố định
        # Chiều cao = Màn hình - 110px (Trừ hao thanh Taskbar + Thanh tiêu đề window)
        app_height = screen_height - 110 
        
        # 3. Tính toán vị trí
        # Căn giữa theo chiều ngang (X)
        x = int((screen_width / 2) - (app_width / 2))
        # Đặt sát mép trên (Y = 0 hoặc 5) thay vì căn giữa để tránh bị đẩy xuống
        y = 5 
        
        # 4. Áp dụng kích thước
        self.root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        
        self.update_title()

    def update_title(self):
        # Hiển thị luôn version trên tiêu đề
        self.root.title(f"{UI_TEXT[self.lang_code]['title']} (v{APP_VERSION})")

    def configure_styles(self):
        style = ttk.Style()
        try: style.theme_use('clam') 
        except: pass

        style.configure(".", background=COLOR_BG, foreground=COLOR_FG, font=FONT_NORMAL)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_FG)
        style.configure("Card.TFrame", background=COLOR_CARD, relief="flat")
        
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
        
        style.configure("Lang.TButton", 
                        background="#555555", foreground="white", 
                        font=("Segoe UI", 8, "bold"), borderwidth=0)

    # --- HÀM XỬ LÝ NGẦM (BACKGROUND THREAD) ---
    def run_init_tasks(self):
        self.auto_detect_drive()
        try:
            # [SỬA] Dùng resource_path để tìm logo
            load = Image.open(resource_path("logo.png"))
            target_height = 140 # Giảm một chút cho gọn
            aspect_ratio = load.width / load.height
            target_width = int(target_height * aspect_ratio)
            self.preloaded_logo_image = load.resize((target_width, target_height), Image.Resampling.LANCZOS)
        except:
            self.preloaded_logo_image = None
        time.sleep(1.5) 
        self.is_app_ready = True

    # --- HÀM LOADING SCREEN ---
    def show_loading_screen(self):
        self.loading_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        center_frame = tk.Frame(self.loading_frame, bg=COLOR_BG)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.loading_frames = [] 
        try:
            # [SỬA] Dùng resource_path để tìm gif
            im = Image.open(resource_path("loading.gif"))
            for frame in ImageSequence.Iterator(im):
                self.loading_frames.append(ImageTk.PhotoImage(frame.copy()))
        except:
            pass 

        self.loading_label = tk.Label(center_frame, bg=COLOR_BG, bd=0)
        self.loading_label.pack(pady=(0, 20))

        tk.Label(center_frame, 
                 text="✨ Đang thực hiện ma thuật hắc ám, vui lòng đợi...", 
                 font=("Segoe UI", 14, "bold"),  
                 fg=COLOR_GOLD,                  
                 bg=COLOR_BG).pack(pady=(10, 0))

        # [QUAN TRỌNG] Chạy init task trước
        threading.Thread(target=self.run_init_tasks, daemon=True).start()

        # [QUAN TRỌNG] Bắt buộc chạy hàm update animation kể cả khi không có gif
        # Để nó có thể check cờ is_app_ready và chuyển cảnh
        self.update_loading_animation(0)

    def update_loading_animation(self, frame_index):
        if not hasattr(self, 'loading_frame') or not self.loading_frame.winfo_exists():
            return

        if self.is_app_ready: 
            self.finish_loading() 
            return

        # Nếu có frame thì cập nhật ảnh, không có thì thôi
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

    # ... [PHẦN CÒN LẠI CỦA CODE GIỮ NGUYÊN NHƯ CŨ] ...
    # Để tiết kiệm không gian, tôi chỉ liệt kê phần thay đổi quan trọng ở trên.
    # Bạn hãy giữ nguyên các hàm bên dưới từ toggle_language trở đi nhé.
    
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

        guide_content = """
*** PHẦN TIẾNG VIỆT ***

1. CHUẨN BỊ:
   - Kết nối thẻ nhớ Switch tới máy tính
    + Cách 1: Cắm thẻ nhớ Switch vào máy tính hoặc qua đầu đọc thẻ.
    + Cách 2: Kết nối Switch qua dây USB Type C thông qua Hekate. Để vào Hekate, bạn cần tắt nguồn Switch hoàn toàn, rồi mở nguồn lên lại (hoặc giữ nút giảm âm lượng khi mở), sau đó vào Tools>Usb Tools>SD card, tiếp theo thực hiện cắm dây USB Type C
   Lưu ý 1: Nếu bạn dùng Hekate USB Tools, hãy Eject thẻ nhớ ra khỏi máy trước khi ngắt kết nối cáp USB.
   Lưu ý 2: Không thể dùng DBI hoặc các MTP Responder để thực hiện các cập nhật cho gói hack. Hãy sử dụng chế độ USB Mass Storage (UMS) trong Hekate.
   - Tại mục "Thẻ nhớ (Root)", bấm "Chọn" để trỏ đến ổ đĩa thẻ nhớ của bạn.
   - Nếu không biết ổ nào, bấm "Auto 🔄" để phần mềm quét giúp bạn.
   - Nếu có thắc mắc gì về bất cứ tính năng nào, hãy trỏ chuột vào biểu tượng dấu chấm hỏi (?) để xem hướng dẫn nhanh.
2. CÁCH TẢI VÀ CÀI ĐẶT:
   - Danh sách được chia thành các nhóm: File Hack, Sysmod, Homebrew...
   - Nút XANH (⚡ Tự động cài): Phần mềm sẽ tự tải file về và giải nén thẳng vào thẻ nhớ. Bạn không cần làm gì thêm.
   - Nút XÁM (Web/Link): Sẽ mở trình duyệt web để bạn đọc hướng dẫn hoặc tải thủ công (đối với các file không cho tải trực tiếp).
   - Nút MŨI TÊN XANH (⬇️ Tải tất cả): Tự động tải lần lượt mọi thứ trong danh mục đó.

3. SỬA LỖI (FIX):
   - Nếu máy gặp lỗi (màn hình đen, crash game...), hãy kéo xuống mục "FIX LỖI NHANH".
   - Bấm vào các nút Fix tương ứng để phần mềm tự động sửa file lỗi trên thẻ nhớ.

------------------------------------------------



*** ENGLISH SECTION ***

1. PREPARATION:
   - Insert your Switch SD card into PC (or connect via USB).
   - At "SD Card (Root)", click "Browse" to select your SD card drive.
   - Click "Auto Detect" if you are unsure which drive it is.

2. HOW TO INSTALL:
   - Apps are categorized into: Hack Files, Sysmods, Homebrew...
   - BLUE Button (⚡ Auto Install): The tool automatically downloads and extracts files to your SD card. No extra steps needed.
   - GREY Button (Web/Link): Opens a web browser for instructions or manual download sources.
   - DOWN ARROW Button (⬇️ Download All): Automatically downloads everything in that category one by one.

3. TROUBLESHOOTING (FIX):
   - If you face issues (black screen, crashes...), scroll down to "QUICK FIX".
   - Click the corresponding Fix buttons to let the tool repair files on your SD card automatically.
"""
        text_area.insert(tk.END, guide_content)
        text_area.config(state=tk.DISABLED) 

    def setup_ui(self):
        text_db = UI_TEXT[self.lang_code]
        data_db = DATA_VI if self.lang_code == "VI" else DATA_EN

        # =========================================================================
        # 1. HEADER (TITLE & BUTTONS)
        # =========================================================================
        top_frame = tk.Frame(self.root, bg=COLOR_BG, pady=10, padx=20)
        top_frame.pack(fill="x", side="top")
        
        # Left Info (Title & Credits)
        left_info = tk.Frame(top_frame, bg=COLOR_BG)
        left_info.pack(side="left", fill="both", expand=True)

        lbl_title = tk.Label(left_info, text=text_db["title"], font=("Segoe UI", 20, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT)
        lbl_title.pack(side="top", anchor="w")

        lbl_credit = tk.Label(left_info, text=text_db["credit"], font=("Segoe UI", 10, "italic"), bg=COLOR_BG, fg="#dddddd")
        lbl_credit.pack(side="top", anchor="w")
        
        lbl_credit_2 = tk.Label(left_info, text=text_db["credit2"],
                                font=("Segoe UI", 9, "italic"), bg=COLOR_BG, fg="#dddddd", justify="left")
        lbl_credit_2.pack(side="top", anchor="w", pady=(2, 0))

        # Right Info (Buttons & Logo)
        right_info = tk.Frame(top_frame, bg=COLOR_BG)
        right_info.pack(side="right", anchor="ne", fill="y")
        
        # Frame chứa nút bấm
        btn_container = tk.Frame(right_info, bg=COLOR_BG)
        btn_container.pack(side="top", anchor="e")

        # Nút Donate (Vàng) & Update nằm cạnh nhau hoặc trên dưới gọn gàng
        btn_update_soft = ttk.Button(btn_container, text=text_db["btn_update_soft"], style="TButton",
                                     command=self.check_for_updates)
        btn_update_soft.pack(side="top", anchor="e", pady=2, fill="x")

        btn_donate_header = tk.Button(btn_container, text=text_db["btn_donate"], bg="#FFD700", fg="black", font=("Segoe UI", 9, "bold"), relief="flat",
                                      activebackground="#ffcc00",
                                      command=lambda: webbrowser.open("https://tsufu.gitbook.io/donate/"))
        btn_donate_header.pack(side="top", anchor="e", pady=2, fill="x")

        # Các nút phụ
        sub_btn_frame = tk.Frame(btn_container, bg=COLOR_BG)
        sub_btn_frame.pack(side="top", anchor="e", pady=2)

        btn_guide = ttk.Button(sub_btn_frame, text=text_db["btn_guide"], style="TButton", width=20,
                               command=self.show_user_guide)
        btn_guide.pack(side="right", padx=2)

        lang_text = "Language: VI" if self.lang_code == "VI" else "Language: EN"
        btn_lang = ttk.Button(sub_btn_frame, text=lang_text, style="Lang.TButton", width=12, command=self.toggle_language)
        btn_lang.pack(side="right", padx=2)

        # LOGO IMAGE (Nằm dưới nút bấm)
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

        # =========================================================================
        # 2. PATH SELECTION ROW (Tách riêng ra để Full Width)
        # =========================================================================
        path_frame = tk.Frame(self.root, bg=COLOR_BG, pady=5, padx=20)
        path_frame.pack(fill="x", side="top") # Pack ngay sau Header
        
        tk.Label(path_frame, text=text_db["path_label"], bg=COLOR_BG, fg="#dddddd", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        entry_path = tk.Entry(path_frame, textvariable=self.dest_path, bg=COLOR_CARD, fg="white", insertbackground="white", relief="flat", font=("Consolas", 11))
        entry_path.pack(side="left", fill="x", expand=True, padx=10, ipady=5)
        
        ttk.Button(path_frame, text=text_db["btn_browse"], command=self.browse_folder).pack(side="left", padx=2)
        ttk.Button(path_frame, text=text_db["btn_detect"], command=lambda: threading.Thread(target=self.auto_detect_drive, daemon=True).start()).pack(side="left", padx=2)
        ttk.Button(path_frame, text=text_db["btn_open"], command=self.open_root_folder).pack(side="left", padx=2)

        # =========================================================================
        # 3. MAIN SCROLLABLE AREA
        # =========================================================================
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

        # RENDER DATA
        categories = data_db.keys()
        
        for cat in categories:
            items = data_db[cat]
            header_frame = tk.Frame(self.scroll_frame, bg=COLOR_HEADER_BG, pady=5)
            header_frame.pack(fill="x", pady=(15, 5), padx=5) # Giảm padding top chút
            
            tk.Label(header_frame, text=cat, font=FONT_HEADER, bg=COLOR_HEADER_BG, fg=COLOR_GOLD, anchor="w").pack(side="left", padx=10)
            
            if "SYSMOD" in cat or "HOMEBREW" in cat:
                btn_dl_all = ttk.Button(header_frame, text=text_db["btn_dl_all"], style="DownloadAll.TButton",
                                        command=lambda c=cat: self.download_category_all(c))
                btn_dl_all.pack(side="right", padx=10)
            
            tk.Frame(header_frame, bg=COLOR_GOLD, height=2).pack(side="bottom", fill="x")

            for item in items:
                self.create_item_card(self.scroll_frame, item)

        # =========================================================================
        # 4. FOOTER
        # =========================================================================
        bot = tk.Frame(self.root, bg=COLOR_CARD, pady=10, padx=20)
        bot.pack(fill="x", side="bottom")
        
        self.progress_var = tk.DoubleVar()
        style_prog = ttk.Style()
        style_prog.configure("Horizontal.TProgressbar", background=COLOR_SUCCESS, troughcolor=COLOR_BG, borderwidth=0)
        self.progress_bar = ttk.Progressbar(bot, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=5)
        
        info_line = tk.Frame(bot, bg=COLOR_CARD)
        info_line.pack(fill="x")
        
        # Tăng kích thước font chữ status để dễ nhìn hơn
        self.status_label = tk.Label(info_line, text=text_db["status_ready"], bg=COLOR_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 12, "bold"))
        self.status_label.pack(side="left")
        # --- [NEW] NÚT BÁO LỖI ---
        btn_bug_report = tk.Button(info_line, text="🐞 Góp ý & báo lỗi (Bug&Report)", 
                                   font=("Segoe UI", 9, "bold"), 
                                   bg=COLOR_CARD, fg="#E06C75", # Màu đỏ nhạt cho dễ nhìn trên nền tối
                                   activebackground="#3e3e42", activeforeground="#ff5555",
                                   bd=0, cursor="hand2",
                                   command=lambda: webbrowser.open("https://rebrand.ly/bugrp"))
        btn_bug_report.pack(side="right")
        # -------------------------

    # --- AUTO UPDATE LOGIC (NEW) ---
    def check_for_updates(self):
        # Hàm kiểm tra cập nhật từ GitHub
        threading.Thread(target=self._process_check_update, daemon=True).start()

    def _process_check_update(self):
        self.status_label.config(text="Checking for updates...", fg=COLOR_INFO)
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                latest_tag = data.get("tag_name", "v0.0.0")
                download_url = ""
                # Tìm file asset có đuôi .exe
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                # So sánh phiên bản (đơn giản bằng chuỗi)
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
        # Tải file update về và tạo script thay thế
        self.status_label.config(text="Downloading update...", fg=COLOR_WARNING)
        try:
            r = requests.get(url, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            
            # Tên file mới tải về
            new_exe_name = "SwitchManager_New.exe"
            with open(new_exe_name, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        self.progress_var.set((downloaded / total_size) * 100)
            
            self.status_label.config(text="Installing update...", fg=COLOR_SUCCESS)
            
            # Tạo file .bat để thay thế file đang chạy
            current_exe = sys.executable
            bat_script = f"""
@echo off
timeout /t 2 /nobreak
del "{current_exe}"
ren "{new_exe_name}" "{os.path.basename(current_exe)}"
start "" "{os.path.basename(current_exe)}"
del "%~f0"
"""
            with open("update_script.bat", "w") as bat:
                bat.write(bat_script)
            
            messagebox.showinfo("Update", "Phần mềm sẽ khởi động lại để hoàn tất cập nhật.")
            
            # Chạy file bat và tắt phần mềm
            subprocess.Popen("update_script.bat", shell=True)
            self.root.quit()

        except Exception as e:
            messagebox.showerror("Update Error", f"Lỗi cập nhật: {e}")

    # --- CÁC HÀM CŨ GIỮ NGUYÊN ---
    def create_item_card(self, parent, item):
        card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        card.pack(fill="x", pady=4, padx=10)
        
        # Name & Info
        name_frame = tk.Frame(card, bg=COLOR_CARD)
        name_frame.pack(side="left", fill="x", expand=True)
        
        lbl_name = tk.Label(name_frame, text=item["name"], font=FONT_TITLE, bg=COLOR_CARD, fg="white", anchor="w")
        lbl_name.pack(side="left")
        
        lbl_info = tk.Label(name_frame, text="❓", font=("Segoe UI", 10), bg=COLOR_CARD, fg=COLOR_INFO, cursor="hand2")
        lbl_info.pack(side="left", padx=5)
        
        ToolTip(lbl_info, item.get("desc", ""))
        
        btn_box = ttk.Frame(card, style="Card.TFrame")
        btn_box.pack(side="right")

        # Logic nút bấm đặc biệt
        if "Việt hóa game" in item["name"] or "Game Translation" in item["name"]:
            txt = "⚡ Auto Install" if self.lang_code == "EN" else "⚡ Cài đặt thông minh"
            ttk.Button(btn_box, text=txt, style="Smart.TButton", command=self.install_translation_pack).pack(side="left", padx=4)
        if "Firmware" in item["name"]:
            txt = "⚡ Auto Install" if self.lang_code == "EN" else "⚡Chọn file nén để tự động chép."
            ttk.Button(btn_box, text=txt, command=self.install_firmware_local).pack(side="left", padx=4)

        # Biến để kiểm tra xem đã có link web nào chưa
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
            elif url.startswith("ACTION_SAVE_PC|"):
                actual_url = url.split("|")[1]
                cmd = lambda u=actual_url: self.download_pc_file_generic(u)
            elif url.startswith("ACTION_RUN_PC|"):
                actual_url = url.split("|")[1]
                cmd = lambda u=actual_url, n=item["name"]: self.process_run_pc(u, n)
            elif url.startswith("ACTION_FIX_"):
                cmd = lambda u=url: self.run_fix_task(u)
            else: 
                cmd = lambda u=url, n=item["name"], l=lbl: self.process_action(u, n, l)

            display_text = lbl
            is_web = "Web" in lbl or "Link" in lbl or "Hướng dẫn" in lbl or "Guide" in lbl or "GBAtemp" in lbl or "Cộng Đồng" in lbl or "TheTechGame" in lbl or "CheatSlips" in lbl or "Link tham khảo" in lbl
            
            # Logic mới cho các nút tải bước 1
            if "Bước 1" in lbl or "Step 1" in lbl:
                 is_web = True

            if not is_web:
                if "Fix" in url: 
                    display_text = lbl
                    btn_style = "Accent.TButton" 
                elif "Tự động" in lbl or "Auto" in lbl or "Tải" in lbl or "Download" in lbl or "Chọn" in lbl or "Pick" in lbl:
                    display_text = "⚡ " + lbl
                    btn_style = "Accent.TButton"
                else:
                    btn_style = "TButton"
            elif "Bước 1" in lbl or "Step 1" in lbl:
                display_text = "⬇️ " + lbl
                btn_style = "Accent.TButton"
            else:
                btn_style = "Web.TButton"
                has_manual_web_link = True # Đánh dấu là đã có nút web thủ công

            ttk.Button(btn_box, text=display_text, style=btn_style, command=cmd).pack(side="left", padx=2)

        # --- [TÍNH NĂNG MỚI] TỰ ĐỘNG THÊM NÚT "MỞ TRANG DOWNLOAD" ---
        # Logic: Quét các link tải, nếu thấy GitHub release thì tự suy ra link trang chủ
        detected_source_url = None
        for u in item["urls"].values():
            # Nếu là link tải trực tiếp từ GitHub (chứa releases/download)
            if "github.com" in u and "/releases/download/" in u:
                # Cắt chuỗi để lấy link thư mục releases
                # VD: .../releases/download/v1.0/file.zip -> .../releases
                detected_source_url = u.split("/releases/download/")[0] + "/releases"
                break
            # Nếu là link Github thông thường (không phải file zip, không phải Action)
            elif "github.com" in u and "ACTION" not in u and ".zip" not in u and ".nro" not in u:
                 detected_source_url = u
                 break

        # Chỉ thêm nút nếu tìm thấy link và (tùy chọn) chưa có nút Web nào khác để tránh trùng lặp
        # Ở đây tôi để hiện luôn để đảm bảo có nút "Download Page" như bạn yêu cầu
        if detected_source_url:
            txt_dl_page = "🌐 Download Page" if self.lang_code == "EN" else "🌐 Mở trang download"
            
            # Kiểm tra xem nút này đã tồn tại chưa để tránh trùng 2 nút dẫn đến cùng 1 link
            is_duplicate = False
            for existing_url in item["urls"].values():
                if existing_url == detected_source_url:
                    is_duplicate = True
            
            if not is_duplicate:
                ttk.Button(btn_box, text=txt_dl_page, style="Web.TButton", 
                           command=lambda u=detected_source_url: webbrowser.open(u)).pack(side="left", padx=2)

    def download_category_all(self, category_name):
        data_db = DATA_VI if self.lang_code == "VI" else DATA_EN
        text_db = UI_TEXT[self.lang_code]
        items = data_db.get(category_name, [])
        if not items: return
        
        msg = text_db["msg_confirm_dl_all"].format(category=category_name)
        if not messagebox.askyesno("Confirm", msg):
            return

        threading.Thread(target=self.process_download_all, args=(items,), daemon=True).start()

    def process_download_all(self, items):
        count = 0
        for item in items:
            for label, url in item["urls"].items():
                if "PC" in label or "Client" in label or "Web" in label or "Guide" in label or "Link" in label or "Hướng dẫn" in label:
                    continue
                # Bỏ qua các bước thủ công
                if "Bước 1" in label or "Step 1" in label or "Bước 2" in label or "Step 2" in label:
                    continue

                if "ACTION_SAVE_PC" in url or "ACTION_PICK_ZIP" in url or "ACTION_FIX" in url:
                    continue

                if url == "TESLA_ACTION":
                    self.root.after(0, lambda: self.status_label.config(text=f"Auto: Tesla Combo...", fg=COLOR_INFO))
                    self.run_tesla_thread(self.dest_path.get())
                    count += 1
                    continue
                elif url == "ULTRAHAND_ACTION":
                    self.root.after(0, lambda: self.status_label.config(text=f"Auto: Ultrahand Combo...", fg=COLOR_INFO))
                    self.run_ultrahand_thread(self.dest_path.get())
                    count += 1
                    continue
                
                self.download_task(item["name"], url, silent_success=False)
                count += 1
                import time
                time.sleep(1)

        self.root.after(0, lambda: messagebox.showinfo("Done", f"Started {count} tasks."))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def auto_detect_drive(self):
        text_db = UI_TEXT[self.lang_code]
        found_drive = None
        if sys.platform == 'win32':
            drives = [f"{chr(x)}:\\" for x in range(68, 91) if os.path.exists(f"{chr(x)}:\\")]
            for drive in drives:
                try:
                    dtype = ctypes.windll.kernel32.GetDriveTypeW(drive)
                    if dtype == 2: 
                        found_drive = drive
                        break
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
            threading.Thread(target=self.download_task, args=("File PC", url), kwargs={'custom_save_path': save_path}, daemon=True).start()

    def process_run_pc(self, url, name):
        if not messagebox.askyesno("Xác nhận cài đặt", f"Bạn có muốn tải và TỰ ĐỘNG CHẠY file cài đặt cho {name} không?"):
            return
        filename = "TegraRcmGUI_Installer.msi" 
        temp_dir = os.environ.get('TEMP', os.getcwd())
        save_path = os.path.join(temp_dir, filename)
        threading.Thread(target=self.download_task, 
                         args=(name, url), 
                         kwargs={'custom_save_path': save_path, 'auto_run': True}, 
                         daemon=True).start()

    def browse_folder(self):
        d = filedialog.askdirectory()
        if d: self.dest_path.set(d)

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
        
        # Nút "Bước 1" cũng là mở web
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
        
        threading.Thread(target=self.download_task, args=(name, url), daemon=True).start()

    def install_tesla_combo(self):
        root_path = self.dest_path.get()
        threading.Thread(target=self.run_tesla_thread, args=(root_path,), daemon=True).start()

    def run_tesla_thread(self, root_path):
        url1 = "https://github.com/ppkantorski/nx-ovlloader/releases/download/v2.0.0/nx-ovlloader+.zip"
        self.download_task("Tesla Loader", url1, silent_success=True)
        url2 = "https://github.com/WerWolv/Tesla-Menu/releases/download/v1.2.3/ovlmenu.zip"
        self.download_task("Tesla Menu UI", url2)

    def install_ultrahand_combo(self):
        root_path = self.dest_path.get()
        threading.Thread(target=self.run_ultrahand_thread, args=(root_path,), daemon=True).start()

    def run_ultrahand_thread(self, root_path):
        url1 = "https://github.com/ppkantorski/nx-ovlloader/releases/download/v2.0.0/nx-ovlloader+.zip"
        self.download_task("Ultrahand Loader", url1, silent_success=True)
        url2 = "https://github.com/ppkantorski/Ultrahand-Overlay/releases/latest/download/ovlmenu.ovl"
        self.download_task("Ultrahand Overlay", url2)

    def download_task(self, name, url, silent_success=False, custom_save_path=None, auto_run=False):
        try:
            if custom_save_path:
                save_path = custom_save_path
            else:
                root_path = self.dest_path.get()
                if not os.path.exists(root_path): os.makedirs(root_path)

            self.root.after(0, lambda: self.status_label.config(text=f"Connecting: {name}...", fg=COLOR_ACCENT))
            
            try:
                r = requests.get(url, stream=True, allow_redirects=True, timeout=30, headers=HEADERS)
                if r.status_code == 403:
                    self.root.after(0, lambda: messagebox.showinfo("Info", f"Server blocked auto-download.\nOpening browser..."))
                    webbrowser.open(url)
                    return
                content_type = r.headers.get('content-type', '')
                if 'text/html' in content_type:
                      self.root.after(0, lambda: messagebox.showinfo("Info", f"Browser verification required.\nOpening browser..."))
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
                is_7z = filename.lower().endswith(".7z")

                if is_nro: save_path = os.path.join(root_path, "switch", filename)
                elif is_ovl: save_path = os.path.join(root_path, "switch", ".overlays", filename)
                elif is_zip: save_path = os.path.join(root_path, "temp_download.zip")
                else: save_path = os.path.join(root_path, filename)

                if not os.path.exists(os.path.dirname(save_path)): os.makedirs(os.path.dirname(save_path))
            else:
                is_zip = save_path.lower().endswith(".zip")
                is_7z = save_path.lower().endswith(".7z")
                is_nro = False; is_ovl = False
                root_path = os.path.dirname(save_path)

            downloaded = 0
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        self.progress_var.set((downloaded / total_size) * 100)

            msg = ""
            if custom_save_path:
                msg = f"Downloaded: {os.path.basename(save_path)}"
                if auto_run:
                    self.root.after(0, lambda: self.status_label.config(text=f"Đang mở trình cài đặt...", fg=COLOR_SUCCESS))
                    try:
                        os.startfile(save_path)
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể mở file: {e}"))
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
            elif is_ovl: msg = f"Overlay Installed: {os.path.basename(save_path)}"
            elif is_nro: msg = f"Copied to /switch/: {os.path.basename(save_path)}"
            else: msg = f"Downloaded {os.path.basename(save_path)}."

            if not silent_success:
                self.root.after(0, lambda: self.status_label.config(text=f"Success: {name}", fg=COLOR_SUCCESS))

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error!", fg="red"))
            messagebox.showerror("Error", f"Detail: {str(e)}")

    def install_local_zip_generic(self, label_name):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        
        # [CẬP NHẬT] Cho phép chọn Zip, Rar, 7z
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

            # TRƯỜNG HỢP 1: File ZIP (Dùng thư viện có sẵn của Python cho nhanh)
            if f_lower.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as z: z.extractall(target_dir)
                extracted_ok = True

            # TRƯỜNG HỢP 2: File 7z hoặc RAR
            elif f_lower.endswith((".7z", ".rar")):
                # Ưu tiên 1: Dùng WinRAR/7-Zip cài trên máy (qua hàm có sẵn extract_archive_external)
                extracted_ok = self.extract_archive_external(file_path, target_dir)
                
                # Ưu tiên 2: Nếu không có WinRAR/7-Zip, thử dùng thư viện Python (nếu có)
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
                raise Exception("Không thể giải nén. Vui lòng cài đặt WinRAR hoặc 7-Zip trên máy tính!")

            self.root.after(0, lambda: self.status_label.config(text=f"Done {label}", fg=COLOR_SUCCESS))
            
            if label == "Firmware":
                 msg = UI_TEXT[self.lang_code]["msg_fw_done"]
                 messagebox.showinfo("Attention", msg)
            else:
                 messagebox.showinfo("Success", f"Installed {label}")

        except Exception as e: messagebox.showerror("Error", str(e))
    # [HÀM MỚI 1] Sự kiện khi bấm nút
    def install_linkalho_special(self):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        # Cho phép chọn mọi loại nén
        file_path = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.zip *.rar *.7z")])
        if file_path: 
            threading.Thread(target=self.process_linkalho_task, args=(file_path, root_path), daemon=True).start()

    # [HÀM MỚI 2] Xử lý giải nén lồng nhau (Nested Extraction)
    def process_linkalho_task(self, source_file, root_path):
        try:
            self.root.after(0, lambda: self.status_label.config(text="Processing Linkalho...", fg=COLOR_WARNING))
            
            # Tạo thư mục tạm
            temp_outer = os.path.join(root_path, "temp_linkalho_outer")
            temp_inner = os.path.join(root_path, "temp_linkalho_inner")
            if os.path.exists(temp_outer): shutil.rmtree(temp_outer)
            if os.path.exists(temp_inner): shutil.rmtree(temp_inner)
            os.makedirs(temp_outer)
            os.makedirs(temp_inner)

            # --- GIAI ĐOẠN 1: Giải nén File Mẹ (file vừa chọn) ---
            if not self.helper_extract_any(source_file, temp_outer):
                 raise Exception("Không thể giải nén file mẹ. Cần WinRAR/7Zip.")

            # --- GIAI ĐOẠN 2: Tìm file nén con (linkalho-v2.0.1...) ---
            inner_archive = None
            for root, dirs, files in os.walk(temp_outer):
                for f in files:
                    # Tìm file có tên chứa 'linkalho' và là file nén
                    if "linkalho" in f.lower() and f.lower().endswith((".zip", ".rar", ".7z")):
                        inner_archive = os.path.join(root, f)
                        break
                if inner_archive: break
            
            if not inner_archive:
                raise Exception("Không tìm thấy file nén con (linkalho-v...zip/rar/7z) bên trong.")

            # --- GIAI ĐOẠN 3: Giải nén File Con ---
            if not self.helper_extract_any(inner_archive, temp_inner):
                 raise Exception("Không thể giải nén file con bên trong.")

            # --- GIAI ĐOẠN 4: Tìm file .nro và chép vào switch/ ---
            nro_found = False
            switch_dir = os.path.join(root_path, "switch")
            if not os.path.exists(switch_dir): os.makedirs(switch_dir)

            for root, dirs, files in os.walk(temp_inner):
                for f in files:
                    if f.lower().endswith(".nro"):
                        src_nro = os.path.join(root, f)
                        shutil.copy2(src_nro, switch_dir)
                        nro_found = True
            
            # Dọn dẹp file rác
            try:
                shutil.rmtree(temp_outer)
                shutil.rmtree(temp_inner)
            except: pass

            if nro_found:
                self.root.after(0, lambda: self.status_label.config(text="Installed Linkalho!", fg=COLOR_SUCCESS))
                messagebox.showinfo("Success", "Đã cài đặt xong Linkalho (.nro) vào thư mục switch.")
            else:
                raise Exception("Không tìm thấy file .nro nào sau khi giải nén.")

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error", fg="red"))
            messagebox.showerror("Error", str(e))

    # [HÀM PHỤ] Hỗ trợ giải nén đa năng (tái sử dụng logic của extract_simple)
    def helper_extract_any(self, file_path, target_dir):
        f_lower = file_path.lower()
        extracted = False
        
        # 1. Thử dùng 7-Zip/WinRAR hệ thống trước (Mạnh nhất)
        if self.extract_archive_external(file_path, target_dir):
            return True

        # 2. Nếu thất bại, thử dùng thư viện Python
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
        if not os.path.exists(root_path): return messagebox.showwarning("Warning", "Select Root first!")
        
        # Tạo cửa sổ chọn
        win = tk.Toplevel(self.root)
        win.title("Chọn nguồn cài đặt")
        
        # FIX 2: Tăng chiều rộng và chiều cao lên 500x220 để không bị cắt chữ
        win.geometry("500x220") 
        win.configure(bg=COLOR_CARD)
        
        # Canh giữa popup (tính lại theo kích thước mới 500x220)
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 110
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text="Bạn muốn chọn File Nén hay Thư Mục?", bg=COLOR_CARD, fg="white", font=("Segoe UI", 11)).pack(pady=(20, 5))
        
        # FIX 2 (Tiếp): Thêm wraplength=480 để text tự xuống dòng nếu quá dài
        tk.Label(win, text="(Hệ thống sẽ tự nhận diện ra file việt hóa trong thư mục để chép vào thẻ nhớ)", 
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

        ttk.Button(btn_frame, text="📄 File Nén (Zip/Rar...)", command=on_zip).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="📂 Thư Mục (Folder)", command=on_folder).pack(side="left", padx=10)

    # --- HÀM GIÚP: Giải nén bằng lệnh hệ thống (Tối ưu cho Windows User) ---
    def extract_archive_external(self, source_file, dest_dir):
        """Dùng WinRAR hoặc 7-Zip đã cài đặt để giải nén"""
        
        # Đường dẫn phổ biến
        seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
        winrar_path = r"C:\Program Files\WinRAR\WinRAR.exe"
        
        cmd = None
        
        if os.path.exists(seven_zip_path):
            # 7z command: x "file" -o"dest" -y
            cmd = [seven_zip_path, "x", source_file, f"-o{dest_dir}", "-y"]
            print("Using 7-Zip...")
            
        elif os.path.exists(winrar_path):
            # WinRAR command: x -ibck "file" "dest\"
            # Lưu ý WinRAR cần dest có dấu \ ở cuối nếu muốn vào folder
            cmd = [winrar_path, "x", "-ibck", source_file, dest_dir + "\\"]
            print("Using WinRAR...")
        
        if cmd:
            try:
                # Chạy lệnh ẩn cửa sổ console
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
            
            # Hàm check ID Game chặt chẽ bằng Regex (Bắt đầu 0100 và đủ 16 ký tự hex)
            def is_game_id_strict(name):
                # Chấp nhận đúng 16 ký tự hex bắt đầu bằng 0100
                return bool(re.match(r'^0100[0-9A-Fa-f]{12}$', name))

            # Xác định tên đầu vào (để xử lý trường hợp user chọn file zip trùng tên ID)
            input_name = os.path.basename(os.path.normpath(source))
            if source_type == "file":
                # Nếu là file zip, lấy tên file bỏ đuôi (vd: 0100...zip -> 0100...)
                input_name = os.path.splitext(input_name)[0]

            search_path = source
            temp_dir = ""

            # Xử lý file nén
            if source_type == "file":
                temp_dir = os.path.join(root_path, "temp_translation_extract")
                if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
                os.makedirs(temp_dir)

                # --- Ưu tiên 1: Dùng lệnh hệ thống ---
                extracted_ok = False
                if source.lower().endswith(".7z") or source.lower().endswith(".rar"):
                    extracted_ok = self.extract_archive_external(source, temp_dir)
                
                # --- Ưu tiên 2: Dùng thư viện Python ---
                if not extracted_ok:
                    if source.lower().endswith(".zip"):
                        with zipfile.ZipFile(source, 'r') as z: z.extractall(temp_dir)
                    elif source.lower().endswith(".7z"):
                        try:
                            import py7zr
                            with py7zr.SevenZipFile(source, mode='r') as z: z.extractall(path=temp_dir)
                        except ImportError:
                            messagebox.showerror("Lỗi thiếu thư viện", "Máy bạn không có 7-Zip/WinRAR và thiếu thư viện py7zr.")
                            return     
                    elif source.lower().endswith(".rar"):
                        try:
                            import rarfile
                            r = rarfile.RarFile(source)
                            r.extractall(temp_dir)
                        except:
                             messagebox.showerror("Lỗi RAR", f"Vui lòng cài WinRAR vào máy tính.")
                             return
                
                search_path = temp_dir

            # --- LOGIC CÀI ĐẶT THÔNG MINH ---
            contents_dir = os.path.join(root_path, "atmosphere", "contents")
            if not os.path.exists(contents_dir): os.makedirs(contents_dir)
            
            found_count = 0

            # 1. TRƯỜNG HỢP: Tên file/folder chọn chính là ID Game
            if is_game_id_strict(input_name):
                dest_game_path = os.path.join(contents_dir, input_name)
                
                # Nếu User chọn folder (không nén)
                if source_type == "folder":
                    if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                    shutil.copytree(source, dest_game_path, dirs_exist_ok=True)
                    found_count = 1
                    
                # Nếu User chọn file nén (đã giải nén vào temp_dir)
                else: 
                    # Kiểm tra xem bên trong temp_dir có folder con trùng tên ID không?
                    nested_path = os.path.join(temp_dir, input_name)
                    if os.path.exists(nested_path) and os.path.isdir(nested_path):
                        # Trường hợp file zip: 0100...zip/0100.../romfs
                        if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                        shutil.copytree(nested_path, dest_game_path, dirs_exist_ok=True)
                        found_count = 1
                    else:
                        # Trường hợp file zip: 0100...zip/romfs (Nội dung nằm ngay root zip)
                        # Copy toàn bộ nội dung temp vào dest_game_path
                        if not os.path.exists(dest_game_path): os.makedirs(dest_game_path)
                        self.copy_tree_custom(temp_dir, dest_game_path)
                        found_count = 1

            # 2. TRƯỜNG HỢP: Quét sâu (Deep Search) - Nếu tên file không phải ID hoặc quét hàng loạt
            else:
                for root, dirs, files in os.walk(search_path):
                    for dirname in dirs[:]:
                        if is_game_id_strict(dirname):
                            src_game_path = os.path.join(root, dirname)
                            dest_game_path = os.path.join(contents_dir, dirname)
                            
                            if os.path.exists(dest_game_path): shutil.rmtree(dest_game_path)
                            shutil.copytree(src_game_path, dest_game_path, dirs_exist_ok=True)
                            found_count += 1
                            dirs.remove(dirname) # Không quét sâu vào ID game nữa

            # Dọn dẹp
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            if found_count > 0:
                self.root.after(0, lambda: self.status_label.config(text=f"Installed {found_count} translations!", fg=COLOR_SUCCESS))
                messagebox.showinfo("Success", f"Đã cài đặt thành công {found_count} gói ngôn ngữ vào atmosphere/contents.")
            else:
                self.root.after(0, lambda: self.status_label.config(text="No translation found.", fg=COLOR_WARNING))
                messagebox.showwarning("Failed", "Không tìm thấy nội dung Việt Hóa hợp lệ.\nHãy chắc chắn tên file/folder là ID Game (0100...) hoặc bên trong có chứa folder ID Game.")

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Error", fg="red"))
            messagebox.showerror("Error", str(e))

    def is_game_id(self, name):
        # Giữ lại hàm cũ để tương thích nếu có chỗ gọi, nhưng logic chính đã dùng is_game_id_strict bên trong
        return bool(re.match(r'^[0-9a-fA-F]{16}$', name))

    def copy_tree_custom(self, src, dst):
        if not os.path.exists(dst): os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s): self.copy_tree_custom(s, d)
            else: shutil.copy2(s, d)

    def run_fix_task(self, fix_type):
        root_path = self.dest_path.get()
        if not os.path.exists(root_path):
            messagebox.showerror("Error", "Select SD Root first!")
            return

        # LOGIC FIX: CÀI LẠI GÓI HACK
        if fix_type == "ACTION_FIX_REINSTALL_PACK":
            msg = "To fix completely, reinstall the AIO Pack.\nApp will scroll to top." if self.lang_code == "EN" else "Để sửa lỗi triệt để nhất, bạn nên cài lại gói hack chuẩn.\nPhần mềm sẽ đưa bạn đến mục trên cùng."
            messagebox.showinfo("Reinstall Pack", msg)
            self.canvas.yview_moveto(0) 
            return

        msg_confirm = "This will modify/delete files on SD card.\nContinue?" if self.lang_code == "EN" else "Hành động này sẽ thay đổi/xóa file trên thẻ nhớ để sửa lỗi.\nBạn có chắc chắn muốn tiếp tục không?"
        if not messagebox.askyesno("Confirm", msg_confirm):
            return

        try:
            msg = "Done!"
            atm_contents = os.path.join(root_path, "atmosphere", "contents")
            
            if fix_type == "ACTION_FIX_THEMES":
                theme_id = "0100000000001000"
                target = os.path.join(atm_contents, theme_id)
                if os.path.exists(target):
                    shutil.rmtree(target)
                    msg = "Deleted Theme. Please reboot."
                else:
                    msg = "Theme folder not found."

            elif fix_type == "ACTION_FIX_DELETE_ALL_CONTENTS":
                msg_warn = "WARNING: Wiping atmosphere/contents.\nAll mods/cheats/sysmodules will be lost.\nProceed?" if self.lang_code == "EN" else "CẢNH BÁO: XÓA SẠCH thư mục atmosphere/contents.\nMất toàn bộ Sysmod, Việt Hóa, Cheat.\nTiếp tục?"
                if messagebox.askyesno("EXTREME WARNING", msg_warn):
                    if os.path.exists(atm_contents):
                        shutil.rmtree(atm_contents)
                        os.makedirs(atm_contents)
                        msg = "Wiped Contents folder."
                    else:
                        os.makedirs(atm_contents)
                        msg = "Folder created."

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
                msg = f"Removed {deleted_count} common sysmodules."

            elif fix_type == "ACTION_FIX_CHEATS":
                deleted_count = 0
                if os.path.exists(atm_contents):
                    for game_id in os.listdir(atm_contents):
                        cheat_path = os.path.join(atm_contents, game_id, "cheats")
                        if os.path.exists(cheat_path):
                            shutil.rmtree(cheat_path)
                            deleted_count += 1
                msg = f"Deleted cheats for {deleted_count} games."

            elif fix_type == "ACTION_FIX_MAC_JUNK":
                deleted_count = 0
                for root, dirs, files in os.walk(root_path):
                    for file in files:
                        if file.startswith("._") or file == ".DS_Store":
                            try:
                                os.remove(os.path.join(root, file))
                                deleted_count += 1
                            except: pass
                msg = f"Cleaned {deleted_count} MacOS junk files."

            messagebox.showinfo("Result", msg)

        except Exception as e:
            messagebox.showerror("Fix Error", str(e))

if __name__ == "__main__":
    # [QUAN TRỌNG] Đặt ID cho App TRƯỚC khi tạo cửa sổ
    # Việc này giúp Windows nhận diện icon dưới Taskbar ngay lập tức
    try:
        myappid = 'tsufu.switch.update.manager.pro.v1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except: 
        pass

    # Sau đó mới tạo cửa sổ
    root = tk.Tk()
    app = SwitchToolApp(root)
    root.mainloop()