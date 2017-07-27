import logging
import os
import time
import json
from random import randint

from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


with open('Riddles.json', encoding='utf-8') as data_file:
    RIDDLES = json.loads(data_file.read())

#default CURREN_RIDDLE is the first riddle in the system
CURRENT_RIDDLE =  RIDDLES['dailyRiddles'][day]
LAUNCH_STATEMENT = True

@ask.launch
def launch():
    return HowToPlay()

@ask.intent('HowToPlay')
def howToPlay():
	how_to_play = ""
	card_title = "HowToPlay"
    if Launch_Statement:
    	how_to_play += "Welcome to Riddle of the Day!"
    	Launch_Statement = False
    else:
    	how_to_play += "In Riddle of the Day, you can ask for a daily riddle.\n"
    	how_to_play += "Say I'd like today's riddle to start.\n"
    	how_to_play += "If you want more, ask for another riddle.\n"
    	how_to_play += "When you are ready to answer, say 'the answer is' blank"
    	how_to_play += "where blank is your answer.\n Enjoy playing!"
    return question(how_to_play).reprompt(how_to_play).simple_card(card_title, how_to_play)

@ask.intent('GetRiddle')
def getTodaysRiddle():
	day = time.strftime('%Y-%m-%d')
    return getRiddle(day)

@ask.intent('GetAnotherRiddle', mapping={'day': 'Day'})
def getRiddle(day):
	card_title = "GetRiddle"
    CURRENT_RIDDLE = RIDDLES['dailyRiddles'][day]
    riddle_text = CURRENT_RIDDLE['riddleText']
    return question(riddle_text).reprompt(riddle_text).simple_card(card_title, riddle_text)
    


@ask.intent('GiveUp')
def getAnswer():
    answer = CURRENT_RIDDLE['answer']
    return statement('The answer is' + answer)


@ask.intent('GetHint')
def getHint():
    hint = CURRENT_RIDDLE['hint']
    card_title = 'Hint'
    return question(hint).reprompt(hint).simple_card(card_title, hint)


@ask.intent('RepeatRiddle')
def repeatRiddle():
    card_title = 'RepeatRiddle'
    text = CURRENT_RIDDLE['riddleText']
    return question(text).repropmt(text).simple_card(card_title, text)



@ask.intent('AnswerRiddle', mapping={'answer': 'Answer'})
def checkAnswer(answer):
    if answer == CURRENT_RIDDLE['answer']:
        result = "Congratulations! That's correct."
    else:
        result = "That is incorrect. Try again."
    return statement(result)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

@ask.session_ended
def session_ended():
    return "{}", 200



if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)