import tkinter
from tkinter import ttk, messagebox
import time
import threading  #スレッド
import psutil

max_count = (60 * 60)

def monitor_task():

    count = 0

    while True:

        count += 1
        if count >= max_count:
            count = 0

        min = count / 60
        sec = count % 60
        timer_str = "%02d:%02d"%(min, sec)
        label_top["text"] = timer_str

        time.sleep(1)  # 1s



if __name__ == '__main__':

    #---------- Window作成 ----------
    root = tkinter.Tk()
    root.title("監視くん")
    root.resizable(False, False)  #リサイズ不可

    #---------- Frame作成 ----------
    frame_top    = tkinter.Frame(root)
    frame_center = tkinter.Frame(root)
    frame_bottom = tkinter.Frame(root)
    separator    = ttk.Separator(root, orient="horizontal", style="blue.TSeparator")

    #---------- Frame配置 ----------
    frame_top.grid(row=0, column=0)
    separator.grid(row=1, column=0, sticky="ew", pady=5)
    frame_center.grid(row=2, column=0)
    frame_bottom.grid(row=3, column=0)    

    #---------- Frame(TOP) ----------
    #Label
    label_top = tkinter.Label(frame_top, text="hoge")
    label_top.grid(row=0, column=0, pady=10)

    #dbg
    hour = 23
    min = 1
    sec = 3
    str = "%02d:%02d %02d"%(hour,min,sec)
    label_top['text'] = str


    #タスク起動
    task_id = threading.Thread(target=monitor_task)
    task_id.daemon = True  #デーモン
    task_id.start()

    root.mainloop()

