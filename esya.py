# Tüm eşyaların atası
class Esya:
    def __init__(self, isim, fiyat, aciklama):
        self.isim = isim
        self.fiyat = fiyat
        self.aciklama = aciklama

# Esya sınıfından miras alan Silah sınıfı
class Silah(Esya):
    def __init__(self, isim, fiyat, aciklama, ekstra_hasar):
        super().__init__(isim, fiyat, aciklama)
        self.ekstra_hasar = ekstra_hasar

# Esya sınıfından miras alan İyileştirme sınıfı
class Tilsim(Esya):
    def __init__(self, isim, fiyat, aciklama, sanity_koruma):
        super().__init__(isim, fiyat, aciklama)
        self.sanity_koruma = sanity_koruma