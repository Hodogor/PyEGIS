from pywinauto.application import Application
import pyautogui
import time

def main():
    start = time.time()
    app = Application(backend="uia").start('C:\RLoader\RLoader.exe')
    win = app['Загрузчик регистров']
    # Опишем окно, которое хотим найти в процессе Notepad.exe
    dlg_spec = app.window(title='Загрузчик регистров')
    # ждем пока окно реально появится
    actionable_dlg = dlg_spec.wait('visible')
    #actionable_dlg.minimize()
    tree = win["Регистр льготников"]
    print(tree.class_name)
    tree.double_click_input()
    #pyautogui.keyDown
    child = win["Региональный"]
    child.double_click_input()
    child = win["Передача направлений"]
    child.select()
    button = win["Старт"]
    button.click()
    win = app['ПС"Передача льготников"']
    dlg_spec = app.window(title='ПС"Передача льготников"')
    actionable_dlg = dlg_spec.wait('visible')
    lgota = win['начать передачу']
    lgota.click()

    print("Прошло времени:", time.time() - start)
    

if __name__ == "__main__":
    main()