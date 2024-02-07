"""
stores copied urls in defanged format in clipboard
"""
import pyperclip
import keyboard

def process_and_copy():
    input_text = pyperclip.paste()  # fetch clipboard content

    # replace
    processed_text = input_text.replace('.', '[.]')

    pyperclip.copy(processed_text)  # copy to clipboard

    print("Defanged:")
    print(processed_text)

#Trigger
keyboard.add_hotkey("ctrl+c", process_and_copy)

print("Waiting for copy trigger...")
keyboard.wait("esc")  # esc for exit
