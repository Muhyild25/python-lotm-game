import random

class NPC:
    def __init__(self, isim, unvan, sirlar):
        self.isim = isim
        self.unvan = unvan
        # NPC'nin bize verebileceği rastgele bilgilerin listesi
        self.sirlar = sirlar 

    def konus(self):
        print(f"\n👤 [{self.unvan}] {self.isim} sana doğru yaklaştı...")
        # Sırlar listesinden rastgele bir cümle seçip söylüyor
        sir = random.choice(self.sirlar)
        print(f"💬 '{sir}'")