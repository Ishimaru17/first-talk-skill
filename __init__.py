from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from adapt.intent import IntentBuilder
from os.path import join, exists
from termios import tcflush, TCIOFLUSH

import subprocess
import re
import sys
import os
import time

#command that activate the response to a speech.
def cmd(action, dir):
	test = TalkTest(action, dir)
	return test.talk_to_you()

#Class inheritant from MycroftSkill which allow the dialog.
class FirstTalk(MycroftSkill):

	#Initializqtion thanks to the super constructor.
	def __init__(self):
		super(FirstTalk, self).__init__(name="FirstTalk")
		self.talk = None
		self.conversation = False
		self.path = self._dir
	
	#Function calls whenever a line of InitialTalk is said
	#This function began the conversation between Mycroft and the user.
	@intent_handler(IntentBuilder("TalkFirstIntent").require("InitialTalk").build())
	def handle_talk_first__intent(self, message):
		if not self.talk:
			self.talk = True
			time.sleep(0.1)
		self.speak_dialog('talk.first')
		self.conversation = True

	#Function which is call when the user ask for help
	#TODO allow this function to be call in the conversation
	@intent_handler(IntentBuilder("TestMessageIntent").require("Help").build())
	def handle_test_message__intent(self, message):
		if self.talk:
			self.speak_dialog('talk.help')

	#Stop the conversation between Mycroft and the user
	def stop_conversation(self):
		self.conversation = False
		self.speak('Leave')

	#If there is a talk, stop it by calling the corresponding function
	def stop(self, message = None):
		if self.talk:
			self.stop_conversation()

	#As long as this function return true, the conversation is still on
	def converse(self, utterance, lang):

		if utterance:
			utterance = utterance[0]
			if self.conversation:
				if "quit" in utterance or "exit" in utterance:
					self.stop_conversation()
					return True
				else: 
					the_talk = cmd(utterance, self.path)
					self.speak(the_talk)
					return True
		return False


#Class of the different talking.
class TalkTest:
	def __init__(self, cmd, dir):
		self.cmd = cmd
		self.dir = dir
		self.data_path = join(self.dir, 'name.txt')

	def is_in(self, vocab, talk):
		voc_path = join('vocab/en-us/', vocab)
		path = join(self.dir, voc_path)
		file = open(path, 'r')
		lines = file.readlines()
		file.close()
		for line in lines:
			if talk.lower() in line.lower():
				return line
		return None

	def is_talk_in(self, talk, vocab, response):
		if self.is_in(vocab, talk) is not None:
			resp_path = join('dialog/en-us/', response)
			path_dialog = join(self.dir, resp_path)
			file = open(path_dialog, 'r')
			content = file.read()
			file.close()
			return content 
		return None

	def save_name(self, vocab, talk):
		name_line = self.is_in(vocab, talk)
		if name_line is not None:
			result = re.split(name_line.lower(), talk.lower())
			name = re.split('\W+', result[1])
			file = open(self.data_path, 'w+')
			file.write(name.capitalize())
			file.close()

	def get_name(self):
		if os.path.exists(self.data_path):
			file = open(self.data_path, 'r')
			name = file.read()
			file.close()
			return name
		return None


	#Act like a parrot. Return the given text.
	def talk_to_you(self):
		talk = self.cmd
		talkative = self.is_talk_in(talk, 'Help.voc', 'Help.dialog')
		is_name = self.save_name('Name.voc', talk)
		if talkative is not None:
			return talkative
		if self.get_name() is not None:
			talk += self.get_name()
		return talk


#create the skill and load it in mycroft when it is launch. 
def create_skill():
	return FirstTalk()

