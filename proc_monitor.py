import tkinter
from tkinter import ttk, messagebox
import time
import threading  #スレッド
import psutil  #プロセス取得

max_count = (60 * 60)

PROC_NAME = "thunderbird.exe"

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

        #プロセス監視
        for proc in psutil.process_iter():
            try:
                proc_str = proc.exe()
                proc_list = proc_str.split("\\")
                if proc_list[-1] == PROC_NAME:
                    print("----------------------------")
                    break
            except Exception as e:
                print(f"proc err: {str(e)}")


        time.sleep(1)  # 1s


def click_btn():
    print("on")


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
    label_top = tkinter.Label(frame_top, text="hoge", font=("system", "40", "bold"))
    label_top.grid(row=0, column=0, pady=10)

    #---------- Frame(BOTTOM) ----------
    #Button
    btn = tkinter.Button(frame_bottom, text="何もしません", font=("system", "10", "normal"),command=click_btn)
    btn.config(state=tkinter.DISABLED)
    btn.grid(row=0, column=0, padx=100, pady=20, ipadx=5, ipady=5)


    #タスク起動
    task_id = threading.Thread(target=monitor_task)
    task_id.daemon = True  #デーモン
    task_id.start()

    root.mainloop()

