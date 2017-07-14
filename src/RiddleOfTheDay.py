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

CURRENT_RIDDLE =  # used so answers and hints can be given


@ask.launch
def launch():
    day = time.strftime('%Y-%m-%d')
    return get_question(day)

@ask.intent('HowToPlay')
def howToPlay():
    print("hey")

@ask.intent('GetAnotherRiddle', mapping={'day': 'Day'})
def getRiddle(day):
    CURRENT_RIDDLE = RIDDLES['dailyRiddle'][day]
    


@ask.intent('GiveUp')
def getAnswer():
    answer = CURRENT_RIDDLE['answer']



@ask.intent('GetHint')
def getHint():
    hint = CURRENT_RIDDLE['hint']


@ask.intent('RepeatRiddle')
def repeatRiddle():
    text = CURRENT_RIDDLE['riddleText']



@ask.intent('AnswerRiddle', mapping={'answer': 'Answer'})
def checkAnswer(answer):
    if answer == CURRENT_RIDDLE['answer']:
        result = "Congratulations! That's correct."
        # enter speak statement here
        return howToPlay()
    else:
        result = "That is incorrect. Try again."
        return repeatRiddle()


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