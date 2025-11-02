import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

urunler = [
    {
        "id": 1,
        "ad": "NYX Far Paleti",
        "fiyat": "1199 TL",
        "resim": "ürün1.jpg"
    },
    {
        "id": 2,
        "ad": "NYX Kapatıcı",
        "fiyat": "900 TL",
        "resim": "ürün2.jpg"
    },
    {
        "id": 3,
        "ad": "Gucci Flora Parfüm",
        "fiyat": "3700 TL",
        "resim": "ürün3.jpg"
    },
    {
        "id": 4,
        "ad": "Rare Beauty Allık",
        "fiyat": "2300 TL",
        "resim": "ürün4.jpg"
    },
    {
        "id": 5,
        "ad": "NYX Buttermelt Aydınlatıcı",
        "fiyat": "950 TL",
        "resim": "ürün5.jpg"
    },
    {
        "id": 6,
        "ad": "YSL Ruj",
        "fiyat": "1699 TL",
        "resim": "ürün6.jpg"
    }
]

global_resim_referanslari = []

def goster_katalog():
    sepet_frame.pack_forget()
    katalog_frame.pack(fill="both", expand=True)

def goster_sepet():
    katalog_frame.pack_forget()
    sepet_frame.pack(fill="both", expand=True)

def satin_alma_islemi():
    if kart_no_entry.get() == "" or kart_skt_entry.get() == "" or kart_cvv_entry.get() == "":
        messagebox.showwarning("Hata", "Lütfen tüm kart bilgilerini girin!")
    else:
        messagebox.showinfo("Başarılı", "Satın alma işlemi tamamlandı!")
        kart_no_entry.delete(0, 'end')
        kart_skt_entry.delete(0, 'end')
        kart_cvv_entry.delete(0, 'end')
        goster_katalog()

def sepete_ekle(urun_adi):
    print(f"{urun_adi} sepete eklendi!")
    messagebox.showinfo("Sepet", f"{urun_adi} başarıyla sepete eklendi!")


root = tk.Tk()
root.title("Kozmetik Alışveriş Kataloğu")
root.geometry("950x600")

katalog_frame = tk.Frame(root) 
sepet_frame = tk.Frame(root)   

canvas = tk.Canvas(katalog_frame)
scrollbar = tk.Scrollbar(katalog_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

mevcut_satir = 0
mevcut_sutun = 0
sutun_limiti = 3

sepete_git_buton_ust = tk.Button(scrollable_frame, text="Sepetim'e Git", command=goster_sepet, font=("Helvetica", 12, "bold"), bg="#FF69B4")
sepete_git_buton_ust.grid(row=mevcut_satir, column=0, columnspan=sutun_limiti, pady=20, padx=10, sticky="ew")

mevcut_satir += 1

for urun in urunler:
    
    urun_kutusu = tk.Frame(scrollable_frame, relief="solid", borderwidth=1)
    
    try:
        urun_resmi_pil = Image.open(urun["resim"])
        urun_resmi_pil = urun_resmi_pil.resize((200, 200), Image.LANCZOS)
        urun_resmi_tk = ImageTk.PhotoImage(urun_resmi_pil)
        
        global_resim_referanslari.append(urun_resmi_tk)

        urun_resmi_label = tk.Label(urun_kutusu, image=urun_resmi_tk)
        urun_resmi_label.pack(pady=10)

    except Exception as e:
        print(f"Hata: {urun['resim']} yüklenemedi. Hata detayı: {e}")
        urun_resmi_label = tk.Label(urun_kutusu, text=f"[{urun['resim']} bulunamadı]", fg="red")
        urun_resmi_label.pack(pady=10, padx=10)

    urun_adi = tk.Label(urun_kutusu, text=urun["ad"], font=("Helvetica", 14, "bold"))
    urun_adi.pack(pady=5)

    urun_fiyati = tk.Label(urun_kutusu, text=f"Fiyat: {urun['fiyat']}", font=("Helvetica", 11))
    urun_fiyati.pack(pady=5)

    sepete_ekle_buton = tk.Button(urun_kutusu, text="Sepete Ekle", 
                                  bg="#800080", fg="white", font=("Helvetica", 10, "bold"),
                                  command=lambda u=urun["ad"]: sepete_ekle(u))
    sepete_ekle_buton.pack(pady=10, ipadx=10, ipady=5) 
    
    urun_kutusu.grid(row=mevcut_satir, column=mevcut_sutun, padx=20, pady=20, sticky="nsew")
    
    mevcut_sutun += 1
    
    if mevcut_sutun >= sutun_limiti:
        mevcut_sutun = 0
        mevcut_satir += 1

for i in range(sutun_limiti):
    scrollable_frame.columnconfigure(i, weight=1)


sepet_baslik = tk.Label(sepet_frame, text="Ödeme Ekranı", font=("Helvetica", 18, "bold"))
sepet_baslik.pack(pady=30)

kart_no_label = tk.Label(sepet_frame, text="Kart Numarası (16 Hane):", font=("Helvetica", 11))
kart_no_label.pack()
kart_no_entry = tk.Entry(sepet_frame, width=30, font=("Helvetica", 11))
kart_no_entry.pack(pady=5)

kart_skt_label = tk.Label(sepet_frame, text="Son Kullanma Tarihi (AA/YY):", font=("Helvetica", 11))
kart_skt_label.pack()
kart_skt_entry = tk.Entry(sepet_frame, width=10, font=("Helvetica", 11))
kart_skt_entry.pack(pady=5)

kart_cvv_label = tk.Label(sepet_frame, text="CVV (3 Hane):", font=("Helvetica", 11))
kart_cvv_label.pack()
kart_cvv_entry = tk.Entry(sepet_frame, width=5, font=("Helvetica", 11), show="*")
kart_cvv_entry.pack(pady=5)

satin_al_buton = tk.Button(sepet_frame, text="Satın Al", bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), command=satin_alma_islemi)
satin_al_buton.pack(pady=20, ipadx=10, ipady=5)

kataloga_don_buton = tk.Button(sepet_frame, text="Kataloğa Geri Dön", command=goster_katalog, font=("Helvetica", 12))
kataloga_don_buton.pack()

goster_katalog() 
root.mainloop()