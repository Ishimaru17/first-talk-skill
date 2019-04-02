from mycroft import MycroftSkill, intent_file_handler


class FirstTalk(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('talk.first.intent')
    def handle_talk_first(self, message):
        self.speak_dialog('talk.first')


def create_skill():
    return FirstTalk()

