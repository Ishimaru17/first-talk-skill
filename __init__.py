from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from adapt.intent import IntentBuilder
from os.path import join, exists
from termios import tcflush, TCIOFLUSH
from test import *

import subprocess
import sys
import os


def read_talk(conv):
	output = ""
	output += conv.stdout.read(1).decode()
	output += "____test____"
	return output

def cmd(talk, action):
	TalkTest(action)

class FirstTalk(MycroftSkill):
	def __init__(self):
		super(FirstTalk, self).__init__(name="FirstTalk")
		self.talk = None
		self.conversation = False
		self.data = join(self._dir, 'data.sh')

	@intent_handler(IntentBuilder("TalkFirstIntent").require("InitialTalk").build())
	def handle_talk_first__intent(self, message):
		if not self.talk:
			self.talk = subprocess.Popen([self.data], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		cmd(self.talk, 'look')
		self.speak_dialog('talk.first')
		self.conversation = True

	def stop_conversation(self):
		self.playing = False
		self.speak('Leave')
		LOG.info('Leave')

	def stop(self, message = None):
		if self.talk:
			self.stop_conversation()

	def converse(self, utterance):
		if utterance:
			utterance = utterance[0]
			if self.conversation:
				if "quit" in utterance or utterance == "exit":
					self.stop_conversation()
					return True
				else: 
					cmd(self.talk, utterance)
					question = read_talk(self.talk)
					if question != "":
						self.speak(question)
						return True
		return False




def create_skill():
	return FirstTalk()

