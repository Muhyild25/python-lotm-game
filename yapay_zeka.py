import os
import random
import time
from dotenv import load_dotenv
from google import genai

# Çevresel değişkenleri yükler ve entegrasyon için gerekli API kimlik doğrulamasını yapılandırır.
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# --- YEREL FALLBACK VERİ HAVUZU ---
# Uzak sunucu servisinin erişilemez olduğu, kota sınırlarının aşıldığı (HTTP 429) 
# veya hız sınırlama (cooldown) mekanizmasının aktif olduğu durumlarda kullanılacak alternatif metin seti.
YEDEK_FISILTILAR = [
    "Karanlıkta binlerce gözün seni izlediğini hissediyorsun...",
    "Antigonus... Sakın o ismi anma...",
    "Duvarların içinden tırmalama ve ağlama sesleri geliyor.",
    "Sislerin içinden biri ismini fısıldıyor ama etrafta kimse yok.",
    "Kan... Tingen'in Arnavut kaldırımlı sokakları kan ağlıyor.",
    "Zihnin parçalanıyor, gölgeler uzayıp boynuna dolanıyor sanki."
]

# Hız sınırlama algoritması için son başarılı uzak bağlantı zaman damgasını (timestamp) saklar.
son_istek_zamani = 0

class YZMotoru:
    @staticmethod
    def fisilti_uret(sanity):
        """
        Karakterin mevcut akıl sağlığı parametresine göre dinamik metin üretir.
        Rate Limiting ve Throttling filtrelerini uygulayarak ağ trafiğini ve GUI kararlılığını optimize eder.
        """
        global son_istek_zamani
        su_an = time.time()
        
        # KONTROL 1: Rate Limiting (Soğuma Süresi)
        # API kaynaklarının aşırı tüketimini önlemek adına ardışık iki istek arasında 
        # minimum 10 saniyelik güvenli bir eşik kontrolü gerçekleştirilir.
        if su_an - son_istek_zamani < 10:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"
            
        # KONTROL 2: Throttling (İstek Seyreltme Filtresi)
        # Her arama tetiklenmesinde uzak sunucuya gitmek yerine %30 olasılıklı bir filtre uygular.
        # Bu işlem, ana GUI thread'inin asenkron beklemelerle donmasını engeller.
        if random.randint(1, 100) > 30:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"

        # API kimlik doğrulama anahtarının varlık kontrolü.
        if not api_key:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"

        try:
            client = genai.Client(api_key=api_key)
            prompt = (
                f"Lord of the Mysteries evreninde Tingen şehrindeyiz. "
                f"Karakterin akıl sağlığı {sanity}. Bana onun duyacağı çok kısa, "
                f"karanlık, tek cümlelik bir fısıltı yaz."
            )
            
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            
            # Başarılı istek sonrası zaman damgası güncellenir.
            son_istek_zamani = su_an 
            return f"🌀 [YZ] {response.text.strip()}"
            
        except Exception:
            # Hata Yönetimi: Bağlantı kopmaları veya RESOURCE_EXHAUSTED durumlarında 
            # sistemin kesintisiz çalışması için yerel kütüphaneye geri dönülür (Fallback).
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"