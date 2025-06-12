# check that var is a list of three numbers
def checklist(var):
  return (
      isinstance(var, list) and len(var) == 3 
      and (all(isinstance(x, (int, float)) for x in var)) 
      and not (all(isinstance(x, bool) for x in var))
      )

# coverage of a slot
slots = {
	'head':	0.1,
	'body':	0.4,
	'arm':	0.08,
	'hand':	0.07,
	'leg':	0.06,
	'foot':	0.04,
	'test':	0
}

# materials of armor, their ideal ac and rigidity
# ЭТО ВРЕМЕННЫЕ ЗНАЧЕНИЯ ИЗ СТАРОЙ ВЕРСИИ ПРАВИЛ --- ИЗМЕНИТЬ!
materials = {
	'cloth':	[[7,6,5],0],
	'leather-s':[[12,7,5],0.2],
	'leather-h':[[15,12,7],0.4],
	'gambeson':	[[9,5,10],0.1],
	'mail':		[[19,10,5],0.5],
	'scales':	[[19,17,13],0.7], # scales, lamellar, laminar
	'plate':	[[19,19,15],1],
	'test':		[[0,0,0],0]
}

class armor_piece:

	def __init__(self,slot,material,L,S=0,slotsdict=slots,materialsdict=materials):
		"""
		Armor piece

		:param slot: 			Armor slot (basic: head, arm, hand, body, leg, foot). Test slot - 'test' (C=0)
		:param material: 		Armor material (basic: cloth, leather-s, leather-h, gambeson, mail, scales, plate). Test material - 'test' (I,R=0)
		:param L:				Layer of armor (1, 2, or 3)
		:param S: 				Shape factor (applied only to plate, for other materials S=0)
		:param slotsdict:		Dict for custom slots ({'<slot_name>':<coverage>}). Default dict - slots. 
		:param materialsdict:	Dict for custom materials ({'<material_name>':<[[<Is>,<Ip>,<Ib>],<R>]>}). I - slashing, piercing, bludgeoning ac. R - rigidity. Default dict - materials. 
		"""
		# slot and material names
		if str(slot) in slotsdict.keys():
			self.__slot = str(slot)
		else:
			print('No such slot. Setting to test (C=0).')
			self.__slot = 'test'

		if str(material) in materialsdict.keys():
			self.__material = str(material)
		else:
			print('No such material. Setting to test (C=0).')
			self.__material = 'test'


		# armor layer
		if (isinstance(L, (int))) and (1 <= L <= 3):
			self.__layer = L
		else: 
			print('Wrong layer. Should be 1, 2, or 3. Setting to 1.')
			self.__layer = 1


		# ideal ac of armor type, I = [Slashing, Piercing, Bludgeoning]
		self.__ideal = materialsdict[self.__material][0]

		# rigidity of armor type (cloth = 0, plate = 1)
		self.__rigidity = materialsdict[self.__material][1]

		# coverage of armor slot
		self.__coverage = slotsdict[self.__slot]

		# shape factor, used only for plate
		if self.__material != 'plate':
			self.__shape = 0
		elif (isinstance(S, (int,float))) and (0 <= S <= 1):
			self.__shape = S
		else: 
			print('Wrong shape. Should be a number between 0 and 1. Setting to 0.')
			self.__shape = 0



	# block of setters and getters:
	@property
	def slot(self):
		return self.__slot

	@slot.setter
	def slot(self, name):
		self.__slot = str(name)

	@property
	def material(self):
		return self.__material

	@material.setter
	def slot(self, name):
		self.__material = str(name)

	@property
	def ideal(self):
		return self.__ideal

	@ideal.setter
	def ideal(self,I):
		self.__ideal = I if checklist(I) else print('Wrong ideal. Should be a list of three numbers.')

	@property
	def rigidity(self):
		return self.__rigidity

	@rigidity.setter
	def rigidity(self,R):
		self.__rigidity = R if (isinstance(R, (int,float))) and (0 <= R <= 1) else print('Wrong rigidity. Should be a number between 0 and 1.')

	@property
	def coverage(self):
		return self.__coverage

	@coverage.setter
	def coverage(self,C):
		self.__coverage = C if (isinstance(C, (int,float))) and (0 <= C <= 1) else print('Wrong coverage. Should be a number between 0 and 1.')

	@property
	def shape(self):
		return self.__shape

	@shape.setter
	def coverage(self,S):
		self.__shape = S if (isinstance(S, (int,float))) and (0 <= S <= 1) else print('Wrong shape. Should be a number between 0 and 1.')

	@property
	def layer(self):
		return self.__layer

	@layer.setter
	def coverage(self,L):
		self.__layer = L if (isinstance(L, (int))) and (1 <= L <= 3) else print('Wrong layer. Should be 1, 2, or 3.')
	# ====================================


	# redefine str for print
	def __str__(self):
		return f"""Armor piece. 
		type: {self.__material}, slot: {self.__slot}, layer: {self.__layer}.
		Ideal: S - {self.__ideal[0]}, P - {self.__ideal[1]}, B - {self.__ideal[2]}.
		Rigidity: {self.__rigidity}.
		Coverage: {self.__coverage}.
		Shape: {self.__shape}."""

	# custom constructor
	@classmethod
	def custom(cls,slot,material,L,Is,Ip,Ib,R,S,C):
		if all([checklist([Is,Ip,Ib]), 
			isinstance(L, (int)), (1 <= L <= 3),
			isinstance(R, (int,float)), (0 <= R <= 1), 
			isinstance(S, (int,float)), (0 <= S <= 1), 
			isinstance(C, (int,float)), (0 <= C <= 1)]):
			newslots = {slot:C}
			newmaterials = {material : [[Is,Ip,Ib],R]}
			return cls(slot,material,L,S,slotsdict=newslots,materialsdict=newmaterials)
			
		else:
			print('One of the parameters are wrong. Setting all to 0.')
			return cls('test','test',1,0)

	# used in calculator to check if input is armor piece
	def check(self):
		pass

	# calculate armor class of a piece
	def ac(self):
		return [i*self.__coverage for i in self.__ideal]




class ArmorCalculator:

	def __init__(self):
		self.__layer1 = []
		self.__layer2 = []
		self.__layer3 = []


	# Add armor piece to calculation
	def add_piece(self,piece):
		try:
			piece.check()

			if piece.layer == 1:
				self.__layer1.append(piece)
			elif piece.layer == 2:
				self.__layer2.append(piece)
			elif piece.layer == 3:
				self.__layer3.append(piece)
			else:
				print("smth's wrong") # if somehow this will happen

		except(AttributeError):
			print("This isn't an object of type armor_piece.")



	def get_ac(self):
		armor_class = [0,0,0]

		# Slashing ac is calculated on the top layer only:
		top_layer = self.__layer3 if self.__layer3 else (self.__layer2 if self.__layer2 else self.__layer1 if self.__layer1 else None)
		for piece in top_layer:
			armor_class[0] += piece.ac()[0]

		return armor_class



# test
pl = armor_piece('head','plate',3)

calc = ArmorCalculator()
calc.add_piece(pl)
calc.add_piece(armor_piece('arm','cloth',2))
calc.add_piece(armor_piece('body','mail',2))

print(calc.get_ac())