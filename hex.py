'''
putzing around with clickable hexes
'''
# Next up move and limit actions to current hex.
from ursina import *
from LiSE import Engine
from LiSE.allegedb import GraphNameError
import networkx as nx
from random import randrange, choice
from agent import Human, Player
from ui import UI

#class Hex(Button):
	



	

player = None

		
class Hex(Button):
	current = None
	agents = []
	map = nx.Graph() #https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py
	location_hash = {}
	directions = {
		"northeast":(0,1),
		"east" : (1,0),
		"southeast" : (1,-1),
		"northwest" : (-1,1),
		"west" : (-1,0),
		"southwest" : (0,-1)
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
		Hex.location_hash[label] = self
		self.base_color = color
		self.base_scale = scale
		self.taint = randrange(1,100)
		self.color = self.base_color.tint(self.taint/100)
		if randrange(1,100) < 20:
			human = Human(self)
	
	def tick(self):
		self.color = self.base_color.tint(self.taint/100)
		for agent in self.agents:
			agent.tick()

	def adjacent(self, location):
		# We are adjacent if the absolute value of the sum of differences is 1 or 0 (1,1) and (-1,-1) aren't adjacent
		q_diff = self.q-location.q
		if abs(q_diff) > 1:
			return False
		r_diff = self.r-location.r
		if abs(r_diff) > 1:
			return False
		print(q_diff)
		print(r_diff)
		print(abs(q_diff + r_diff))
		return abs(q_diff+r_diff) <= 1

	def select(self):
		if Hex.current and Hex.current != self:
			Hex.current.scale = Hex.current.base_scale
		#self.text = "clicked"
		self.scale = self.base_scale * 1.2
		#self.icon = "human"
		Hex.current = self
		UI.left_text.text = str((self))
		UI.left_text.visible = True
		player = Player.getOrCreatePlayer(self)
		print(self)
		print(player.location)
		if(player.location == self):
			UI.remove_action("Move here")
			if(self.taint > 0):
				UI.add_action("Purify", player.purify)
			else:
				UI.remove_action("Purify")
		elif(self.adjacent(player.location)):
			player.target = self
			UI.remove_action("Purify")
			UI.add_action("Move here", player.move)
		else:
			UI.remove_action("Move here")
	
	def __str__(self):
		result = str((self.q,self.r))
		result += "\ntaint:\t"+str(round(self.taint,1))+"%"
		return result

	def get_random_neighbor(self):
		direction = choice(list(self.directions.values()))
		result = Hex.get(self.q+direction[0], self.r+direction[1])
		print(str(self) + "->" + str(result))
		if result is not None:
			print(self.adjacent(result))
		else:
			print("empty result")
		return result

	@classmethod
	def tick_all(cls):
		for hex_label in cls.location_hash:
			cls.location_hash[hex_label].tick()

	@classmethod
	def get(cls, q, r):
		try:
			return cls.location_hash[str((q,r))]
		except KeyError:
			return None

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




