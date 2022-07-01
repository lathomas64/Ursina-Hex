from ursina import Text, Button
import traceback, sys

class UI:
    actions = {}
    active_actions = {}
    action_buttons = []
    start_y = .3
    margin_y = .055

    @classmethod
    def add_action(cls, text, callback):
        if text not in cls.actions:
            new_button  = Button(text=text,
                                        disabled=False,
                                        visible=True,
                                        y=cls.start_y-len(cls.actions)*cls.margin_y,
                                        x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
            cls.actions[text] = new_button

        cls.actions[text].on_click = callback
        if text not in cls.active_actions:
            cls.active_actions[text] = cls.actions[text]
        cls.update_ui()

    @classmethod
    def remove_action(cls, text):
        if text in cls.active_actions:
            del cls.active_actions[text]
        cls.update_ui()

    @classmethod
    def clear_actions(cls):
        cls.active_actions = {}
        cls.update_ui()

    @classmethod
    def update_ui(cls):
        position = 0
        for label in cls.actions:
            if label in cls.active_actions:
                action = cls.active_actions[label]
                action.y = cls.start_y-position*cls.margin_y
                position += 1
                action.visible = True
                action.disabled = False
            else:
                action = cls.actions[label]
                action.y = 9000
                action.visible = False
                action.disabled = True

    @classmethod
    def create_ui(cls):
        cls.main_text = Text(text='Choose a starting location.', y=.4, z=-1, scale=2, origin=(0,0), background=True)
        cls.left_text = Text(text='Left Text.', y=.4, x=-.6, z=-1, scale=2, origin=(0,0), background=True)
        cls.right_text = Text(text='Right Text.', y=.4, x=.6, z=-1, scale=2, origin=(0,0), background=True)
        #cls.action1 = Button(text="Gather Time", disabled=True, visible=False, y=.3, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
        #cls.action2 = Button(text="Gather Space", disabled=True, visible=False, y=.245, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))