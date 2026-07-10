# Lord of the Mysteries - Tingen Sokakları (Masaüstü RPG)

Karanlık ve deliliğin iç içe geçtiği *Lord of the Mysteries* evreninde geçen, hikaye odaklı ve hayatta kalma mekaniklerine sahip masaüstü rol yapma oyunu.

## 🔮 Oyun Özellikleri (V2.0 - GUI Güncellemesi)
* **Görsel Arayüz (PyQt6):** Karanlık temalı, tamamen tıklanabilir ve dinamik masaüstü penceresi.
* **Dinamik Hikaye İlerlemesi:** Sıradan bir insan olarak başlayıp, Karaborsa'dan alınan iksirlerle kaderinizi çizin (Sleepless, Seer, Assassin).
* **Yapay Zeka Destekli Fısıltılar:** Akıl sağlığı (Sanity) düştükçe zihninize sızan karanlık fısıltılar (Google Gemini 2.0 Flash API).
* **Hata Toleranslı (Fallback) YZ Mimarisi:** API kota aşımı veya bağlantı kopmalarında oyun çökmez, yedek yerel metin kütüphanesi devreye girer.
* **Kalıcı Kayıt Sistemi:** SQLite altyapısı ile karakter gelişimi anlık olarak `lotm_save.db` dosyasına işlenir.
* **Epik Boss Savaşları:** Müzik ve ses efektleriyle desteklenmiş, hikayeye sadık Megose (Gerçek Yaratıcı'nın Tohumu) final savaşı.

## 🛠️ Teknolojiler ve Mimari
* **Arayüz:** PyQt6 
* **Veritabanı:** SQLite3
* **Yapay Zeka:** Google GenAI
* **Mimari:** Modüler, Nesne Yönelimli Programlama (OOP)

## 🚀 Kurulum
1. Repoyu bilgisayarınıza klonlayın.
2. Gerekli kütüphaneleri yükleyin: `pip install PyQt6 google-genai python-dotenv`
3. Ana dizinde bir `.env` dosyası oluşturup Gemini API anahtarınızı ekleyin: `GEMINI_API_KEY=sizin_anahtariniz_buraya`
4. Yeni arayüzü başlatmak için terminale şu komutu girin: `python gui_ana.py`