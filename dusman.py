from varlik import Varlik
import random

class Dusman(Varlik):
    """
    Oyun dünyasındaki tüm düşman ve canavar varyasyonlarını temsil eden alt sınıf (Child Class).
    Varlik temel sınıfından (Base Class) miras alır; düşmana özgü nitelikleri ve 
    hasar aralıklarını (Damage Ranges) saklar.
    """
    def __init__(self, isim, hp, min_hasar, max_hasar):
        super().__init__(isim, hp)
        self.min_hasar = min_hasar
        self.max_hasar = max_hasar

    def saldir(self):
        """
        Düşmanın saldırı eylemini gerçekleştirir.
        Belirlenen alt ve üst hasar sınırları arasında RNG (Random Number Generation) 
        tabanlı dinamik bir hasar çözümlemesi (Damage Resolution) uygular.
        """
        return random.randint(self.min_hasar, self.max_hasar)