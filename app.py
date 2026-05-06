import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import os
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
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

    # background
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    label {
        color: white !important;
    }

    .stTextInput input {
        background: white;
        color: black;
        border-radius: 1px;
        width: 1000%;
    }

    .stButton>button {
        background: #4facfe;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    users = load_users()

    # 🔥 CENTER FORM (INI KUNCINYA)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div style="
            background: rgba(0,0,0,0.85);
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 20px rgba(0,0,0,0.5);
            text-align:center;
        ">
        """, unsafe_allow_html=True)

        # ===============================
        # LOGIN
        # ===============================
        if st.session_state.auth_mode == "login":

            st.markdown("<h4 style='color:white; text-align:center;'>FORM LOGIN</h4>", unsafe_allow_html=True)

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

            if st.button("Belum punya akun? Register"):
                st.session_state.auth_mode = "register"
                st.rerun()

        # ===============================
        # REGISTER
        # ===============================
        else:

            st.markdown("<h4 style='color:white; text-align:center;'>FORM REGISTER</h4>", unsafe_allow_html=True)

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

            if st.button("Sudah punya akun? Login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

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
# UPLOAD DATA (FIXED)
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

    st.markdown('<div class="card">', unsafe_allow_html=True)
    file = st.file_uploader("Upload file CSV", type=["csv"])
    st.markdown('</div>', unsafe_allow_html=True)

    if file is not None:
        df = pd.read_csv(file)

        st.subheader("Tabel Dataset")
        st.dataframe(df.head(), use_container_width=True)

        text_col = st.selectbox("Pilih kolom teks", df.columns)

        if st.button("Jalankan Analisis"):

            import time

            with st.spinner("⏳ Memproses dataset..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

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
                fig, ax = plt.subplots()
                ax.pie([pos, net, neg],
                       labels=["Positif", "Netral", "Negatif"],
                       autopct='%1.1f%%')
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots()
                ax.bar(["Positif", "Netral", "Negatif"], [pos, net, neg])
                st.pyplot(fig)

            st.markdown("---")

            # ===============================
            # EVALUASI MODEL
            # ===============================
            if "Rating" in df.columns:

                from sklearn.model_selection import train_test_split
                import seaborn as sns

                def label_sentiment(rating):
                    if rating >= 4:
                        return 'positif'
                    elif rating >= 2:
                        return 'netral'
                    else:
                        return 'negatif'

                df["sentiment"] = df["Rating"].apply(label_sentiment)

                X = df[text_col].astype(str)
                y = df["sentiment"]

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )

                y_pred_nb = nb_model.predict(X_test)
                y_pred_svm = svm_model.predict(X_test)

                # ===============================
                # ACCURACY
                # ===============================
                acc_nb = accuracy_score(y_test, y_pred_nb)
                acc_svm = accuracy_score(y_test, y_pred_svm)

                col1, col2 = st.columns(2)
                col1.metric("Accuracy NB", f"{acc_nb:.3f}")
                col2.metric("Accuracy SVM", f"{acc_svm:.3f}")

                st.markdown("---")

                # ===============================
                # CONFUSION MATRIX
                # ===============================
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Naive Bayes")
                    cm_nb = confusion_matrix(y_test, y_pred_nb)
                    fig1, ax1 = plt.subplots()
                    sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Blues', ax=ax1)
                    st.pyplot(fig1)

                with col2:
                    st.subheader("SVM")
                    cm_svm = confusion_matrix(y_test, y_pred_svm)
                    fig2, ax2 = plt.subplots()
                    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens', ax=ax2)
                    st.pyplot(fig2)

                st.markdown("---")

                # ===============================
                # CLASSIFICATION REPORT
                # ===============================
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🔵 Naive Bayes")
                    report_nb = classification_report(y_test, y_pred_nb, output_dict=True)
                    st.dataframe(pd.DataFrame(report_nb).transpose())

                with col2:
                    st.subheader("🟢 SVM")
                    report_svm = classification_report(y_test, y_pred_svm, output_dict=True)
                    st.dataframe(pd.DataFrame(report_svm).transpose())

                # ===============================
                # 🔥 PERBANDINGAN F1 (FIX)
                # ===============================
                f1_nb = report_nb['weighted avg']['f1-score']
                f1_svm = report_svm['weighted avg']['f1-score']

                st.markdown("### 🏆 Kesimpulan Model Terbaik") 
                col1, col2 = st.columns(2) 
                col1.metric("F1 NB", f"{f1_nb:.3f}") 
                col2.metric("F1 SVM", f"{f1_svm:.3f}") 
                if f1_nb > f1_svm: st.success("🏆 Naive Bayes lebih unggul") 
                    elif f1_nb < f1_svm: st.success("🏆 SVM lebih unggul") 
                    else: st.info("⚖️ Keduanya setara") 
                        else: st.warning("Dataset tidak memiliki kolom Rating, evaluasi model dilewati.")


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
