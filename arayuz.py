import random
import sys
from yapay_zeka import YZMotoru 

def deli_yazdir(metin, sanity):
    """
    Karakterin Akıl Sağlığı (Sanity) state'ine göre View (Görünüm) katmanındaki metinleri dinamik olarak manipüle eder.
    Düşük akıl sağlığında LLM tabanlı fısıltıları araya enjekte eder ve metin bozulması (Text Obfuscation) uygular.
    """
    if sanity >= 60:
        print(metin)
        return
        
    # UI/UX Algoritması: Asenkron olmayan (Synchronous) API çağrılarında yaşanacak gecikmeyi (Latency) 
    # kullanıcıdan gizlemek için geçici bir yükleme (Loading) mesajı basılır (Latency Masking).
    print("⏳ Zihninin derinliklerinden bir ses yükseliyor...", end="", flush=True)
    
    # Uzak sunucu (LLM) çağrısı tetiklenir
    ai_fisilti = YZMotoru.fisilti_uret(sanity)
    
    # Dinamik Konsol Render: Carriage Return (\r) kullanılarak stdout (standart çıktı) üzerindeki 
    # geçici yükleme mesajı temizlenir ve buffer boşaltılır.
    print("\r" + " " * 50 + "\r", end="", flush=True) 

    # Phase 1: Hafif Yozlaşma (Halüsinasyon Enjeksiyonu)
    if 30 <= sanity < 60:
        if ai_fisilti: 
            print(ai_fisilti)
        print(metin)
        
    # Phase 2: İleri Seviye Yozlaşma (String Manipulation & Obfuscation)
    elif sanity < 30:
        if ai_fisilti: 
            print(ai_fisilti)
            
        # RNG tabanlı karakter değişimi ile metin bozulması (String Corruption Algorithm)
        bozuk_metin = "".join(random.choice(["#", "?", "!", "%", "x", "_"]) if harf != " " and random.randint(1, 6) == 1 else harf for harf in metin)
        print(bozuk_metin)