from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import threading
import datetime
import pandas as pd
import video
import audio
import random
from tkinter import messagebox
import pyautogui as pag
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


global interval

interval = 120
relax_interval = 60

scr_w, scr_h = pag.size()
print("画面サイズの幅：", scr_w)
print("画面サイズの高さ：", scr_h)

video = video.Video()
audio = audio.Audio()

task_count=7

def click_close():
    if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
        """cap.release()
        out.release()
        cv2.destroyAllWindows()
        root.destroy()"""
        close()
        return 0

def close():
    """cap.release()
    out.release()
    cv2.destroyAllWindows()"""
    root.destroy()


"""def record(cap, out, f):
    tm=cv2.TickMeter()
    tm.start()
    count = 0
    count1 = 0
    max_count = 1
    fps = 0
    n = 0
    # 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
    while(cap.isOpened()):
        ret, frame = cap.read()                           # フレームを取得
        if ret == True:
            if count == max_count:
                tm.stop()
                fps = max_count / tm.getTimeSec()
                tm.reset()
                tm.start()
                count = 0
            cv2.putText(frame, 'FPS: {:.2f}'.format(fps),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            #cv2.putText(frame, 'Frame:{:.0f}'.format(count1),(1000, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
            out.write(frame)
            cv2.imshow('camera', frame)                            # フレームを画面に表示
            f.write(str(count1) + "," + str(fps) + "\n")
            count1 += 1
            count += 1
            # キー操作があればwhileループを抜ける
            k = cv2.waitKey(33)
            if k == 27:    # Esc key to stop
                break
        else:
            break
    # 撮影用オブジェクトとウィンドウの解放
    f.close()
    cap.release()
    out.release()
    cv2.destroyAllWindows()"""


def QUESTION():

    one = random.randint(51, 90)
    two = random.randint(20, 50)

    hugo = ["×"]
    ans = [one * two]

    # 問題をランダムに生成
    hugo = hugo[0]
    ans = ans[0]
    radio_button_list = [ans, ans - 10, ans + 10, ans + two]
    random.shuffle(radio_button_list)  # 配列の中をシャッフル
    question = "{} {} {} = ".format(one, hugo, two)

    print("hugo", hugo)
    print("ans", ans)

    return ans, question, radio_button_list


####切り替えボタン####
def change():
    global canvas2
    canvas2 = tk.Canvas(root, highlightthickness=0)
    canvas2.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    # 各種ウィジェットの作成
    label1_frame_app = tk.Label(canvas2, text="準備ができたら課題に進んでください", font=("", 40))
    button_change_frame_app = tk.Button(
        canvas2, text="進む", font=("", 40), bg="grey", command=lambda: task_select(),relief="solid"
    )
    # logに書き込み
    log.logging(
        situation="準備ができたら課題に進んでください",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
        evaluation="-",
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )
    # 各種ウィジェットの設置
    label1_frame_app.pack(anchor="center", expand=1)
    button_change_frame_app.pack(anchor="center", expand=1)


####relax動画####
def timecount(canvas, video, audio):
    second = 0
    flg = True
    # time_label = tk.Label(canvas, text="", font=("",20))
    # time_label.pack(anchor='nw',expand=0)
    while flg:
        second += 1
        time.sleep(1)  # convert second to hour, minute and seconds
        elapsed_minute = (second % 3600) // 60
        elapsed_second = second % 3600 % 60
        # print as 00:00:00
        print(str(elapsed_minute).zfill(2) + ":" + str(elapsed_second).zfill(2))
        # time_label.configure(text=f"経過時間：{str(elapsed_minute).zfill(2)}:{str(elapsed_second).zfill(2)}")

        # print(interval)
        if second == relax_interval:
            # logに書き込み
            log.logging(
                situation="リラックスモード終了",
                action="-",
                user_input="-",
                correct="-",
                judge="-",
                evaluation="-",
                eye_ans="-",
                ans_position="-",
                eye_correct="-",
                choice_1="-",
                choice_2="-",
                choice_3="-",
                choice_4="-",
            )

            video.stop()
            audio.stop()
            canvas.destroy()
            change()
            flg = False
            return 0


def movie(canvas1,v1):
    print("集中度:%s" % v1.get())

    # logに書き込み
    log.logging(
        situation="集中度の自己評価",
        action="okボタン押した",
        user_input="-",
        correct="-",
        judge="-",
        evaluation=str(v1.get()),
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )


    canvas1.destroy()
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    label = tk.Label(canvas, text="2分間休憩時間です", font=("", 40))
    label.pack(anchor="center", expand=1)

    # logに書き込み
    log.logging(
        situation="リラックスモードに移行(2分休憩スライド)",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
        evaluation="-",
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )

    # sleep 前のエポック秒(UNIX時間)を取得
    startSec = time.time()
    canvas.frame = tk.Label(canvas)
    canvas.frame.pack(side=tk.BOTTOM)
    video.openfile("./relax.mp4", canvas.frame)
    audio.openfile("./relax.wav")
    Q=[label,canvas]
    root.after(
        3000,
        image_de,
        Q
    )

def image_de(Q):
    label=Q[0]
    canvas=Q[1]
    label.pack_forget()
    # 経過時間スレッドの開始
    thread = threading.Thread(
        name="thread", target=timecount, args=[canvas, video, audio], daemon=True
    )
    thread.start()

    audio.play()
    video.play()

    # logに書き込み
    log.logging(
        situation="リラックスモード(動画開始)",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
        evaluation="-",
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )

def end(canvas):
    label = tk.Label(canvas, text="課題は終了です。", font=("", 40))
    label1 = tk.Label(canvas, text="お疲れ様でした。", font=("", 40))
    label.pack(anchor="center", expand=1)
    label1.pack(anchor="center", expand=1)

    root.after(
        3000,
        close
    )

####課題選択####
def task_select():
    canvas2.destroy()
    canvas1 = tk.Canvas(root, highlightthickness=0)  # ,bg = "cyan")
    canvas1.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    print("count:" + str(count))

    # logに書き込み
    log.logging(
        situation="準備ができたら課題に進んでください",
        action="進むボタンを押した",
        user_input="-",
        correct="-",
        judge="-",
        evaluation="-",
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )

    if count == task_count:
        end(canvas1)
    elif count % 2 == 0:
        eye_task(master=canvas1)
    else:
        Application(master=canvas1)
    # print(App)

####アンケート評価####
def questionnaire():
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    """# Frame
    frame1 = ttk.Frame(root, padding=10)"""
    # Style - Theme
    ttk.Style().configure('MyWidget.TRadiobutton' ,font=(None,30))#, relief="flat",overrelief="raised")
    ttk.Style().map('MyWidget.TRadiobutton',
                    foreground=[ ('active', 'blue')],
                    background=[ ('active', 'white')]
                    )
    #ttk.Style().theme_use("alt")
    label = tk.Label(canvas, text="課題を通して自分の集中度を評価してください", font=("", 30))
    #whi = tk.Label(canvas, text="", font=("", 30))

    # Radiobutton 1
    v1 = StringVar()
    rb1 = ttk.Radiobutton(
        canvas,
        text="1.集中していた",
        value='1',
        style='MyWidget.TRadiobutton',
        variable=v1, command =lambda: change_state(button1))

    # Radiobutton 2
    rb2 = ttk.Radiobutton(
        canvas,
        text='2.少し集中していた',
        value='2',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb3 = ttk.Radiobutton(
        canvas,
        text='3.どちらでもない',
        value='3',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb4 = ttk.Radiobutton(
        canvas,
        text='4.少し集中できなかった',
        value='4',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Radiobutton 2
    rb5 = ttk.Radiobutton(
        canvas,
        text='5.全く集中できなかった',
        value='5',
        style='MyWidget.TRadiobutton',
        variable=v1, command = lambda: change_state(button1))

    # Button
    button1 = tk.Button(
        canvas,
        text='OK',
        font=("", 30),
        command=lambda: movie(canvas,v1),
        state=tk.DISABLED,relief="solid",
        bg="grey")

    label.pack(anchor="center",expand=1)
    rb1.pack(anchor="center",pady=20)
    rb2.pack(anchor="center",pady=20)
    rb3.pack(anchor="center",pady=20)
    rb4.pack(anchor="center",pady=20)
    rb5.pack(anchor="center",pady=20)
    button1.pack(anchor="center", expand=1)

    # logに書き込み
    log.logging(
        situation="集中度の自己評価アンケートの表示",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
        evaluation="-",
        eye_ans="-",
        ans_position="-",
        eye_correct="-",
        choice_1="-",
        choice_2="-",
        choice_3="-",
        choice_4="-",
    )


def change_state(button1):
    if button1["state"] == tk.DISABLED:
        button1["state"] = tk.NORMAL

####視線課題####
class eye_task(tk.Frame):
    def __init__(self, master):
        # logに書き込み
        log.logging(
            situation="視線課題の説明",
            action="-",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )

        super().__init__(master)
        # self.pack()
        self.column_data = (0, 0, 1, 1)
        self.row_data = (0, 1, 0, 1)
        # 各種ウィジェットの作成
        self.label1_frame_app = tk.Label(self.master, text="〇", font=("", 100),fg="red")
        self.label2_frame_app = tk.Label(self.master, text="を選択・クリックしてください", font=("", 40))
        self.button_change_frame_app = tk.Button(
            self.master, text="課題に進む", font=("", 40), bg="grey", command=lambda: self.rocate(),relief="solid"
        )
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.label2_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)


    def rocate(self):
        # logに書き込み
        log.logging(
            situation="視線課題の説明",
            action="進むボタンを押した",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )
        self.label1_frame_app.pack_forget()
        self.label2_frame_app.pack_forget()
        self.button_change_frame_app.pack_forget()

        self.text = self.random_symbol()
        self.flg = True

        self.symbol = []
        self.button = []
        # logに書き込み
        log.logging(
            situation="視線課題の開始",
            action="進むボタンを押した",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )
        #print(self.text)
        for i in range(4):
            self.symbol.append(tk.StringVar())
            self.symbol[i].set(self.text[i][0])
            # print(self.symbol[i])
            self.button.append(
                tk.Button(
                    self.master,
                    textvariable=self.symbol[i],
                    fg=self.text[i][1],
                    font=("", 100),
                )
            )
            self.button[i].grid(
                column=self.column_data[i],
                row=self.row_data[i],
                padx=30,
                pady=30,
                sticky="nsew",
            )
            # ボタンクリック時のイベント設定
            self.button[i].bind("<ButtonPress>",  (lambda e, num=i: self.button_func(e, num)))

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer, daemon=True)
        self.t.start()

    def random_symbol(self):  # 問題作成
        self.text = [["〇", "red"]]
        self.label = ["〇", "△", "□", "×"]
        self.color = ["red"]#, "green", "blue", "yellow"]

        for i in range(3):
            self.a = random.choice(self.label)
            self.b = random.choice(self.color)
            while self.a == "〇" and self.b == "red":
                self.a = random.choice(self.label)
                self.b = random.choice(self.color)
            self.text.append([self.a, self.b])
        random.shuffle(self.text)
        self.pos = self.text
        return self.text

    def button_func(self, event,num):
        if num == 0:
            position = "第2象限"
        elif num == 1:
            position = "第3象限"
        elif num == 2:
            position = "第1象限"
        elif num == 3:
            position = "第4象限"
        # logに書き込み
        log.logging(
            situation="集中",
            action="userがボタン入力",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans=str(event.widget.cget("text")),
            ans_position=str(position),
            eye_correct="〇",
            choice_1=str(self.pos[2][0]),
            choice_2=str(self.pos[0][0]),
            choice_3=str(self.pos[1][0]),
            choice_4=str(self.pos[3][0]),

        )
        # event.widget.config(fg="red")
        print(position)
        print("形:" + event.widget.cget("text") + "　色:" + event.widget.cget("fg"))
        for i in range(4):
            self.button[i].grid_forget()
        self.master.create_text(
            scr_w / 2, scr_h / 2, text="●", font=("", 40), tag="line"
        )

        # 1000ms後にchange_label_textを実行
        root.after(
            1000,
            self.change_label_text,
        )

    def timer(self):
        self.second = 0
        self.flg = True
        # print(self.second)
        while self.flg:
            # print(self.second)
            self.second += 1
            time.sleep(1)

            # 2分経ったら
            if self.second == interval:
                # logに書き込み
                log.logging(
                    situation="視線課題の終了",
                    action="-",
                    user_input="-",
                    correct="-",
                    judge="-",
                    evaluation="-",
                    eye_ans="-",
                    ans_position="-",
                    eye_correct="-",
                    choice_1="-",
                    choice_2="-",
                    choice_3="-",
                    choice_4="-",
                )
                self.second = 0
                self.destroy()
                self.master.destroy()
                global count
                count += 1
                self.flg = False
                print("----------------------")
                questionnaire()

                return 0

    def change_label_text(self):
        self.text = self.random_symbol()
        print(self.flg)
        if self.flg == True:
            self.master.delete("line")
            for i in range(4):
                self.symbol[i].set(self.text[i][0])
                self.button[i]["fg"] = self.text[i][1]
                self.button[i].grid(
                    column=self.column_data[i],
                    row=self.row_data[i],
                    padx=30,
                    pady=30,
                    sticky="nsew",
                )


####計算課題####


class Application(tk.Frame):
    def __init__(self, master):
        # logに書き込み
        log.logging(
            situation="計算課題の説明",
            action="-",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )

        super().__init__(master)
        self.pack()

        # 問題数インデックス
        self.index = 0

        # 正解数カウント用
        self.correct_cnt = 0


        # self.pack()
        self.column_data = (0, 0, 1, 1)
        self.row_data = (0, 1, 0, 1)
        # 各種ウィジェットの作成
        self.label1_frame_app = tk.Label(self.master, text="2桁の ＋,－,× を行います", font=("", 40))#,fg="red")
        self.label2_frame_app = tk.Label(self.master, text="4択のうち正しい答えを選択し決定してください", font=("", 40))
        self.button_change_frame_app = tk.Button(
            self.master, text="課題に進む", font=("", 40), bg="grey", command=lambda: self.rocate(),relief="solid"
        )
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.label2_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)


    def rocate(self):
        # logに書き込み
        log.logging(
            situation="計算課題の説明",
            action="進むボタンを押した",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )
        self.label1_frame_app.pack_forget()
        self.label2_frame_app.pack_forget()
        self.button_change_frame_app.pack_forget()
        self.create_widgets()

        # 経過時間スレッドの開始
        self.t = threading.Thread(target=self.timer, daemon=True)
        self.t.start()

        # Tkインスタンスに対してキーイベント処理を実装
        # self.master.bind("<KeyPress>", self.type_event)

    # ウィジェットの生成と配置
    def create_widgets(self):
        # logに書き込み
        log.logging(
            situation="計算課題の開始",
            action="-",
            user_input="-",
            correct="-",
            judge="-",
            evaluation="-",
            eye_ans="-",
            ans_position="-",
            eye_correct="-",
            choice_1="-",
            choice_2="-",
            choice_3="-",
            choice_4="-",
        )
        self.ans_label2 = tk.Label(self, text="", width=10, anchor="w", font=("", 40))
        self.ans_label2.grid(row=0, column=0)
        self.q_label = tk.Label(self, text="お題：", font=("", 40))
        self.q_label.grid(row=1, column=0)

        # 問題作成
        self.ans, q, radio_button_list = QUESTION()
        self.q_label2 = tk.Label(self, text=q, width=20, anchor="w", font=("", 40))
        self.q_label2.grid(row=1, column=1)
        self.ans_label = tk.Label(self, text="解答：", font=("", 40))
        self.ans_label.grid(row=2, column=0)
        self.answer = tk.Label(self, text="", width=20, anchor="w", font=("", 40))
        self.answer.grid(row=2, column=1)

        self.result_label = tk.Label(self, text="", font=("", 40))
        self.result_label.grid(row=3, column=0, columnspan=2)

        # ウィジェットの作成
        self.radio_value = tk.IntVar()  # ラジオボタンの初期値を0にする

        # ラジオボタンの作成
        self.radio0 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[0]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[0]),  # ラジオボタンに割り付ける値の設定
            indicator=0,
            background="light blue",
            font=("", 20),
            width=20,
            height=3,
        )

        self.radio1 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[1]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[1]),  # ラジオボタンに割り付ける値の設定
            indicator=0,
            background="light blue",
            font=("", 20),
            width=20,
            height=3,
        )

        self.radio2 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[2]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[2]),  # ラジオボタンに割り付ける値の設定
            indicator=0,
            background="light blue",
            font=("", 20),
            width=20,
            height=3,
        )

        self.radio3 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[3]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[3]),  # ラジオボタンに割り付ける値の設定
            indicator=0,
            background="light blue",
            font=("", 20),
            width=20,
            height=3,
        )

        # ボタンの作成
        self.button = tk.Button(
            self.master,
            text="OK",  # ボタンの表示名
            command=self.button_click,  # クリックされたときに呼ばれるメソッド
            relief="solid",
            state=tk.DISABLED,
            width=20,
            height=3,
            bg="grey",
        )

        # ボタンクリックに対してキーイベント処理を実装
        # self.button.bind("<ButtonPress>", self.type_event)

        # ウィジェットの設置
        self.radio0.pack()
        self.radio1.pack()
        self.radio2.pack()
        self.radio3.pack()
        self.button.pack(expand=1)

        # # 時間計測用のラベル
        self.time_label = tk.Label(self, text="", font=("", 20))
        self.time_label.grid(row=4, column=0, columnspan=2)
        self.result_label = tk.Label(self, text="", font=("", 20))
        self.result_label.grid(row=5, column=0, columnspan=2)

        self.flg2 = True

    def radio_click(self):
        # ラジオボタンの値を取得
        value = self.radio_value.get()
        print(f"ラジオボタンの値は {value} です")
        self.answer.configure(text=value)
        if self.button["state"] == tk.DISABLED:
            self.button["state"] = tk.NORMAL
            self.button["bg"] = "white"

        # "OK"のボタンを押したかどうか
        self.next = False

    # def button_click(self):
    #     # 問題を次に移動させるフラグを立てる
    #     value = self.radio_value.get()
    #     self.ans_label2 = value
    #     self.next = True

    # キー入力時のイベント処理
    def button_click(self):
        global log
        value = self.radio_value.get()
        self.ans_label2 = value

        if self.button["state"] == tk.NORMAL:
            self.button["state"] = tk.DISABLED
            self.button["bg"] = "grey"

        # 入力値の答え合わせ
        print("OKボタンを押しました")
        print(f"押した答え:{self.ans_label2},本当の答え：{self.ans}")
        if str(self.ans) == str(self.ans_label2):
            # logに書き込み
            log.logging(
                situation="集中",
                action="userがボタン入力",
                user_input=str(self.ans_label2),
                correct=str(self.ans),
                judge="正解",
                evaluation="-",
                eye_ans="-",
                ans_position="-",
                eye_correct="-",
                choice_1="-",
                choice_2="-",
                choice_3="-",
                choice_4="-",
            )

            self.result_label.configure(text="正解！", fg="red")
            self.correct_cnt += 1
        else:
            # logに書き込み
            log.logging(
                situation="集中",
                action="userがボタン入力",
                user_input=str(self.ans_label2),
                correct=str(self.ans),
                judge="不正解",
                evaluation="-",
                eye_ans="-",
                ans_position="-",
                eye_correct="-",
                choice_1="-",
                choice_2="-",
                choice_3="-",
                choice_4="-",
            )

            self.result_label.configure(text="残念！", fg="blue")

        # 次の問題を出題
        self.index += 1
        self.ans, q, radio_button_list = QUESTION()
        self.q_label2.configure(text=q)
        self.radio0.configure(
            text=str(radio_button_list[0]), value=str(radio_button_list[0])
        )
        self.radio1.configure(
            text=str(radio_button_list[1]), value=str(radio_button_list[1])
        )
        self.radio2.configure(
            text=str(radio_button_list[2]), value=str(radio_button_list[2])
        )
        self.radio3.configure(
            text=str(radio_button_list[3]), value=str(radio_button_list[3])
        )
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
            if self.second == interval:
                # logに書き込み
                log.logging(
                    situation="計算課題の終了",
                    action="-",
                    user_input="-",
                    correct="-",
                    judge="-",
                    evaluation="-",
                    eye_ans="-",
                    ans_position="-",
                    eye_correct="-",
                    choice_1="-",
                    choice_2="-",
                    choice_3="-",
                    choice_4="-",
                )

                self.q_label2.configure(text="")
                messagebox.showinfo(
                    "リザルト",
                    f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。",
                )

                # logに書き込み
                # root.destroy()

                # quit_me(root)
                # sys.exit(0)
                self.second = 0
                self.destroy()
                self.master.destroy()

                global count
                count += 1
                questionnaire()
                return 0

# log
class Log:
    def first_log(self, first_time):
        self.first_time = first_time

    def logging(
            self, situation: str, action: str, user_input: str, correct: str, judge: str, evaluation: str, eye_ans: str, ans_position: str, eye_correct: str,
            choice_1: str, choice_2: str, choice_3: str, choice_4: str,
    ):
        self.situation = situation
        self.action = action
        self.user_input = user_input
        self.correct = correct
        self.judge = judge
        self.evaluation = evaluation
        self.eye_ans = eye_ans
        self.ans_position = ans_position
        self.eye_correct = eye_correct
        self.choice_1 = choice_1
        self.choice_2 = choice_2
        self.choice_3 = choice_3
        self.choice_4 = choice_4

        filepath = f".\\log_dir\\{self.first_time}.csv"
        columns = ["時間", "状態", "アクション", "計算課題の入力", "正解値", "正誤判定","集中度自己評価","視線課題の入力","答えの位置","正解","第1象限","第2象限","第3象限","第4象限"]

        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y_%m_%d_%H.%M.%S')
        print(time)
        # self.log_data = {
        #     "time": [],
        #     "situation": [],
        #     "action": [],
        #     "user_input": [],
        #     "correct": [],
        #     "judge": [],
        # }
        self.log_data = {
            "時間": [],
            "状態": [],
            "アクション": [],
            "計算課題の入力": [],
            "正解値": [],
            "正誤判定": [],
            "集中度自己評価": [],
            "視線課題の入力": [],
            "答えの位置": [],
            "正解": [],
            "第1象限": [],
            "第2象限": [],
            "第3象限": [],
            "第4象限": [],
        }
        # self.log_data["time"].append(time)
        # self.log_data["situation"].append(self.situation)
        # self.log_data["action"].append(self.action)
        # self.log_data["user_input"].append(self.user_input)
        # self.log_data["correct"].append(self.correct)
        # self.log_data["judge"].append(self.judge)

        self.log_data["時間"].append(time)
        self.log_data["状態"].append(self.situation)
        self.log_data["アクション"].append(self.action)
        self.log_data["計算課題の入力"].append(self.user_input)
        self.log_data["正解値"].append(self.correct)
        self.log_data["正誤判定"].append(self.judge)
        self.log_data["集中度自己評価"].append(self.evaluation)
        self.log_data["視線課題の入力"].append(self.eye_ans)
        self.log_data["答えの位置"].append(self.ans_position)
        self.log_data["正解"].append(self.eye_correct)
        self.log_data["第1象限"].append(self.choice_1)
        self.log_data["第2象限"].append(self.choice_2)
        self.log_data["第3象限"].append(self.choice_3)
        self.log_data["第4象限"].append(self.choice_4)

        if os.path.isfile(filepath):
            df1 = pd.read_csv(filepath, encoding="shift_jis")
            df2 = pd.DataFrame(self.log_data)
            df = pd.merge(df1, df2, how="outer")
            df.to_csv(
                filepath,
                encoding="shift_jis",
                index=False,
            )
        else:
            df = pd.DataFrame(self.log_data)
            df.to_csv(
                filepath,
                encoding="shift_jis",
                index=False,
                columns=columns
            )


if __name__ == "__main__":
    """#dt_now = datetime.datetime.now()
    dt_before = datetime.datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    #dt_before = datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    print("カメラを起動した時刻"+str(dt_before))
    cap = cv2.VideoCapture(1)

    fps = 30
    w = 1280
    h = 720
    #cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
    # 動画ファイル保存用の設定
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(fps)# カメラのFPSを取得
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')     # 動画保存時のfourcc設定（mp4用）

    dt_after = datetime.datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    #dt_after = datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    print("カメラを起動後の時刻"+str(dt_after))
    name="./camera/test"
    txt_name = str(name)+'.txt'
    f = open(str(txt_name), 'w')
    print(f)
    camera_name = str(name)+'_video.mp4'
    out = cv2.VideoWriter(str(camera_name), fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    dt_after = datetime.datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    #dt_after = datetime.now().strftime('%Y_%b_%d_%H.%M.%S.%f')[:-3]
    print("カメラを起動後の時刻"+str(dt_after))
    f.write("カメラを起動した時刻,"+str(dt_before)+"\nカメラを起動後の時刻,"+str(dt_after)+"\n解像度,"+str(w)+"×"+str(h)+"\n動画FPS,"+str(fps)+"\n")
    f.write("フレーム数,FPS\n")
    thread = threading.Thread(name="thread", target=record, args=[cap, out, f], daemon=True)
    thread.start()"""

    root = tk.Tk()
    # root.geometry("1280x720")
    # root.state("zoomed")
    global count
    count = 1
    root.attributes("-fullscreen", True)
    root.title("タイピングゲーム！")

    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y_%m_%d_%H.%M.%S')[:-3]
    global log
    log = Log()
    log.first_log(now)
    # logに書き込み
    log.logging(situation="課題スタート", action="-", user_input="-", correct="-", judge="-", evaluation="-", eye_ans="-",ans_position="-", eye_correct="-",
                choice_1="-", choice_2="-", choice_3="-", choice_4="-")
    #print("A:"+datetime.datetime.now().strftime('%Y_%m_%d_%H.%M.%S.%f')[:-3])

    # log.log_to_csv()

    change()  # シーン変更先
    # change(eye_task)
    root.protocol("WM_DELETE_WINDOW", click_close)
    root.mainloop()
# https://max999blog.com/pandas-add-row-to-dataframe/
