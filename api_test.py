import os
from google import genai

# Sistemdeki API anahtarını alıyoruz
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("HATA: GEMINI_API_KEY sistemde bulunamadı!")
else:
    print("API Anahtarı algılandı. Sunucuya bağlanılıyor...")
    try:
        # Yeni nesil client kurulumu
        client = genai.Client(api_key=api_key)
        
        print("İstek gönderiliyor...")
        response = client.models.generate_content(
            model='gemini-2.0-flash', # veya 'gemini-pro'
            contents='Lord of the Mysteries evreninde, Tingen şehrinde geçen karanlık, tek cümlelik bir fısıltı yaz.'
        )
        print("\n--- BAŞARILI YANIT ---")
        print(response.text)
        
    except Exception as e:
        print("\n--- API ÇÖKME SEBEBİ ---")
        print(e)