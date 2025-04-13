#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:33:15 2024

@author: glg
"""

from flask import Flask, request, redirect, url_for

ROOT_URL = "pywer4"
app = Flask(__name__,
            static_url_path=f"/{ROOT_URL}/",
            static_folder='static')
# --> http://127.0.0.1:5000/test/ouahh.html


#%%

from tokens import Tokens, YELLOW, RED, EMPTY
import json


def user_play(user_input):
    tokens = Tokens(user_input["state"]["nblines"], user_input["state"]["nbcols"])
    for token in user_input["state"]["user_tokens"]:
        tokens.set_token(token[0], token[1], YELLOW)
    for token in user_input["state"]["computer_tokens"]:
        tokens.set_token(token[0], token[1], RED)
    valid_move = tokens.check(user_input["user_move"][0], user_input["user_move"][1])
    if valid_move:
        tokens.set_token(user_input["user_move"][0], user_input["user_move"][1], YELLOW)
    user_win, squares = tokens.win(color = YELLOW)
    full = tokens.isfull()
    return {"valid_move":valid_move,
            "user_win":user_win,
            "full":full,
            "squares":squares            
            }

def computer_play(state):
    tokens = Tokens(state["nblines"], state["nbcols"])
    for token in state["user_tokens"]:
        tokens.set_token(token[0], token[1], YELLOW)
    for token in state["computer_tokens"]:
        tokens.set_token(token[0], token[1], RED)
    best_col, best_score = tokens.computer_play(state["level"])
    best_line = tokens.get_line(best_col)
    # sets the token
    tokens.set_col(best_col, RED)
    computer_win, squares = tokens.win(color = RED)
    full = tokens.isfull()
    return {"move":[best_line, best_col],
            "computer_win":computer_win,
            "full":full,
            "squares":squares      
            }
    
state = {"nblines":6,
         "nbcols":7,
         "level":1,
         "user_tokens":[(2,5), (1,2), (1,4)],
         "computer_tokens":[(1,5), (2,3), (1,3)]
         }

user_input = {"state":state,
              "user_move":(3, 4)
              }
#user_play(user_input)
#computer_play(state)
#%%


@app.route(f"/{ROOT_URL}/user_play", methods=['POST'])
def web_user_play():
    #print(request.form)
    user_input_json = request.form['parameter']
    #print(user_input_json)
    user_input = json.loads(user_input_json)
    #print(user_input)
    return user_play(user_input)

@app.route(f"/{ROOT_URL}/computer_play", methods=['POST'])
def web_computer_play():
    #print(request.form)
    state_json = request.form['parameter']
    #print(state_json)
    state = json.loads(state_json)
    #print(state)
    return computer_play(state)

@app.route(f"/{ROOT_URL}")
def pywer4():
    return app.send_static_file('pywer4.html')

@app.route('/')
def default():
    return redirect(url_for(ROOT_URL))
    #return "A voir: <a href='pywer4'>Pywer4</a>"

#%%

if __name__ == "__main__":
    app.run(host='0.0.0.0')
