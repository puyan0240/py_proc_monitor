import tkinter
import tkinter.simpledialog
from tkinter import ttk, messagebox
import time
import os
import threading  #スレッド
from gtts import gTTS  #文字->音声ファイル化
from playsound import playsound  #音声ファイルを再生
import psutil  #プロセス取得

max_count = (60 * 60)
count = 0
play_str = ""

#一時ファイル
TMP_PLAY_FILENAME = "tmp_play.mp3"

PROC_NAME = "thunderbird.exe"

############################################################
#音声再生タスク
############################################################
def play_task():
    global play_str

    while True:

        if play_str != "":
            print("-------------------------")
            #音声ファイル化
            try:
                out = gTTS(play_str, lang='ja', slow=False)
                out.save(TMP_PLAY_FILENAME)
            except Exception as e:
                print(f"mp3 file err: {str(e)}")

            #音声ファイルを再生
            try:
                playsound(TMP_PLAY_FILENAME)
            except Exception as e:
                print(f"play err: {str(e)}")


            play_str = ""

            #音声ファイルを削除
            if os.path.exists(TMP_PLAY_FILENAME) == True:
                os.remove(TMP_PLAY_FILENAME)

        time.sleep(1)


############################################################
#プロセス監視タスク
############################################################
def monitor_task():
    global count,play_str

    while True:

        #プロセス監視
        for proc in psutil.process_iter():
            try:
                proc_str = proc.exe()
                proc_list = proc_str.split("\\")
                if proc_list[-1] == PROC_NAME:
                    if count == 0:
                        #ボタン押下許可
                        btn.config(state=tkinter.NORMAL)
                    
                        if play_str == "":
                            play_str = "政府の個人情報保護委員会は2日、対話型人工知能（AI）「チャットGPT」を開発した米新興企業オープンAIに対し行政指導したと発表した。"
                    break
            except psutil.AccessDenied: #アクセス権なし
                pass
            except Exception as e:
                print(f"proc err: {str(e)}")

        #残り時間を表示&タイマ減算
        if count != 0:
            min = count / 60
            sec = count % 60
            timer_str = "%02d:%02d"%(min, sec)
            label_top["text"] = timer_str
            count -= 1

        time.sleep(1)  # 1s


def click_btn():
    global count

    #タイマーセット
    count = max_count

    #ボタン押下禁止
    btn.config(state=tkinter.DISABLED)


############################################################
#フレームの終了「×」を押された時のイベント
############################################################
def click_close():
    global play_str

    val = tkinter.StringVar()
    val.set(tkinter.simpledialog.askstring('パスワード', 'パスワードを入力してください'))
    if val.get() == "":
        # tkinter終了
        root.destroy()

        #音声ファイルを削除
        if os.path.exists(TMP_PLAY_FILENAME) == True:
            os.remove(TMP_PLAY_FILENAME)
    else:
        messagebox.showerror("エラー","パスワードが間違っています")

        play_str = "パスワードが間違っています"


if __name__ == '__main__':

    #---------- Window作成 ----------
    root = tkinter.Tk()
    root.title("監視くん")
    root.resizable(False, False)  #リサイズ不可

    #---------- Frame作成 ----------
    frame_top    = tkinter.Frame(root)
    frame_bottom = tkinter.Frame(root)
    separator    = ttk.Separator(root, orient="horizontal", style="blue.TSeparator")

    #---------- Frame配置 ----------
    frame_top.grid(row=0, column=0)
    separator.grid(row=1, column=0, sticky="ew", pady=5)
    frame_bottom.grid(row=2, column=0)    

    #---------- Frame(TOP) ----------
    #Label
    label_top = tkinter.Label(frame_top, text="00:00", font=("system", "40", "bold"))
    label_top.grid(row=0, column=0, pady=10)

    #---------- Frame(BOTTOM) ----------
    #Button
    btn = tkinter.Button(frame_bottom, text="静かにしてください", font=("system", "10", "normal"),command=click_btn)
    btn.config(state=tkinter.DISABLED)
    btn.grid(row=0, column=0, padx=100, pady=20, ipadx=5, ipady=5)


    #---------- タスク起動 ----------
    #プロセス監視タスク
    monitor_task_id = threading.Thread(target=monitor_task)
    monitor_task_id.daemon = True  #デーモン
    monitor_task_id.start()

    #音声再生タスク
    play_task_id = threading.Thread(target=play_task)
    play_task_id.daemon = True  #デーモン
    play_task_id.start()


    #終了ボタン押下イベント登録
    root.protocol("WM_DELETE_WINDOW", click_close)

    root.mainloop()

