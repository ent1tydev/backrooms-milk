import tkinter as tk; import os, random, requests
from tkinter import Text, Scrollbar
from threading import Thread
import time

uid=random.randint(1000, 20000)

API_CHAT_ADDRESS=open('static/server.txt', 'r', encoding='utf-8').read()
chat_addr=API_CHAT_ADDRESS

def frame_update(text):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

class Backend:
    def check_conn():
        try:
            requests.get(chat_addr, verify=False)
            lbc = tk.Label(root, text="[+] - Network reachable      ", fg="green", bg="#171717", font=("Arial", 12, "bold"))
            lbc.place(x=10, y=570)
        except:
            lbc = tk.Label(root, text="[-] - Network unreachable", fg="red", bg="#171717", font=("Arial", 12, "bold"))
            lbc.place(x=10, y=570)
    
    def update():
        Backend.check_conn()
        try:
            chat_text_1=requests.get(chat_addr+'/allchat', verify=False).text
            chat_text=chat_text_1.replace('\\n', '\n').replace('"', '')
            frame_update(chat_text)
        except Exception as E1:
            print('\033[91m{}\033[0m'.format(E1))
        time.sleep(1)
        Backend.update()



def send_story():
    story = text_input.get("1.0", tk.END)
    send_button.configure(text="Sending...", state='disabled')
    try:
        recv=requests.post(f'{chat_addr}/sendmsg/{uid}/{story}', verify=False).text
        print(recv)
        send_button.configure(text="Send message", state='normal')
    except:
        send_button.configure(text="Error while sending", state='disabled')
        time.sleep(1)
        send_button.configure(text="Send message", state='normal')


root = tk.Tk()
root.title("Backrooms Milk")
root.geometry("800x600")
root.iconbitmap('static/icon.ico')
root.resizable(False, False)

backgrounds_dir = "static/backgrounds"
backgrounds = os.listdir(backgrounds_dir)

background_image = random.choice(backgrounds)
background_path = os.path.join(backgrounds_dir, background_image)

photo = tk.PhotoImage(file=background_path)
label = tk.Label(root, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)

text_label = tk.Label(root, text="Backrooms Milk", font=("Courier New", 24, "bold"), fg="white")
text_label.config(bg="black")
text_label.place(x=20, y=20)

text_frame = tk.Frame(root, bg="#171717", highlightthickness=0)
text_frame.place(x=310, y=20, relwidth=0.6, relheight=0.9, anchor=tk.NW)

text_widget = Text(text_frame, bg="#171717", fg="white", font=("Verdana", 12))
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget.config(state=tk.NORMAL)   
text_widget.insert(tk.END, "Updating...")
text_widget.config(state=tk.DISABLED)

text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

text_input = tk.Text(root, bg="#171717", fg="white", font=("Verdana", 12), height=6)
text_input.place(x=20, y=100, width=270)

send_button = tk.Button(root, text="Send message", font=("Verdana", 12), bg="#171717", fg="white", command=send_story)
send_button.place(x=20, y=250, width=270)

Thread(target=Backend.update).start()

root.mainloop()
