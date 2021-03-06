# -*- coding: utf-8 -*-
from my_module.module import add_quotes, is_gs_installed, get_abs_path_to_convert_exe
import my_module.module as mod
import tkinter as tk

window = tk.Tk()
myApp = mod.MainWindow(window)
myApp.set_icon("icon.ico")

myApp.display_title()

if not is_gs_installed():
    myApp.display_gs_not_found_error()

ABS_PATH_CONVERT = get_abs_path_to_convert_exe()

if ABS_PATH_CONVERT == None:
    myApp.display_get_convert_manually()
else:
    if ' ' in ABS_PATH_CONVERT:
        ABS_PATH_CONVERT = add_quotes(ABS_PATH_CONVERT)
        ABS_PATH_CONVERT = mod.double_backslash(ABS_PATH_CONVERT)
    myApp.set_abs_path_to_convert_exe(ABS_PATH_CONVERT)

myApp.display_pdf_selection()
myApp.display_options()
myApp.display_conversion_launcher()

window.mainloop()
