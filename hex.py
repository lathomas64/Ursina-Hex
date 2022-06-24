'''
putzing around with clickable hexes
'''
# Next up move and limit actions to current hex.
from ursina import *
from LiSE import Engine
from LiSE.allegedb import GraphNameError
import networkx as nx
from random import randrange

#class Hex(Button):
	
app = Ursina()
window.color = color._20

gold = 0
counter = Text(text='Choose a starting location.', y=.4, z=-1, scale=2, origin=(0,0), background=True)
left_text = Text(text='Left Text.', y=.4, x=-.6, z=-1, scale=2, origin=(0,0), background=True)
right_text = Text(text='Right Text.', y=.4, x=.6, z=-1, scale=2, origin=(0,0), background=True)
action1 = Button(text="Gather Time", disabled=True, visible=False, y=.3, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
action2 = Button(text="Gather Space", disabled=True, visible=False, y=.245, x=.6, z=-1, scale=(.2,.05,.1), origin=(0,0))
left_text.visible = False
#right_text.visible = False
#player_icon = 'sword'


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
	
class Agent(Entity):
	def __init__(self, location, texture):
		self.location = location
		#Entity(parent=self.model, name=f'buttonicon_entity_{value}', model='quad', texture=value, z=-.1, add_to_scene_entities=False)
		super().__init__(parent=location, model='quad', scale=location.scale,texture=texture, disabled=False, z=-.1)
	
	def tick(self):
		raise NotImplementedError("Children of Agent should implement this")

player = None
class Player(Agent):
	def __init__(self, location):
		self.taint = 0
		self.turn = 1
		super().__init__(location, "vine-flower")
		
	@classmethod
	def createPlayer(cls, location):
		global player
		player = Player(location)
		
	def tick(self):
		counter.text = "Turn: "+str(self.turn)

	def purify(self):
		purify_amount = 10 * ((100.0-self.taint)/100)
		self.taint = self.taint + 1 
		Hex.current.taint  -= purify_amount
		if Hex.current.taint < 0:
			Hex.current.taint = 0 
		left_text.text = str((Hex.current))
		self.turn = self.turn + 1
		tick()
		right_text.text = "Your taint: "+str(self.taint)+"%"
		if self.taint >100:
			counter.text = "You Died!"
	
	def ground(self):
		self.taint -= 10
		if self.taint < 0:
			self.taint = 0 
		self.turn = self.turn + 1
		tick()
		right_text.text = "Your taint: "+str(self.taint)+"%"

class Human(Agent):
	def __init__(self, location):
		super().__init__(location, "human")
		
class Hex(Button):
	current = None
	agents = []
	map = nx.Graph() #https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py
	directions = {
		"northeast":(1,-1),
		"east" : (1,0),
		"southeast" : (0,1),
		"northwest" : (0,-1),
		"west" : (-1,0),
		"southwest" : (-1,1)
	}
	def __init__(self, q,r,scale = .125, color=color.azure, disabled=False, **kwargs):
		self.q = q
		self.r = r
		x_offset = q * scale + r * scale/2
		y_offset = r * scale
		super().__init__(x=x_offset, y=y_offset, scale=scale, color=color, disabled=disabled, kwargs=kwargs)
		self.model = Circle(6)
		self.on_click = self.select		
		label = str((self.q,self.r))
		Hex.map.add_node(label, data=self)
		self.base_color = color
		self.base_scale = scale
		self.taint = randrange(1,100)
		self.color = self.base_color.tint(self.taint/100)
		if randrange(1,100) < 20:
			human = Human(self)
	
	def tick(self):
		self.color = self.base_color.tint(self.taint/100)

	def select(self):
		global player
		if Hex.current and Hex.current != self:
			Hex.current.scale = Hex.current.base_scale
		#self.text = "clicked"
		self.scale = self.base_scale * 1.2
		#self.icon = "human"
		Hex.current = self
		left_text.text = str((self))
		left_text.visible = True
		if player is None:
			Player.createPlayer(self)
		if(self.taint > 0):
			action1.text = "Purify"
			action1.on_click = player.purify
			action1.disabled = False 
			action1.visible = True
		else:
			action1.disabled = True
	
	def __str__(self):
		result = str((self.q,self.r))
		result += "\ntaint:\t"+str(round(self.taint,1))+"%"
		return result

	@classmethod
	def create_map(cls, radius):
		for q in range(-radius, radius+1):
			for r in range(-radius, radius+1):
				if abs(q+r) <=radius:
					hex = Hex(q,r)

		#cls.map["created"] = {}
		#cls.map["created"][(0,0)] = 
		#for index = -radius; index <= radius; index++:
		#	Hex(cls.directions["northeast"][0], cls.directions["northeast"][1])



Hex.create_map(3)
print("\n\nHex MAP!\n\n")
print(Hex.map.nodes)
print(Hex.map["(0, 0)"])
print(Hex.map["(0, 0)"])
print("======================")


app.run()
