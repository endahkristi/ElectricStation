import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Bali Energy Transition Analysis",
    layout="wide"
)

# --- 2. TITLE AND OVERVIEW ---
st.title("⚡ Analisis Transisi Energi dan Kendaraan Listrik Bali")
st.markdown("Dokumen ini merupakan hasil analisis data untuk memproyeksikan kebutuhan infrastruktur energi di Bali dalam mendukung transisi menuju **Energi Baru Terbarukan (EBT)** dan **Kendaraan Listrik (EV)**.")
st.markdown("---")


# --- 3. DYNAMIC INPUTS (Sidebar) ---
st.sidebar.title("Parameters Simulasi")

# Dynamic parameter 1 (from previous version)
cagr_input = st.sidebar.slider(
    'Asumsi CAGR Konsumsi Listrik (%)',
    min_value=1.0, max_value=8.0, value=3.5, step=0.5,
    help='Compound Annual Growth Rate used to project future electricity consumption.'
)

st.sidebar.markdown("---")
st.sidebar.header("Kebutuhan SPKLU (Input dari User)")

# Dynamic parameters 2-5: Required SPKLU Units (replacing the static data)
# Use st.number_input for integer values
required_spklu_target = st.sidebar.number_input(
    'SPKLU Target/Eksisting (Unit)',
    min_value=10, max_value=500, value=145, step=5,
    help='Jumlah SPKLU yang sudah ada atau ditargetkan untuk Bali.'
)

required_conservative = st.sidebar.number_input(
    'SPKLU Dibutuhkan - Konservatif',
    min_value=50, max_value=1000, value=200, step=10,
    help='Kebutuhan SPKLU dalam skenario Konservatif.'
)

required_moderate = st.sidebar.number_input(
    'SPKLU Dibutuhkan - Moderat',
    min_value=50, max_value=1000, value=350, step=10,
    help='Kebutuhan SPKLU dalam skenario Moderat.'
)

required_aggressive = st.sidebar.number_input(
    'SPKLU Dibutuhkan - Agresif',
    min_value=50, max_value=1000, value=550, step=10,
    help='Kebutuhan SPKLU dalam skenario Agresif.'
)

required_throughput = st.sidebar.number_input(
    'SPKLU Dibutuhkan - Konservatif (Tinggi Throughput)',
    min_value=50, max_value=1000, value=120, step=10,
    help='Kebutuhan SPKLU dalam skenario Konservatif dengan asumsi throughput tinggi.'
)

# --- 4. DATA FRAME GENERATION (Now based on user input) ---
data = {
    'Skenario EV': ['Konservatif', 'Moderat', 'Agresif', 'Konservatif (Tinggi Throughput)'],
    'SPKLU Eksisting (Target)': [required_spklu_target] * 4, # Target is the same for all scenarios
    'SPKLU yang Dibutuhkan': [required_conservative, required_moderate, required_aggressive, required_throughput]
}
df_spklu_comparison = pd.DataFrame(data)

# --- 5. KEYWORDS (From Notebook Markdown Cell) ---
with st.expander("📚 **Daftar Istilah Kunci (Keywords)**"):
    st.markdown("""
    | Kategori | Istilah | Deskripsi |
    | :--- | :--- | :--- |
    | Energi & Listrik | **kWh** | Satuan energi listrik (Kilowatt-hour). |
    | Energi & Listrik | **EBT** | Energi ramah lingkungan dari sumber alami (Matahari, Angin, Biomassa). |
    | Kendaraan Listrik | **SPKLU** | Stasiun Pengisian Kendaraan Listrik Umum. |
    """)
    st.caption("Sumber data dan istilah berasal dari notebook `balitransition.ipynb`.")

# --- 6. CORE ANALYSIS & DYNAMIC VISUALIZATION ---

st.header("Analisis Kebutuhan SPKLU Berdasarkan Skenario EV")

st.markdown(f"Saat ini, target **SPKLU Eksisting** yang menjadi dasar perbandingan adalah **{required_spklu_target} Unit**.")

# Apply the input CAGR to a simple projection (example of dynamic calculation)
st.metric(label="Asumsi CAGR Konsumsi Listrik Tahunan",
          value=f"{cagr_input}%",
          delta="Dapat disesuaikan pada sidebar untuk proyeksi kebutuhan energi.")

# Plotting the SPKLU comparison
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.35

# Calculate the 'Kekurangan' (Shortfall) for visualization
df_spklu_comparison['Kekurangan/Kelebihan'] = df_spklu_comparison['SPKLU Eksisting (Target)'] - df_spklu_comparison['SPKLU yang Dibutuhkan']

# Bar chart showing the Required vs. Target SPKLU
bar_required = ax.bar(df_spklu_comparison['Skenario EV'], df_spklu_comparison['SPKLU yang Dibutuhkan'], width, label='SPKLU yang Dibutuhkan', color='#2ca02c')
bar_target = ax.bar(df_spklu_comparison['Skenario EV'], df_spklu_comparison['SPKLU Eksisting (Target)'], width, label='Target Eksisting', color='#1f77b4', alpha=0.5)

ax.set_ylabel('Jumlah Unit SPKLU')
ax.set_title(f'Perbandingan Kebutuhan SPKLU vs. Target Eksisting ({required_spklu_target} Unit)')
ax.legend()
plt.xticks(rotation=15, ha="right")
plt.tight_layout()

# Use Streamlit to display the plot
st.pyplot(fig)

# --- 7. KEY FINDING / CONCLUSION ---
st.subheader("📝 Kesimpulan Utama (Berdasarkan Input Simulasi)")
st.warning(f"""
Dengan target SPKLU eksisting sebanyak **{required_spklu_target} unit** yang Anda input, perbandingan dengan kebutuhan unit pada setiap skenario (Konservatif: {required_conservative}, Moderat: {required_moderate}, Agresif: {required_aggressive}, Konservatif Tinggi Throughput: {required_throughput}) dapat dilihat pada grafik di atas.
""")

st.markdown("---")
st.caption("Aplikasi ini dibuat berdasarkan analisis dari notebook `balitransition.ipynb`.")