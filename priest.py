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

    def animate(self):
        now = pg.time.get_ticks()
        if self.isReadingMass: #walking S towards player
            if now - self.last_update > WALKING_ANIMATION_UPDATE_TIME:
                self.last_update = now
                self.image = self.getReadingMassAnimation();
        else:
            self.image = game.priest_img

    def getReadingMassAnimation(self):
        self.current_frame = (self.current_frame + 1) % len(self.game.priestReadingAnimation)
        return self.game.priestReadingAnimation[self.current_frame]
