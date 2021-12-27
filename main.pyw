"""MADE FOR WINDOWS_NT OS, PYTHON3 (PYW OPTIMIZED, NO __builtins__.print AND NOCONSOLE), FEEL FREE TO ADAPT TO LINUX OR MACOS"""

# /*Static imports, very important*/
import os
from sys import argv,path as selfPath,exit
from tkinter import messagebox,Tk,filedialog

# <--! accessibility voids -->
def findpypath():
    possible = []
    for i in selfPath:
        if "python" in i.split("\\")[-1].lower():
            possible.append(i)
    min = len(possible[0].split("\\"))
    for i in possible:
        print(len(i.split("\\")),"comparing to",min)
        if len(i.split("\\")) < min:
            min = len(i.split("\\"))
        else:
            pass
    for i in possible:
        if len(i.split("\\")) == min:
            return i+"\\python.exe"
    return "python"
def ShowDir(path):
    # Show work, made for NT Win, no unix support
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    path = os.path.normpath(path)
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
def GenEnv():
    # Generate environment for the script
    dt = datetime.datetime.now().strftime("Render(%Y-%m-%d-%H-%M-%S)")
    os.mkdir(dt) #Create the dir, each time is unique
    txt = ""
    for i in range(random.randint(5,20)):
        txt = txt + random.choice("1234567890ìqwertyuioasdfghjklzxcvbnm")
    return txt,dt

try:
    # /* Another import section with try */ -> some modules are not python stdlib, i recommend installing them!
    import cv2
    import numpy as np
    import random,datetime,subprocess
    from requests import get
    from threading import Thread
except ImportError:
    pypt = findpypath()
    os.system(f"{pypt} -m pip install opencv-python")
    os.system(f"{pypt} -m pip install requests")
    os.system(f"{pypt} -m pip install datetime")
    os.system(f"{pypt} -m pip install subprocess")
    os.system(f"{pypt} -m pip install threading")
    import cv2
    import numpy as np
    import random,datetime,subprocess
    from requests import get
    from threading import Thread
# Various declarations of vars etc...
root = Tk()
root.withdraw()
errors = False
times = 0 # referred to errors
succeded = 0 # start from zero

# <--! set path to read the file -->
if ".py" in argv[-1][-5:]:
    path_to_read = filedialog.askopenfilename(title="Insert txt file",parent=root)
else:
    path_to_read = argv[-1] # works with args as well!

# <--! script itself -->
if __name__ == "__main__":
    urls,count = open(path_to_read).read().splitlines(),1 # another declaration of main branch
    filebase,chrdir = GenEnv()
    for i in urls:
        try:
            if "http" in i[:5]:
                with open("temp.png","wb") as f:
                    f.write(get(i).content)
            else:
                with open("temp.png","wb") as f:
                        f.write(open(i,"rb").read())
            img = cv2.imread('temp.png')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1];mask = 255 - mask
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel);mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel);mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT);mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)
            result = img.copy()
            result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = mask
            cv2.imwrite(chrdir+'\\{}.png'.format(str(filebase)+str(count)), result)
            count = count + 1
        except Exception as e:
            # /* in case of exception, like permission denied etc... */
            messagebox.showerror(title="Error",message="An error occured while scanning line {}".format(urls.index(i)),parent=root)
            errors = True
            times = times + 1
    ShowDir(chrdir) # <--! Show work -->
    messagebox.showinfo(title="Success!",message="Removed bg from all images\nTotal: {}\nErrors:{} {} Times\nSucceded: {}".format(len(urls),errors,times,succeded),parent=root)
    try:
        os.remove("temp.png") # Clear temporary file!
    except Exception as e:
        pass
root.destroy() # Close root window and end the process
exit(0) # process.exe -> status:0, success! ( i guess -u- )