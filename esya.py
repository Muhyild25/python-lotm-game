class Esya:
    """
    Oyun içi nesneler için Temel Sınıf (Base Class).
    Ekonomi (fiyat) ve envanter yönetiminde kullanılacak ortak nitelikleri (Attributes) tanımlar.
    """
    def __init__(self, isim, fiyat, aciklama):
        self.isim = isim
        self.fiyat = fiyat
        self.aciklama = aciklama


class Silah(Esya):
    """
    Esya sınıfından türetilmiş (Inherited) saldırı nesnesi alt sınıfı.
    Karakterin hasar hesaplama algoritmasına eklenecek 'ekstra_hasar' çarpanını (Modifier) barındırır.
    """
    def __init__(self, isim, fiyat, aciklama, ekstra_hasar):
        super().__init__(isim, fiyat, aciklama)
        self.ekstra_hasar = ekstra_hasar


class Tilsim(Esya):
    """
    Esya sınıfından türetilmiş defansif/mistik nesne alt sınıfı.
    Karakterin delilik (Sanity) mekaniğinde, ceza hafifletici (Damage Mitigation / Buff) olarak işlev görür.
    """
    def __init__(self, isim, fiyat, aciklama, sanity_koruma):
        super().__init__(isim, fiyat, aciklama)
        self.sanity_koruma = sanity_koruma