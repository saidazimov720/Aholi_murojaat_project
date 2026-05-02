import customtkinter as ctk
from interface import MijozIlovasi
import os

def initialize_app():
    """
    Ilovani ishga tushirishdan oldin kerakli sozlamalarni yuklash
    """
    # 1. Tashqi ko'rinishni sozlash
    ctk.set_appearance_mode("dark")  # "light" yoki "dark"
    ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue"

    # 2. Uploads papkasi mavjudligini tekshirish (fayllar vaqtincha saqlanishi uchun)
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

def main():
    # Ilovani sozlash
    initialize_app()

    # Interfeysni yaratish
    app = MijozIlovasi()
    
    # Ilovani sarlavhasini va o'lchamini qayta tekshirish (ixtiyoriy)
    app.title("Aholi Murojaat Tizimi v1.0 (Xavfsiz ulanish)")
    
    # Asosiy siklni ishga tushirish
    try:
        app.mainloop()
    except Exception as e:
        print(f"Dastur ishlashida xatolik yuz berdi: {e}")

if __name__ == "__main__":
    main()