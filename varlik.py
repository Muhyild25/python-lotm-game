class Varlik:
    """
    Oyun evrenindeki tüm karakter ve düşmanların türetildiği temel sınıf (Base Class).
    Kalıtım (Inheritance) hiyerarşisinin kökünü oluşturur ve ortak durum (state) yönetimini sağlar.
    """
    def __init__(self, isim, hp):
        self.isim = isim
        self.hp = hp

    def hasar_al(self, miktar):
        """
        Varlığın sağlık puanı (HP) durumunu günceller.
        Hesaplama sonrası sağlık değerinin negatif sınırlara inmesini engelleyerek veri tutarlılığını (Data Consistency) korur.
        """
        self.hp -= miktar
        
        # Sınır kontrolü (Clamping)
        if self.hp < 0:
            self.hp = 0