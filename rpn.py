############################################################
#                         CirCAL                           #
#     Software is provided "as is" without warranty.       #
#   Any and all critical structural failures are the sole  # 
#               responsibility of the user.                #
#                                                          #
############################################################

############################################################
#                      Changelog                           #
############################################################
# v1.0 initial code


import math
import sys
from fractions import Fraction
import tkinter as tk
import base64
import tempfile
import threading

stack = []
insert = []
display = []

# If possible return a number, else return num as a string
def get_number(num):

    for cast in (int, float):
        try:
            num = cast(num)
            return num
        except ValueError:
            pass
    if num[0] == "0":
        for base in (2, 8, 16):
            try:
                num = int(num, base)
                return num
            except ValueError:
                pass

    return num

# Calculator Class
class Calculator:

    def __init__(self):

        self.loop_flag = True

        self.rounding_value = None

        self.operation = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
            "//": self.int_div,
            "%": self.modulo,
            "^": self.pow,
            "sqrt": self.sqrt,
            "exp": self.exp,
            "log10": self.log10,
            "ln": self.loge,
            "abs": self.absolute_value,
            "inv": self.inv,
            "neg": self.neg,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
            "torad": self.to_radian,
            "todeg": self.to_degree,
            "switch": self.switch,
            "del": self.del_,
            "copy": self.copy,
            "pi": self.const_pi,
            "tau": self.const_tau,
            "e": self.const_e,
            "sum": self.sum,
            "fact": self.factorial,
            "round": self.round,
            "ave": self.average,
            "q": self.quit
        }


# Check if there is text in the input
    def check_input(self):
        if not insert:
            return False
        return True

# Wipe insert
    def clear_insert(self):
        insert.clear()
# Evaluate the string and enter it into the stack
    def evaluate(self, string):
        for i in string.split():
            i = get_number(i)
            if isinstance(i, (int, float)):
                stack.append(i)

            elif isinstance(i, str):
                if not insert:
                    self.operation[i]()
                elif insert:
                    stack.insert("end", ''.join(map(str, insert)))
                    self.operation[i]()
                    
                else:
                    print("Unknow command: {}".format(i))

            else:
                raise "Should never happend"

# Check if the stack is sufficient for an operation
    def check_stack(self, num, command):
        inlen = 0
        if insert:
            inlen = 1
        if len(stack)+inlen < num:
            print("Not enough numbers in the stack for {} command".format(command))
            return False

        return True

# Sum the 2 most recent stack entries
    def add(self):
        if self.check_stack(2, "+"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value1 + value2)
# Difference of the 2 most recent stack entries
    def sub(self):
        if self.check_stack(2, "-"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value2 - value1)
            self.clear_insert()
            
            
# Multiply the 2 most recent stack entries
    def mul(self):
        if self.check_stack(2, "*"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value1 * value2)
# Divide the 2nd most recent stack entry by the most recent stack entry
    def div(self):
        if self.check_stack(2, "/"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            if value1 == 0:
                print("Impossible to divide by 0")
                stack.append(value1)
            else:
                value2 = stack.pop()
                res = value2 / value1
                if res.is_integer():
                    stack.append(int(res))
                else:
                    stack.append(res)
                    
# Divide the 2nd most recent stack entry by the most recent stack entry and enter the integer result to the stack
    def int_div(self):
        if self.check_stack(2, "//"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            if value1 == 0:
                print("Impossible to divide by 0")
                stack.append(value1)
            else:
                value2 = stack.pop()
                stack.append(value2 // value1)

# Divide the 2nd most recent stack entry by the most recent stack entry and enter the remainder to the stack
    def modulo(self):
        if self.check_stack(2, "%"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            if value1 == 0:
                print("Impossible to divide by 0")
                stack.append(value1)
            else:
                value2 = stack.pop()
                stack.append(value2 % value1)

# Raise the 2nd most recent stack entry by the most recent stack entry
    def pow(self):
        if self.check_stack(2, "**"):
            if insert:
                value1 = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value2 ** value1)

# Square root of the most recent stack entry
    def sqrt(self):
        if self.check_stack(1, "sqrt"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value < 0:
                print("Square root require non-negative value")
                stack.append(value)
            else:
                stack.append(math.sqrt(value))

# e^x where x is the most recent stack entry
    def exp(self):
        if self.check_stack(1, "exp"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(math.exp(value))

# log base 10 of the most recent stack entry
    def log10(self):
        if self.check_stack(1, "log10"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value > 0:
                stack.append(math.log10(value))
            else:
                print("Number out of domain for logarithm")
                stack.append(value)

# log base e of the most recent stack entry
    def loge(self):
        if self.check_stack(1, "loge"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value > 0:
                stack.append(math.log(value))
            else:
                print("Number out of domain for logarithm")
                stack.append(value)

# Absolute value of the most recent stack entry
    def absolute_value(self):
        if self.check_stack(1, "abs"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(abs(value))

# Inverse of the most recent stack entry
    def inv(self):
        if self.check_stack(1, "inv"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(1 / value)

# Change the sign (Multiply by -1) of the most recent stack entry
    def neg(self):
        if self.check_stack(1, "neg"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
##            if value < 0:
##                stack.append(abs(value))
##            else:
##                stack.append(0 - value)
            stack.append(-1*value)

# Sine of most recent stack entry in radians
    def sin(self):
        if self.check_stack(1, "sin"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(math.sin(value))

# Cosine of most recent stack entry in radians
    def cos(self):
        if self.check_stack(1, "cos"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(math.cos(value))

# Tangent of most recent stack entry in radians
    def tan(self):
        if self.check_stack(1, "tan"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(math.tan(value))

# Arcsine of most recent stack entry in radians
    def asin(self):
        if self.check_stack(1, "asin"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value < -1 or value > 1:
                print("Number out of domain for asin")
                stack.append(value)
            else:
                stack.append(math.asin(value))

# Arccosine of most recent stack entry in radians
    def acos(self):
        if self.check_stack(1, "acos"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value < -1 or value > 1:
                print("Number out of domain for acos")
                stack.append(value)
            else:
                stack.append(math.acos(value))

# Arctangent of most recent stack entry in radians
    def atan(self):
        if self.check_stack(1, "atan"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(math.atan(value))

# Convert degrees to radians
    def to_radian(self):
        if self.check_stack(1, "torad"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(value / 180 * math.pi)

# Convert radians to degrees
    def to_degree(self):
        if self.check_stack(1, "todeg"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            stack.append(value * 180 / math.pi)

# Switch the most recent 2 numbers in the stack
    def switch(self):
        if self.check_stack(2, "switch"):
            value1 = stack.pop()
            value2 = stack.pop()
            stack.append(value1)
            stack.append(value2)

# Remove the most recent stack entry
    def del_(self):
        if self.check_stack(1, "del"):
            stack.pop()

# Duplicate the most recent stack entry
    def copy(self):
        if self.check_stack(1, "copy"):
            stack.append(stack[-1])

# Add pi to the stack
    def const_pi(self):
        stack.append(math.pi)

# Add tau to the stack
    def const_tau(self):
        stack.append(math.tau)

# Add e to the stack
    def const_e(self):
        stack.append(math.e)

# Sum of the stack
    def sum(self):
        if self.check_stack(1, "sum"):
            total = sum(stack)
            stack.clear()
            stack.append(total)

# Calculate n! where n is the most recent stack entry
    def factorial(self):
        if self.check_stack(1, "fact"):
            if insert:
                value = int(''.join(map(str, insert)))
                self.clear_insert()
            else:
                value = stack.pop()
            if value < 0:
                print("Impossible to compute factorial for negative number")
                stack.append(value)
            elif isinstance(value, float):
                print("Impossible to compute factorial for float number")
                stack.append(value)
            else:
                stack.append(math.factorial(value))

# Round the most recent stack entry
    def round(self):
        if self.check_stack(1, "round"):
            value = stack.pop()
            stack.append(round(value, self.rounding_value))

# Average the numbers in the stack
    def average(self):
        if self.check_stack(1, "ave"):
            size = len(stack)
            total = sum(stack)
            stack.clear()
            stack.append(total / size)

# quit
    def quit(self):
        exit()

# Stack Handler
#class stackHandler:

# save fingers
cal = Calculator()

# set up window
gui = tk.Tk()

gui.configure(background="white")
gui.title("CirCAL")
gui.resizable(False,False)
gui.geometry("400x650")
gui.protocol("WM_DELETE_WINDOW", cal.quit)

# blank icon
##ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
##    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
##_, ICON_PATH = tempfile.mkstemp()
##with open(ICON_PATH, 'wb') as icon_file:
##    icon_file.write(ICON)
##gui.iconbitmap(default=ICON_PATH)

# Smith
ICON = ('R0lGODlhGQAZAMQAALu7u/////f39+7u7ubm5t3d3dXV1czMzMTExLOzs6qqqpmZmZGRkYiIiICAgHd3d29vb2ZmZl5eXlVVVU1NTURERDMzMyIiIgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAZABkAAAXxICCKwlJRKDVZETG+MDBQEBHct8BYRwwXlgRueDNUGD4RoYIgOgWSh8BHaTqvD0gMMbl6AxIFjGL4Xo2DkYFi9jIeI4kw1x5aECJ2YEkREA1+TgkSFxd6ERhOBBgUA0MXGAIUhXpmGAw4hZqUdUSbmpWdARikm6GiNxiGKKhEjJgVrUMzmGQBAwoSEbu8EhAHTge2DAzCEhUHTMkHBwsWThPCDEs4FYgVFRjY2Ik4AhWSFAAQCzex5jeYTg0PjOIDPEPqVwINEgKrIgeXdQcWDQJUkRmBwFoCR0RwqTAAAJJAGLkoSPAFoSKFBgwbFnoVAgA7')
ico = tk.PhotoImage(data=ICON)
gui.iconphoto(False, ico)

# input window
inputtext = tk.Label(gui, bg="white", width=400, height=2, state='disabled', relief="sunken",text="")

# stack window
stackgui = tk.Frame(gui, width=400, height=180, relief="sunken")
stacktext = tk.Text(stackgui, state='disabled')


# update input window
def updateInputText():
    inputNum = ''.join(map(str, insert))
##    stack[len(stack)+1] = inputNum
    inputtext.configure(state='normal')
    inputtext.configure(text=inputNum)
    inputtext.configure(state='disabled')
    inputtext.pack()

# update stack window
def updateStackText():
    display = stack
    display = [str(n)+"\n" for n in display]
    stacktext.configure(state='normal')
    stacktext.delete("1.0","end")
    stacktext.insert("end", ''.join(map(str, display)))
##    if (len(stack) % 2 == 0):
##        stacktext.tag_configure("end-1",background="gray70")
##        stacktext.insert("end", ''.join(map(str, display)))
##    else:
##        stacktext.tag_configure("end-1",background="gray70")
##        stacktext.insert("end", ''.join(map(str, display)))
    stacktext.configure(state='disabled')
    stacktext.pack()
    updateInputText()
    
    
    
# numpad handling
# fuck it ill do it myself
def pad0():
    insert.append(0)
    updateInputText()
def pad1():
    insert.append(1)
    updateInputText()
def pad2():
    insert.append(2)
    updateInputText()
def pad3():
    insert.append(3)
    updateInputText()
def pad4():
    insert.append(4)
    updateInputText()
def pad5():
    insert.append(5)
    updateInputText()
def pad6():
    insert.append(6)
    updateInputText()
def pad7():
    insert.append(7)
    updateInputText()
def pad8():
    insert.append(8)
    updateInputText()
def pad9():
    insert.append(9)
    updateInputText()
    
def padDecimal():
    if not insert:
        insert.append("0")
        insert.append(".")
    elif "." not in insert:
        insert.append(".")
    else:
        return
    updateInputText()
    
def padSign():
    if not insert:
        insert.insert(0, "-")
    elif insert[0] != '-':
        insert.insert(0, "-")
    else:
        insert.pop(0)
    updateInputText()
    
# clear input
def clearInput():
    insert.clear()
    updateInputText()

# Handle a backspace
def backSpace(event):
    if not insert:
        return
    else:
        insert.pop()
        updateInputText()
    
# clear stack
def memClear():
    stack.clear()
    updateStackText()
    
# push input text to stack
def inputToStack():
    cal.evaluate(''.join(map(str, insert)))
    insert.clear()
    updateInputText()
    updateStackText()
    
def enterToStack(event):
    cal.evaluate(''.join(map(str, insert)))
    insert.clear()
    updateInputText()
    updateStackText()
    
# button array
ipad =[["sin", "arcsin", "sqrt","ToDEG", "7", "8", "9", "+", "-"],
       ["cos", "arccos", "eⁿ","ToRAD", "4", "5", "6", "/", "*"],
       ["tan", "arctan", "INV", "SWP", "1", "2", "3", "//", "%"],
       ["log", "ln", "ABS", "NEG", "0", ".", "(-)", "!", "^"],
       ["avg", "pi", "tau", "DUP", "e", "Σ", "DEL", "Clear", "Enter"]]

fpad =[[cal.sin, cal.asin, cal.sqrt,cal.to_degree, pad7, pad8, pad9, cal.add, cal.sub],
       [cal.cos, cal.acos, cal.exp,cal.to_radian, pad4, pad5, pad6, cal.div, cal.mul],
       [cal.tan, cal.atan, cal.inv, cal.switch, pad1, pad2, pad3, cal.int_div, cal.modulo],
       [cal.log10, cal.loge, cal.absolute_value, cal.neg, pad0, padDecimal, padSign, cal.factorial, cal.pow],
       [cal.average, cal.const_pi, cal.const_tau, cal.copy, cal.const_e, cal.sum, clearInput, memClear, inputToStack]]

cpad =[["gray85", "gray85", "gray85", "gray85", "snow", "snow", "snow", "gray85", "gray85"],
       ["gray85", "gray85", "gray85", "gray85", "snow", "snow", "snow", "gray85", "gray85"],
       ["gray85", "gray85", "gray85", "gray85", "snow", "snow", "snow", "gray85", "gray85"],
       ["gray85", "gray85", "gray85", "gray85", "snow", "snow", "snow", "gray85", "gray85"],
       ["gray85", "gray85", "gray85", "gray85", "gray85", "gray85", "gray85", "gray85", "gray85"]]


# process key input
keys =[['1',pad1],
       ['2',pad2],
       ['3',pad3],
       ['4',pad4],
       ['5',pad5],
       ['6',pad6],
       ['7',pad7],
       ['8',pad8],
       ['9',pad9],
       ['0',pad0],
       ['/',cal.div],
       ['*',cal.mul],
       ['-',cal.sub],
       ['+',cal.add],
       ['^',cal.pow],
       ['!',cal.factorial],
       ['%',cal.modulo],
       ['.',padDecimal]]
       
def keypresses(k):
    print(k.char)
    for n in range(len(keys)):
        if k.char == keys[n][0]:
            keys[n][1]()
            updateStackText()
            

# run fpad function and update
def combiner(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

# buttons
pad = tk.Canvas(gui, width=400, height=300)

for r in range(5):
   for c in range(9):
      tk.Button(pad, command=combiner(fpad[r][c],updateStackText), padx="4", pady="4", text=ipad[r][c],borderwidth=2, bg=cpad[r][c] ).grid(row=r,column=c,padx="2",pady="6")

# pack the shit
inputtext.pack()
stackgui.pack()
stacktext.pack()
pad.pack()

# Bind key presses
gui.bind('<Key>', keypresses)
gui.bind('<Return>', enterToStack)
gui.bind('<BackSpace>', backSpace)
# start the GUI
if __name__ == "__main__":
    gui.mainloop()
    

