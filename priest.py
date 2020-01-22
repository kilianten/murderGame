from townsPeople import *

class Priest(Person):
    def __init__(self, game, x, y, image):
        super().__init__(game, x, y, image)
        self.hitbox.setDimensions(-70, -80)
        self.rect.center = (self.x, self.y)
