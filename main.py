from hex import Hex
from ui import UI
from agent import Player
from ursina import Ursina, color, window

player = None
app = Ursina()
window.color = color._20

UI.create_ui()

def tick():
	# TODO replace this with ticking all the hexes
	Hex.current.tick()
	if Hex.current.taint <=0:
		action1.disabled = True
	else:
		action1.disabled = False
	if player.taint > 0:
		action2.text = "Ground"
		action2.on_click = player.ground
		action2.disabled = False
		action2.visible = True
	else:
		action2.disabled = True

Hex.create_map(3)

app.run()