import os
import time
import openai
import requests
import pytesseract
import tkinter as tk
from PIL import Image
import pyscreenshot as ImageGrab


debug = True
window = tk.Tk()
openai.api_key = 'YOUR_API_KEY'

# Path to tesseract on pc
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


class functions:
  
  def imgCheck():
    if not os.path.exists('newProblem.png'):
      problem_photo = 'https://itzcozi.github.io/itzCozi-Hosting/resources/newProblem.png'
      functions.install(problem_photo, os.getcwd(), 'newProblem.png')
    else:
      pass

  def request():
    # Request AI answer
    response = openai.Completion.create(
      model='text-davinci-003',
      prompt=functions.imgToString(),
      temperature=0.1,
      max_tokens=130
    )
    if debug:
      print('Request made!')
    return response
  
  def install(URL, destination, name=""):
    # Download and write to file
    file_content = requests.get(URL)
    open(f'{destination}/{name}', 'wb').write(file_content.content)

  def resetAll():
    # Reset everything
    for widget in window.winfo_children():
      widget.destroy()
    if debug:
      print('Window reset!')

  # Image to string
  def imgToString():
    time.sleep(1)
    currentProblem = pytesseract.image_to_string(Image.open('newProblem.png'))
    if debug:
      print('Problem translated to string')
    return currentProblem


# Print the response to tinker window (Find a way to input response into the website)
def printResponse():
  window.geometry('700x600')
  window.title('IXL AI')
  if debug:
    print('Started!')
    print('Display initiated!')

  problemWidget = tk.Text(window,height=5,width=52,bg='Black',fg='Red')
  clearall = tk.Button(window,text='reset',command=functions.resetAll,bg='Black',fg='Red')
  Txt = tk.Text(window,height=5,width=52,fg='Red',bg='Black')
  Heading = tk.Label(window,text='------ English IXL Artificial Intelligence ------',bg='Black',fg='Red')

  # Config text widgets
  Heading.config(font=('Consolas', 16))
  problemWidget.config(font=('Consolas', 12))
  Txt.config(font=('Consolas', 12))
  clearall.config(font=('Consolas', 16))

  # Config packs
  Heading.pack(ipadx=20,ipady=20,anchor=tk.N,fill=tk.X)
  problemWidget.pack(ipadx=110,ipady=20,anchor=tk.CENTER,expand=True,fill=tk.BOTH)
  Txt.pack(ipadx=125,ipady=20,anchor=tk.CENTER,expand=True,fill=tk.BOTH)
  clearall.pack(anchor=tk.CENTER,fill=tk.X)

  # Insert text to widgets
  problemWidget.config(state='normal')
  problemWidget.insert(tk.END, functions.imgToString())
  problemWidget.config(state='disabled')
  Txt.config(state='normal')
  Txt.insert(tk.END, functions.request())
  Txt.config(state='disabled')

  # Take Screenshot on key press
  def screenShot(event):
    # Find general x,y location for the problem
    x1 = 385
    y1 = 250
    x2 = 1200
    y2 = 750

    im = ImageGrab.grab(bbox=(int(x1), int(y1), int(x2), int(y2)))
    im.save('newProblem.png')
    functions.imgToString()
    time.sleep(0.5)
    functions.resetAll()
    time.sleep(0.5)
    printResponse()
    if debug:
      print('Screenshot taken')

  window.bind('p', screenShot)
  window.mainloop()  # Code will run window in a loop


# Load the tkinter window
try:
  functions.imgCheck()
  printResponse()
except Exception as e:
  print('Exited - {e}]\n')
  if debug:
    print('! Window Terminated !')
