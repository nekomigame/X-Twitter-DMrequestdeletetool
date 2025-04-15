import pyautogui
import os
import time

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

def main():
    while True:
        click_img(r"./img/batu.jpg")
        time.sleep(0.2)
        click_img(r"./img/delete.jpg")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)    