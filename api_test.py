import os
from google import genai

# Çevresel değişkenlerden (Environment Variables) kimlik doğrulama anahtarını (API Key) çeker.
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Kimlik doğrulama hatası (Authentication Failure)
    print("[SYS_ERR] Kritik Hata: 'GEMINI_API_KEY' çevresel değişkeni sistemde bulunamadı.")
else:
    print("[SYS_INFO] API Anahtarı doğrulandı. Uzak sunucuya (Remote Server) bağlantı başlatılıyor...")
    try:
        # GenAI Client örneklendirmesi (Instantiation) ve yetkilendirme
        client = genai.Client(api_key=api_key)
        
        print("[SYS_INFO] İstek paketi (Request Payload) hazırlanıyor ve sunucuya iletiliyor...")
        
        # LLM modeline senkron (Synchronous) içerik üretim isteği gönderilir.
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents='Lord of the Mysteries evreninde, Tingen şehrinde geçen karanlık, tek cümlelik bir fısıltı yaz.'
        )
        
        print("\n[HTTP_200] BAŞARILI YANIT (Response Body):")
        print(response.text.strip())
        
    except Exception as e:
        # Ağ, kota (Rate Limit) veya sunucu taraflı (Server-Side) hataların yakalanması (Exception Handling)
        print("\n[HTTP_ERR] API BAĞLANTI VEYA YÜRÜTME HATASI:")
        print(str(e))