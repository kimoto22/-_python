import tkinter as tk
import sys
import keyboard
import time
import threading
import random
import datetime
import pandas as pd
import video
import audio
from tkinter import messagebox

video = video.Video()
audio = audio.Audio()

def QUESTION():
    one = random.randint(10, 20)
    two = random.randint(1, 9)
    hugo_index = random.randint(0,2)

    hugo = ["×", "-", "+"]
    ans = [one*two, one-two, one+two]

    hugo = hugo[hugo_index]
    ans = ans[hugo_index]

    question = "{} {} {} = ".format(one,hugo,two)

    print("hugo", hugo)
    print("ans", ans)

    return ans, question

def movie():
    # sleep 前のエポック秒(UNIX時間)を取得
    startSec = time.time()
    time.sleep(5)
    # sleep していた秒数を計算して表示
    print(time.time() - startSec)

    canvas = tk.Canvas()
    canvas.place(x=-2, y=-2) # キャンバス
    canvas.frame = tk.Label(canvas)
    canvas.frame.pack()
    video.openfile("./relax.mp4",canvas.frame)
    audio.openfile("./relax.wav")
    audio.play()
    video.play()



class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        # 問題数インデックス
        self.index = 0

        # 正解数カウント用
        self.correct_cnt = 0

        self.create_widgets()

        self.columes = ["time", "action", "correct","situation", "judge"]
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d %H:%M:%S.%f')
        data = [[time, "start", "-","-", "-"]]
        # self.df = pd.DataFrame(data, index=self.columes)
        self.df = pd.DataFrame(data, columns=self.columes)
        #print(self.df)

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer,daemon=True)
        self.t.start()

        # Tkインスタンスに対してキーイベント処理を実装
        self.master.bind("<KeyPress>", self.type_event)

    def click_close(self):
        if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
            root.destroy()
            #self.t.setDaemon(True)
            return 0

    # ウィジェットの生成と配置
    def create_widgets(self):
        #print("A")
        self.ans_label2 = tk.Label(self, text="", width=10, anchor="w", font=("",40))
        self.ans_label2.grid(row=0, column=0)
        self.q_label = tk.Label(self, text="お題：", font=("",40))
        self.q_label.grid(row=1, column=0)

        # 問題作成
        self.ans, q = QUESTION()
        self.q_label2 = tk.Label(self, text=q, width=20, anchor="w", font=("",40))
        self.q_label2.grid(row=1, column=1)
        self.ans_label = tk.Label(self, text="解答：", font=("",40))
        self.ans_label.grid(row=2, column=0)
        self.ans_label2 = tk.Label(self, text="", width=20, anchor="w", font=("",40))
        self.ans_label2.grid(row=2, column=1)
        self.result_label = tk.Label(self, text="", font=("",40))
        self.result_label.grid(row=3, column=0, columnspan=2)

        # ウィジェットの作成
        button1 = tk.Button(self, text="button1", width=80, height=10)
        button2 = tk.Button(self, text="button2",width=80, height=10)
        button3 = tk.Button(self, text="button3",width=80, height=10)
        button4 = tk.Button(self, text="button4", width=80, height=10)
        # ウィジェットの設置
        button1.grid(column=0, row=10,padx=50, pady=20)
        button2.grid(column=1, row=10)
        button3.grid(column=0, row=20,padx=50)
        button4.grid(column=1, row=20)

        # # 時間計測用のラベル
        self.time_label = tk.Label(self, text="", font=("",20))
        self.time_label.grid(row=4, column=0, columnspan=2)
        self.result_label = tk.Label(self, text="", font=("",40))
        self.result_label.grid(row=5, column=0, columnspan=2)

        self.flg2 = True


    # キー入力時のイベント処理
    def type_event(self, event):
        # 入力値がEnterの場合は答え合わせ
        if event.keysym == "Return":
            if str(self.ans) == self.ans_label2["text"]:
                # logに書き込み
                self.log(self.ans_label2["text"], self.ans,"concentrate", "correct", False)
                self.result_label.configure(text="正解！", fg="red")
                self.correct_cnt += 1
            else:
                # logに書き込み
                self.log(self.ans_label2["text"], self.ans,"concentrate", "miss", False)

                self.result_label.configure(text="残念！", fg="blue")

            # 解答欄をクリア
            self.ans_label2.configure(text="")

            # 次の問題を出題
            self.index += 1
            self.ans, q = QUESTION()
            self.q_label2.configure(text=q)
            self.log("problem_switching","-", "concentrate", "-", False)

        elif event.keysym == "BackSpace":
            text = self.ans_label2["text"]
            self.ans_label2["text"] = text[:-1]

        # else:
            # # 入力値がEnter以外の場合は数字を入力してくださいと追記する
            # self.ans_label2["text"] += event.keysym

    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            print(self.second)
            self.second += 1
            #self.time_label.configure(text=f"経過時間：{self.second}秒")
            time.sleep(1)

            # 2分経ったら
            if self.second == 10:
                self.q_label2.configure(text="")
                messagebox.showinfo("リザルト", f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。")

                # logに書き込み
                self.log("-", "-","relax", "-", False)
                #root.destroy()

                #quit_me(root)
                #sys.exit(0)
                self.second = 0
                #self.t.join()


                self.destroy()

                movie()
                return 0


    def log(self, situation, correct, action, judge, flag):
        # logに書き込み
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d %H:%M:%S.%f')

        data = [[time, situation, correct,action, judge]]
        self.df1 = pd.DataFrame(data, columns=self.columes)
        self.df = pd.concat([self.df, self.df1], axis=0)
        #print(self.df)
        print(flag)

        if flag==False:
            # log書き出し
            dt_now = datetime.datetime.now()
            self.df.to_csv(".\\log_dir\\{}.csv".format(dt_now.strftime('%Y-%m-%d-%H-%M')), index=False)
            print("READ")


if __name__ == "__main__":
    root = tk.Tk()
    label = tk.Label(root, text="2分間休憩時間です", font=("",40))
    label.pack(anchor='center',expand=1)
    #master.geometry("1280x720")
    #root.state("zoomed")
    root.attributes('-fullscreen', True)
    root.title("タイピングゲーム！")

    canvas1 = tk.Canvas(width = 1280,height = 720,bg = "cyan")

    canvas1.place(x=0, y=0) # キャンバス
    App = Application(master=canvas1)
    print(App)

    root.protocol("WM_DELETE_WINDOW", App.click_close)
    root.mainloop()
# https://max999blog.com/pandas-add-row-to-dataframe/