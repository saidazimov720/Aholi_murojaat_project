import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server_app.database import DatabaseManager
from shared.security_utils import CryptoManager


SECRET_KEY = b"SI_O8XF6eL3_S2N9yJ4-uX0zR1vL5mN8qA2cW4bP6k8="

crypto = CryptoManager(SECRET_KEY)
db = DatabaseManager()

st.set_page_config(page_title="Admin Panel - Aholi Murojaati", layout="wide")

st.title("Murojaatlarni boshqarish tizimi")
st.sidebar.header("Filterlar")

st.subheader("Kelib tushgan murojaatlar")
murojaatlar = db.get_all_murojaatlar()

col1, col2, col3, col4 = st.columns([1, 2, 4, 2])
col1.markdown("**ID**")
col2.markdown("**Foydalanuvchi**")
col3.markdown("**Asl Murojaat (Deshifrlangan)**")
col4.markdown("**AI Toifasi**")

for item in murojaatlar:
    murojaat_id, user, encrypted_msg, file_path, category, vaqt = item
    try:
        decrypted = crypto.decrypt_data(encrypted_msg)
    except Exception:
        decrypted = "Xato: Kalit mos kelmadi"

    with st.container():
        c1, c2, c3, c4 = st.columns([1, 2, 4, 2])
        c1.write(murojaat_id)
        c2.write(user)
        c3.info(decrypted)
        c4.warning(category)
        if file_path:
            st.caption(f"Fayl: {file_path}")

st.divider()
st.subheader("Analitika")

if murojaatlar:
    chart_data = pd.DataFrame(
        murojaatlar,
        columns=["ID", "Foydalanuvchi", "Matn", "Fayl", "Toifa", "Vaqt"],
    )
    chart_data = chart_data.groupby("Toifa").size().reset_index(name="Soni")
    st.bar_chart(data=chart_data, x="Toifa", y="Soni")
else:
    st.info("Hali murojaatlar kelib tushmagan.")
