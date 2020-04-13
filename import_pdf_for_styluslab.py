import my_module.module as mod
import tkinter as tk
import os

ABS_PATH_CONVERT = mod.get_abs_path_to_convert_exe()
# print(os.path.dirname(os.path.realpath(__file__)))

window = tk.Tk()
myApp = mod.MainWindow(window)
myApp.set_title("Convert PDF for StylusLab")

if ABS_PATH_CONVERT == None:
    myApp.display_get_convert_manually()
    ABS_PATH_CONVERT = myApp.get_AbsPathConvertExe()
else:
    myApp.set_abs_path_to_convert_exe(ABS_PATH_CONVERT)

myApp.display_pdf_selection()
myApp.display_options()
myApp.display_convertion_launcher()

window.mainloop()