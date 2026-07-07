import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasındaki gizli şifreyi güvenle belleğe yüklüyoruz
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API yapılandırması
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

class YZMotoru:
    @staticmethod
    def fisilti_uret(sanity):
        if sanity >= 60:
            return ""
            
        if 30 <= sanity < 60:
            derece = "başlangıç aşamasında"
            baglam = "Lord of the Mysteries evrenindeyiz. Oyuncu görünmeyen varlıklar tarafından izleniyor. Sislerin içinden gelen, paranoyayı tetikleyen, gizemli ve rahatsız edici kısa bir sanrı yaz. Türkçe olsun. (Maksimum 8 kelime, tırnak kullanma)"
        else:
            derece = "tamamen çıldırmak üzere, kontrolü kaybediyor"
            baglam = "Lord of the Mysteries evreninin kozmik dehşeti! Gerçek Yaratıcı'nın (True Creator) fısıltıları, derinin altında sürünen kurtçuklar, kan, mutasyon ve etin yozlaşması hakkında zihni paramparça eden çok korkunç, hastalıklı bir cümle yaz. Kesinlikle Türkçe olsun. (Maksimum 10 kelime, tırnak kullanma)"
            
        try:
            response = model.generate_content(f"Sen oyuncunun zihnine sızan Dış Tanrılardan (Outer Deities) birisin. Oyuncunun delilik seviyesi: {derece}. {baglam}")
            return f"\n(👁️ Gölgeler fısıldıyor... '{response.text.strip()}')"
            
        except Exception as e:
            print(f"\n[SİSTEM HATASI]: {e}")
            return "\n(Gölgeler hareket ediyor...)"