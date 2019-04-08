from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from adapt.intent import IntentBuilder
from os.path import join, exists
from termios import tcflush, TCIOFLUSH

import subprocess
import sys
import os
import time


def read_talk(conv):
	output = ""
	output += conv.stdout.read(1).decode()
	output += "____test____"
	return output

def cmd(action):
	test = TalkTest(action)
	return test.talk_to_you()


class FirstTalk(MycroftSkill):
	def __init__(self):
		super(FirstTalk, self).__init__(name="FirstTalk")
		self.talk = None
		self.conversation = False
	
	@intent_handler(IntentBuilder("TalkFirstIntent").require("InitialTalk").build())
	def handle_talk_first__intent(self, message):
		if not self.talk:
			self.talk = True
			time.sleep(0.1)
		self.speak_dialog('talk.first')
		self.conversation = True

	@intent_handler(IntentBuilder("TestMessageIntent").require("Help").build())
	def handle_test_message__intent(self, message):
		if self.talk:
			self.speak_dialog('talk.help')

	def stop_conversation(self):
		self.conversation = False
		self.speak('Leave')

	def stop(self, message = None):
		if self.talk:
			self.stop_conversation()

	def converse(self, utterance, lang):
		if utterance:
			utterance = utterance[0]
			if self.conversation:
				if "quit" in utterance or "exit" in utterance:
					self.stop_conversation()
					return True
				else: 
					the_talk = cmd(utterance)
					self.speak(the_talk)
					return True
		return False



class TalkTest:
	def __init__(self, cmd):
		self.cmd = cmd

	def talk_to_you(self):
		if self.cmd == "quit" or self.cmd == "exit":
			return "Bye human!"
		else:
			talk = "I like " + self.cmd
			return talk



def create_skill():
	return FirstTalk()

