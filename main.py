from tkinter import *
from random import random, choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}


# DataFrame
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/American_English_Words.csv")
    to_card = original_data.to_dict(orient="records", )
else:
    to_card = data.to_dict(orient="records")


def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_card)
    canvas.itemconfig(card_titles, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_titles, text="Spanish", fill="white")
    canvas.itemconfig(card_word, text=current_card["Spanish"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():

    try:

        to_card.remove(current_card)
        # Creating File csv to store words to learn.
        data = pd.DataFrame(to_card)
        data.to_csv("data/words_to_learn.csv", index=False)
        new_word()

    except ValueError:

        print("The deck is done")
    except IndexError:
        print("The deck is done")


window = Tk()
window.title("Flash Cards")
window.minsize(width=900, height=526)
window.maxsize(width=900, height=726)
window.config(padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

# Labels
card_titles = canvas.create_text(
    400, 150, text="Title", font=("ariel", 40, "italic"))
card_word = canvas.create_text(
    400, 263, text="Word", font=("ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="images/right.png", )
right_btn = Button(image=right_img, command=is_known)
right_btn.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, command=new_word)
wrong_btn.grid(column=0, row=1)

new_word()

window.mainloop()
