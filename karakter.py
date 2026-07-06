from varlik import Varlik
import random

# ANA KARAKTER KALIBI
class Karakter(Varlik):
    def __init__(self, isim, pathway):
        super().__init__(isim, hp=100) 
        self.pathway = pathway
        self.sequence = 9
        self.sanity = 100
        self.pound = 15
        self.envanter = [] 
        
    def durum_goster(self):
        print(f"\n=== {self.isim} Karakter Ekranı ===")
        print(f"🔮 Yol (Pathway) : {self.pathway}")
        print(f"🔼 Dizi (Sequence): {self.sequence}")
        print(f"❤️ Can (HP)      : {self.hp}/100")
        print(f"🧠 Akıl Sağlığı  : {self.sanity}/100")
        print(f"💰 Bakiye        : {self.pound} Pound")
        print("🎒 Envanter      :")
        if not self.envanter:
            print("  - Boş")
        else:
            for esya in self.envanter:
                print(f"  - {esya.isim} ({esya.aciklama})")
        print("===================================\n")

    def _ekstra_hasar_hesapla(self):
        ekstra = 0
        for esya in self.envanter:
            if hasattr(esya, 'ekstra_hasar'):
                ekstra += esya.ekstra_hasar
        return ekstra

    def esya_al(self, yeni_esya):
        self.envanter.append(yeni_esya)
        print(f"📦 '{yeni_esya.isim}' envantere eklendi.")

    def iksir_ic(self):
        print("\n🧪 Kazanda kaynayan mistik sıvıyı kafana diktin...")
        self.sequence -= 1 
        delilik_hasari = 30
        for esya in self.envanter:
            if hasattr(esya, 'sanity_koruma'):
                delilik_hasari -= esya.sanity_koruma
                print(f"✨ Üzerindeki {esya.isim} parladı ve seni yozlaşmadan biraz korudu!")
        self.sanity -= delilik_hasari  
        print(f"✨ Gözlerinin önünde yıldızlar patlıyor! Gizli varlıkların fısıltılarını duyuyorsun...")
        print(f"🔼 Tebrikler! Dizi (Sequence) {self.sequence} oldun!")

    def saldir(self):
        return random.randint(10, 20) + self._ekstra_hasar_hesapla()

    # Eğer alt sınıf özel yetenek tanımlamazsa diye boş bir kalıp bırakıyoruz
    def ozel_yetenek(self):
        return 0

# ==========================================
# PATHWAY (YOL) ALT SINIFLARI VE YETENEKLERİ
# ==========================================

class Seer(Karakter):
    def __init__(self, isim):
        super().__init__(isim, pathway="Seer")
        
    def saldir(self):
        taban_hasar = random.randint(8, 15)
        if random.randint(1, 4) == 1:
            print("✨ Geleceği öngörerek düşmanın zayıf noktasına vurdun! (KRİTİK HASAR)")
            taban_hasar *= 2
        return taban_hasar + self._ekstra_hasar_hesapla()
        
    def ozel_yetenek(self):
        if self.sanity >= 15:
            self.sanity -= 15
            print("\n🔮 [YETENEK] 'Ruhsal Kırbaç': Düşmanın zihnine doğrudan saldırdın! (-15 Sanity)")
            return random.randint(25, 35) + self._ekstra_hasar_hesapla()
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0

class Sleepless(Karakter):
    def __init__(self, isim):
        super().__init__(isim, pathway="Sleepless")
        self.hp = 120 
        
    def saldir(self):
        print("⚔️ Gecenin karanlığından güç alarak ağır bir darbe indirdin!")
        return random.randint(12, 18) + self._ekstra_hasar_hesapla()
        
    def ozel_yetenek(self):
        if self.sanity >= 10:
            self.sanity -= 10
            iyilesme = 35
            self.hp = min(120, self.hp + iyilesme)
            print(f"\n🌙 [YETENEK] 'Karanlığın Kucağı': Gölgeler kanayan yaralarını sardı! (+{iyilesme} HP, -10 Sanity)")
            return 0 # Hasar vurmuyor, kendini iyileştiriyor
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0

class Assassin(Karakter):
    def __init__(self, isim):
        super().__init__(isim, pathway="Assassin")
        
    def saldir(self):
        if random.randint(1, 5) == 1:
            print("💨 Hızlı davranmaya çalışırken gölgelerde takıldın ve ıskaladın!")
            return 0
        else:
            print("🗡️ Gölgelerin içinden ölümcül bir hızla fırladın!")
            return random.randint(15, 25) + self._ekstra_hasar_hesapla()
            
    def ozel_yetenek(self):
        if self.sanity >= 20:
            self.sanity -= 20
            print("\n🗡️ [YETENEK] 'Gölge İnfazı': Tamamen görünmez olup düşmanın kalbine saldırdın! (-20 Sanity)")
            return random.randint(45, 60) + self._ekstra_hasar_hesapla()
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0