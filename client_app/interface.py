import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from client_app.utils import ClientUtils
except ImportError:
    from utils import ClientUtils

from shared.security_utils import CryptoManager


SECRET_KEY = b"SI_O8XF6eL3_S2N9yJ4-uX0zR1vL5mN8qA2cW4bP6k8="
SERVER_URL = "http://127.0.0.1:8000/receive_murojaat"

crypto = CryptoManager(SECRET_KEY)


class MijozIlovasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aholi Murojaat Tizimi - Xavfsiz mijoz")
        self.geometry("800x700")
        self.selected_file_path = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        self.header_label = ctk.CTkLabel(
            self.main_container,
            text="Yangi murojaat shakli",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.header_label.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(
            self.main_container,
            text="Barcha ma'lumotlar shifrlangan holda yuboriladi",
            text_color="gray",
        )
        self.info_label.pack(pady=(0, 20))

        self.label_text = ctk.CTkLabel(self.main_container, text="Murojaat matni:", font=("Arial", 14))
        self.label_text.pack(anchor="w", padx=40)

        self.text_editor = ctk.CTkTextbox(
            self.main_container,
            width=700,
            height=250,
            border_width=2,
            corner_radius=10,
        )
        self.text_editor.pack(padx=40, pady=10)

        self.file_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.file_frame.pack(fill="x", padx=40, pady=10)

        self.btn_attach = ctk.CTkButton(
            self.file_frame,
            text="Fayl biriktirish (PDF, IMG)",
            command=self.choose_file,
            width=220,
            fg_color="#3d5a80",
            hover_color="#293241",
        )
        self.btn_attach.pack(side="left")

        self.file_info = ctk.CTkLabel(self.file_frame, text="Fayl tanlanmagan", text_color="gray")
        self.file_info.pack(side="left", padx=20)

        self.btn_send = ctk.CTkButton(
            self.main_container,
            text="Murojaatni shifrlash va yuborish",
            command=self.process_and_send,
            height=50,
            width=300,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
        )
        self.btn_send.pack(pady=40)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Murojaatga tegishli faylni tanlang",
            filetypes=[("Hujjat va Rasmlar", "*.pdf *.png *.jpg *.jpeg")],
        )
        if not file_path:
            return

        is_valid, validation_message = ClientUtils.validate_file(file_path)
        if not is_valid:
            messagebox.showwarning("Fayl xatosi", validation_message)
            return

        self.selected_file_path = file_path
        filename = os.path.basename(file_path)
        icon = ClientUtils.get_file_icon(file_path)
        self.file_info.configure(text=f"{icon} Tanlandi: {filename}", text_color="#3498db")

    def process_and_send(self):
        murojaat_matni = self.text_editor.get("1.0", "end-1c").strip()

        if not murojaat_matni:
            messagebox.showwarning("Xatolik", "Murojaat matni bo'sh bo'lishi mumkin emas!")
            return

        file_handle = None
        try:
            cleaned_text = ClientUtils.clean_text(murojaat_matni)
            encrypted_content = crypto.encrypt_data(cleaned_text)

            data = {"message": encrypted_content}
            files = None

            if self.selected_file_path:
                file_handle = open(self.selected_file_path, "rb")
                files = {"file": (os.path.basename(self.selected_file_path), file_handle)}

            response = requests.post(SERVER_URL, data=data, files=files, timeout=15)
            response.raise_for_status()
            result = response.json()

            messagebox.showinfo(
                "Muvaffaqiyatli",
                f"Murojaat yuborildi. AI toifasi: {result.get('category', 'Nomalum')}",
            )
            self.clear_form()
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Xato",
                "Server ishlamayapti. Avval serverni ishga tushiring:\n"
                "uvicorn server_app.main:app --host 127.0.0.1 --port 8000",
            )
        except requests.exceptions.HTTPError as e:
            try:
                detail = e.response.json().get("detail", str(e))
            except Exception:
                detail = str(e)
            messagebox.showerror("Xato", f"Server xatosi: {detail}")
        except Exception as e:
            messagebox.showerror("Xato", f"Yuborishda xatolik yuz berdi: {str(e)}")
        finally:
            if file_handle:
                file_handle.close()

    def clear_form(self):
        self.text_editor.delete("1.0", "end")
        self.selected_file_path = None
        self.file_info.configure(text="Fayl tanlanmagan", text_color="gray")


if __name__ == "__main__":
    app = MijozIlovasi()
    app.mainloop()
