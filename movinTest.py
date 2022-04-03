

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    import mouse
    import time 
    # Code of your program here
    time.sleep(3)
    mouse.move(525, 433, absolute=True, duration=0)
    mouse.click()
    print(mouse.version)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)