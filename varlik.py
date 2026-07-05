# Her canlının ortak özelliklerini tutan Ata Sınıf (Parent Class)
class Varlik:
    def __init__(self, isim, hp):
        self.isim = isim
        self.hp = hp

    # Ortak bir yetenek: Hasar alma
    def hasar_al(self, miktar):
        self.hp -= miktar
        # Can eksiye düşmesin diye sıfıra sabitliyoruz
        if self.hp < 0:
            self.hp = 0