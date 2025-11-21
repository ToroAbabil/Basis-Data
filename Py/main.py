# Import library
import streamlit as st
import pandas as pd
from datetime import datetime

# Import fungsi dari config.py
from config import *

# Set konfigurasi halaman dashboard
st.set_page_config("Dashboard", page_icon="", layout="wide")  # Judul, ikon, tata letak lebar

# Ambil data pelanggan
result_customers = view_customers()

# Buat DataFrame pelanggan
df_customers = pd.DataFrame(result_customers, columns=[
    "customer_id", "name", "email", "phone", "address", "birthdate"
])

# Hitung usia dari birthdate
df_customers['birthdate'] = pd.to_datetime(df_customers['birthdate']) #merubah tipe string menjadi datetime
df_customers['Age'] = (datetime.now() - df_customers['birthdate']).dt.days // 365 # waktu sekarang - dt.days : mengambil jumlah harinya saja dari selisih tersebut / 365.

# Fungsi tampilkan tabel + export CSV
def tabelCustomers_dan_export():
    # Hitung jumlah pelanggan
    total_customers = df_customers.shape[0]

    # Tampilkan metrik
    col1, col2, col3 = st.columns(3) # Fungsi st.columns(3) membuat tiga kolom sejajar di tampilan web Streamlit, menjadi tiga bagian horizontal — col1, col2, dan col3.
    with col1:
        st.metric(label="📦 Total Pelanggan", value=total_customers, delta="Semua Data")

    #Sidebar: Filter Rentang Usia
    st.sidebar.header("FilterWhere Rentang Usia") # akan muncul area kiri sidebar
    min_age = int(df_customers['Age'].min()) # min : mengambil kolom berisi umur termuda, int : dalam bentuk bilangan bulat
    max_age = int(df_customers['Age'].max()) # maz : mengambil kolom berisi umur tertua, int : dalam bentuk bilangan bulat
    age_range = st.sidebar.slider( # membuat slider (penggeser) di sidebar untuk memilih rentang usia.
        "Pilih Rentang Usia",
        min_value=min_age, # Nilai minimum umur
        max_value=max_age, # nilai maxsimum umur
        value=(min_age, max_age) # Nilai awal slider, misal (19, 40)
    )

    #Terapkan filter usia
    filtered_df = df_customers[df_customers['Age'].between(*age_range)]

    # Tampilkan tabel pelanggan
    st.markdown("### 📋 Tabel Data Pelanggan")
    
    showdata = st.multiselect( # menampilkan daftar kolom dari filtered_df yang bisa dipilih pengguna.
        "Pilih Kolom Pelanggan yang Ditampilkan",
        options=filtered_df.columns, # menampilkan semua nama kolom yang tersedia.
        default=["customer_id", "name", "email", "phone", "address", "birthdate", "Age"]
    )
    
    # Menampilkan tabel data pelanggan ke layar dengan hanya kolom yang dipilih (showdata).
    # use_container_width=True membuat tabel otomatis menyesuaikan lebar layar (responsif).
    st.dataframe(filtered_df[showdata], use_container_width=True) 

    # Mendefinisikan fungsi helper untuk mengubah DataFrame menjadi file CSV.
    # @st.cache_data adalah decorator Streamlit agar fungsi ini tidak dijalankan ulang setiap kali halaman di-refresh
    # _df.to_csv(index=False) mengubah DataFrame menjadi teks CSV tanpa kolom indeks.
    # membuat hasilnya bisa diunduh dengan karakter yang benar

    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df_to_csv(filtered_df[showdata])
    st.download_button(
        label="⬇️ Download Data Pelanggan sebagai CSV",
        data=csv,
        file_name='data_pelanggan.csv',
        mime='text/csv'
    )


# Ambil data produk
result_products = view_products()

# Buat DataFrame produk
df_products = pd.DataFrame(result_products, columns=[
    "product_id", "name", "description", "price", "stock"
])

def tabelProducts_dan_export():
    total_products = df_products.shape[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🛒 Total Produk", total_products)

    st.markdown("### 📦 Tabel Produk")

    showdata = st.multiselect(
        "Pilih Kolom Produk",
        options=df_products.columns,
        default=["product_id", "name", "description", "price", "stock"]
    )

    st.dataframe(df_products[showdata], use_container_width=True)

    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode("utf-8")

    csv = convert_df_to_csv(df_products[showdata])
    st.download_button(
        label="⬇️ Download Data Produk sebagai CSV",
        data=csv,
        file_name="data_produk.csv",
        mime="text/csv"
    )

# Ambil data orders + customer name
result_orders = view_orders_with_customers()

df_orders = pd.DataFrame(result_orders, columns=[
    "order_id", "order_date", "total_amount", "customer_name", "phone"
])

# Convert order_date ke datetime
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])

def tabelOrders_dan_export():
    total_orders = df_orders.shape[0]
    total_income = df_orders["total_amount"].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧾 Total Order", total_orders)
    with col2:
        st.metric("💰 Total Pendapatan", f"Rp {total_income:,.0f}")

    st.markdown("### 🧾 Tabel Orders")

    showdata = st.multiselect(
        "Pilih Kolom Orders",
        options=df_orders.columns,
        default=["order_id", "order_date", "customer_name", "total_amount", "phone"]
    )

    st.dataframe(df_orders[showdata], use_container_width=True)

    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode("utf-8")

    csv = convert_df_to_csv(df_orders[showdata])
    st.download_button(
        label="⬇️ Download Data Orders sebagai CSV",
        data=csv,
        file_name="data_orders.csv",
        mime="text/csv"
    )

# Ambil data order details lengkap
result_details = view_order_details_with_info()

df_details = pd.DataFrame(result_details, columns=[
    "order_detail_id",
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "product_id",
    "product_name",
    "unit_price",
    "quantity",
    "subtotal",
    "order_total",
    "phone"
])

df_details["order_date"] = pd.to_datetime(df_details["order_date"])

def tabelOrderDetails_dan_export():
    total_details = df_details.shape[0]
    total_revenue = df_details["subtotal"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📑 Total Order Items", total_details)
    with col2:
        st.metric("💵 Total Pendapatan Item", f"Rp {total_revenue:,.0f}")

    st.markdown("### 📑 Tabel Order Details")

    showdata = st.multiselect(
        "Pilih Kolom Order Details",
        options=df_details.columns,
        default=[
            "order_detail_id", "order_id", "order_date", "customer_name",
            "product_name", "unit_price", "quantity", "subtotal"
        ]
    )

    st.dataframe(df_details[showdata], use_container_width=True)

    @st.cache_data
    def convert_df_to_csv(_df):
        return _df.to_csv(index=False).encode("utf-8")

    csv = convert_df_to_csv(df_details[showdata])
    st.download_button(
        label="⬇️ Download Order Details sebagai CSV",
        data=csv,
        file_name="data_order_details.csv",
        mime="text/csv"
    )

st.sidebar.success("Pilih Tabel:")

menu = st.sidebar.radio(
    "Menu Data",
    ["Customers", "Products", "Orders", "Order Details"]
)

if menu == "Customers":
    tabelCustomers_dan_export()
elif menu == "Products":
    tabelProducts_dan_export()
elif menu == "Orders":
    tabelOrders_dan_export()
elif menu == "Order Details":
    tabelOrderDetails_dan_export()