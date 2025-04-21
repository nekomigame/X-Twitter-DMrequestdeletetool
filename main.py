import pyautogui
from pyautogui import ImageNotFoundException
import ctypes
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
    try:
        x, y = pyautogui.locateCenterOnScreen(targetimage,
                                                grayscale=gray_scale,
                                                confidence=confidence)  # type: ignore
        # 座標をクリック
        pyautogui.click(x + offset_x, y + offset_y, button=click_lr)
        return x, y
    except ImageNotFoundException:
        raise
    except Exception as e:
        raise

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
    if os.name == 'nt':  # Windowsの場合のみ実行
        try:
            # DPI Awareness をPer-monitor high DPI awareに設定 (推奨)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                # Windows 8.1 以前の場合
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass # どちらのAPIも存在しない場合は何もしない

    # --- メインウィンドウの作成 ---
    root = tk.Tk()

    # --- ウィンドウの基本的な設定 ---
    # タイトルバーのテキストを設定
    root.title("X(Twitter)DMリクエスト自動削除")

    # ウィンドウの初期サイズを設定 (推奨しないが、初期配置の参考に)
    # root.geometry("1000x500")

    # ウィンドウのリサイズを禁止 (オプション)
    root.resizable(False, False) # (幅方向, 高さ方向)

    # --- ウィジェットの作成と配置 (packを使用) ---
    XscreenmodeLabel = tk.Label(root,text="X(Twitter)の画面モードを選んでください")
    XscreenmodeLabel.pack(pady=(10, 0), anchor=tk.W, padx=10) # 上に少しpadding

    Xscreenmode = ("default","darkblue","black")
    combobox = ttk.Combobox(root,values=Xscreenmode)
    combobox.pack(pady=5, anchor=tk.W, padx=10)

    button_frame = ttk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    button = ttk.Button(button_frame, text="削除開始", command=DMdelete)
    button.pack(side=tk.LEFT)

    # 詳細設定フレーム
    detail_frame = ttk.LabelFrame(root, text="詳細設定")
    detail_frame.pack(fill=tk.X, padx=10, pady=10)

    # offsetX
    offsetx_frame = ttk.Frame(detail_frame)
    offsetx_frame.pack(fill=tk.X, pady=5)
    offsetxLabel = tk.Label(offsetx_frame, text="クリックするX座標のオフセット(px)", width=30, anchor=tk.W)
    offsetxLabel.pack(side=tk.LEFT)
    offsetxEntry = tk.Entry(offsetx_frame, width=10)
    offsetxEntry.pack(side=tk.LEFT)
    offsetxEntry.insert(0, "0")

    # offsetY
    offsety_frame = ttk.Frame(detail_frame)
    offsety_frame.pack(fill=tk.X, pady=5)
    offsetyLabel = tk.Label(offsety_frame, text="クリックするY座標のオフセット(px)", width=30, anchor=tk.W)
    offsetyLabel.pack(side=tk.LEFT)
    offsetyEntry = tk.Entry(offsety_frame, width=10)
    offsetyEntry.pack(side=tk.LEFT)
    offsetyEntry.insert(0, "0")

    # Clicktype
    clicktype_frame = ttk.Frame(detail_frame)
    clicktype_frame.pack(fill=tk.X, pady=5)
    clicktypeLabel = tk.Label(clicktype_frame, text="左・右クリック選択", width=30, anchor=tk.W)
    clicktypeLabel.pack(side=tk.LEFT)
    clicktypeCombobox = ttk.Combobox(
        clicktype_frame, justify="center", values=("left", "right"), width=10)
    clicktypeCombobox.pack(side=tk.LEFT)
    clicktypeCombobox.insert(0, "left")

    # grayscale
    grayscale_frame = ttk.Frame(detail_frame)
    grayscale_frame.pack(fill=tk.X, pady=5)
    grayscaleLabel = tk.Label(grayscale_frame, text="画像認識時のグレースケールのON/OFF", width=30, anchor=tk.W)
    grayscaleLabel.pack(side=tk.LEFT)
    grayscaleCombobox = ttk.Combobox(grayscale_frame, justify="center", values=("ON", "OFF"), width=10)
    grayscaleCombobox.pack(side=tk.LEFT)
    grayscaleCombobox.insert(0, "ON")

    # Recognition accuracy
    acc_frame = ttk.Frame(detail_frame)
    acc_frame.pack(fill=tk.X, pady=5)
    accLabel = tk.Label(acc_frame, text="画像認識精度（Max:1,Min:0）", width=30, anchor=tk.W)
    accLabel.pack(side=tk.LEFT)
    accEntry = tk.Entry(acc_frame, width=10)
    accEntry.pack(side=tk.LEFT)
    accEntry.insert(0, "0.8")

    # --- イベントループの開始 ---
    # この行がないとウィンドウが表示されません
    root.mainloop()