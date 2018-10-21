from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:/KiwoomFlash3/bin/nkministarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

btn_id_login = dlg.Button5
if btn_id_login.ControlID() == 163:
    # ID 로그인 탭 선택
    btn_id_login.Click()

pass_ctrl = dlg.Edit1
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('hkpking')

cert_ctrl = dlg.Edit2
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('hkp1212')

btn_ctrl = dlg.Button0
btn_ctrl.Click()

# 로그인 안내 경고창 [예] 클릭
title2 = "번개3"
dlg2 = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title2))
btn_y = dlg2.Button0
btn_y.Click()

time.sleep(30)
os.system("taskkill /im nkmini.exe")