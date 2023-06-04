import tkinter
import tkinter.simpledialog
from tkinter import ttk, messagebox
import time
import os
import threading  #スレッド
from gtts import gTTS  #文字->音声ファイル化
import pygame  #音声ファイルを再生
import psutil  #プロセス取得

#待ち時間
max_count = (10 * 60) #10分

display_count = count = 0
last_play_str = ""

#アイコン
ICON_FILENAME = "icon/icon.png"

#一時ファイル
TMP_PLAY_FILENAME = "tmp_play.mp3"

#文字リスト
DATA_FILENAME = "data.txt"
data_list = []
data_pos = 0

#監視するプロセス
PROC_NAME = "steam.exe"


############################################################
#音声再生関数 (pygameで再生する)
############################################################
def play_voice(play_str):
    global last_play_str

    #空文字は処理しない
    if play_str == "":
        return

    #再生中に他のアナウンスを流す場合の対処
    if pygame.mixer.music.get_busy() == True:
        if last_play_str == play_str:
            return  #同じアナウンスのため
        else:
            #音声再生を停止
            pygame.mixer.music.stop()

    #再生中のアナウンスを保持
    last_play_str = play_str


    #アナウンスを文字化⇒音声再生する
    try:
        #先にunloadしないと、音声ファイルにアクセスができない
        pygame.mixer.music.unload()
        #音声ファイルを削除
        if os.path.exists(TMP_PLAY_FILENAME) == True:
            os.remove(TMP_PLAY_FILENAME)

        #音声ファイル化
        out = gTTS(play_str, lang='ja', slow=False)
        out.save(TMP_PLAY_FILENAME)

        #音声ファイルを再生
        pygame.mixer.music.load(TMP_PLAY_FILENAME)
        pygame.mixer.music.play(0) #1回再生

    except Exception as e:
        print(f"play err: {str(e)}")


############################################################
#プロセス監視タスク
############################################################
def monitor_task():
    global display_count,count,data_pos

    while True:

        #プロセス監視
        for proc in psutil.process_iter():  #起動中のプロセス一覧を取得
            try:
                proc_str = proc.exe()  #プロセス名を取得
                proc_list = proc_str.split("\\")

                if proc_list[-1] == PROC_NAME:  #監視対象のプロセスです
                    if count == 0:  #タイムアウトしました
                        #ボタン押下許可
                        btn.config(state=tkinter.NORMAL)

                        #音声再生
                        #警告メッセージが消えてしまうので、ここでは空きまで待つ
                        if pygame.mixer.music.get_busy() == False:
                            if len(data_list) == 0:
                                play_voice("こんにちは")
                            else:
                                #文字リストの内容をアナウンスする
                                data_str = data_list[data_pos]
                                play_voice(data_str)
                    break #プロセス

            except psutil.AccessDenied: #アクセス権なし
                pass
            except Exception as e:
                print(f"proc err: {str(e)}")

        #タイマ減算
        if count > 0:
            count -= 1

        #残り時間を表示 ※前回から変化があった場合のみ
        if display_count != count:
            min = count / 60
            sec = count % 60
            timer_str = "%02d:%02d"%(min, sec)
            label_top["text"] = timer_str
            display_count = count

        time.sleep(1)  # 1s


############################################################
#ボタンを押された時のイベント
############################################################
def click_btn():
    global count,data_pos

    #音声アナウンスを停止
    if pygame.mixer.music.get_busy() == True:  #再生中?
        pygame.mixer.music.stop()  #再生を停止

    #次回アナウンスする文字リストの位置を確定
    if len(data_list) != 0:
        data_pos += 1
        if data_pos >= len(data_list):
            data_pos = 0

    #タイマーセット
    count = max_count

    #ボタン押下禁止
    btn.config(state=tkinter.DISABLED)


############################################################
#フレームの終了「×」を押された時のイベント
############################################################
def click_close():

    val = tkinter.StringVar()
    val.set(tkinter.simpledialog.askstring('パスワード', 'パスワードを入力してください'))
    if val.get() == "":

        #アナウンス中は停止する
        if pygame.mixer.music.get_busy() == True:
            pygame.mixer.music.stop()

        #先にunloadしないと、音声ファイルにアクセスができない
        pygame.mixer.music.unload()
        #音声ファイルを削除
        if os.path.exists(TMP_PLAY_FILENAME) == True:
            os.remove(TMP_PLAY_FILENAME)

        # tkinter終了
        root.destroy()

    else:
        #音声再生(警告メッセージ)
        play_voice("パスワードが間違っています")

        #ポップアップメッセージ
        messagebox.showerror("エラー","パスワードが間違っています")


if __name__ == '__main__':

    #---------- Window作成 ----------
    root = tkinter.Tk()
    root.title("監視くん")
    root.resizable(False, False)  #リサイズ不可

    #---------- アイコン ----------
    root.iconphoto(False, tkinter.PhotoImage(file=ICON_FILENAME))

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

    #アナウンス文字を外部ファイルから読み込む
    if os.path.exists(DATA_FILENAME) == False:
        with open(DATA_FILENAME, 'w', encoding='utf-8') as f:
            pass #ファイルが無ければ空ファイル作成

    with open(DATA_FILENAME, 'r', encoding='utf-8') as f:
        lines = f.read()
        for line in lines.split('\n'):
            if len(line) != 0:
                data_list.append(line) #行単位で文字リストへ格納

    #pygameを初期化
    pygame.init()

    #終了ボタン押下イベント登録
    root.protocol("WM_DELETE_WINDOW", click_close)

    root.mainloop()

