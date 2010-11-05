# Pucks Video Analyzer

## About

This was a class project I had to make a while back.  It analyzes recorded video of an air-hockey table that has been moded into a lab to demonstrate collisions between particles in the atmosphere.  The program analyzes the video frames, determines the positions of the pucks relative to defined bins then outputs the resulting distribution.

## Disclaimer

The way this project was written is a little funky (mostly with where it expects binaries to be placed, naming conventions, etc.).  It had to meet very specific requirements that I did not come up with.

## Dependencies

This project was developed and tested on Windows.  However, adapting it for OSX/Linux should be trivial.  They reasons for why the program expects certain binaries to be where it does is due to the fact that I needed the ability to distribute the entire program as a single zipped file that could be copy/pasted and just work with as few other dependencies as possible.  The binary depepdency checking is contained within the **check_deps** method in the *go.py* file, feel free to comment out its contents.

* Place the *Gnuplot* binary for Windows (wgnuplot.exe & all of its friends) into *bin/gnuplot*
* Place the Windows binary for *mencoder* (along with its dependencies) in *bin/mencoder*

The program was designed to launch the installers of *numpy* and *Python Imaging Library* if they were not already installed.  Don't bother with this, jjust make sure that these packages are installed.


### *more to come...*
