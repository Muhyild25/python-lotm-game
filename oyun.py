from karakter import Karakter
from dusman import Dusman
from npc import NPC
from esya import Esya, Silah, Tilsim
from hikaye import HikayeYoneticisi
import veritabani
import time
import random

def deli_yazdir(metin, sanity):
    """Karakterin delilik seviyesine göre ekrana basılan metni bozar."""
    if sanity >= 60:
        print(metin)
        return
    fisiltilar = ["\n(Gölgeler hareket ediyor...)", "\n(Onlara güvenme...)", "\n(Gözlere bakma...)", "\n(Derinin altında bir şeyler sürünüyor...)"]
    if 30 <= sanity < 60:
        if random.randint(1, 4) == 1: print(random.choice(fisiltilar))
        print(metin)
    elif sanity < 30:
        if random.randint(1, 3) == 1: print(random.choice(fisiltilar))
        bozuk_metin = "".join(random.choice(["#", "?", "!", "%", "x", "_"]) if harf != " " and random.randint(1, 6) == 1 else harf for harf in metin)
        print(bozuk_metin)

# === OYUN BAŞLANGIÇ AYARLARI ===
veritabani.veritabani_kur()

baslangic_silahi = Silah("Eski bir Revolver", fiyat=0, aciklama="Paslı ama iş görür (+5 Hasar)", ekstra_hasar=5)
dukkan_esyalari = [
    Silah("Kanlı Avcı Bıçağı", fiyat=20, aciklama="Karanlıkta parlar (+12 Hasar)", ekstra_hasar=12),
    Tilsim("Güneş Kuşu Tüyü", fiyat=30, aciklama="Zihni korur (15 Sanity korur)", sanity_koruma=15),
    Esya("Mutant Beyonder Gözü", fiyat=50, aciklama="Ritüel için gerekli")
]
tum_esyalar = [baslangic_silahi] + dukkan_esyalari

print("🌫️ Tingen şehrinin yağmurlu, isli ve karanlık sokaklarında gözlerini açtın...")
print("📜 Lord of the Mysteries Evrenine Hoş Geldiniz...\n")

oyuncu = Karakter(isim="Klein Moretti", pathway="Seer")
oyuncu.esya_al(baslangic_silahi)

# İŞTE ÇÖZÜLEN KISIM: Önce hikaye objesini yarat, sonra veri tabanına yolla!
hikaye = HikayeYoneticisi() 
veritabani.kayit_yukle(oyuncu, tum_esyalar, hikaye)

gizemli_haberci = NPC("Azik", "Tarot Elçisi", ["Bölüm sonundaki kiliseye gitmeden önce mutlaka akıl sağlığını fulle."])

# === ANA OYUN DÖNGÜSÜ ===
while True:
    print("\n" + "="*50)
    print(hikaye.gorev_metnini_getir())
    print("="*50)
    
    print("1 - Kendini Kontrol Et (Durum ve Envanter)")
    print("2 - Gölgelerin Arasında Araştırma Yap (İlerleme/Para)")
    print("3 - 🏥 Gizli Kliniğe Gir (Can/Sanity Yenile)")
    print("4 - Sokağın Sonundaki Hırıltıya Doğru İlerle (Canavar Avı)")
    print("5 - 🕯️ Gizli Ritüel Yap (Seviye Atla)")
    print("6 - 🛒 Karaborsaya Gir (Dükkan)")
    print("7 - 👤 Sislerin İçindeki Figüre Yaklaş (Konuş)")
    
    if hikaye.adim == 2:
        print("8 - ⛪ TINGEN KİLİSESİNE GİR (BOSS SAVAŞI!)")
        print("9 - Oyunu Kaydet ve Çık")
    else:
        print("8 - Oyunu Kaydet ve Çık")
        
    print("="*50)
    secim = input("Ne yapacaksın?: ")
    
    if secim == '1':
        oyuncu.durum_goster()
        
    elif secim == '2':
        print("\nKaranlık ve ıslak taşların üzerinde yürüyorsun...")
        time.sleep(1)
        kazanc = random.randint(1, 4)
        oyuncu.pound += kazanc
        deli_yazdir(f"Yerde {kazanc} Pound buldun.", oyuncu.sanity)
        
        hikaye_metni = hikaye.sokak_arastirmasi_yap()
        if hikaye_metni:
            print(hikaye_metni)
                
    elif secim == '3':
        print("\n🏥 Kliniğe girdin. 1- Terapist (5£, +20 Sanity) | 2- Cerrah (8£, +40 HP) | 0- Çıkış")
        klinik_secim = input("Seçiminiz: ")
        if klinik_secim == '1' and oyuncu.pound >= 5:
            oyuncu.pound -= 5; oyuncu.sanity = min(100, oyuncu.sanity + 20)
            print("\n🛋️ Terapist zihnini rahatlattı.")
        elif klinik_secim == '2' and oyuncu.pound >= 8:
            oyuncu.pound -= 8; oyuncu.hp = min(100, oyuncu.hp + 40)
            print("\n💉 Cerrah yaralarını dikti.")
            
    elif secim == '4':
        yaratik = Dusman("Mutasyon Geçirmiş Avcı", hp=40, min_hasar=5, max_hasar=15)
        deli_yazdir(f"\n🦇 Karanlıktan '{yaratik.isim}' fırladı!", oyuncu.sanity)
        while yaratik.hp > 0 and oyuncu.hp > 0:
            if input(f"[HP: {oyuncu.hp} | Canavar: {yaratik.hp}] 1- Saldır, 2- Kaç: ") == '1':
                yaratik.hasar_al(oyuncu.saldir())
                if yaratik.hp > 0: oyuncu.hasar_al(yaratik.saldir())
            else: break
        if oyuncu.hp <= 0:
            print("\n💀 Öldün... Tingen sokakları seni de yuttu."); break
        elif yaratik.hp <= 0:
            kazanc = random.randint(10, 20)
            oyuncu.pound += kazanc
            print(f"\n🏆 Canavarı yendin! {kazanc} Pound kazandın.")
            
    elif secim == '5':
        if any(e.isim == "Mutant Beyonder Gözü" for e in oyuncu.envanter):
            oyuncu.envanter = [e for e in oyuncu.envanter if e.isim != "Mutant Beyonder Gözü"]
            oyuncu.iksir_ic()
            if oyuncu.sanity <= 0: print("\n💀 Delirdin..."); break
        else:
            print("\n❌ Ritüel için 'Mutant Beyonder Gözü' lazım!")
            
    elif secim == '6':
        print("\n=== KARABORSA DÜKKANI ===")
        for i, esya in enumerate(dukkan_esyalari): print(f"{i+1}. {esya.isim} - {esya.fiyat} Pound")
        alim = input("Almak istediğiniz (Çıkış için 0): ")
        if alim.isdigit() and 0 < int(alim) <= len(dukkan_esyalari):
            secilen = dukkan_esyalari[int(alim)-1]
            if oyuncu.pound >= secilen.fiyat:
                oyuncu.pound -= secilen.fiyat; oyuncu.esya_al(secilen)
            else: print("\n❌ Paran yetmiyor!")
            
    elif secim == '7':
        gizemli_haberci.konus()
        time.sleep(1.5)
        
    elif secim == '8' and hikaye.adim != 2:
        veritabani.oyunu_kaydet(oyuncu, hikaye)
        break
        
    elif secim == '8' and hikaye.adim == 2:
        boss = Dusman("Yozlaşmış Rahip Lane", hp=90, min_hasar=12, max_hasar=22)
        print(f"\n⛪ Kilisenin kapısını kırarak içeri girdin! '{boss.isim}' sana saldırdı!")
        while boss.hp > 0 and oyuncu.hp > 0:
            if input(f"🚨 [SENİN HP: {oyuncu.hp} | BOSS HP: {boss.hp}] 1- Karşı Koy: ") == '1':
                boss.hasar_al(oyuncu.saldir())
                if boss.hp > 0: oyuncu.hasar_al(boss.saldir())
        if oyuncu.hp <= 0:
            print("\n💀 Boss zihnini paramparça etti."); break
        elif boss.hp <= 0:
            hikaye.adim = 3
            print("\n🏆 Boss yere yığıldı. 1. BÖLÜMÜN SONU. Harika bir iş çıkardın!")
            veritabani.oyunu_kaydet(oyuncu, hikaye)
            break
            
    elif secim == '9' and hikaye.adim == 2:
        veritabani.oyunu_kaydet(oyuncu, hikaye)
        break