import os
import random
import time
from dotenv import load_dotenv
from google import genai

# .env dosyasındaki şifreyi yüklüyoruz
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# --- YEDEK FISILTILAR KÜTÜPHANESİ ---
# API çökerse, kotan dolarsa veya cooldown süresindeysek bunlar devreye girecek.
YEDEK_FISILTILAR = [
    "Karanlıkta binlerce gözün seni izlediğini hissediyorsun...",
    "Antigonus... Sakın o ismi anma...",
    "Duvarların içinden tırmalama ve ağlama sesleri geliyor.",
    "Sislerin içinden biri ismini fısıldıyor ama etrafta kimse yok.",
    "Kan... Tingen'in Arnavut kaldırımlı sokakları kan ağlıyor.",
    "Zihnin parçalanıyor, gölgeler uzayıp boynuna dolanıyor sanki."
]

# API'yi boğmamak için zaman damgası tutuyoruz
son_istek_zamani = 0

class YZMotoru:
    @staticmethod
    def fisilti_uret(sanity):
        global son_istek_zamani
        su_an = time.time()
        
        # 1. KONTROL: Cooldown (Son API çağrısından bu yana en az 10 saniye geçmeli)
        if su_an - son_istek_zamani < 10:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"
            
        # 2. KONTROL: Olasılık Filtresi (Sadece %30 ihtimalle gerçek API'yi yor)
        # Sürekli API'ye gitmek hem kotayı doldurur hem de PyQt arayüzünü dondurur.
        if random.randint(1, 100) > 30:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"

        # Eğer kalkanları geçtiksek, Google sunucularına bağlanıyoruz
        if not api_key:
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"

        try:
            client = genai.Client(api_key=api_key)
            prompt = f"Lord of the Mysteries evreninde Tingen şehrindeyiz. Karakterin akıl sağlığı {sanity}. Bana onun duyacağı çok kısa, karanlık, tek cümlelik bir fısıltı yaz."
            
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            
            # Başarılı olursa zamanlayıcıyı sıfırla
            son_istek_zamani = su_an 
            return f"🌀 [YZ] {response.text.strip()}"
            
        except Exception:
            # API 429 Hatası verirse veya çökerse sessizce yedeği döndür
            return f"🧠 {random.choice(YEDEK_FISILTILAR)}"