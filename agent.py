from ursina import Entity
from ui import UI

class Agent(Entity):
    def __init__(self, location, texture):
        self.location = location
        # Entity(parent=self.model, name=f'buttonicon_entity_{value}', model='quad', texture=value, z=-.1, add_to_scene_entities=False)
        super().__init__(parent=location, model='quad', scale=location.scale, texture=texture, disabled=False, z=-.1)

    def tick(self):
        raise NotImplementedError("Children of Agent should implement this")

    def move(self):
        if self.target == None:
            return
        else:
            self.parent = self.target
            self.location = self.target
            self.target = None
            self.tick()


class Player(Agent):
    player = None
    def __init__(self, location):
        self.taint = 0
        self.turn = 1
        super().__init__(location, "vine-flower")

    @classmethod
    def getOrCreatePlayer(cls, location):
        if cls.player == None:
            cls.player = Player(location)
        UI.main_text.text = "Turn: " + str(cls.player.turn)
        return cls.player

    def tick(self):
        UI.main_text.text = "Turn: " + str(self.turn)
        if (self.location.taint > 0):
            UI.add_action("Purify", self.purify)
        else:
            UI.remove_action("Purify")
        if self.taint > 0:
            UI.add_action("Ground", self.ground)
        else:
            UI.remove_action("Ground")

    def purify(self):
        purify_amount = 10 * ((100.0 - self.taint) / 100)
        self.taint = self.taint + 1
        self.location.taint -= purify_amount
        if self.location.taint < 0:
            self.location.taint = 0
        UI.left_text.text = str((self.location))
        self.turn = self.turn + 1
        self.tick()
        UI.right_text.text = "Your taint: " + str(self.taint) + "%"
        if self.taint > 100:
            UI.main_text.text = "You Died!"
        self.location.tick()

    def ground(self):
        self.taint -= 10
        if self.taint < 0:
            self.taint = 0
        self.turn = self.turn + 1
        self.tick()
        UI.right_text.text = "Your taint: " + str(self.taint) + "%"

    def move(self):
        self.turn = self.turn + 1
        super().move()
        UI.remove_action("Move here")
        if (self.location.taint > 0):
            UI.add_action("Purify", self.purify)
        else:
            UI.remove_action("Purify")


class Human(Agent):
    def __init__(self, location):
        super().__init__(location, "human")