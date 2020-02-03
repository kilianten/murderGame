from townsPeople import *

class Priest(Person):
    def __init__(self, game, x, y, image):
        super().__init__(game, x, y, image)
        self.hitbox.setDimensions(-70, -80)
        self.rect.center = (self.x, self.y)
        self.isReadingMass = True
        self.last_update = 0
        self.current_frame = 0
        self.speechInit()

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

    def speechInit(self):
        self.sermon = ["The path of the righteous man is beset on all sides by the inequities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of the darkness. For he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who attempt to poison and destroy my brothers. And you will know I am the Lord when I lay my vengeance upon you. Ezekiel 25:17."]
