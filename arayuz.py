import random
import sys
from yapay_zeka import YZMotoru 

def deli_yazdir(metin, sanity):
    if sanity >= 60:
        print(metin)
        return
        
    # YENİ: Bekleme süresini gizlemek için gerilim efekti
    print("⏳ Zihninin derinliklerinden bir ses yükseliyor...", end="", flush=True)
    
    # Oyun burada Google'ı beklerken ekranda üstteki gerilim yazısı kalacak
    ai_fisilti = YZMotoru.fisilti_uret(sanity)
    
    # Gelen cevabı yazdırırken o gerilim yazısını '\r' ile silip üstüne yazıyoruz
    print("\r" + " " * 50 + "\r", end="", flush=True) 

    if 30 <= sanity < 60:
        if ai_fisilti: print(ai_fisilti)
        print(metin)
        
    elif sanity < 30:
        if ai_fisilti: print(ai_fisilti)
        bozuk_metin = "".join(random.choice(["#", "?", "!", "%", "x", "_"]) if harf != " " and random.randint(1, 6) == 1 else harf for harf in metin)
        print(bozuk_metin)