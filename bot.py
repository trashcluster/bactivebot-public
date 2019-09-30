#imports
import requests
import re
from functools import wraps
from telegram.ext import Updater
updater = Updater(token='883813261:AAGc4qLy7VWuqa6PudbRTxQ2KMinEstfofs', use_context=True)

#idk
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#...typing while handling requests
"""def send_action(action):
    ""Sends `action` while processing func command.""
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator"""


#/Start
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#fetch all bactive player authcodes
def playercodeall():
	codes = []
	for i in range(10):
		r = requests.post('http://vps.gopnik.net:8070/index.php/code/player'+str(i+1)+'bactive')
		if len(r.text) == 5 :
			codes.append(r.text)
		else : 
			codes.append('NULL')
		print(i+1)
	return codes

#fetch specific acc authcode
def playercode(name):
	r = requests.post('http://vps.gopnik.net:8070/index.php/code/'+str(name))
	print(r)
	return(str(name)+' : '+str(r.text))


#debug
#print(playercodeall())

#/code
def code(update, context):
	if context.args == [] :
		r = 'Send account name after /code, send "all" to get all accounts authcodes'
	elif len(context.args) > 1 :
		r = 'Sand only 1 acc name pls'
	elif context.args[0] == 'all':
		r = playercodeall()
	else :
		name = context.args[0]
		if len(name) >= 20 :
			r = 'Usernames over 20 character are`\'t accepted!'
#		elif re.search([/:;,{}], name) == true :
#			r = 'Invalid username'
		else :
			r = playercode(name)

	context.bot.send_message(chat_id=update.message.chat_id, text=r)

#@send_action(ChatAction.TYPING)
#def my_handler(bot, update):
#    pass  # user will see 'typing' while your bot is handling the request.

from telegram.ext import CommandHandler
code_handler = CommandHandler('code', code)
dispatcher.add_handler(code_handler)

updater.start_polling()


#Examples

#def caps(update, context):
#    text_caps = ' '.join(context.args).upper()
#    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

#caps_handler = CommandHandler('caps', caps)
#dispatcher.add_handler(caps_handler)

#echo anything
#def echo(update, context):
#    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

#from telegram.ext import MessageHandler, Filters
#echo_handler = MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)
