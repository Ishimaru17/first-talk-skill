from mycroft import MycroftSkill, intent_file_handler
from adapt.intent import IntentBuilder

class FirstTalk(MycroftSkill):
	def __init__(self):
		super(FirstTalk, self).__init__(name="FirstTalk")

	@intent_file_handler(IntentBuilder("TalkFirstIntent").require("InitialTalk").build())
	def handle_talk_first(self, message):
		self.speak_dialog('talk.first')

	def stop(self):
		pass


def create_skill():
	return FirstTalk()

