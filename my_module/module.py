# -*- coding: utf-8 -*-

from webbrowser import open_new
from tkinter import filedialog
import tkinter as tk
import os
import sys
import base64
import shutil

def display_error_window(error_name, msg):
    error_window = tk.Tk()
    error_window.title(error_name)
    permission_error_frame = tk.Frame(error_window)
    tk.Label(
        permission_error_frame,
        text=msg
    ).pack(padx=5, pady=10, side=tk.TOP)
    tk.Button(
        permission_error_frame,
        text="OK",
        command=lambda: error_window.destroy()
    ).pack(side=tk.TOP)
    permission_error_frame.pack(padx=15, pady=10)


def center_window(win):
    win.withdraw()
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_reqwidth()) / 2
    y = (win.winfo_screenheight() - win.winfo_reqheight()) / 2
    win.geometry("+%d+%d" % (x, y))
    win.deiconify()


def find(name, path):
    """ Search a file and return the first match.
    
    :name: 'example.txt'
    :path: the path to start looking for the file
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def is_gs_installed():
    gs_default_inst_folder = 'C:/Program Files/gs'
    if os.path.isdir(gs_default_inst_folder):
        if find('gswin64c.exe', gs_default_inst_folder) != None:
            return True
        if find('gswin32c.exe', gs_default_inst_folder) != None:
            return True
    else:
        return False


def get_abs_path_to_convert_exe():
    """ Get from the PATH variable the abs path of the 'convert.exe' file in the
    ImageMagick installation folder. Return the abs path if found, return False if not.

    """
    listPATH = os.environ['PATH'].split(';')
    for path in listPATH:
        if 'ImageMagick' in path:
            path_convert_exe = path + '/convert.exe'
            return path_convert_exe
    return None


def get_dir_and_name(abs_path_pdf):
    """ Return the abs path of pdf directory AND the name of the PDF (without .pdf).
    Example of returned dir path: C:/this/is/an/abs/path

    """
    if not abs_path_pdf == '':
        abs_path_dir = abs_path_pdf[:-4]  # remove '.pdf' extension
        name = ''
        while abs_path_dir[-1] != '/':
            name = abs_path_dir[-1] + name
            abs_path_dir = abs_path_dir[:-1]
        if not abs_path_dir[-2:] == ':/':
            abs_path_dir = abs_path_dir[:-1]
        return abs_path_dir, name
    else:
        return ''


def browse_in_explorer(filetype):
    """ Return the abs path of the selected file.

    :filetype: '.exe', '.pdf', etc...
    """
    abs_path = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select file",
        filetypes = ((filetype[1:] + " files", "*"+filetype),("all files","*.*"))
    )
    return abs_path


def is_pdf(path_to_file):
    if path_to_file[-4:] == '.pdf':
        return True
    return False


def replace_char_in_path(abs_path_to_file, old_char, new_char):
    """ Replace all old_char characters in the abs path by a new_char. 
    Return the new abs path of the PDF file.

    """
    pdf_dir, pdf_name = get_dir_and_name(abs_path_to_file)

    # for the directory name and all parent directories.
    if old_char in pdf_dir:
        splitted_path = pdf_dir.split('/')

        renamed_path = splitted_path[0]
        tmp_new_path = splitted_path[0]

        for i in range(1, len(splitted_path), 1):
            subdir = splitted_path[i]

            if old_char in subdir:
                splitted_subdir = subdir.split(old_char)
                renamed_subdir = ''
                for element in splitted_subdir:
                    renamed_subdir += element + new_char
                renamed_subdir = renamed_subdir[:-1]

                renamed_path += '/' + renamed_subdir
                tmp_new_path += '/' + splitted_path[i]
                os.rename(tmp_new_path, renamed_path)
                tmp_new_path = renamed_path
            else:
                renamed_path += '/' + splitted_path[i]
                tmp_new_path += '/' + splitted_path[i]

        pdf_dir = renamed_path
        new_path = pdf_dir + '/' + pdf_name + '.pdf'

    # (then) rename the file
    if old_char in pdf_name:
        splitted_name = pdf_name.split(old_char)
        new_name = ''
        for i in splitted_name:
            new_name += i + new_char
        new_name = new_name[:-1]

        if pdf_dir[-2:] == ':/':
            old_path = pdf_dir + pdf_name + '.pdf'
            new_path = pdf_dir + new_name + '.pdf'
            os.rename(old_path, new_path)
        else:
            old_path = pdf_dir + '/' + pdf_name + '.pdf'
            new_path = pdf_dir + '/' + new_name + '.pdf'
            os.rename(old_path, new_path)
    
    return new_path


def create_output_dir(abs_path_pdf):
    """ Create the output directory and return it as a string. """

    pdf_dir, pdf_name = get_dir_and_name(abs_path_pdf)

    if pdf_dir[-2:] == ':/':
        output_dir = pdf_dir + pdf_name + "_converted_for_StylusLab"
    else:
        output_dir = pdf_dir + '/' + pdf_name + "_converted_for_StylusLab"
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        shutil.rmtree(output_dir, ignore_errors=True)
        try:
            os.mkdir(output_dir)
        except PermissionError:
            display_error_window("Access denied", "Access denied. Please try again.")
            return "Failed"
    return output_dir


def conversion(abs_path_pdf, abs_path_convert_exe, density, int_transparent_bg):
  
    pdf_name = get_dir_and_name(abs_path_pdf)[1]
   
    abs_path_output_dir = create_output_dir(abs_path_pdf)
    if abs_path_output_dir == "Failed":
        return "Retry"
    
    # Conversion PDF --> JPG
    if abs_path_convert_exe == None or abs_path_convert_exe[-11:] != 'convert.exe':
        print("The path to 'convert.exe' is wrong.")
        return "Failed"
    
    print("Convert PDF to images - may take a while...")
    density_option = ' -density '+ density + ' '
    if int_transparent_bg == 1:
        transparency_option = ' -background white -alpha remove -strip '
    else:
        transparency_option = ''
    
    print_version_cmd = abs_path_convert_exe + ' -version'
    conversion_cmd = abs_path_convert_exe + ' -verbose ' + \
        density_option + transparency_option + \
        ' ' + abs_path_pdf + ' ' + abs_path_output_dir + '/' + pdf_name + '.jpg'
    
    os.system(print_version_cmd + ' && ' + conversion_cmd)

    # Getting the number of pages
    list_img = [name for name in os.listdir(abs_path_output_dir)]
    number_of_pages = len(list_img)
    print("Number of pages : ", number_of_pages)

    # Conversion JPG --> SVG and creation of the body of the HTML file
    SVG_START = '''<svg width='1101px' height='1976px' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
    <defs> <style type='text/css'><![CDATA[ 
    path { stroke-linecap: round; stroke-linejoin: round; }
    .ruleline { shape-rendering: crispEdges; }
    ]]></style> </defs>
    <g id='page_1' width='1101.000' height='1660.000' xruling='0.000' yruling='40.000' marginLeft='100.000' papercolor='#FFFFFF' rulecolor='#FF0000FF'>
    '''
    SVG_END = '''
    </g>
    </svg>
    '''

    body_string = ''
    page_number = 0
    for img in list_img:
        # JPG -> SVG
        page_number += 1
        print("Encoding Image : " + img)
        path_to_img = abs_path_output_dir + '/' + img
        jpg_file = open(path_to_img, 'rb')
        base64data = base64.b64encode(jpg_file.read())
        base64string = '<image xlink:href="data:image/jpg;base64,{0}" width="1101" '\
            'height="1660" x="0" y="0" />'.format(str(base64data)[2:-1])
        svg_string = SVG_START + base64string + SVG_END

        page_name = pdf_name + '_page{:03}.svg'.format(page_number)
        with open(abs_path_output_dir + '/' + page_name, 'w') as sv:
            sv.write(svg_string)
        
        # Generating the thumbail
        if page_number == 1:
            print("Generating thumbail")
            thumbail_data_uri = base64data.decode("ascii")

        del jpg_file
        os.remove(path_to_img)

        # add svg source to the body of the html
        body_string += '''<object data="{0}" type="image/svg+xml" width="1101" height="1660"></object>\n'''.format(page_name)

    # Generating the HTML file
    html_string = '''<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>{}</title>
    <script type="text/writeconfig">
    <int name="pageNum" value="0" />
    <float name="xOffset" value="-390.196" />
    <float name="yOffset" value="-73.5294" />
    </script>
    </head>
    <body>

    <img id='thumbnail' style='display:none;' src='data:image/jpg;base64,{}'/>
    {}
    </body>
    </html>'''.format(pdf_name, thumbail_data_uri, body_string)

    print("Saving HMTL file")
    with open(abs_path_output_dir + '/' + pdf_name +'.html', 'w') as ht:
        ht.write(html_string)
    
    return abs_path_output_dir


def callback(url):
    open_new(url)


class MainWindow:
    
    def __init__(self, window):
        self.window = window
        self.window.title("Convert PDF for StylusLab")
        
        self.frPathConvertNotFound = tk.Frame(self.window)
        self.bSelectConvertExe = tk.Button(self.frPathConvertNotFound)
        self.lAbsPathConvertExe = tk.Label(self.frPathConvertNotFound)

        self.frSelectPDF = tk.Frame(self.window)

        self.frChoicePDF = tk.Frame(self.frSelectPDF)
        self.bChoosePDF = tk.Button(self.frChoicePDF)
        self.lAbsPathPDF = tk.Label(self.frChoicePDF)
        self.abs_path_pdf = ""

        self.frWhitespaceError = tk.Frame(self.frSelectPDF)
        self.lWhpaceErrorMsg = tk.Label(self.frWhitespaceError)
        self.bChooseAnotherPDF = tk.Button(self.frWhitespaceError)
        self.bRename = tk.Button(self.frWhitespaceError)

        self.frOptions = tk.Frame(self.window)

        self.frDensityOption = tk.Frame(self.frOptions)
        self.frDensity = tk.Frame(self.frDensityOption)
        self.eDensityValue = tk.Entry(self.frDensity)
        self.frDensityDescription = tk.Frame(self.frDensityOption)

        self.frTransparencyOption = tk.Frame(self.frOptions)
        self.PDFHasTranspBackground = tk.IntVar(self.frTransparencyOption)
        self.cbBgIsTransparent = tk.Checkbutton(self.frTransparencyOption)

        self.frConversionLauncher = tk.Frame(self.window)
        self.bLaunch = tk.Button(self.frConversionLauncher)


    def set_icon(self, filename):
        self.window.iconbitmap(filename)


    def display_title(self):
        tk.Label(
            self.window,
            text="Import PDF into Stylus Lab 'Write'",
            font=('Helvetica', 18, 'bold')
            ).pack()
        url_github_repo = "https://github.com/hello-d4n/import_PDF_into_StylusLab_Write"
        link = tk.Label(
            self.window,
            text = "https://github.com/hello-d4n/import_PDF_into_StylusLab_Write",
            font=('Helvetica', 8, 'italic'),
            cursor="hand2"
        )
        link.pack()
        link.bind("<Button-1>", lambda e: open_new(url_github_repo))
    

    def display_gs_not_found_error(self):
        frGsNotFound = tk.Frame(highlightbackground="black", highlightthickness=1)
        tk.Label(
            frGsNotFound,
            text="It seems that GhostScript is not installed on your computer.\n" \
                "Please make sure to install GhostScript. You can download it here :",
            font=('Helvetica', 10, 'bold')
        ).pack()
        lDownloadLink = tk.Label(
            frGsNotFound,
            text = "https://www.ghostscript.com/download/gsdnld.html (choose AGP Licence)",
            font=('Helvetica', 9, 'italic'),
            foreground="blue",
            cursor="hand2"
        )
        lDownloadLink.pack(pady=5)
        link = "https://www.ghostscript.com/download/gsdnld.html"
        lDownloadLink.bind("<Button-1>", lambda e: open_new(link))
        tk.Label(
            frGsNotFound,
            text="If GhostScript is already installed on your computer, ignore "\
                "this message.",
            font=('Helvetica', 10, 'bold')
        ).pack()
        frGsNotFound.pack(pady=20)
        
        
    def set_abs_path_to_convert_exe(self, abs_path_to_convert_exe):
        """ Method only used if convert.exe is in PATH variable. """
        self.lAbsPathConvertExe.configure(text=abs_path_to_convert_exe)


    def when_bSelectConvertExe_clicked(self):
            self.lAbsPathConvertExe.configure(text=browse_in_explorer('.exe'))


    def display_get_convert_manually(self):
        """ Display a label and a button to select 'convert.exe' abs path in 
        explorer.
        
        """
        tk.Label(
            self.frPathConvertNotFound,
            text="'convert.exe' was not found in PATH variable.\n"\
                "Please make sure ImageMagick is installed.\nYou can use the download link below :",
            font=('Helvetica', 10, 'bold')
        ).pack()
        lDownloadLink = tk.Label(
            self.frPathConvertNotFound,
            text = "ftp://ftp.imagemagick.org/pub/ImageMagick/binaries\n"\
                "(if you dont not which file to download, try one that ends by Q16-x86-static.exe)",
            font=('Helvetica', 9, 'italic'),
            foreground="blue",
            cursor="hand2"
        )
        lDownloadLink.pack(pady=5)
        link = "ftp://ftp.imagemagick.org/pub/ImageMagick/binaries"
        lDownloadLink.bind("<Button-1>", lambda e: open_new(link))
        tk.Label(
            self.frPathConvertNotFound,
            text="If ImageMagick is already installed or if you use the Portable version,\n"\
                "then please select the file :",
            font=('Helvetica', 10, 'bold')
        ).pack()
        self.bSelectConvertExe.configure(
            text="Select 'convert.exe'",
            command=self.when_bSelectConvertExe_clicked
        )
        self.bSelectConvertExe.pack(padx=5)
        self.lAbsPathConvertExe.configure(text="")
        self.lAbsPathConvertExe.pack(padx=5)

        self.frPathConvertNotFound.configure(highlightbackground="black", highlightthickness=1)
        self.frPathConvertNotFound.pack(padx=10, pady=10)


    def get_AbsPathConvertExe(self):
        return self.lAbsPathConvertExe.cget("text")


    def when_bChooseAnotherPDF_clicked(self):
        self.frWhitespaceError.pack_forget()
        self.lAbsPathPDF.configure(text="")
        self.bChoosePDF.configure(state="normal")
        self.bLaunch.pack(pady=10)


    def when_bRename_clicked(self, choosen_path):
        try:
            renamed_path = replace_char_in_path(choosen_path, ' ', '_')
        except PermissionError:
            error_msg = "It seems that the programm does not have permission to rename\n" \
                "the name or the parent directory(ies) of the PDF file. \n\n" \
                "Try to remove from the filename (or folder name) the following characters :\n" \
                " '%'  '@'  '~'  ':'  '<'  '>'  '?'  '!'  '*'  '|'\t and retry.\n\n" \
                "If it still does not work, then pleace retry with Administrator Privileges\n" \
                "(right click on the exe file and click 'Run as administrator')."
            display_error_window("Permission Error", error_msg)
        if 'renamed_path' in locals():
            self.frWhitespaceError.pack_forget()
            self.abs_path_pdf = renamed_path
            self.lAbsPathPDF.configure(text=renamed_path, foreground="green")
            self.bChoosePDF.configure(state="normal")
            self.bLaunch.configure(state="normal")
            self.bLaunch.pack(pady=10)


    def when_bChoosePDF_clicked(self):
        self.lAbsPathPDF.configure(text=browse_in_explorer('.pdf'))
        choosen_path = self.lAbsPathPDF.cget("text")

        if is_pdf(choosen_path):
            whitespace = ' '
            if whitespace in choosen_path:
                self.lAbsPathPDF.configure(foreground="red4")
                self.bLaunch.configure(state="disabled")
                self.bChoosePDF.configure(state="disabled")

                self.lWhpaceErrorMsg.configure(
                    text="Whitespace character(s) have benn detected in the filename or path of the PDF.\n" \
                        "To work properly, this programm needs that the PDF filename or path does not include \n" \
                        "whitespace character(s). To solve this problem, the file must be renamed by \n" \
                        "replacing each whitespace character by an underscore symbol ( _ ). \n" \
                        "What would you like to do ?",
                    foreground="blue"
                )
                self.lWhpaceErrorMsg.pack()

                self.bRename.configure(
                    text="Rename file",
                    foreground="blue",
                    command=lambda: self.when_bRename_clicked(choosen_path)
                    )
                self.bRename.pack(side=tk.TOP)

                self.bChooseAnotherPDF.configure(
                    text="Choose Another PDF",
                    foreground="blue",
                    command=self.when_bChooseAnotherPDF_clicked
                    )
                self.bChooseAnotherPDF.pack(side=tk.TOP)

                self.frWhitespaceError.pack(padx=10, pady=10)
                self.frSelectPDF.pack()


            else:
                self.lAbsPathPDF.configure(foreground="green4")
                self.bLaunch.configure(state="normal")
        else:
            print("Please choose a PDF file")


    def display_pdf_selection(self):
        tk.Label(
            text="Please select the PDF file you want to import in Stylus Lab 'Write' "
        ).pack(side=tk.TOP)

        self.bChoosePDF.configure(
            text="Choose PDF",
            command=self.when_bChoosePDF_clicked
        )
        self.bChoosePDF.pack(padx=5, pady=5, side=tk.LEFT)

        self.lAbsPathPDF.configure(text="")
        self.lAbsPathPDF.pack(padx=5, pady=5, side=tk.RIGHT)

        self.frChoicePDF.pack()
        self.frSelectPDF.pack(padx=10)


    def display_options(self):
        
        self.cbBgIsTransparent.configure(
            text="PDF has transparent background (check this box if the output document "\
                "has a black bakcground)",
            variable=self.PDFHasTranspBackground,
            offvalue=0,
            onvalue=1
            )
        self.cbBgIsTransparent.pack(padx=10, side=tk.TOP)
        
        self.frTransparencyOption.pack(side=tk.TOP)
        tk.Label(
            self.frDensity,
            text="ImageMagick Density"
        ).pack(padx=10, pady=10, side=tk.LEFT)
        self.eDensityValue.insert(0, str(200))
        self.eDensityValue.configure(width=8)
        self.eDensityValue.pack(padx=5, pady=3, side=tk.LEFT)
        self.frDensity.pack(side=tk.TOP)
        tk.Label(
            self.frDensityDescription,
            text="Density is usually an integer between 100 and 500. " \
                "To change the text sharpening, try modifying the density value."
        ).pack(padx=10, pady=4)
        link = tk.Label(
            self.frDensityDescription,
            text="More info on : https://imagemagick.org/script/command-line-options.php#density.",
            cursor="hand2"
        )
        link.pack(padx=10, pady=4)
        link.bind("<Button-1>", lambda e: callback("https://imagemagick.org/script/command-line-options.php#density"))
        self.frDensityDescription.pack(side=tk.TOP)

        self.frDensityOption.pack(side=tk.TOP)

        self.frOptions.pack()


    def when_bConvertAnotherPDF_clicked(self, frame_after_conversion):
        frame_after_conversion.pack_forget()
        self.bChoosePDF.configure(state="normal")
        self.lAbsPathPDF.configure(text="")
        self.eDensityValue.configure(state="normal")
        self.bLaunch.pack(pady=10)


    def when_bLaunch_clicked(self):
        self.bChoosePDF.configure(state="disabled")
        self.bLaunch.configure(state="disabled")
        self.eDensityValue.configure(state="disabled")

        abs_path_to_pdf = self.lAbsPathPDF.cget("text")
        abs_path_to_convert = self.lAbsPathConvertExe.cget("text")
        density = self.eDensityValue.get()
        bool_transparent_bg = self.PDFHasTranspBackground.get()
        print(bool_transparent_bg)

        output_dir = conversion(abs_path_to_pdf, abs_path_to_convert, density, bool_transparent_bg)
        
        frAfterConversion = tk.Frame(self.window)

        if output_dir == "Failed":
            tk.Label(
                frAfterConversion,
                text="Conversion FAILED :( ",
                background="gray80"
                ).pack(pady=3)
            tk.Button(
                frAfterConversion,
                text="Convert an other PDF or Retry",
                command=lambda: self.when_bConvertAnotherPDF_clicked(frAfterConversion)
                ).pack()
        elif output_dir == "Retry":
            self.bChoosePDF.configure(state="normal")
            self.bLaunch.configure(state="normal")
            self.eDensityValue.configure(state="normal")
        else:
            tk.Label(
                frAfterConversion,
                text="PDF converted SUCCESSFULY. Converted document is located at :\n" + output_dir,
                background="gray80"
                ).pack(pady=3)
            tk.Button(
                frAfterConversion,
                text="Open folder in File Explorer",
                command=lambda: os.startfile(output_dir)
                ).pack()
            tk.Button(
                frAfterConversion,
                text="Convert an other PDF",
                command=lambda: self.when_bConvertAnotherPDF_clicked(frAfterConversion)
                ).pack()
        frAfterConversion.pack(padx=10, pady=5)

    def display_conversion_launcher(self):
        tk.Label(
            self.frConversionLauncher,
            text="\nConversion may take some time if the PDF have a lot of pages",
            font=('helvetica 8 italic')
            ).pack()
        self.bLaunch.configure(
            text="Launch conversion",
            command=self.when_bLaunch_clicked,
            state="disabled"
            )
        self.bLaunch.pack(pady=10)
        self.frConversionLauncher.pack(pady=5)
