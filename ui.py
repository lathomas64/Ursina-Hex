from ursina import Text, Button

class UI:
    actions = {}
    start_y = .3
    margin_y = .055

    @classmethod
    def add_action(cls, text, callback):
        print(cls.actions)
        print(cls.start_y)
        print(len(cls.actions))
        print(cls.margin_y)
        print(cls.start_y-len(cls.actions)*cls.margin_y)
        print("===")
        if text not in cls.actions:
            cls.actions[text] = Button(text=text,
                                        disabled=False,
                                        visible=True,
                                        y=cls.start_y-len(cls.actions)*cls.margin_y,
                                        x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
        cls.actions[text].on_click = callback
        print(cls.actions)
        print("***")

    @classmethod
    def remove_action(cls, text):
        cls.actions[text].visible = False
        cls.actions[text].disabled = True
        del cls.actions[text]

    @classmethod
    def clear_actions(cls):
        del(cls.actions)
        cls.actions = {}


    @classmethod
    def create_ui(cls):
        cls.main_text = Text(text='Choose a starting location.', y=.4, z=-1, scale=2, origin=(0,0), background=True)
        cls.left_text = Text(text='Left Text.', y=.4, x=-.6, z=-1, scale=2, origin=(0,0), background=True)
        cls.right_text = Text(text='Right Text.', y=.4, x=.6, z=-1, scale=2, origin=(0,0), background=True)
        #cls.action1 = Button(text="Gather Time", disabled=True, visible=False, y=.3, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
        #cls.action2 = Button(text="Gather Space", disabled=True, visible=False, y=.245, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))