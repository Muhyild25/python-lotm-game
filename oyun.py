from karakter import Karakter, Seer, Sleepless, Assassin
from dusman import Dusman
from npc import NPC
from esya import Esya, Silah, Tilsim
from hikaye import HikayeYoneticisi
from arayuz import deli_yazdir       # UI/UX Modülü entegrasyonu
from savas import SavasYoneticisi    # Combat Controller entegrasyonu
import veritabani
import time
import random

# === SİSTEM BAŞLATMA VE BAĞIMLILIK YAPILANDIRMASI (Initialization) ===
veritabani.veritabani_kur()

# Obje Örneklendirme (Object Instantiation) - Başlangıç nesneleri tanımlanır
baslangic_silahi = Silah("Eski bir Revolver", fiyat=0, aciklama="Paslı ama iş görür (+5 Hasar)", ekstra_hasar=5)
dukkan_esyalari = [
    Silah("Kanlı Avcı Bıçağı", fiyat=20, aciklama="Karanlıkta parlar (+12 Hasar)", ekstra_hasar=12),
    Tilsim("Güneş Kuşu Tüyü", fiyat=30, aciklama="Zihni korur (15 Sanity korur)", sanity_koruma=15),
    Esya("Mutant Beyonder Gözü", fiyat=50, aciklama="Ritüel için gerekli")
]
tum_esyalar = [baslangic_silahi] + dukkan_esyalari

print("🌫️ Tingen şehrinin yağmurlu, isli ve karanlık sokaklarında gözlerini açtın...")
print("📜 Lord of the Mysteries Evrenine Hoş Geldiniz...\n")

# State Kontrolü: Kalıcı veritabanından (Persistent Storage) ön okuma yapılır
eski_yol = veritabani.kayitli_yol_bul("Klein Moretti")

if eski_yol:
    # Polymorphism: Kayıtlı sınıfa göre uygun alt sınıf (Child Class) örneklendirilir
    if eski_yol == "Seer": oyuncu = Seer(isim="Klein Moretti")
    elif eski_yol == "Sleepless": oyuncu = Sleepless(isim="Klein Moretti")
    elif eski_yol == "Assassin": oyuncu = Assassin(isim="Klein Moretti")
else:
    # Yeni Karakter Yaratım Evresi (Character Creation Flow)
    print("Hangi yolda (Pathway) yürümek istersin?")
    print("1 - Seer (Kahin): Taktikseldir. %25 Kritik şansı. Yeteneği: Ruhsal Kırbaç")
    print("2 - Sleepless (Uykusuz): Dayanıklıdır. 120 HP. Yeteneği: Karanlığın Kucağı")
    print("3 - Assassin (Suikastçi): Ölümcüldür. %20 Iskalama. Yeteneği: Gölge İnfazı")
    
    while True:
        yol_secimi = input("\nSeçiminiz (1/2/3): ")
        if yol_secimi == '1': oyuncu = Seer(isim="Klein Moretti"); break
        elif yol_secimi == '2': oyuncu = Sleepless(isim="Klein Moretti"); break
        elif yol_secimi == '3': oyuncu = Assassin(isim="Klein Moretti"); break
        else: print("❌ Lütfen geçerli bir yol seçin (1, 2 veya 3).")
    
    oyuncu.esya_al(baslangic_silahi)

# Core Sistemlerin Enjeksiyonu (Dependency Injection)
hikaye = HikayeYoneticisi() 
veritabani.kayit_yukle(oyuncu, tum_esyalar, hikaye)
gizemli_haberci = NPC("Azik", "Tarot Elçisi", ["Bölüm sonundaki kiliseye gitmeden önce mutlaka akıl sağlığını fulle."])

# === ANA OYUN DÖNGÜSÜ (Main Game Loop) ===
while True:
    # View (Görünüm) Katmanı Güncellemesi
    print("\n" + "="*50)
    print(hikaye.gorev_metnini_getir())
    print("="*50)
    
    # Eylem Menüsü (Action State Menu)
    print("1 - Kendini Kontrol Et (Durum ve Envanter)")
    print("2 - Gölgelerin Arasında Araştırma Yap (İlerleme/Para)")
    print("3 - 🏥 Gizli Kliniğe Gir (Can/Sanity Yenile)")
    print("4 - Sokağın Sonundaki Hırıltıya Doğru İlerle (Canavar Avı)")
    print("5 - 🕯️ Gizli Ritüel Yap (Seviye Atla)")
    print("6 - 🛒 Karaborsaya Gir (Dükkan)")
    print("7 - 👤 Sislerin İçindeki Figüre Yaklaş (Konuş)")
    
    # State tabanlı dinamik menü yönetimi
    if hikaye.adim == 2:
        print("8 - ⛪ TINGEN KİLİSESİNE GİR (BOSS SAVAŞI!)")
        print("9 - Oyunu Kaydet ve Çık")
    else:
        print("8 - Oyunu Kaydet ve Çık")
        
    print("="*50)
    
    # Event Listener (Kullanıcı girdisini dinler)
    secim = input("Ne yapacaksın?: ")
    
    # I/O İşleme ve State Değişikliği (Action Handling)
    if secim == '1': 
        oyuncu.durum_goster()
        
    elif secim == '2':
        # Keşif ve Ekonomi entegrasyonu (Exploration Event)
        print("\nKaranlık ve ıslak taşların üzerinde yürüyorsun...")
        time.sleep(1)
        kazanc = random.randint(1, 4)
        oyuncu.pound += kazanc
        deli_yazdir(f"Yerde {kazanc} Pound buldun.", oyuncu.sanity)
        hikaye_metni = hikaye.sokak_arastirmasi_yap()
        if hikaye_metni: print(hikaye_metni)
                
    elif secim == '3':
        # İyileşme (Rest & Recovery) servisi
        print("\n🏥 Kliniğe girdin. 1- Terapist (5£, +20 Sanity) | 2- Cerrah (8£, +40 HP) | 0- Çıkış")
        klinik_secim = input("Seçiminiz: ")
        if klinik_secim == '1' and oyuncu.pound >= 5:
            oyuncu.pound -= 5; oyuncu.sanity = min(100, oyuncu.sanity + 20)
            print("\n🛋️ Terapist zihnini rahatlattı.")
        elif klinik_secim == '2' and oyuncu.pound >= 8:
            oyuncu.pound -= 8; oyuncu.hp = min(100, oyuncu.hp + 40)
            print("\n💉 Cerrah yaralarını dikti.")
            
    elif secim == '4':
        # Normal Combat Engine Çağrısı
        yaratik = Dusman("Mutasyon Geçirmiş Avcı", hp=40, min_hasar=5, max_hasar=15)
        sonuc = SavasYoneticisi.normal_savas(oyuncu, yaratik, deli_yazdir)
        if sonuc == "oldu": break
            
    elif secim == '5':
        # Progression / Seviye Atlama Algoritması
        if any(e.isim == "Mutant Beyonder Gözü" for e in oyuncu.envanter):
            oyuncu.envanter = [e for e in oyuncu.envanter if e.isim != "Mutant Beyonder Gözü"]
            oyuncu.iksir_ic()
            if oyuncu.sanity <= 0: print("\n💀 Delirdin..."); break
        else: print("\n❌ Ritüel için 'Mutant Beyonder Gözü' lazım!")
            
    elif secim == '6':
        # Karaborsa / Store Management
        print("\n=== KARABORSA DÜKKANI ===")
        for i, esya in enumerate(dukkan_esyalari): print(f"{i+1}. {esya.isim} - {esya.fiyat} Pound")
        alim = input("Almak istediğiniz (Çıkış için 0): ")
        if alim.isdigit() and 0 < int(alim) <= len(dukkan_esyalari):
            secilen = dukkan_esyalari[int(alim)-1]
            if oyuncu.pound >= secilen.fiyat:
                oyuncu.pound -= secilen.fiyat; oyuncu.esya_al(secilen)
            else: print("\n❌ Paran yetmiyor!")
            
    elif secim == '7':
        # Dialog Trigger (NPC Etkileşimi)
        gizemli_haberci.konus()
        time.sleep(1.5)
        
    elif secim == '8' and hikaye.adim != 2:
        # Standart Oyun İçi Kayıt (Save State Persistence)
        veritabani.oyunu_kaydet(oyuncu, hikaye)
        break
        
    elif secim == '8' and hikaye.adim == 2:
        # Final Boss Encounter Tetikleyicisi
        boss = Dusman("Yozlaşmış Rahip Lane", hp=90, min_hasar=12, max_hasar=22)
        sonuc = SavasYoneticisi.boss_savasi(oyuncu, boss)
        
        if sonuc == "oldu":
            break
        elif sonuc == "kazandi":
            # Chapter Transition (Bölüm Geçişi ve State Kaydı)
            hikaye.adim = 3
            print("\n🏆 Boss yere yığıldı. 1. BÖLÜMÜN SONU. Harika bir iş çıkardın!")
            veritabani.oyunu_kaydet(oyuncu, hikaye)
            break
            
    elif secim == '9' and hikaye.adim == 2:
        # Alternatif Kayıt ve Çıkış Bloğu
        veritabani.oyunu_kaydet(oyuncu, hikaye)
        break