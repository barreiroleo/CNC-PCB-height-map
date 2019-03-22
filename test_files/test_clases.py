class prueba:
	atrib = 1
	
	def cambio_atrib(self,parametro):
		self.atrib = parametro
		self.print_atrib()
	
	def print_atrib(self):
		print(self.atrib)

test1 = prueba()
test1.print_atrib()
test1.cambio_atrib(3)
#print(test.atrib)

test2 = prueba()
test2.print_atrib()
test2.cambio_atrib(5)