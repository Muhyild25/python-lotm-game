from varlik import Varlik
import random

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
        
        # Envanter yazdırma mantığı değişti (Çünkü artık çantamızda nesneler var)
        print("🎒 Envanter      :")
        if not self.envanter:
            print("  - Boş")
        else:
            for esya in self.envanter:
                print(f"  - {esya.isim} ({esya.aciklama})")
        print("===================================\n")

    def saldir(self):
        # Eğer envanterde ekstra hasar veren bir silah varsa gücümüze eklenir
        taban_hasar = random.randint(10, 20)
        ekstra_guc = 0
        for esya in self.envanter:
            if hasattr(esya, 'ekstra_hasar'): # Eşyanın hasar özelliği var mı diye bakıyoruz
                ekstra_guc += esya.ekstra_hasar
                
        return taban_hasar + ekstra_guc
        
    def esya_al(self, yeni_esya):
        self.envanter.append(yeni_esya)
        # Artık parametre bir obje olduğu için yeni_esya.isim yazıyoruz
        print(f"📦 '{yeni_esya.isim}' envantere eklendi.")

    def iksir_ic(self):
        print("\n🧪 Kazanda kaynayan mistik sıvıyı kafana diktin...")
        self.sequence -= 1 
        
        # Eğer envanterde tılsım varsa delilik daha az vurur
        delilik_hasari = 30
        for esya in self.envanter:
            if hasattr(esya, 'sanity_koruma'):
                delilik_hasari -= esya.sanity_koruma
                print(f"✨ Üzerindeki {esya.isim} parladı ve seni yozlaşmadan biraz korudu!")
                
        self.sanity -= delilik_hasari  
        
        print(f"✨ Gözlerinin önünde yıldızlar patlıyor! Gizli varlıkların fısıltılarını duyuyorsun...")
        print(f"🔼 Tebrikler! Dizi (Sequence) {self.sequence} oldun!")
        if self.sanity > 0:
            print(f"⚠️ Dikkat! Akıl sağlığın kritik seviyeye düştü: {self.sanity}/100")