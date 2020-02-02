from townsPeople import *

class Priest(Person):
    def __init__(self, game, x, y, image):
        super().__init__(game, x, y, image)
        self.hitbox.setDimensions(-70, -80)
        self.rect.center = (self.x, self.y)
        self.isReadingMass = True
        self.last_update = 0
        self.current_frame = 0

    def update(self):
        super().update()
        self.animate()
        if self.desire == "readMass" and pg.sprite.collide_rect(self, self.game.alter):
            self.state = "readingMass"
            self.desire = "idle"
            self.pos = vec(self.game.alter.x, self.game.alter.y)
            self.offsetImageX = -32
            self.offsetImageY = -66


    def animate(self):
        now = pg.time.get_ticks()
        if self.state == "readingMass": #walking S towards player
            if now - self.last_update > WALKING_ANIMATION_UPDATE_TIME:
                self.last_update = now
                self.image = self.getReadingMassAnimation();
        else:
            self.image = self.game.priest_img

    def getReadingMassAnimation(self):
        self.current_frame = (self.current_frame + 1) % len(self.game.priestReadingAnimation)
        return self.game.priestReadingAnimation[self.current_frame]
