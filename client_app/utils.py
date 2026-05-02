import os
from tkinter import messagebox

class ClientUtils:
    """
    Mijoz ilovasi uchun yordamchi funksiyalar
    """
    
    # Ruxsat etilgan fayl formatlari
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
    # Maksimal fayl hajmi (masalan, 5 MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024 

    @staticmethod
    def validate_file(file_path):
        """
        Tanlangan faylni format va hajm bo'yicha tekshiradi
        """
        if not file_path:
            return False, "Fayl tanlanmagan"

        # Formatni tekshirish
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ClientUtils.ALLOWED_EXTENSIONS:
            return False, f"Noma'lum format: {ext}. Faqat PDF va Rasmlar (JPG, PNG) mumkin."

        # Hajmni tekshirish
        file_size = os.path.getsize(file_path)
        if file_size > ClientUtils.MAX_FILE_SIZE:
            return False, "Fayl hajmi juda katta (Maksimal 5 MB bo'lishi kerak)"

        return True, "Fayl qabul qilindi"

    @staticmethod
    def get_file_icon(file_path):
        """
        Fayl kengaytmasiga qarab ikonka nomini qaytaradi (interfeys uchun)
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return "📄"
        else:
            return "🖼️"

    @staticmethod
    def clean_text(text):
        """
        Matndagi ortiqcha bo'shliqlarni va zararli belgilarni tozalash
        """
        if not text:
            return ""
        # Ortiqcha bo'shliqlarni olib tashlash
        cleaned = " ".join(text.split())
        return cleaned

    @staticmethod
    def log_event(message):
        """
        Dastur ichidagi jarayonlarni terminalga chiqarish (debugging uchun)
        """
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] LOG: {message}")