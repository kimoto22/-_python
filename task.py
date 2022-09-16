import sys
import tkinter as tk
import time
import threading
import random
import datetime
import pandas as pd
import video
import audio
import random
from tkinter import messagebox
import pyautogui as pag
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from PIL import Image, ImageTk # ← 追加

global interval
interval = 10
scr_w, scr_h = pag.size()
print("画面サイズの幅：", scr_w)
print("画面サイズの高さ：", scr_h)

video = video.Video()
audio = audio.Audio()

task_count=7

def click_close():
    if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        root.destroy()
        return 0

def close():
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    root.destroy()


def record(cap, out, f):
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
    cv2.destroyAllWindows()




def QUESTION():
    one = random.randint(50, 200)
    two = random.randint(1, 49)
    hugo_index = random.randint(0, 2)

    random_radiobutton = random.randint(0, 3)
    hugo = ["×", "-", "+"]
    ans = [one * two, one - two, one + two]

    # 問題をランダムに生成
    hugo = hugo[hugo_index]
    ans = ans[hugo_index]
    radio_button_list = [ans, ans * 10, ans - 10, ans * 5]
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
        canvas2, text="進む", font=("", 40), bg="grey", command=lambda: task_select()
    )
    # logに書き込み
    log.logging(
        situation="準備ができたら課題に進んでください",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
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
        if second == interval:
            video.stop()
            audio.stop()
            canvas.destroy()
            change()
            flg = False

            return 0


def movie():
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(
        fill=tk.BOTH, expand=True
    )  # configure canvas to occupy the whole main window
    label = tk.Label(canvas, text="2分間休憩時間です", font=("", 40))
    label.pack(anchor="center", expand=1)

    # logに書き込み
    log.logging(
        situation="リラックスモードモードに移行",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
    )


    # sleep 前のエポック秒(UNIX時間)を取得
    startSec = time.time()


    canvas.frame = tk.Label(canvas)
    canvas.frame.pack(side=tk.BOTTOM)
    video.openfile("./relax.mp4", canvas.frame)
    audio.openfile("./relax.wav")
    # 経過時間スレッドの開始
    thread = threading.Thread(
        name="thread", target=timecount, args=[canvas, video, audio], daemon=True
    )
    thread.start()

    # logに書き込み
    log.logging(
        situation="リラックスモードモード",
        action="-",
        user_input="-",
        correct="-",
        judge="-",
    )

    """audio.play()
    video.play()
    label.pack_forget()"""
    # sleep していた秒数を計算して表示
    print(time.time() - startSec)
    #time.sleep(3)

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
        action="-",
        user_input="進むボタンを押した",
        correct="-",
        judge="-",
    )

    if count == task_count:
        end(canvas1)
    elif count % 2 == 0:
        eye_task(master=canvas1)
    else:
        Application(master=canvas1)
    # print(App)


####視線課題####


class eye_task(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        # self.pack()
        self.column_data = (0, 0, 1, 1)
        self.row_data = (0, 1, 0, 1)
        # 各種ウィジェットの作成
        self.label1_frame_app = tk.Label(self.master, text="〇", font=("", 100),fg="red")
        self.label2_frame_app = tk.Label(self.master, text="を選択・クリックしてください", font=("", 40))
        self.button_change_frame_app = tk.Button(
            self.master, text="課題に進む", font=("", 40), bg="grey", command=lambda: self.rocate()
        )
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.label2_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)


    def rocate(self):
        self.label1_frame_app.pack_forget()
        self.label2_frame_app.pack_forget()
        self.button_change_frame_app.pack_forget()

        self.text = self.random_symbol()
        self.flg = True

        self.symbol = []
        self.button = []
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
            self.button[i].bind("<ButtonPress>", self.button_func)

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
        self.color = ["red", "green", "blue", "yellow"]

        for i in range(3):
            self.a = random.choice(self.label)
            self.b = random.choice(self.color)
            while self.a == "〇" and self.b == "red":
                self.a = random.choice(self.label)
                self.b = random.choice(self.color)
            self.text.append([self.a, self.b])
        random.shuffle(self.text)
        return self.text

    def button_func(self, event):
        # event.widget.config(fg="red")
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
            print(self.second)
            self.second += 1
            time.sleep(1)

            # 2分経ったら
            if self.second == interval:
                self.second = 0
                self.destroy()
                self.master.destroy()
                global count
                count += 1
                self.flg = False
                print("----------------------")
                movie()

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
            self.master, text="課題に進む", font=("", 40), bg="grey", command=lambda: self.rocate()
        )
        # 各種ウィジェットの設置
        self.label1_frame_app.pack(anchor="center", expand=1)
        self.label2_frame_app.pack(anchor="center", expand=1)
        self.button_change_frame_app.pack(anchor="center", expand=1)


    def rocate(self):
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
            font=("", 20),
        )

        self.radio1 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[1]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[1]),  # ラジオボタンに割り付ける値の設定
            font=("", 20),
        )

        self.radio2 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[2]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[2]),  # ラジオボタンに割り付ける値の設定
            font=("", 20),
        )

        self.radio3 = tk.Radiobutton(
            self.master,
            text=str(radio_button_list[3]),  # ラジオボタンの表示名
            command=self.radio_click,  # クリックされたときに呼ばれるメソッド
            variable=self.radio_value,  # 選択の状態を設定する
            value=str(radio_button_list[3]),  # ラジオボタンに割り付ける値の設定
            font=("", 20),
        )

        # ボタンの作成
        self.button = tk.Button(
            self.master,
            text="OK",  # ボタンの表示名
            command=self.button_click,  # クリックされたときに呼ばれるメソッド
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
        self.time_label = tk.Label(self, text="", font=("", 20))
        self.time_label.grid(row=4, column=0, columnspan=2)
        self.result_label = tk.Label(self, text="", font=("", 40))
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
        global log
        value = self.radio_value.get()
        self.ans_label2 = value
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
                movie()
                return 0


# log


class Log:
    def first_log(self, first_time):
        self.first_time = first_time

    def logging(
        self, situation: str, action: str, user_input: str, correct: str, judge: str
    ):
        self.situation = situation
        self.action = action
        self.user_input = user_input
        self.correct = correct
        self.judge = judge

        filepath = f".\\log_dir\\{self.first_time}.csv"
        columns = ["時間", "状態", "アクション", "ユーザーの入力", "正解値", "正誤判定"]

        dt_now = datetime.datetime.now()
        time = dt_now.strftime("%Y-%m-%d-%H-%M-%S")
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
            "ユーザーの入力": [],
            "正解値": [],
            "正誤判定": [],
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
        self.log_data["ユーザーの入力"].append(self.user_input)
        self.log_data["正解値"].append(self.correct)
        self.log_data["正誤判定"].append(self.judge)

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
    #dt_now = datetime.datetime.now()
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
    thread.start()

    root = tk.Tk()
    # root.geometry("1280x720")
    # root.state("zoomed")
    global count
    count = 1
    root.attributes("-fullscreen", True)
    root.title("タイピングゲーム！")

    dt_now = datetime.datetime.now()
    now = dt_now.strftime("%Y-%m-%d-%H-%M-%S")
    global log
    log = Log()
    log.first_log(now)
    # logに書き込み
    log.logging(situation="課題スタート", action="-", user_input="-", correct="-", judge="-")

    # log.log_to_csv()

    change()  # シーン変更先
    # change(eye_task)
    root.protocol("WM_DELETE_WINDOW", click_close)
    root.mainloop()
# https://max999blog.com/pandas-add-row-to-dataframe/
