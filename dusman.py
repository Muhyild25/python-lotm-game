from varlik import Varlik
import random

# Dusman da Varlik sınıfından miras alır
class Dusman(Varlik):
    def __init__(self, isim, hp, min_hasar, max_hasar):
        super().__init__(isim, hp)
        self.min_hasar = min_hasar
        self.max_hasar = max_hasar

    # Düşmanın kendine has saldırı yeteneği
    def saldir(self):
        return random.randint(self.min_hasar, self.max_hasar)