%%writefile app.py
%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import sympy as sp

# ==========================================
# 1. KONFIGURASI HALAMAN & JUDUL UTAMA
# ==========================================
st.set_page_config(page_title="Project UAS Matematika Komputasi", layout="centered")

st.title("🖥️ Project UAS Matematika Komputasi")
st.subheader("Aplikasi Metode Numerik Interaktif Berbasis Web untuk Menentukan Akar Persamaan Nonlinier")

# Menampilkan nama kelompok sesuai dengan laporan UAS Anda
st.markdown("""
**Nama Kelompok:**
1. Nadin Nur Indah
2. Destiana Lingga Sari
3. Rezza Ramadani
""")
st.markdown("---")

# ==========================================
# 2. NAVIGASI MENU SIDEBAR (PILIH METODE)
# ==========================================
st.sidebar.title("🧭 Navigasi Metode")
menu = st.sidebar.selectbox(
    "Pilih Metode Numerik yang Ingin Diuji:",
    ("Metode Bisection (Bagi Dua)", "Metode Newton-Raphson", "Metode Secant (Tali Busur)")
)

# ==========================================
# 3. LOGIKA OPERASIONAL MASING-MASING METODE
# ==========================================

# ------------------------------------------
# A. KODE UNTUK METODE BISECTION
# ------------------------------------------
if menu == "Metode Bisection (Bagi Dua)":
    st.header("🧮 Metode Bisection (Bagi Dua)")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="bis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Batas Bawah (a):", value=2.0)
    with col2:
        b = st.number_input("Batas Atas (b):", value=3.0)
    with col3:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    def f_bis(x_val):
        x = x_val
        return eval(fungsi_input)

    if st.button("Hitung Akar dengan Bisection"):
        try:
            if f_bis(a) * f_bis(b) >= 0:
                st.error("❌ Nilai f(a) dan f(b) harus berlawanan tanda! Interval awal tidak mengurung akar.")
            else:
                konten_tabel = []
                iterasi = 0
                while abs(b - a) >= toleransi and iterasi < 100:
                    iterasi += 1
                    c = (a + b) / 2
                    fc = f_bis(c)
                    
                    konten_tabel.append({
                        "Iterasi": iterasi,
                        "Batas Bawah (a)": round(a, 6),
                        "Batas Atas (b)": round(b, 6),
                        "Titik Tengah (c)": round(c, 6),
                        "f(c)": round(fc, 6),
                        "Lebar Interval": round(abs(b - a), 6)
                    })
                    
                    if f_bis(a) * fc < 0:
                        b = c
                    else:
                        a = c
                
                st.success(f"✅ Konvergen! Akar persamaan ditemukan pada x = **{c:.6f}**")
                st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)
        except Exception as e:
            st.error(f"Sintaks rumus salah atau terjadi error perhitungan: {e}")

# ------------------------------------------
# B. KODE UNTUK METODE NEWTON-RAPHSON
# ------------------------------------------
elif menu == "Metode Newton-Raphson":
    st.header("📈 Metode Newton-Raphson")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="nr")
    
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("Tebakan Awal (x0):", value=2.0)
    with col2:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    x_simbol = sp.symbols('x')
    try:
        ekspresi = sp.sympify(fungsi_input)
        turunan_ekspresi = sp.diff(ekspresi, x_simbol)
        st.info(f"🔍 **Turunan f'(x) Otomatis Berhasil Dibuat:** `{turunan_ekspresi}`")
    except Exception as e:
        st.error(f"Sintaks fungsi bermasalah: {e}")
        ekspresi = None

    def f_nr(x_val):
        x = x_val
        return eval(fungsi_input)

    def df_nr(x_val):
        x = x_val
        return eval(str(turunan_ekspresi))

    if ekspresi is not None and st.button("Hitung Akar dengan Newton-Raphson"):
        try:
            konten_tabel = []
            x_sekarang = x0
            iterasi = 0
            
            while iterasi < 100:
                iterasi += 1
                fx = f_nr(x_sekarang)
                dfx = df_nr(x_sekarang)
                
                if dfx == 0:
                    st.error("❌ Turunan f'(x) bernilai 0! Perhitungan dihentikan agar tidak pembagian dengan nol.")
                    break
                    
                x_baru = x_sekarang - (fx / dfx)
                galat = abs(x_baru - x_sekarang)
                
                konten_tabel.append({
                    "Iterasi": iterasi,
                    "x_n": round(x_sekarang, 6),
                    "f(x_n)": round(fx, 6),
                    "f'(x_n)": round(dfx, 6),
                    "x_(n+1)": round(x_baru, 6),
                    "Galat (Error)": round(galat, 6)
                })
                
                if galat < toleransi:
                    st.success(f"✅ Konvergen! Akar persamaan ditemukan pada x = **{x_baru:.6f}**")
                    break
                x_sekarang = x_baru
                
            st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)
        except Exception as e:
            st.error(f"Terjadi kesalahan kalkulasi: {e}")

# ------------------------------------------
# C. KODE UNTUK METODE SECANT
# ------------------------------------------
elif menu == "Metode Secant (Tali Busur)":
    st.header("📐 Metode Secant")
    
    fungsi_input = st.text_input("Masukkan fungsi f(x):", value="x**3 - 4*x - 9", key="sec")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x0 = st.number_input("Tebakan Awal Pertama (x0):", value=2.0)
    with col2:
        x1 = st.number_input("Tebakan Awal Kedua (x1):", value=3.0)
    with col3:
        toleransi = st.number_input("Toleransi:", value=0.0001, format="%.4f")

    def f_sec(x_val):
        x = x_val
        return eval(fungsi_input)

    if st.button("Hitung Akar dengan Secant"):
        try:
            konten_tabel = []
            x_min1 = x0
            x_sekarang = x1
            iterasi = 0
            
            while iterasi < 100:
                iterasi += 1
                fx_min1 = f_sec(x_min1)
                fx_sekarang = f_sec(x_sekarang)
                
                if (fx_sekarang - fx_min1) == 0:
                    st.error("❌ Pembagi (f(x_n) - f(x_n-1)) bernilai 0! Perhitungan tidak bisa dilanjutkan.")
                    break
                    
                x_baru = x_sekarang - (fx_sekarang * (x_sekarang - x_min1)) / (fx_sekarang - fx_min1)
                galat = abs(x_baru - x_sekarang)
                
                konten_tabel.append({
                    "Iterasi": iterasi,
                    "x_(n-1)": round(x_min1, 6),
                    "x_n": round(x_sekarang, 6),
                    "x_(n+1)": round(x_baru, 6),
                    "Galat (Error)": round(galat, 6)
                })
                
                if galat < toleransi:
                    st.success(f"✅ Konvergen! Akar persamaan ditemukan pada x = **{x_baru:.6f}**")
                    break
                    
                x_min1 = x_sekarang
                x_sekarang = x_baru
                
            st.dataframe(pd.DataFrame(konten_tabel), use_container_width=True)
        except Exception as e:
            st.error(f"Terjadi kesalahan kalkulasi: {e}")
