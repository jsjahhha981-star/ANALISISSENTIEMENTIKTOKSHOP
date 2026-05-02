import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import os
# ===============================
# DATABASE USER (CSV)
# ===============================
USER_FILE = "users.csv"

def load_users():
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)
        return df

    try:
        df = pd.read_csv(USER_FILE)
        if df.empty or "username" not in df.columns:
            df = pd.DataFrame(columns=["username", "password"])
        return df
    except:
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)
        return df

def save_users(df):
    df.to_csv(USER_FILE, index=False)

# ===============================
# SESSION
# ===============================
if "login" not in st.session_state:
    st.session_state.login = False

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# ===============================
# 🔐 LOGIN SYSTEM
# ===============================
def auth_page():

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    /* CENTER WRAPPER */
    .auth-wrapper {
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }

    /* 🔥 CARD DIPERKECIL */
    .auth-card {
        background: rgba(0,0,0,0.85);
        padding: 18px;               /* sebelumnya 30px */
        border-radius: 12px;
        width: 280px;                /* sebelumnya 360px */
        box-shadow: 0 0 20px rgba(0,0,0,0.6);
    }

    /* 🔥 TITLE DIPERKECIL */
    .title {
        text-align:center;
        color:white;
        font-size:16px;              /* sebelumnya 22px */
        font-weight:bold;
        margin-bottom:10px;
    }

    /* LABEL */
    label {
        color:white !important;
        font-size:12px !important;   /* kecil */
    }

    /* INPUT */
    .stTextInput input {
        background:white;
        color:black;
        border-radius:6px;
        padding:6px;
        font-size:12px;              /* kecil */
    }

    /* BUTTON */
    .stButton>button {
        background:#4facfe;
        color:white;
        border-radius:6px;
        width:100%;
        font-weight:bold;
        padding:6px;
        font-size:12px;              /* kecil */
    }
    </style>
    """, unsafe_allow_html=True)

    users = load_users()

    # 🔥 WRAPPER + CARD FIX
    st.markdown('<div class="auth-wrapper"><div class="auth-card">', unsafe_allow_html=True)

    # ================= LOGIN =================
    if st.session_state.auth_mode == "login":

        st.markdown('<div class="title">🔐 LOGIN</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            users = load_users()

            user = users[
                (users["username"].astype(str).str.strip() == str(username).strip()) &
                (users["password"].astype(str).str.strip() == str(password).strip())
            ]

            if not user.empty:
                import time

                st.success("Login berhasil!")
                progress = st.progress(0)

                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i+1)

                st.balloons()

                st.session_state.login = True
                st.rerun()
            else:
                st.error("Username atau password salah!")

        if st.button("Register"):
            st.session_state.auth_mode = "register"
            st.rerun()

    # ================= REGISTER =================
    else:

        st.markdown('<div class="title">📝 REGISTER</div>', unsafe_allow_html=True)

        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")

        if st.button("Daftar"):

            users = load_users()

            new_user = str(new_user).strip()
            new_pass = str(new_pass).strip()

            if new_user == "" or new_pass == "":
                st.warning("Isi semua field!")

            elif new_user in users["username"].astype(str).str.strip().values:
                st.error("Username sudah digunakan!")

            else:
                new_data = pd.DataFrame([[new_user, new_pass]], columns=["username", "password"])
                users = pd.concat([users, new_data], ignore_index=True)
                save_users(users)

                st.success("Registrasi berhasil!")
                st.session_state.auth_mode = "login"
                st.rerun()

        if st.button("Login"):
            st.session_state.auth_mode = "login"
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# ===============================
# ROUTING LOGIN
# ===============================
if not st.session_state.login:
    auth_page()
    st.stop()
else:
    # reset background setelah login
    st.markdown("""
    <style>
    .stApp {
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>

/* ===============================
SIDEBAR DARK GRADIENT
=============================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
}

/* ===============================
TEXT DI SIDEBAR
=============================== */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===============================
HOVER MENU
=============================== */
.nav-link {
    border-radius: 8px;
    transition: 0.3s;
}

.nav-link:hover {
    background-color: rgba(255,255,255,0.1) !important;
}

/* ===============================
ACTIVE MENU
=============================== */
.nav-link.active {
    background: linear-gradient(to right, #4fc3f7, #81d4fa) !important;
    color: black !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
# ===============================
# CONFIG (WAJIB PALING ATAS)
# ===============================
st.set_page_config(page_title="Sentimen TikTok Shop", layout="wide")

st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD MODEL
# ===============================
nb_model = joblib.load("nb_model.joblib")
svm_model = joblib.load("svm_model.joblib")

# ===============================
# FILE RIWAYAT
# ===============================
HISTORY_FILE = "history.csv"

def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    else:
        return pd.DataFrame(columns=["Teks", "Naive Bayes", "SVM"])

def save_history(df):
    df.to_csv(HISTORY_FILE, index=False)

# ===============================
# SESSION STATE
# ===============================
if "history" not in st.session_state:
    st.session_state.history = load_history().to_dict("records")

# ===============================
# SIDEBAR MENU
# ===============================
with st.sidebar:
    st.markdown(
        """
        <div style="
            background-color:#2b2b2b;
            padding:10px;
            border-radius:10px;
            margin-bottom:10px;
            color:black;
            font-weight:bold;
        ">
            Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )
    selected = option_menu(
        menu_title=None,
        options=["Beranda", "Input Text", "Upload Data", "Riwayat", "Logout"],
        icons=["house", "chat-dots", "upload", "archive", "box-arrow-right"],
        menu_icon="cast",
        default_index=0, 
    )
# ===============================
# LOGOUT
# ===============================
if selected == "Logout":
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
# ===============================
# BERANDA
# ===============================
if selected == "Beranda":

    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #2E86C1;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: gray;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===============================
    # TITLE
    # ===============================
    st.markdown("""
    <div class="main-title">
    ANALISIS SENTIMEN PLATFORM <br> E-COMMERCE TIKTOK SHOP
    </div>
    <div class="subtitle">
    Naive Bayes vs Support Vector Machine
    </div>
    <br>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ===============================
    # DESKRIPSI
    # ===============================
    st.markdown("""
    <div style='text-align:center; font-size:18px'>
    Aplikasi ini digunakan untuk menganalisis sentimen ulasan pengguna pada platform 
    <b>TikTok Shop</b> menggunakan metode Machine Learning.
    <br><br>
    Sistem akan mengklasifikasikan ulasan menjadi:
    <br>
    😊 <b>Positif</b> | 😐 <b>Netral</b> | 😡 <b>Negatif</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ===============================
    # FITUR (CARD)
    # ===============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>Input Teks</h3>
        Analisis 1 ulasan secara langsung
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>Upload Dataset</h3>
        Analisis banyak data sekaligus
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>Riwayat</h3>
        Menyimpan hasil prediksi otomatis
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ===============================
    # TEKNOLOGI
    # ===============================
    

    col1, col2 = st.columns(2)

    with col1:
        st.info("🤖 Naive Bayes\n\nCepat dan efisien untuk klasifikasi teks")

    with col2:
        st.info("🧠 Support Vector Machine\n\nAkurat untuk data kompleks")

    

    

# ===============================
# INPUT TEXT (VERSI KEREN)
# ===============================
elif selected == "Input Text":

    # ===============================
    # STYLE
    # ===============================
    st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #2E86C1;
    }
    .subtitle {
        text-align: center;
        color: gray;
        font-size: 18px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    }
    .result-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    .positive { background-color: #d4edda; color: #155724; }
    .neutral { background-color: #fff3cd; color: #856404; }
    .negative { background-color: #f8d7da; color: #721c24; }
    </style>
    """, unsafe_allow_html=True)

    # ===============================
    # HEADER
    # ===============================
    st.markdown("""
    <div class="title">ANALISIS SENTIMEN TEKS</div>
    <div class="subtitle">Masukkan ulasan TikTok Shop untuk dianalisis</div>
    <br>
    """, unsafe_allow_html=True)

    # ===============================
    # INPUT BOX
    # ===============================
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text = st.text_area("Masukkan Teks...", height=150)

    char_count = len(text)
    st.caption(f"Jumlah karakter: {char_count}")

    predict_btn = st.button("Analisis Sekarang")

    st.markdown('</div>', unsafe_allow_html=True)

    # ===============================
    # PROSES PREDIKSI
    # ===============================
    if predict_btn:

        if text.strip() == "":
            st.warning("⚠️ Teks tidak boleh kosong!")
        else:
            nb_pred = nb_model.predict([text])[0]
            svm_pred = svm_model.predict([text])[0]

            # ===============================
            # SIMPAN KE RIWAYAT + CSV
            # ===============================
            new_data = {
                "Teks": text,
                "Naive Bayes": nb_pred,
                "SVM": svm_pred
            }

            st.session_state.history.append(new_data)
            df_history = pd.DataFrame(st.session_state.history)
            save_history(df_history)

            st.markdown("<br>", unsafe_allow_html=True)

            # ===============================
            # HASIL
            # ===============================
            col1, col2 = st.columns(2)

            def get_class(sentiment):
                if sentiment == "positif":
                    return "positive", "😊 Positif"
                elif sentiment == "netral":
                    return "neutral", "😐 Netral"
                else:
                    return "negative", "😡 Negatif"

            nb_class, nb_text = get_class(nb_pred)
            svm_class, svm_text = get_class(svm_pred)

            with col1:
                st.subheader("Naive Bayes")
                st.markdown(
                    f'<div class="result-box {nb_class}">{nb_text}</div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.subheader("Support Vector Machine")
                st.markdown(
                    f'<div class="result-box {svm_class}">{svm_text}</div>',
                    unsafe_allow_html=True
                )

            st.markdown("---")

            # ===============================
            # INFO TAMBAHAN
            # ===============================
            st.info(f"📌 Teks dianalisis: \"{text[:100]}...\"")

# ===============================
# UPLOAD DATA (VERSI KEREN)
# ===============================
elif selected == "Upload Data":


    st.markdown("""
    <h2 style='text-align:center; color:#2E86C1; font-weight:bold;'>
     UPLOAD DATASET
</h2>
<p style='text-align:center; color:gray;'>
Analisis sentimen data secara otomatis
</p>
<br>
    """, unsafe_allow_html=True)

    # ===============================
    # CARD UPLOAD
    # ===============================
    st.markdown('<div class="card">', unsafe_allow_html=True)

    file = st.file_uploader("Upload file CSV", type=["csv"])

    st.markdown('</div>', unsafe_allow_html=True)

    if file is not None:
        df = pd.read_csv(file)

        # ===============================
        # PREVIEW DATA
        # ===============================
        st.subheader("Tabel Dataset")
        st.dataframe(df.head(), use_container_width=True)

        text_col = st.selectbox("Pilih kolom teks", df.columns)

        if st.button("Jalankan Analisis"):

            import time

            # ===============================
            # LOADING
            # ===============================
            with st.spinner("⏳ Memproses dataset..."):
                progress = st.progress(0)

                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

                # ===============================
                # PREDIKSI MODEL
                # ===============================
                df["NB"] = nb_model.predict(df[text_col].astype(str))
                df["SVM"] = svm_model.predict(df[text_col].astype(str))

            st.success("✅ Analisis selesai!")

            # ===============================
            # STATISTIK
            # ===============================
            total = len(df)
            pos = (df["NB"] == "positif").sum()
            net = (df["NB"] == "netral").sum()
            neg = (df["NB"] == "negatif").sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("📊 Total Data", total)
            col2.metric("😊 Positif", pos)
            col3.metric("😐 Netral", net)
            col4.metric("😡 Negatif", neg)

            st.markdown("---")

            # ===============================
            # CHART
            # ===============================
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Distribusi Sentimen")
                fig, ax = plt.subplots()
                ax.pie([pos, net, neg],
                       labels=["Positif", "Netral", "Negatif"],
                       autopct='%1.1f%%')
                st.pyplot(fig)

            with col2:
                st.subheader("Jumlah Sentimen")
                fig, ax = plt.subplots()
                ax.bar(["Positif", "Netral", "Negatif"], [pos, net, neg])
                ax.set_ylabel("Jumlah")
                st.pyplot(fig)

            st.markdown("---")

            # ===============================
            # DOWNLOAD
            # ===============================
            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Hasil CSV",
                data=csv,
                file_name="hasil_sentimen.csv",
                mime="text/csv"
            )

            # ===============================
            # TABEL
            # ===============================
            st.subheader("Hasil Prediksi")
            st.dataframe(df.head(20), use_container_width=True)

            # =========================================================
            # 🔥 MODEL PERFORMANCE DASHBOARD (KEREN)
            # =========================================================
            st.markdown("""
            <br>
            <div style='text-align:center'>
                <h2>📊 Model Performance Dashboard</h2>
                <p style='color:gray'>Perbandingan Naive Bayes vs SVM</p>
            </div>
            """, unsafe_allow_html=True)

            from sklearn.model_selection import train_test_split
            from sklearn.metrics import confusion_matrix, accuracy_score
            import seaborn as sns

            if "Rating" in df.columns:

                def label_sentiment(rating):
                    if rating >= 4:
                        return 'positif'
                    elif rating >= 2:
                        return 'netral'
                    else:
                        return 'negatif'

                df["sentiment"] = df["Rating"].apply(label_sentiment)

                X_eval = df[text_col].astype(str)
                y_eval = df["sentiment"]

                X_train, X_test, y_train, y_test = train_test_split(
                    X_eval, y_eval, test_size=0.2, random_state=42, stratify=y_eval
                )

                # ===============================
                # PREDIKSI
                # ===============================
                y_pred_nb = nb_model.predict(X_test)
                y_pred_svm = svm_model.predict(X_test)

                acc_nb = accuracy_score(y_test, y_pred_nb)
                acc_svm = accuracy_score(y_test, y_pred_svm)

                # ===============================
                # METRIC (KEREN)
                # ===============================
                col1, col2, col3 = st.columns(3)

                col1.metric("Naive Bayes", f"{acc_nb:.3f}")
                col2.metric("SVM", f"{acc_svm:.3f}")

                if acc_nb > acc_svm:
                    col3.markdown("### **Naive Bayes Menang**")
                else:
                    col3.markdown("### **SVM Lebih Unggul**")

                st.markdown("---")

                # ===============================
                # CONFUSION MATRIX (KECIL & SEJAJAR)
                # ===============================
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("##### 🔵 Naive Bayes")

                    cm_nb = confusion_matrix(y_test, y_pred_nb)

                    fig1, ax1 = plt.subplots(figsize=(3.5, 3))
                    sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Blues',
                                annot_kws={"size": 9}, ax=ax1)

                    ax1.set_xlabel("Pred", fontsize=8)
                    ax1.set_ylabel("Actual", fontsize=8)
                    ax1.tick_params(labelsize=8)

                    st.pyplot(fig1, use_container_width=False)

                with col2:
                    st.markdown("##### 🟢 Support Vector Machine")

                    cm_svm = confusion_matrix(y_test, y_pred_svm)

                    fig2, ax2 = plt.subplots(figsize=(3.5, 3))
                    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens',
                                annot_kws={"size": 9}, ax=ax2)

                    ax2.set_xlabel("Pred", fontsize=8)
                    ax2.set_ylabel("Actual", fontsize=8)
                    ax2.tick_params(labelsize=8)

                    st.pyplot(fig2, use_container_width=False)

            else:
                st.warning("Dataset tidak memiliki kolom Rating, evaluasi model dilewati.")

# ===============================
# RIWAYAT
# ===============================
# ===============================
# RIWAYAT (VERSI KEREN)
# ===============================
elif selected == "Riwayat":

    # ===============================
    # HEADER KEREN
    # ===============================
    st.markdown("""
    <h2 style='text-align:center; color:#2E86C1; font-weight:800;'>
    RIWAYAT PREDIKSI
    </h2>
    <p style='text-align:center; color:gray;'>
    Data hasil analisis yang telah dilakukan
    </p>
    <br>
    """, unsafe_allow_html=True)

    df_history = pd.DataFrame(st.session_state.history)

    if df_history.empty:
        st.info("📭 Belum ada riwayat prediksi")
    else:

        # ===============================
        # STATISTIK SINGKAT
        # ===============================
        total = len(df_history)
        pos = (df_history["Naive Bayes"] == "positif").sum()
        net = (df_history["Naive Bayes"] == "netral").sum()
        neg = (df_history["Naive Bayes"] == "negatif").sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📊 Total", total)
        col2.metric("😊 Positif", pos)
        col3.metric("😐 Netral", net)
        col4.metric("😡 Negatif", neg)

        st.markdown("---")

        # ===============================
        # TABEL
        # ===============================
        st.subheader("📄 Data Riwayat")
        st.dataframe(df_history, use_container_width=True)

        st.markdown("---")

        # ===============================
        # BUTTON DOWNLOAD (SEJAJAR)
        # ===============================
        col1, col2, col3 = st.columns(3)

        # CSV
        csv = df_history.to_csv(index=False).encode('utf-8')
        col1.download_button(
            "⬇️ Download CSV",
            csv,
            "riwayat.csv",
            "text/csv"
        )

        # Excel
        excel_file = "riwayat.xlsx"
        df_history.to_excel(excel_file, index=False)

        with open(excel_file, "rb") as f:
            col2.download_button(
                "⬇️ Download Excel",
                f,
                file_name="riwayat.xlsx"
            )

        # ===============================
        # HAPUS RIWAYAT (WARNING STYLE)
        # ===============================
        with col3:
            if st.button("🗑️ Hapus Riwayat"):
                st.session_state.history = []
                save_history(pd.DataFrame(columns=["Teks","Naive Bayes","SVM"]))
                st.success("✅ Riwayat berhasil dihapus!")



            # ===========================
# FOOTER (UPGRADE)
# ===========================

st.markdown("""<br>
<hr>
<div style='text-align:center; padding:10px'>
    <b>🎓 Analisis Sentimen</b><br>
    Menggunakan Machine Learning NB & SVM<br><br>
    <span style='font-size:12px; opacity:0.6'>
    © 2026 | Skripsi
    </span>
</div>
""", unsafe_allow_html=True)
