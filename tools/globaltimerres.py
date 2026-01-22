import winreg
def setGTRR():
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel")
        
        winreg.SetValueEx(key,
            "GlobalTimerResolutionRequests",0,
            winreg.REG_DWORD,1)

        winreg.CloseKey(key)
        print("Added global timer res registry")
    except PermissionError:
        print("global timer res script not running as admin")
    except Exception as e:
        print("unexpected error:",e)

if __name__ == "__main__":
    setGTRR()
