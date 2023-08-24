"""
Especially when you copy-paste from a place that does
not index sentences such as PDF, sentences are printed
line by line. This script fixes this. It pulls the data
from the clipboard, turns it into a single line, puts it
back to the clipboard. When you paste, it becomes a single
line. It triggers the operation with ctrl+c, you can change
it from the script, so you better do the copy operation
with the mouse. Or change the trigger.
"""
import pyperclip
import keyboard

def process_and_copy():
    input_text = pyperclip.paste()  # fetch clipboard content

    # replace
    processed_text = input_text.replace('\n', ' ')

    pyperclip.copy(processed_text)  # copy to clipboard

    print("Metin işlendi ve sonuç panoa kopyalandı:")
    print(processed_text)

# trigger
keyboard.add_hotkey("ctrl+c", process_and_copy)

print("Waiting for copy trigger...")
keyboard.wait("esc")  # esc for exit
