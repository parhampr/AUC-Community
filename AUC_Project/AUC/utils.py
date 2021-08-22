
from django.contrib import messages
class SendMessage:
    def __init__(self, request):
        self.REQUEST = request
        self.MESSAGE_TYPE = 20
        self.MESSAGE = ""
        self.EXTRA_TAGS = None
    
    def Message(self, message, extras, type=20):
        self.EXTRA_TAGS = extras
        if type == 30 and extras == None:
            return KeyError
        self.MESSAGE_TYPE = type
        self.MESSAGE = message
        messages.add_message(self.REQUEST, self.MESSAGE_TYPE, self.MESSAGE, extra_tags=self.EXTRA_TAGS)
        return self
    
    def Info(self, message, extras = None):
        return self.Message(message, extras)
    
    def Success(self, message, extras = None):
        return self.Message(message, extras, 25)
    
    def Warning(self, message, extras = None):
        return self.Message(message, extras, 30)
    
    def Error(self, message, extras = None):
        return self.Message(message, extras, 40)