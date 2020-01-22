import sys, os, platform

def LOADPATH():

    computer = platform.architecture()

    if computer[0] == '32bit':
        try:
            sys.path.append(os.environ["PROGRAMFILES"]+"/FreeCAD 0.18/bin")
        except Exception("Misconfigured, Not Installed, or not FreeCAD 0.18"):
            print("Path not found")
            exit(-1)
    elif computer[0] == '64bit':
        try:
            sys.path.append(os.environ["ProgramW6432"]+"/FreeCAD 0.18/bin")
        except Exception("Misconfigured, Not Installed, or not FreeCAD 0.18"):
            print("Path not found")
            exit(-1)
    else:
        raise Exception("Unsupported")
        exit(-1)


if __name__ == "__main__":
    LOADPATH()
    import FreeCAD