import sys
import tkinter as tk
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
    random_radiobutton = random.randint(0,3)
    hugo = ["×", "-", "+"]
    ans = [one*two, one-two, one+two]
    # 問題をランダムに生成
    hugo = hugo[hugo_index]
    ans = ans[hugo_index]
    radio_button_list = [ans,ans*10,ans-10,ans*5]
    random.shuffle(radio_button_list) # 配列の中をシャッフル
    question = "{} {} {} = ".format(one,hugo,two)

    print("hugo", hugo)
    print("ans", ans)

    return ans, question, radio_button_list

####切り替えボタン####
def change(sence):
    global canvas2
    canvas2 = tk.Canvas(root, highlightthickness=0)
    canvas2.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window
    # 各種ウィジェットの作成
    label1_frame_app = tk.Label(canvas2, text="準備ができたら課題に進んでください", font=("",40))
    button_change_frame_app = tk.Button(canvas2, text="進む", font=("",40),command=sence)
    # 各種ウィジェットの設置
    label1_frame_app.pack(anchor='center',expand=1)
    button_change_frame_app.pack(anchor='center',expand=1)

####relax動画####
def timecount(canvas,video,audio):
    second = 0
    flg = True
    #time_label = tk.Label(canvas, text="", font=("",20))
    #time_label.pack(anchor='nw',expand=0)
    while flg:
        second += 1
        time.sleep(1)   # convert second to hour, minute and seconds
        elapsed_minute = (second % 3600) // 60
        elapsed_second = (second % 3600 % 60)
        # print as 00:00:00
        print(str(elapsed_minute).zfill(2) + ":" + str(elapsed_second).zfill(2))
        #time_label.configure(text=f"経過時間：{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}")

        if second==10:
            #video.stop()
            audio.stop()
            canvas.destroy()
            change()

            return 0

def movie():
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window
    label = tk.Label(canvas, text="2分間休憩時間です", font=("",40))
    label.pack(anchor='center',expand=1)
    # sleep 前のエポック秒(UNIX時間)を取得
    startSec = time.time()
    time.sleep(1)
    # sleep していた秒数を計算して表示
    print(time.time() - startSec)
    canvas.frame = tk.Label(canvas)
    canvas.frame.pack(side = tk.BOTTOM)
    video.openfile("./relax.mp4",canvas.frame)
    audio.openfile("./relax.wav")
    # 経過時間スレッドの開始
    thread = threading.Thread(name="thread", target=timecount, args=[canvas,video,audio], daemon=True)
    thread.start()

    audio.play()
    video.play()
    label.pack_forget()
    time.sleep(3)
    change(math)    #シーン変更先

####計算課題####
def math():
    canvas2.destroy()
    canvas1 = tk.Canvas(root, highlightthickness=0)
    canvas1.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window

    App = Application(master=canvas1)
    print(App)

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

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer,daemon=True)
        self.t.start()

        # Tkインスタンスに対してキーイベント処理を実装
        # self.master.bind("<KeyPress>", self.type_event)

    def click_close(self):
        if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
            root.destroy()
            return 0

    # ウィジェットの生成と配置
    def create_widgets(self):
        self.ans_label2 = tk.Label(self, text="", width=10, anchor="w", font=("",40))
        self.ans_label2.grid(row=0, column=0)
        self.q_label = tk.Label(self, text="お題：", font=("",40))
        self.q_label.grid(row=1, column=0)

        # 問題作成
        self.ans, q, radio_button_list = QUESTION()
        self.q_label2 = tk.Label(self, text=q, width=20, anchor="w", font=("",40))
        self.q_label2.grid(row=1, column=1)
        self.ans_label = tk.Label(self, text="解答：", font=("",40))
        self.ans_label.grid(row=2, column=0)

        self.result_label = tk.Label(self, text="", font=("",40))
        self.result_label.grid(row=3, column=0, columnspan=2)

        # ウィジェットの作成
        self.radio_value = tk.IntVar()             # ラジオボタンの初期値を0にする

        # ラジオボタンの作成
        self.radio0 = tk.Radiobutton(self.master,
                                text = str(radio_button_list[0]),      # ラジオボタンの表示名
                                command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                                variable = self.radio_value, # 選択の状態を設定する
                                value = str(radio_button_list[0])                    # ラジオボタンに割り付ける値の設定
                                )

        self.radio1 = tk.Radiobutton(self.master,
                                text = str(radio_button_list[1]),      # ラジオボタンの表示名
                                command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                                variable = self.radio_value, # 選択の状態を設定する
                                value = str(radio_button_list[1])                    # ラジオボタンに割り付ける値の設定
                                )

        self.radio2 = tk.Radiobutton(self.master,
                                text = str(radio_button_list[2]),      # ラジオボタンの表示名
                                command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                                variable = self.radio_value, # 選択の状態を設定する
                                value = str(radio_button_list[2])                    # ラジオボタンに割り付ける値の設定
                                )

        self.radio3 = tk.Radiobutton(self.master,
                                     text = str(radio_button_list[3]),      # ラジオボタンの表示名
                                     command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                                     variable = self.radio_value, # 選択の状態を設定する
                                     value = str(radio_button_list[3])                    # ラジオボタンに割り付ける値の設定
                                     )

        # ボタンの作成
        self.button = tk.Button(self.master,
                           text = "OK",  # ボタンの表示名
                           command = self.button_click  # クリックされたときに呼ばれるメソッド
                           )

        # ボタンクリックに対してキーイベント処理を実装
        # self.button.bind("<ButtonPress>", self.type_event)

        # ウィジェットの設置
        self.radio0.pack()
        self.radio1.pack()
        self.radio2.pack()
        self.radio3.pack()
        self.button.pack()

        # # 時間計測用のラベル
        self.time_label = tk.Label(self, text="", font=("",20))
        self.time_label.grid(row=4, column=0, columnspan=2)
        self.result_label = tk.Label(self, text="", font=("",40))
        self.result_label.grid(row=5, column=0, columnspan=2)

        self.flg2 = True

    def radio_click(self):
        # ラジオボタンの値を取得
        value = self.radio_value.get()
        print(f"ラジオボタンの値は {value} です")

        # "OK"のボタンを押したかどうか
        self.next = False
    # def button_click(self):
    #     # 問題を次に移動させるフラグを立てる
    #     value = self.radio_value.get()
    #     self.ans_label2 = value
    #     self.next = True


    # キー入力時のイベント処理
    def button_click(self):
        value = self.radio_value.get()
        self.ans_label2 = value
        # 入力値の答え合わせ
        print("OKボタンを押しました")
        print(f"押した答え:{self.ans_label2},本当の答え：{self.ans}")
        if str(self.ans) == str(self.ans_label2):
            # logに書き込み
            self.log(self.ans_label2, self.ans,"concentrate", "correct", False)
            self.result_label.configure(text="正解！", fg="red")
            self.correct_cnt += 1
        else:
            # logに書き込み
            self.log(self.ans_label2, self.ans,"concentrate", "miss", False)

            self.result_label.configure(text="残念！", fg="blue")

        # 解答欄をクリア
        self.ans_label2 = ""

        # 次の問題を出題
        self.index += 1
        self.ans, q, radio_button_list = QUESTION()
        self.q_label2.configure(text=q)
        self.radio0.configure(text=str(radio_button_list[0]), value=str(radio_button_list[0]))
        self.radio1.configure(text=str(radio_button_list[1]), value=str(radio_button_list[1]))
        self.radio2.configure(text=str(radio_button_list[2]), value=str(radio_button_list[2]))
        self.radio3.configure(text=str(radio_button_list[3]), value=str(radio_button_list[3]))
        self.log("problem_switching","-", "concentrate", "-", False)
        # "OK"のボタンを押したかどうか
        self.next = False


    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            self.second += 1
            self.time_label.configure(text=f"経過時間：{self.second}秒")
            time.sleep(1)

            # 2分経ったら
            if self.second == 1:
                self.q_label2.configure(text="")
                messagebox.showinfo("リザルト", f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。")

                # logに書き込み
                self.log("-", "-","relax", "-", False)
                #root.destroy()

                #quit_me(root)
                #sys.exit(0)
                self.second = 0
                self.destroy()
                self.master.destroy()

                movie()
                return 0


    def log(self, situation, correct, action, judge, flag):
        # logに書き込み
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y-%m-%d %H:%M:%S.%f')

        data = [[time, situation, correct,action, judge]]
        self.df1 = pd.DataFrame(data, columns=self.columes)
        self.df = pd.concat([self.df, self.df1], axis=0)
        print(flag)

        if flag==False:
            # log書き出し
            dt_now = datetime.datetime.now()
            self.df.to_csv(".\\log_dir\\{}.csv".format(dt_now.strftime('%Y-%m-%d-%H-%M')), index=False)
            print("READ")


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("1280x720")
    #root.state("zoomed")
    root.attributes('-fullscreen', True)
    root.title("タイピングゲーム！")

    change(math)    #シーン変更先

    #root.protocol("WM_DELETE_WINDOW", App.click_close)
    root.mainloop()
# https://max999blog.com/pandas-add-row-to-dataframe/