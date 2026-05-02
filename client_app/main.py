import os
import sys
from pathlib import Path

import customtkinter as ctk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from client_app.interface import MijozIlovasi
except ImportError:
    from interface import MijozIlovasi


def initialize_app():
    """
    Ilovani ishga tushirishdan oldin kerakli sozlamalarni yuklash
    """
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")


def main():
    initialize_app()

    app = MijozIlovasi()
    app.title("Aholi Murojaat Tizimi v1.0 (Xavfsiz ulanish)")

    try:
        app.mainloop()
    except Exception as e:
        print(f"Dastur ishlashida xatolik yuz berdi: {e}")


if __name__ == "__main__":
    main()
