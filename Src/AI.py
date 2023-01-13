# TODO: Shorten response so it can be easy to read and inserted into Delta Math with web driver
# TODO: Make script input answer into delta math and add 'Exit' button
# TODO: Speed up the script!
# TODO: Fine Tune GPT-3 for math (Maybe IDK how complicated https://beta.openai.com/docs/guides/fine-tuning)
# Next project will have a GUI with it because they are fun

import os
import time
import tkinter as tk

import openai
import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
from colorama import Fore, Style

debug = True
window = tk.Tk()
openai.api_key = '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'

# Path to tesseract on pc
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# Send to openAI
def request():
	# Request AI answer
	response = openai.Completion.create(model="text-davinci-003", prompt=img_to_string(), temperature=0.3,
	                                    max_tokens=150)
	if debug:
		print(Fore.BLUE + "Request made!" + Style.RESET_ALL)
	return response


def resetAll():
	# Reset everything
	for widget in window.winfo_children():
		widget.destroy()
	if debug:
		print(Fore.BLUE + "Window reset!" + Style.RESET_ALL)


# Image to string
def img_to_string():
	time.sleep(1)
	currentProblem = pytesseract.image_to_string(Image.open('newProblem.png'))
	if debug:
		print(Fore.MAGENTA + 'Problem translated to string' + Style.RESET_ALL)
	return currentProblem


# Print the response to tinker window (Find a way to input response into the website)
def printResponse():
	window.geometry("700x600")
	window.title("IXL AI")
	if debug:
		print(Fore.GREEN + "Started!" + Fore.RESET)
		print(Fore.BLUE + "Display initiated!" + Style.RESET_ALL)

	problemWidget = tk.Text(window, height=5, width=52, bg='Black', fg='Red')
	clearall = tk.Button(window, text='reset', command=resetAll, bg='Black', fg='Red')
	Txt = tk.Text(window, height=5, width=52, fg='Red', bg='Black')
	Heading = tk.Label(window, text="------ English IXL Artificial Intelligence ------", bg='Black', fg='Red')

	# Config text widgets
	Heading.config(font=("Consolas", 16))
	problemWidget.config(font=("Consolas", 12))
	Txt.config(font=("Consolas", 12))
	clearall.config(font=("Consolas", 16))

	# Config packs
	Heading.pack(ipadx=20, ipady=20, anchor=tk.N, fill=tk.X)
	problemWidget.pack(ipadx=110, ipady=20, anchor=tk.CENTER, expand=True, fill=tk.BOTH)
	Txt.pack(ipadx=125, ipady=20, anchor=tk.CENTER, expand=True, fill=tk.BOTH)
	clearall.pack(anchor=tk.CENTER, fill=tk.X)

	# Insert text to widgets
	problemWidget.config(state="normal")
	problemWidget.insert(tk.END, img_to_string())
	problemWidget.config(state="disabled")
	Txt.config(state="normal")
	Txt.insert(tk.END, request())
	Txt.config(state="disabled")

	# Take Screenshot on key press
	def screenShot(event):
		# Find general x,y location for the problem
		os.remove("newProblem.png")
		x1 = 385
		# y1 changed from 390 Results: (GOOD)
		y1 = 250
		# x2 changed from 1230 Results: (GOOD)
		x2 = 1200
		# y2 changed from 590 Results: (VALUE PERFECT)
		y2 = 750
		im = ImageGrab.grab(bbox=(int(x1), int(y1), int(x2), int(y2)))
		im.save('newProblem.png')
		img_to_string()
		time.sleep(0.5)
		resetAll()
		time.sleep(0.5)
		printResponse()
		if debug:
			print(Fore.BLUE + "Screenshot taken" + Style.RESET_ALL)

	window.bind("p", screenShot)
	window.mainloop()  # Code will run window in a loop


# Load the tkinter window
printResponse()
if debug:
	print(Style.BRIGHT + Fore.RED + "! Terminated !" + Style.RESET_ALL)
