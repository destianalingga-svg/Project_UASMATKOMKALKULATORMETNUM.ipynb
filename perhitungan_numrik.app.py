# Import Library
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy as sp

# Judul Aplikasi

st.title("Project UAS Matematika Komputasi")

st.write("""
Aplikasi ini digunakan untuk mencari akar persamaan nonlinier menggunakan:

1. Metode Bisection
2. Metode Newton-Raphson
3. Metode Secant
""")

# Memilih Metode

metode = st.selectbox(
    "Pilih metode yang akan digunakan:",
    [
        "Bisection",
        "Newton-Raphson",
        "Secant",
        "Perbandingan Metode"
    ]
)

# Metode Bisection

if metode == "Bisection":

    st.header("Metode Bisection")

    # Input Data dari Pengguna

    fungsi = st.text_input(
        "Masukkan fungsi",
        value="x**3 - 4*x - 9"
    )

    batas_bawah = st.number_input(
        "Masukkan batas bawah",
        value=2.0
    )

    batas_atas = st.number_input(
        "Masukkan batas atas",
        value=3.0
    )

    toleransi = st.number_input(
        "Masukkan toleransi",
        value=0.0001,
        format="%.4f"
    )

    # Perhitungan Metode Bisection

    if st.button("Hitung Bisection"):

        def hitung_fungsi(x):
            return eval(fungsi)

        if hitung_fungsi(batas_bawah) * hitung_fungsi(batas_atas) > 0:

            st.error(
                "Interval tidak memenuhi syarat Metode Bisection"
            )

        else:

            data_iterasi = []

            jumlah_iterasi = 0

            bawah = batas_bawah
            atas = batas_atas

            while abs(atas - bawah) > toleransi:

                titik_tengah = (
                    bawah + atas
                ) / 2

                data_iterasi.append([
                    jumlah_iterasi + 1,
                    bawah,
                    atas,
                    titik_tengah
                ])

                if (
                    hitung_fungsi(bawah)
                    * hitung_fungsi(titik_tengah)
                    < 0
                ):
                    atas = titik_tengah
                else:
                    bawah = titik_tengah

                jumlah_iterasi += 1

            akar = (
                bawah + atas
            ) / 2

            st.success(
                f"Akar persamaan = {akar:.6f}"
            )

            st.write(
                f"Jumlah iterasi = {jumlah_iterasi}"
            )

            # Menampilkan Tabel Iterasi

            tabel_iterasi = pd.DataFrame(
                data_iterasi,
                columns=[
                    "Iterasi",
                    "Batas Bawah",
                    "Batas Atas",
                    "Titik Tengah"
                ]
            )

            st.dataframe(tabel_iterasi)

            # Menampilkan Grafik Fungsi

            x = np.linspace(
                bawah - 2,
                atas + 2,
                400
            )

            y = [
                hitung_fungsi(nilai_x)
                for nilai_x in x
            ]

            plt.figure(figsize=(8,5))

            plt.plot(x, y)

            plt.axhline(y=0)

            plt.title("Grafik Fungsi")

            plt.xlabel("Nilai x")

            plt.ylabel("Nilai f(x)")

            plt.grid()

            st.pyplot(plt)

# Metode Newton-Raphson

if metode == "Newton-Raphson":

    st.header("Metode Newton-Raphson")

    # Input Data dari Pengguna

    fungsi = st.text_input(
        "Masukkan fungsi",
        value="x**3 - 4*x - 9",
        key="nr_fungsi"
    )

    tebakan_awal = st.number_input(
        "Masukkan tebakan awal",
        value=3.0,
        key="nr_tebakan"
    )

    toleransi = st.number_input(
        "Masukkan toleransi",
        value=0.0001,
        format="%.4f",
        key="nr_tol"
    )

    # Membuat Fungsi dan Turunan Fungsi

    x_simbol = sp.symbols("x")

    fungsi_sympy = sp.sympify(fungsi)

    turunan_sympy = sp.diff(
        fungsi_sympy,
        x_simbol
    )

    f = sp.lambdify(
        x_simbol,
        fungsi_sympy,
        "numpy"
    )

    f_turunan = sp.lambdify(
        x_simbol,
        turunan_sympy,
        "numpy"
    )

    # Perhitungan Metode Newton-Raphson

    if st.button("Hitung Newton-Raphson"):

        data_iterasi = []

        x0 = tebakan_awal

        jumlah_iterasi = 0

        while True:

            x1 = x0 - (
                f(x0) / f_turunan(x0)
            )

            data_iterasi.append([
                jumlah_iterasi + 1,
                x0,
                x1
            ])

            if abs(x1 - x0) < toleransi:
                break

            x0 = x1

            jumlah_iterasi += 1

        akar = x1

        st.success(
            f"Akar persamaan = {akar:.6f}"
        )

        st.write(
            f"Jumlah iterasi = {jumlah_iterasi + 1}"
        )

        # Menampilkan Tabel Iterasi

        tabel_iterasi = pd.DataFrame(
            data_iterasi,
            columns=[
                "Iterasi",
                "x lama",
                "x baru"
            ]
        )

        st.dataframe(tabel_iterasi)

        # Menampilkan Grafik Fungsi

        x = np.linspace(
            akar - 3,
            akar + 3,
            400
        )

        y = f(x)

        plt.figure(figsize=(8,5))

        plt.plot(x, y)

        plt.axhline(y=0)

        plt.title("Grafik Fungsi")

        plt.xlabel("Nilai x")

        plt.ylabel("Nilai f(x)")

        plt.grid()

        st.pyplot(plt)

# Metode Secant

if metode == "Secant":

    st.header("Metode Secant")

    # Input Data dari Pengguna

    fungsi = st.text_input(
        "Masukkan fungsi",
        value="x**3 - 4*x - 9",
        key="sec_fungsi"
    )

    tebakan_pertama = st.number_input(
        "Masukkan tebakan pertama",
        value=2.0,
        key="sec_x0"
    )

    tebakan_kedua = st.number_input(
        "Masukkan tebakan kedua",
        value=3.0,
        key="sec_x1"
    )

    toleransi = st.number_input(
        "Masukkan toleransi",
        value=0.0001,
        format="%.4f",
        key="sec_tol"
    )

    # Membuat Fungsi Matematika

    def hitung_fungsi(x):
        return eval(fungsi)

    # Perhitungan Metode Secant

    if st.button("Hitung Secant"):

        data_iterasi = []

        x0 = tebakan_pertama
        x1 = tebakan_kedua

        jumlah_iterasi = 0

        while True:

            x2 = x1 - (
                hitung_fungsi(x1)
                * (x1 - x0)
                / (
                    hitung_fungsi(x1)
                    - hitung_fungsi(x0)
                )
            )

            data_iterasi.append([
                jumlah_iterasi + 1,
                x0,
                x1,
                x2
            ])

            if abs(x2 - x1) < toleransi:
                break

            x0 = x1
            x1 = x2

            jumlah_iterasi += 1

        akar = x2

        st.success(
            f"Akar persamaan = {akar:.6f}"
        )

        st.write(
            f"Jumlah iterasi = {jumlah_iterasi + 1}"
        )

        # Menampilkan Tabel Iterasi

        tabel_iterasi = pd.DataFrame(
            data_iterasi,
            columns=[
                "Iterasi",
                "x0",
                "x1",
                "x2"
            ]
        )

        st.dataframe(tabel_iterasi)

        # Menampilkan Grafik Fungsi

        x = np.linspace(
            akar - 3,
            akar + 3,
            400
        )

        y = [
            hitung_fungsi(nilai_x)
            for nilai_x in x
        ]

        plt.figure(figsize=(8,5))

        plt.plot(x, y)

        plt.axhline(y=0)

        plt.title("Grafik Fungsi")

        plt.xlabel("Nilai x")

        plt.ylabel("Nilai f(x)")

        plt.grid()

        st.pyplot(plt)

# Perbandingan Metode

if metode == "Perbandingan Metode":

    st.header("Perbandingan Ketiga Metode")

    # Input Data dari Pengguna

    fungsi = st.text_input(
        "Masukkan fungsi",
        value="x**3 - 4*x - 9",
        key="banding_fungsi"
    )

    batas_bawah = st.number_input(
        "Batas bawah (Bisection)",
        value=2.0,
        key="banding_bawah"
    )

    batas_atas = st.number_input(
        "Batas atas (Bisection)",
        value=3.0,
        key="banding_atas"
    )

    tebakan_awal = st.number_input(
        "Tebakan awal (Newton-Raphson)",
        value=3.0,
        key="banding_newton"
    )

    toleransi = st.number_input(
        "Toleransi",
        value=0.0001,
        format="%.4f",
        key="banding_tol"
    )

    if st.button("Bandingkan Metode"):

        def f(x):
            return eval(fungsi)

        # Perhitungan Metode Bisection

        bawah = batas_bawah
        atas = batas_atas

        iterasi_bisection = 0

        while abs(atas - bawah) > toleransi:

            tengah = (bawah + atas) / 2

            if f(bawah) * f(tengah) < 0:
                atas = tengah
            else:
                bawah = tengah

            iterasi_bisection += 1

        akar_bisection = (bawah + atas) / 2

        # Perhitungan Metode Newton-Raphson

        x_simbol = sp.symbols("x")

        fungsi_sympy = sp.sympify(fungsi)

        turunan = sp.diff(
            fungsi_sympy,
            x_simbol
        )

        fungsi_num = sp.lambdify(
            x_simbol,
            fungsi_sympy,
            "numpy"
        )

        turunan_num = sp.lambdify(
            x_simbol,
            turunan,
            "numpy"
        )

        x0 = tebakan_awal

        iterasi_newton = 0

        while True:

            x1 = x0 - (
                fungsi_num(x0)
                / turunan_num(x0)
            )

            iterasi_newton += 1

            if abs(x1 - x0) < toleransi:
                break

            x0 = x1

        akar_newton = x1

        # Perhitungan Metode Secant

        x0 = batas_bawah
        x1 = batas_atas

        iterasi_secant = 0

        while True:

            x2 = x1 - (
                f(x1)
                * (x1 - x0)
                / (f(x1) - f(x0))
            )

            iterasi_secant += 1

            if abs(x2 - x1) < toleransi:
                break

            x0 = x1
            x1 = x2

        akar_secant = x2

        # Menampilkan Tabel Perbandingan

        tabel_perbandingan = pd.DataFrame(
            {
                "Metode": [
                    "Bisection",
                    "Newton-Raphson",
                    "Secant"
                ],
                "Akar Persamaan": [
                    akar_bisection,
                    akar_newton,
                    akar_secant
                ],
                "Jumlah Iterasi": [
                    iterasi_bisection,
                    iterasi_newton,
                    iterasi_secant
                ]
            }
        )

        st.subheader("Tabel Perbandingan")

        st.dataframe(
            tabel_perbandingan
        )

        # Grafik Perbandingan Jumlah Iterasi

        st.subheader(
            "Grafik Perbandingan Jumlah Iterasi"
        )

        plt.figure(figsize=(8, 5))

        plt.bar(
            tabel_perbandingan["Metode"],
            tabel_perbandingan["Jumlah Iterasi"]
        )

        plt.xlabel("Metode")

        plt.ylabel("Jumlah Iterasi")

        plt.title(
            "Perbandingan Jumlah Iterasi"
        )

        plt.grid()

        st.pyplot(plt)

        # Kesimpulan

        metode_tercepat = tabel_perbandingan.loc[
            tabel_perbandingan["Jumlah Iterasi"].idxmin(),
            "Metode"
        ]

        st.subheader("Kesimpulan")

        st.write(
            f"""
Berdasarkan hasil perhitungan yang diperoleh, ketiga metode berhasil memberikan pendekatan nilai akar persamaan sesuai dengan data masukan yang diberikan pengguna.

Perbedaan utama terlihat pada jumlah iterasi yang dibutuhkan untuk mencapai tingkat ketelitian yang sama. Pada percobaan ini, metode yang paling cepat adalah {metode_tercepat} karena membutuhkan jumlah iterasi paling sedikit.

Hasil yang diperoleh dapat berbeda untuk setiap fungsi, interval, maupun tebakan awal yang digunakan. Oleh karena itu, efisiensi masing-masing metode juga dapat berubah tergantung pada kasus yang diuji.

Dengan demikian, pengguna dapat memilih metode yang paling sesuai berdasarkan kebutuhan dan karakteristik fungsi yang akan diselesaikan.
"""
        )
