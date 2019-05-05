import prompt

class Test():
	def __init__(self):
		self.CONST = 5

t = Test()

while 1:
	user_input = prompt.command(globals())

	try:
		exec(user_input)
	except Exception as e:
		print(e)