# Posiciones en memoria de tipos de datos:
# int 0-5,000, float 5,001-10,000, bool 10,001-15,000
class VarTable(dict):
	def __init__(self, pInt = 0, pDecim = 5001, pBool = 10001, pVoid = 15001):
		self.aux = 0
		self.pLast = 0
		self.pInt = pInt
		self.pDecim = pDecim
		self.pBool = pBool
		self.pVoid = pVoid

	def getpInt(self):
		return self.pInt

	def getpDecim(self):
		return self.pDecim

	def getpBool(self):
		return self.pBool

	def getpVoid(self):
		return self.pVoid

	def getpLast(self):
		return self.last.pointer

	def add(self, funcName, t, name):
		if funcName not in self:
			self[funcName] = {}
			
		if t not in self[funcName]:
			self[funcName][t] = {}
			
		if name is "aux":
			name = "t" + str(self.aux)
			self.aux += 1
			
		if t == 'int':
			self[funcName][t][name] = self.pInt
			self.pLast = self.pInt
			self.pInt += 1
		elif t == 'decim':
			self[funcName][t][name] = self.pDecim
			self.pLast = self.pDecim
			self.pDecim += 1
		elif t == 'bool':
			self[funcName][t][name] = self.pBool
			self.pLast = self.pBool
			self.pBool += 1
		elif t == 'funcType':
			self[funcName][t]["return"] = name
		elif t == 'void':
                        self[funcName][t][name] = self.pVoid
                        self.pLast = self.pVoid
                        self.pVoid += 1
		else:
			raise Exception("No such type: " + t)
		return self.pLast

	def addArr(self, funcName, t, name, size):
		if funcName not in self:
			self[funcName] = {}
			
		if t not in self[funcName]:
			self[funcName][t] = {}
			
		if name is "aux":
			name = "t" + str(self.aux)
			self.aux += 1
			
		if t == 'int':
			self[funcName][t][name] = self.pInt
			self.pLast = self.pInt
			self.pInt += size
		elif t == 'decim':
			self[funcName][t][name] = self.pDecim
			self.pLast = self.pDecim
			self.pDecim += size
		elif t == 'bool':
			self[funcName][t][name] = self.pBool
			self.pLast = self.pBool
			self.pBool += size
		else:
			raise Exception("No such type: " + t)
		return self.pLast


