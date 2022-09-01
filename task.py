import tkinter as tk
from tkinter import messagebox
import sys
import time
import threading
import random
import datetime
import pandas as pd


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


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("300x200")
        master.title("タイピングゲーム！")

        # 問題数インデックス
        self.index = 0

        # 正解数カウント用
        self.correct_cnt = 0

        self.create_widgets()

        self.columes = ["time", "action", "situation", "judge"]
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d-%H%M%S')
        data = [[time, "start", "-", "-"]]
        # self.df = pd.DataFrame(data, index=self.columes)
        self.df = pd.DataFrame(data, columns=self.columes)
        print(self.df)

        # 経過時間スレッドの開始
        t = threading.Thread(target=self.timer)
        t.start()

        # Tkインスタンスに対してキーイベント処理を実装
        self.master.bind("<KeyPress>", self.type_event)






    # ウィジェットの生成と配置
    def create_widgets(self):
        self.q_label = tk.Label(self, text="お題：", font=("",20))
        self.q_label.grid(row=0, column=0)

        # 問題作成
        self.ans, q = QUESTION()

        self.q_label2 = tk.Label(self, text=q, width=10, anchor="w", font=("",20))
        self.q_label2.grid(row=0, column=1)
        self.ans_label = tk.Label(self, text="解答：", font=("",20))
        self.ans_label.grid(row=1, column=0)
        self.ans_label2 = tk.Label(self, text="", width=10, anchor="w", font=("",20))
        self.ans_label2.grid(row=1, column=1)
        self.result_label = tk.Label(self, text="", font=("",20))
        self.result_label.grid(row=2, column=0, columnspan=2)

        # # 時間計測用のラベル
        self.time_label = tk.Label(self, text="", font=("",20))
        self.time_label.grid(row=3, column=0, columnspan=2)

        self.flg2 = True


    # キー入力時のイベント処理
    def type_event(self, event):
        # 入力値がEnterの場合は答え合わせ
        if event.keysym == "Return":
            if str(self.ans) == self.ans_label2["text"]:
                # logに書き込み
                self.log(self.ans_label2["text"], "concentrate", "○", False)

                self.result_label.configure(text="正解！", fg="red")
                self.correct_cnt += 1
            else:
                # logに書き込み
                self.log(self.ans_label2["text"], "concentrate", "×", False)

                self.result_label.configure(text="残念！", fg="blue")

            # 解答欄をクリア
            self.ans_label2.configure(text="")

            # 次の問題を出題
            self.index += 1
            # 2分経ったら
            if self.index == 5:
                self.flg = False
                self.q_label2.configure(text="終了！")
                messagebox.showinfo("リザルト", f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。")

                # logに書き込み
                self.log("end", "-", "-", True)
                sys.exit(0)

            self.ans, q = QUESTION()
            self.q_label2.configure(text=q)

        elif event.keysym == "BackSpace":
            text = self.ans_label2["text"]
            self.ans_label2["text"] = text[:-1]

        else:
            # 入力値がEnter以外の場合は数字を入力してくださいと追記する
            self.ans_label2["text"] += event.keysym

    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            self.second += 1
            self.time_label.configure(text=f"経過時間：{self.second}秒")
            time.sleep(1)

    def log(self, situation, action, judge, flag):
        # logに書き込み
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d-%H-%M-%S')

        data = [[time, situation, action, judge]]
        self.df1 = pd.DataFrame(data, columns=self.columes)
        self.df = pd.concat([self.df, self.df1], axis=0)
        print(self.df)

        if flag:
            # log書き出し
            dt_now = datetime.datetime.now()
            self.df.to_csv(".\\log_dir\\{}.csv".format(dt_now.strftime('%Y-%m-%d-%H-%M-%S')), index=False)



if __name__ == "__main__":
    root = tk.Tk()
    Application(master=root)
    root.mainloop()


# https://max999blog.com/pandas-add-row-to-dataframe/