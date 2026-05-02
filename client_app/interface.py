import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import requests  # Server bilan aloqa uchun
from shared.security_utils import CryptoManager

# Eslatma: Bu kalit serverdagi kalit bilan bir xil bo'lishi shart
# Key_generator.py orqali olingan kalitni shu yerga qo'ying
SECRET_KEY = b'SI_O8XF6eL3_S2N9yJ4-uX0zR1vL5mN8qA2cW4bP6k8=' 
crypto = CryptoManager(SECRET_KEY)

class MijozIlovasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Oyna sozlamalari
        self.title("Aholi Murojaat Tizimi - Xavfsiz mijoz")
        self.geometry("800x700")
        
        # Grid konfiguratsiyasi
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Asosiy Frame
        self.main_container = ctk.CTkFrame(self, corner_radius=15)
        self.main_container.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        
        # Sarlavha
        self.header_label = ctk.CTkLabel(
            self.main_container, 
            text="Yangi murojaat shakli", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(pady=(20, 10))

        self.info_label = ctk.CTkLabel(
            self.main_container, 
            text="Barcha ma'lumotlar AES algoritmi orqali shifrlanadi", 
            text_color="gray"
        )
        self.info_label.pack(pady=(0, 20))

        # 1. Matn redaktori qismi
        self.label_text = ctk.CTkLabel(self.main_container, text="Murojaat matni:", font=("Arial", 14))
        self.label_text.pack(anchor="w", padx=40)
        
        self.text_editor = ctk.CTkTextbox(
            self.main_container, 
            width=700, 
            height=250, 
            border_width=2,
            corner_radius=10
        )
        self.text_editor.pack(padx=40, pady=10)

        # 2. Fayl biriktirish qismi
        self.file_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.file_frame.pack(fill="x", padx=40, pady=10)

        self.btn_attach = ctk.CTkButton(
            self.file_frame, 
            text="📁 Fayl biriktirish (PDF, IMG)", 
            command=self.choose_file,
            width=200,
            fg_color="#3d5a80",
            hover_color="#293241"
        )
        self.btn_attach.pack(side="left")

        self.file_info = ctk.CTkLabel(self.file_frame, text="Fayl tanlanmagan", text_color="gray")
        self.file_info.pack(side="left", padx=20)

        # 3. Yuborish tugmasi
        self.btn_send = ctk.CTkButton(
            self.main_container, 
            text="Murojaatni shifrlash va yuborish", 
            command=self.process_and_send,
            height=50,
            width=300,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.btn_send.pack(pady=40)

        # O'zgaruvchilar
        self.selected_file_path = None

    def choose_file(self):
        """Fayl tanlash muloqot oynasi"""
        file_path = filedialog.askopenfilename(
            title="Murojaatga tegishli faylni tanlang",
            filetypes=[("Hujjat va Rasmlar", "*.pdf *.png *.jpg *.jpeg")]
        )
        if file_path:
            self.selected_file_path = file_path
            filename = os.path.basename(file_path)
            self.file_info.configure(text=f"Tanlandi: {filename}", text_color="#3498db")

    def process_and_send(self):
        """Ma'lumotni shifrlash va serverga jo'natish mantiqi"""
        murojaat_matni = self.text_editor.get("1.0", "end-1c").strip()
        
        if not murojaat_matni:
            messagebox.showwarning("Xatolik", "Murojaat matni bo'sh bo'lishi mumkin emas!")
            return

        try:
            # 1. Matnni shifrlash
            encrypted_content = crypto.encrypt_data(murojaat_matni)
            
            # 2. Ma'lumotlarni paketlash (Serverga yuborish uchun)
            # Fayl bo'lsa uni multipart sifatida yuboramiz
            data = {"message": encrypted_content}
            files = None
            
            if self.selected_file_path:
                files = {'file': open(self.selected_file_path, 'rb')}

            # 3. Serverga POST so'rovi (Hozircha test rejimida)
            # Eslatma: Server ishga tushgach URL o'zgartiriladi
            server_url = "http://127.0.0.1:8000/receive_murojaat"
            
            # Bu qism server tayyor bo'lganda ishlaydi:
            # response = requests.post(server_url, data=data, files=files)
            
            # Hozircha terminalda natijani ko'ramiz
            print(f"--- Shifrlangan xabar ---\n{encrypted_content}\n-------------------------")
            
            messagebox.showinfo("Muvaffaqiyatli", "Murojaat shifrlangan holda yuborildi!")
            
            # Shaklni tozalash
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Xato", f"Yuborishda xatolik yuz berdi: {str(e)}")

    def clear_form(self):
        """Shaklni tozalash"""
        self.text_editor.delete("1.0", "end")
        self.selected_file_path = None
        self.file_info.configure(text="Fayl tanlanmagan", text_color="gray")

if __name__ == "__main__":
    app = MijozIlovasi()
    app.mainloop()