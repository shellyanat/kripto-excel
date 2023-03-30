# L I B R A R Y ------------
import streamlit as st
import pandas as pd
import numpy as np
import random
from io import BytesIO
import xlwt
from xlwt.Workbook import *
from PIL import Image

# P A G E  S E T T I N G ------------


st.set_page_config(page_title = "Kriptografi - Pengamanan Data Pada File Excel", layout="wide")

st.markdown('''
<style>
/*center metric label*/
[data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: right;
}

/*center metric value*/
[data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: right;
}
</style>
''', unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 2% 2% 2% 8%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: blue;
}
</style>
"""
, unsafe_allow_html=True)

font_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 20px;
}
</style>
"""

text_input = """
<style>
div[class*="stTextInput"] label p {
  font-size: 16px;
}
</style>
"""

st.write(font_css, unsafe_allow_html=True)
st.write(text_input, unsafe_allow_html=True)


# G E N E R A L  F U N C T I O N ------------

#fpb
def FPB(m,n):
    if m<n:
        o=m
        m=n
        n=o
    s=m%n
    while s!=0:
        m=n
        n=s
        s=m%n
    return n

#cekprima
def cekprima(j):
    tes=0
    i=2
    while i <j:
        if FPB(j,i) == 1:
            tes=tes+0
        elif FPB(j,i)!=1:
            tes=tes+1
        i+=1
    return tes
        
#inversmodulo
def InvMod(a,b):
    inv=1
    while(inv*a)%b!=1:
        inv+=1
    return inv


# G U I  P Y T H O N --------------------------
with st.sidebar:
    st.title("Pilih Program Di Sini")
    sub = st.selectbox("Pengamanan Data File Excel", ('Home','Pembangkitan Kunci', 'Enkripsi File', 'Dekripsi File'))

if sub == "Home":
    import base64
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('excelbg4.png') 
    st.write(
        '''
        ### Pengamanan Data Pada File Excel dengan Diffie-Hellman-RSA

        #### Terdapat 3 jenis program:

        #### 1. Pembangkitan Kunci

        #### 2. Enkripsi File

        #### 3. Dekripsi File

        #### Silahkan pilih salah satu program pada tombol di samping.
        ''')

# TAB 0 : pembangkitan kunci
if sub == "Pembangkitan Kunci":
    a, b, c = st.columns([3,4,2])
    with b:
        '''
        ### Program Pembangkitan Kunci
        '''

    whitespace = 30
    list_tab = [
        "Kunci Publik Alice",
        "Kunci Privat Bob"]
    tab_kunci = st.tabs([s.center(whitespace,"\u2001") for s in list_tab])

    with tab_kunci[0]:
    #petunjuk penggunaan 
        st.markdown('#### Kunci Publik (Alice)')
        with st.expander("PETUNJUK PENGGUNAAN"):
            '''
        Berikut langkah-langkah untuk melakukan pembangkitan kunci publik oleh Alice:

        1. Input nilai g, n, a dengan syarat:

            - Nilai g dan n harus bilangan prima yang telah disepakati bersama Bob
        
            - Nilai n > g > 126 (Nilai n lebih besar dari g dan 126)

            - Nilai a < n (Nilai a kurang dari n) dan nilai a tidak boleh diketahui siapapun

        2. Klik tombol "Hitung Nilai X", nilai X kemudian harus dikirimkan kepada Bob

        3. Input nilai Y yang didapatkan dari Bob

        4. Klik tombol "Bangkitkan Kunci Publik" untuk mendapatkan kunci publik
        
        5. Gunakan kunci publik untuk mengenkripsi data pada file excel dan kirimkan hasil enkripsi serta kunci publik kepada Bob
            '''
        
        bag_g_a, bag_n_a = st.columns([5,5])
        with bag_g_a:
            g_a = st.text_input('Input nilai g yang telah disepakati bersama Bob:')
            if g_a:
                if cekprima(int(g_a)) > 0:
                    st.error('Nilai g harus merupakan bilangan prima, input nilai g baru', icon="🚨")
                if int(g_a) <= 126:
                    st.error('Nilai g harus lebih dari 126, input nilai g baru', icon="🚨")  
        with bag_n_a:
            n_a = st.text_input('Input nilai n yang telah disepakati bersama Bob:')
            if n_a:
                if cekprima(int(n_a)) > 0:
                    st.error('Nilai n harus merupakan bilangan prima, input nilai n baru',icon="🚨")
                if int(n_a) <= int(g_a) :
                    st.error('Nilai n harus lebih dari g, input nilai n baru',icon="🚨")
        bag_x_a, bag_y_a = st.columns([5,5])
        with bag_x_a:
            x_a = st.text_input('Input nilai a, rahasiakan nilai a dari siapapun :')
            if x_a:
                if int(x_a) >= int(n_a) :
                    st.error('Nilai a harus kurang dari nilai n, input nilai a baru',icon="🚨")
        with bag_y_a:        
            Y_A = st.text_input('Input nilai Y dari Bob:')
            if Y_A:
                Y_A = int(Y_A)
        
        hit_x_a, hit_key_a = st.columns([5,5])
        with hit_x_a:
            if st.button('Hitung Nilai X'):
                g_a = int(g_a)
                n_a = int(n_a)
                x_a = int(x_a)

                X_A = (g_a**x_a)%n_a
                st.metric('Nilai X untuk dikirim ke Bob adalah ', X_A)
                st.warning(' Kirim Nilai X ke Bob', icon="⚠️")
        with hit_key_a:
            if st.button('Bangkitkan Kunci Publik'):
                g_a = int(g_a)
                n_a = int(n_a)
                x_a = int(x_a)
                K1 = (Y_A**x_a)%n_a
                N1 = n_a*g_a*K1
                touN_A= (n_a-1)*(g_a-1)
                key_e = random.randrange(1,touN_A)
                z = FPB(key_e,touN_A)
                while z != 1:
                    key_e = random.randrange(1,touN_A)
                    z = FPB(key_e,touN_A)

                publickey = str(key_e) + ' ' + str(N1)
                st.metric('Kunci Publik untuk Enkripsi', publickey)
                st.warning(' Simpan Kunci Publik', icon="⚠️")

    
    with tab_kunci[1]:
        st.markdown(' #### Kunci Privat (Bob)')
        with st.expander("PETUNJUK PENGGUNAAN"):
            '''
        Berikut langkah-langkah untuk melakukan pembangkitan kunci privat oleh Bob:

        1. Input nilai g, n, b dengan syarat:

            - Nilai g dan n harus bilangan prima yang telah disepakati bersama Alice
        
            - Nilai n > g > 126 (Nilai n lebih besar dari g dan 126)

            - Nilai b < n (Nilai b kurang dari n) dan nilai b hanya boleh diketahui oleh diri sendiri

        2. Klik tombol "Hitung Nilai Y", nilai Y kemudian harus dikirimkan kepada Alice

        3. Input nilai X dan juga nilai kunci publik yang didapatkan dari Alice

        4. Klik tombol "Bangkitkan Kunci Privat" untuk mendapatkan kunci privat
        
        5. Gunakan kunci privat untuk mendekripsi data pada file excel
            '''
        bag_g_b, bag_n_b = st.columns([5,5])
        with bag_g_b:
            g_b = st.text_input('Input nilai g yang telah disepakati bersama Alice  :')
            if g_b:
                if cekprima(int(g_b)) > 0:
                    st.error('Nilai g harus merupakan bilangan prima, input nilai g baru', icon="🚨")
                if int(g_b) <= 126:
                    st.error('Nilai g harus lebih dari 126, input nilai g baru', icon="🚨")  
        with bag_n_b:
            n_b = st.text_input('Input nilai yang telah disepakati bersama Alice  :')
            if n_b:
                if cekprima(int(n_b)) > 0:
                    st.error('Nilai n harus merupakan bilangan prima, input nilai n baru', icon="🚨")
                if int(n_b) <= int(g_b) :
                    st.error('Nilai n harus lebih dari g, input nilai n baru',icon="🚨")
        bag_y_b, bag_x_b = st.columns([5,5])
        with bag_y_b:
            y_b = st.text_input('Input nilai b, rahasiakan nilai b dari siapapun :')
            if y_b:
                if int(y_b) >= int(n_b) :
                    st.error('Nilai y harus kurang dari nilai n, input nilai y baru',icon="🚨")
        with bag_x_b:
            X_B = st.text_input('Input nilai X dari Alice :')
            if X_B:
                X_B = int(X_B)

        a, b = st.columns([5,5])
        with b:
            kunci_publik = st.text_input('Input nilai kunci publik dari Alice :')
            if kunci_publik:
                public_key = kunci_publik.split()
                e = public_key[0]
                N1 = public_key[1]                
                e = int(e)
                N1 = int(N1)

        hit_y_b, hit_key_b = st.columns([5,5])
        with hit_y_b:
            if st.button('Hitung Nilai Y'):
                g_b = int(g_b)
                n_b = int(n_b)
                y_b = int(y_b)

                Y_B = (g_b**y_b)%n_b
                st.metric('Nilai Y untuk dikirim ke Alice adalah ', Y_B)
        with hit_key_b:

            if st.button('Bangkitkan Kunci Privat'):
                g_b = int(g_b)
                n_b = int(n_b)
                y_b = int(y_b)
                K2 = (X_B**y_b)%n_b
                
                X_B = int(e)
                N1 = int(N1)

                touN= (n_b-1)*(g_b-1)
                
                key_d = InvMod(e,touN)
                N2 = N1/K2
                N2 = int(N2)

                privatkey = str(key_d) + ' ' + str(N2)

                st.metric('Kunci Privat untuk Dekripsi', privatkey)
                st.warning(' Simpan Kunci Privat', icon="⚠️")

# TAB 1 : enkripsi

# specific function : enkripsi
@st.cache_data(show_spinner=False)
def encrypt_cell(cell, e, N1):
    p_teks = str(cell)
    len_teks = len(cell)
    i = 0
    cipherteks = ''
    while i < len_teks:
        p = p_teks[i] #membaca plainteks per karakter
        p = ord(p) #ubah karakter ke code ASCII
        cipher = (p**e % N1)
        if cipher < 100: 
            cipher = '0' + str(cipher)
        cipher = str(cipher)
        cipherteks = cipherteks + cipher + ' '
        i = i + 1
    return cipherteks

if sub == "Enkripsi File": 
    a, b, c = st.columns([3.6,4,2])
    with b:
        '''
        ### Program Enkripsi File
        '''
    #petunjuk penggunaan
    with st.expander("PETUNJUK PENGGUNAAN"):
        '''
    Berikut langkah-langkah untuk melakukan proses enkripsi:
    
    1. Input nilai kunci publik 
    
    2. Upload File Excel/CSV yang akan dienkripsi dengan menekan tombol “Browse Files”

    3. Tekan tombol “Enkripsi File”, tunggu sampai proses enkripsi selesai
    
    4. Download file dengan menekan tombol “Download Encrypted File” untuk mendownload file yang telah dienkripsi.
        '''
    #input kunci publik dan file excel
    pubkey = st.text_input('Masukkan kunci publik:')

    uploaded_file = st.file_uploader("Upload File Excel atau CSV:")
    
    if uploaded_file is not None:
        
        #proses enkripsi
        if st.button('Enkripsi File'):
            #kunci publik
            public_key = pubkey.split()
            e = public_key[0]
            N1 = public_key[1]
            e = int(e)
            N1 = int(N1)

            #tipe file
            filename=uploaded_file.name

            #jika tipe file adalah excel
            if filename[-4:]=='xlsx':
                sheets = pd.ExcelFile(uploaded_file).sheet_names
                    
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')

                for i, sheet in enumerate(sheets):
                    dataframe = pd.read_excel(uploaded_file, sheet_name = sheet, header = None, dtype = 'string')
                    dataframe.fillna('nan-empty-values-kosong-dhrsa', inplace = True)                    

                    dataframe = dataframe.astype(str)
                    encrypted_df = dataframe.applymap(lambda x: encrypt_cell(x,e,N1))

                    globals()['df' + str(i+1)] = encrypted_df.copy()
                    wb = Workbook()
                    worksheet = wb.add_sheet(sheet)
                    globals()['df' + str(i+1)].to_excel(writer, header = False, index=False, sheet_name=sheet)
                
                writer.save()
                processed_data = output.getvalue()
                
                data_xlsx = processed_data
                st.download_button(label='📥 Download Encrypted File',
                                data=data_xlsx,
                                file_name= 'encrypted ' + filename)
            
            #jika tipe file adalah csv
            if filename[-3:]=='csv':
                dataframe = pd.read_csv(uploaded_file, header = None)
                dataframe.fillna('nan-empty-values-kosong-dhrsa', inplace = True)
                
                dataframe = dataframe.astype(str)
                encrypted_df = dataframe.applymap(lambda x: encrypt_cell(x,e,N1))

                data_csv = encrypted_df.to_csv(header = False, index=False)
                st.download_button(label='📥 Download Encrypted File',
                                data= data_csv,
                                file_name= 'encrypted ' + filename)
        
        if uploaded_file is None:
            st.write('')




# TAB 2 : dekripsi

# specific function: dekripsi
@st.cache_data(show_spinner=False)
def decrypt_cell(cell, d, N2):
    c_teks = cell.split()
    cipher = []
    for teks in c_teks:
        cipher.append(int(teks))
    plainteks = ''
    for c in cipher:
        plain = (c**d % N2)
        plain = chr(plain)
        plainteks = plainteks + plain
    return plainteks


if sub == "Dekripsi File":
    a, b, c = st.columns([3.6,4,2])
    with b:
        '''
        ### Program Dekripsi File
        '''
    #petunjuk penggunaan
    with st.expander("PETUNJUK PENGGUNAAN"):
        '''
    Berikut langkah-langkah untuk melakukan proses dekripsi:

    1. Input nilai kunci privat 
    
    2. Upload File Excel/CSV yang akan didekripsi dengan menekan tombol “Browse Files”
    
    3. Tekan tombol “Dekripsi File”, tunggu sampai proses dekripsi selesai
    
    4. Download file dengan menekan tombol “Download Decrypted File” untuk mendownload file yang telah didekripsi.    
        '''

    privkey = st.text_input('Masukkan kunci privat:')

    uploaded_file = st.file_uploader("Upload Encrypted File Excel atau CSV:")
    if uploaded_file is not None:

        if st.button('Dekripsi File'):
        #kunci privat
            privat_key = privkey.split()
            d = int(privat_key[0])
            N2 = int(privat_key[1])

        #tipe file
            filename = uploaded_file.name

        #jika tipe file adalah excel
            if filename[-4:] == 'xlsx':
                sheets = pd.ExcelFile(uploaded_file).sheet_names
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')

                #file dibaca untuk setiap sheet
                for i, sheet in enumerate(sheets):
                    #pembacaan data
                    dataframe = pd.read_excel(uploaded_file, sheet_name=sheet, header=None)
                    #dekripsi data dengan def decrypt_cell
                    decrypted_df = dataframe.applymap(lambda x: decrypt_cell(x, d, N2))
                    #menulis kembali data yang sebelumnya merupakan empty values
                    decrypted_df.replace("nan-empty-values-kosong-dhrsa", np.NaN, inplace=True)
                    
                    #menulis kembali hasil dekripsi pada file excel
                    globals()['df' + str(i+1)] = decrypted_df.copy()
                    wb = Workbook()
                    worksheet = wb.add_sheet(sheet)
                    globals()['df' + str(i+1)].to_excel(writer, header=False, index=False, sheet_name=sheet)
                
                #output 
                writer.save()
                processed_data = output.getvalue()
                st.download_button(
                                    label='📥 Download Decrypted File',
                                    data=processed_data,
                                    file_name= 'decrypted ' + filename)

        #jika tipe file adalah csv
            if filename[-3:] == 'csv':
                #pembacaan data
                dataframe = pd.read_csv(uploaded_file, header=None)
                #dekripsi data dengan def decrypt_cell
                decrypted_df = dataframe.applymap(lambda x: decrypt_cell(x, d, N2))
                #menulis kembali data yang sebelumnya merupakan empty values
                decrypted_df.replace("nan-empty-values-kosong-dhrsa", np.NaN, inplace=True)
                
                #menulis kembali hasil dekripsi ke file csv
                data_csv = decrypted_df.to_csv(header=False, index=False)
                #output
                st.download_button(
                                    label='📥 Download Decrypted File',
                                    data=data_csv,
                                    file_name='decyrpted ' + filename)

    if uploaded_file is None:
        st.write('')
