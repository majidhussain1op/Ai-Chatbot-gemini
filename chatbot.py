import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except AttributeError:
    messagebox.showerror("Error", "GEMINI_API_KEY not found in .env file.")
    exit()

# Start the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])

# Send message to Gemini
def send_message():
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("Empty Input",
         "Gemini needs something to work with!")
        return
    
    chat_area.insert(tk.END, f"You: {user_input}\n")
    entry.delete(0, tk.END)

    try:
        response = chat.send_message(user_input, stream=True)
        chat_area.insert(tk.END, "Gemini: ")
        for chunk in response:
            chat_area.insert(tk.END, chunk.text)
        chat_area.insert(tk.END, "\n\n")
        chat_area.see(tk.END)
    except Exception as e:
        chat_area.insert(tk.END, f"\nError: {e}\n\n")


def quit_app():
    root.destroy()


root = tk.Tk()
root.title("Gemini Flash - Chatbot")
root.geometry("600x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=5, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))

send_button = tk.Button(entry_frame, text="Send",
command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12))
send_button.pack(side=tk.RIGHT, padx=(5, 10))

exit_button = tk.Button(root, text="Quit", 
command=quit_app, bg="#f44336", fg="white", font=("Arial", 12))
exit_button.pack(pady=5)

root.mainloop()
