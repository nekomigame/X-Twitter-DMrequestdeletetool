import pyautogui
from pyautogui import ImageNotFoundException
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

os.chdir(os.path.dirname(__file__))

def click_img(targetimage: str = "", **kwargs):
    if targetimage == "":
        raise TypeError("ファイルが選択されていません")
    # 可変長引数を代入
    offset_x = kwargs.pop('offset_x', 0)         # 画像認識した座標とクリック座標をx方向にオフセット
    offset_y = kwargs.pop('offset_y', 0)         # 画像認識した座標とクリック座標をy方向にオフセット
    click_lr = kwargs.pop('click_lr', 'left')    # 左クリックor右クリック
    gray_scale = kwargs.pop('gray_scale', True)  # 画像認識時のグレースケールONOFF
    confidence = kwargs.pop('confidence', 0.8)   # 画像認識時の判定度合い
    # 画像の座標を代入
    x, y = pyautogui.locateCenterOnScreen(targetimage,
                                          grayscale=gray_scale,
                                          confidence=confidence)  # type: ignore
    # 座標をクリック
    pyautogui.click(x + offset_x, y + offset_y, button=click_lr)
    return x, y

def DMdelete():
    global combobox
    screenmode = combobox.get()
    if screenmode == "":
        messagebox.showerror("エラー","画面モードが選択されていません")
        return
    while True:
        try:
            click_img(rf"./img/{screenmode}_batu.jpg")
            time.sleep(0.2)
            click_img(rf"./img/{screenmode}_delete.jpg")
        except ImageNotFoundException:
            messagebox.showerror("ImageNotFoundException","指定された画像が見つからないため処理を停止しました")
            return
        except Exception as e:
            messagebox.showerror("予期せぬエラー",str(e))
            return

if __name__ == "__main__":

    # --- メインウィンドウの作成 ---
    root = tk.Tk()

    # --- ウィンドウの基本的な設定 ---
    # タイトルバーのテキストを設定
    root.title("X(Twitter)DMリクエスト自動削除")

    # ウィンドウの初期サイズを設定 (幅x高さ)
    root.geometry("300x120")

    # ウィンドウのリサイズを禁止 (オプション)
    root.resizable(False, False) # (幅方向, 高さ方向)

    XscreenmodeLabel = tk.Label(root,text="X(Twitter)の画面モードを選んでください")
    XscreenmodeLabel.place(x=0,y=0)

    Xscreenmode = ("default","darkblue","black")
    combobox = ttk.Combobox(root,values=Xscreenmode)
    combobox.place(x=0,y=30)

    button = ttk.Button(root, text="削除開始", command=DMdelete)
    button.place(x=0,y=70) # 上下に10ピクセルのパディングを追加して配置

    # --- イベントループの開始 ---
    # この行がないとウィンドウが表示されません
    root.mainloop()
