# -*- coding: utf-8 -*-

import my_module.module as mod
import tkinter as tk

window = tk.Tk()
myApp = mod.MainWindow(window)
myApp.set_icon("icon.ico")

if not mod.is_gs_installed():
    myApp.window.withdraw()
    myApp.display_gs_not_found_error()

myApp.display_title()

ABS_PATH_CONVERT = mod.get_abs_path_to_convert_exe()

if ABS_PATH_CONVERT == None:
    myApp.display_get_convert_manually()
else:
    myApp.set_abs_path_to_convert_exe(ABS_PATH_CONVERT)

myApp.display_pdf_selection()
myApp.display_options()
myApp.display_convertion_launcher()

window.mainloop()
