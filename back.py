
import tkinter as tk
import random
root = tk.Tk()

#root.geometry("1280x720")
#root.state("zoomed")
root.attributes('-fullscreen', True)
root.title("タイピングゲーム！")

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window

def random_symbol():#問題作成
    text = [["〇","red"]]
    label = ["〇","△","□","×"]
    color = ["red","green","blue","yellow"]

    for i in range(3):
        a = random.choice(label)
        b = random.choice(color)
        while (a == "〇" and b == "red"):
            a = random.choice(label)
            b = random.choice(color)
        text.append([a,b])
    print(text)
    random.shuffle(text)
    print(text)
    return text

def button_func(event):

    #event.widget.config(fg="red")
    print("形:"+event.widget.cget("text") + "　色:" +event.widget.cget("fg"))
    text=random_symbol()

    for i in range(4):
        symbol[i].set(text[i][0])
        button[i]["fg"] = text[i][1]

column_data = (0, 0, 1, 1)
row_data = (0, 1, 0, 1)
text=random_symbol()

symbol=[]
button=[]
for i in range(4):
    symbol.append(tk.StringVar())
    symbol[i].set(text[i][0])
    print(symbol[i])
    button.append(tk.Button(canvas,textvariable=symbol[i],fg = text[i][1], font=("",100)))
    button[i].grid(column = column_data[i], row = row_data[i],padx=30,pady=30, sticky = 'nsew')
    # ボタンクリック時のイベント設定
    button[i].bind("<ButtonPress>", button_func)


canvas.grid_columnconfigure(0, weight = 1)
canvas.grid_columnconfigure(1, weight = 1)
canvas.grid_rowconfigure(0, weight = 1)
canvas.grid_rowconfigure(1, weight = 1)

root.mainloop()