import random

class NPC:
    """
    Oyun dünyasındaki oyuncu dışı karakterleri (Non-Playable Character) temsil eden sınıf.
    Evrenin arka plan hikayesinin aktarımı (Lore Delivery) ve ipucu (Hint) sağlama işlevlerini yönetir.
    """
    def __init__(self, isim, unvan, sirlar):
        self.isim = isim
        self.unvan = unvan
        
        # Encapsulation: NPC'nin etkileşim anında kullanacağı diyalog havuzunu (Dialogue Pool) tutan veri yapısı.
        self.sirlar = sirlar 

    def konus(self):
        """
        Kullanıcı tarafından bir diyalog etkileşimi (Interaction Event) tetiklendiğinde çalışır.
        RNG (Random Number Generation) kullanılarak diyalog havuzundan dinamik metin seçilir.
        """
        print(f"\n👤 [{self.unvan}] {self.isim} sana doğru yaklaştı...")
        
        # Dinamik bilgi aktarımı (Lore/Hint injection)
        sir = random.choice(self.sirlar)
        print(f"💬 '{sir}'")