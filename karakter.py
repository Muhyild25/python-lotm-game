from varlik import Varlik
import random

class Karakter(Varlik):
    """
    Oynanabilir karakterler için Temel Sınıf (Base Class).
    Varlik sınıfından miras (Inheritance) alır; oyuncunun envanter, 
    ekonomi ve gelişim durumlarını (State Management) yönetir.
    """
    def __init__(self, isim, pathway):
        super().__init__(isim, hp=100) 
        self.pathway = pathway
        self.sequence = 9
        self.sanity = 100
        self.pound = 15
        self.envanter = [] 
        
    def durum_goster(self):
        """Karakterin anlık state'lerini View (Görünüm) katmanına yansıtır."""
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
        """
        [Protected Method] Karakterin envanterindeki nesnelerin hasar 
        çarpanlarını (Modifiers) iteratif olarak toplayıp hesaplar.
        """
        ekstra = 0
        for esya in self.envanter:
            if hasattr(esya, 'ekstra_hasar'):
                ekstra += esya.ekstra_hasar
        return ekstra

    def esya_al(self, yeni_esya):
        self.envanter.append(yeni_esya)
        print(f"📦 '{yeni_esya.isim}' envantere eklendi.")

    def iksir_ic(self):
        """
        Karakter Gelişim Algoritması (Progression Mechanism).
        Envanterdeki koruyucu eşyaların (Buff) özelliklerini dinamik olarak 
        sorgulayıp (hasattr) Sanity cezasını (Penalty) hafifletir.
        """
        print("\n🧪 Kazanda kaynayan mistik sıvıyı kafana diktin...")
        self.sequence -= 1 
        
        # Ceza Hafifletme (Penalty Mitigation) Algoritması
        delilik_hasari = 30
        for esya in self.envanter:
            if hasattr(esya, 'sanity_koruma'):
                delilik_hasari -= esya.sanity_koruma
                print(f"✨ Üzerindeki {esya.isim} parladı ve seni yozlaşmadan biraz korudu!")
                
        self.sanity -= delilik_hasari  
        print(f"✨ Gözlerinin önünde yıldızlar patlıyor! Gizli varlıkların fısıltılarını duyuyorsun...")
        print(f"🔼 Tebrikler! Dizi (Sequence) {self.sequence} oldun!")

    def saldir(self):
        """Varsayılan (Default) hasar hesaplama metodu."""
        return random.randint(10, 20) + self._ekstra_hasar_hesapla()

    def ozel_yetenek(self):
        """
        Sanal Metot (Virtual Method) şablonu.
        Polymorphism gereği alt sınıflar (Child Classes) tarafından ezilmelidir (Override).
        """
        return 0

# ==========================================
# POLYMORPHIC ALT SINIFLAR (CHILD CLASSES)
# ==========================================

class Seer(Karakter):
    """Kahin Sınıfı: Yüksek kritik şansı ve doğrudan zihinsel hasar dinamikleri barındırır."""
    def __init__(self, isim):
        super().__init__(isim, pathway="Seer")
        
    def saldir(self):
        # Method Overriding: Seer sınıfına özel kritik vuruş (Critical Hit) algoritması.
        taban_hasar = random.randint(8, 15)
        if random.randint(1, 4) == 1:
            print("✨ Geleceği öngörerek düşmanın zayıf noktasına vurdun! (KRİTİK HASAR)")
            taban_hasar *= 2
        return taban_hasar + self._ekstra_hasar_hesapla()
        
    def ozel_yetenek(self):
        # Resource (Sanity) harcayarak yüksek burst hasar çıkarır.
        if self.sanity >= 15:
            self.sanity -= 15
            print("\n🔮 [YETENEK] 'Ruhsal Kırbaç': Düşmanın zihnine doğrudan saldırdın! (-15 Sanity)")
            return random.randint(25, 35) + self._ekstra_hasar_hesapla()
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0

class Sleepless(Karakter):
    """Uykusuz Sınıfı: Yüksek base HP ve kendini iyileştirme (Self-Heal) mekanikleri barındırır."""
    def __init__(self, isim):
        super().__init__(isim, pathway="Sleepless")
        self.hp = 120 # Stat Scaling (Temel dayanıklılık artışı)
        
    def saldir(self):
        print("⚔️ Gecenin karanlığından güç alarak ağır bir darbe indirdin!")
        return random.randint(12, 18) + self._ekstra_hasar_hesapla()
        
    def ozel_yetenek(self):
        # Hasar yerine karakterin HP state'ini yenileyen defansif yetenek.
        if self.sanity >= 10:
            self.sanity -= 10
            iyilesme = 35
            self.hp = min(120, self.hp + iyilesme)
            print(f"\n🌙 [YETENEK] 'Karanlığın Kucağı': Gölgeler kanayan yaralarını sardı! (+{iyilesme} HP, -10 Sanity)")
            return 0 
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0

class Assassin(Karakter):
    """Suikastçi Sınıfı: Yüksek risk (ıskalama şansı) ve aşırı yüksek anlık hasar (Burst) dinamikleri barındırır."""
    def __init__(self, isim):
        super().__init__(isim, pathway="Assassin")
        
    def saldir(self):
        # RNG tabanlı miss (ıskalama) mekaniği entegrasyonu.
        if random.randint(1, 5) == 1:
            print("💨 Hızlı davranmaya çalışırken gölgelerde takıldın ve ıskaladın!")
            return 0
        else:
            print("🗡️ Gölgelerin içinden ölümcül bir hızla fırladın!")
            return random.randint(15, 25) + self._ekstra_hasar_hesapla()
            
    def ozel_yetenek(self):
        # Yüksek riskli (20 Sanity), yüksek ödüllü ultimate yetenek.
        if self.sanity >= 20:
            self.sanity -= 20
            print("\n🗡️ [YETENEK] 'Gölge İnfazı': Tamamen görünmez olup düşmanın kalbine saldırdın! (-20 Sanity)")
            return random.randint(45, 60) + self._ekstra_hasar_hesapla()
        else:
            print("\n❌ Zihnin bu büyüyü kaldıramaz! Yeterli Akıl Sağlığın yok.")
            return 0