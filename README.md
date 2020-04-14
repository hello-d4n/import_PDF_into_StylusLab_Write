# import PDF into StylusLab 'Write'

[StylusLab Write](http://www.styluslabs.com/) is one of the best note-taking sofware  I've experienced, but it has one drawback : you can't import PDF documents. However, as it saves document in HTML and SVG files, it is possible to open a PDF document in StylusLab Write by converting it into a series of SVG images.

This program is for **Windows users only** and was written in Python 3. It is inspired from the script written by [sdfgeoff](https://github.com/sdfgeoff/stylus_labs_pdf_converter) for linux users and I've added features (such as a GUI).

## Demo :

[![Watch the video](https://i.imgur.com/HAOabaX.png)](https://vimeo.com/407703378)

## Requirements :

The 2 following softwares have to be installed on your computer :

* __ImageMagick__ : Download link : ftp://ftp.imagemagick.org/pub/ImageMagick/binaries

If you don't know which file to download, try one which ends by *Q16-x86-static.exe*. I used *ImageMagick-6.9.11-6-Q16-x86-static.exe* to make this program.

During the installation process, make sure to check "Add application directory to your system path" :

![alt text](https://i.imgur.com/SaDPh38.jpg)

* __GhostScript__ : Download link : [https://www.ghostscript.com/download/gsdnld.html](https://www.ghostscript.com/download/gsdnld.html) (AGPL Release)

