class TalkTest:
	def __init__(self, cmd):
		self.cmd = cmd
		talk_to_you()

	def talk_to_you(self):
		if self.cmd == "quit" or self.cmd == "exit":
			return "Bye human!"
		else:
			talk = "I like " + self.cmd
			return talk
