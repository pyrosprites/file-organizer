![image](https://github.com/pyrosprites/file-organizer/assets/90645120/5b0fc5f0-aa3b-48e8-bb87-74217617a3c3)
#

Currently only working for **windows**, this is my first attempt to create a finished project in python, so if you discover any issues besides the ones already mentioned or perhaps an oversight in the way I have constructed my code, please feel free to make any advancing changes.

# Take a look at these
[Installation](#installation)
[Known Issues](#issues-found-so-far)

### Issues found so far:
- [ ] Minor issue catching temp files when processing downloads

### Installation:
My current setup works with a bat script in my startup folder to run this python project.

Where do we find this folder? Press `Win` + `R`, this will open a window where you
will copy and paste this directory `C:\Users\(your-name)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`.

There you will create a file called `startup.bat`, the name doesn't matter only the contents that follow.
```bat
@echo off
start "WhatEverTitleYouWant" "C:\Python311\Projects\organiser\main.pyw"
```
The directory in the second paramater is there for you to provide where you wish to have this project be. I chose my root python directory to get rid of my own stress >.> but you can do what you want.

From here you must have setup the startup and where you want the project to be so let's continue, now let's make sure it works. Restart your device and when you boot up again you should see your files already organized, if not then you must simply move a file to the Downloads folder and you should see it work.


Otherwise, please create an issue and elaborate on your situation or how the process can be improved.