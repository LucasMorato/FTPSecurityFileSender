# IMPORTANT! All files/folders must be in the same location as the script
# IMPORTANT 2! All folders must exist on the server

#connect using TLS  1.2 version
from ftplib import FTP_TLS
import ssl
import base64
import os

#insert output colored (green for success | red for fail)
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def connect():
    FTP_IP = '187.45.242.111' ####### INSERT FTP HOST IP ADDRESS
    USERNAME = "user" ####### INSERT USERNAME HERE
    PASSWORD = 'Sk9ITkRPRTEyMw=='  ####### INSERT A BASE64 PASSWORD HERE (use https://www.base64encode.org/enc/pass/)
    PORT = 21 ####### CHANGE PORT IF YOU NEED (DEFAULT IS 21)

    # password encrypted
    base64.b64decode(PASSWORD)
    code_string = base64.b64decode(PASSWORD)
    passwd = code_string.decode('utf-8')

    ftp = FTP_TLS()
    ftp.ssl_version = ssl.PROTOCOL_TLSv1_2
    ftp.debugging = 0
    ftp.connect(FTP_IP, PORT)
    ftp.login(USERNAME, passwd)
    return ftp

ftp = connect()
ftp.encoding = "utf-8"

def sendFiles():
    ########### edit here the strings to the files names
    file1 = "file1.txt"
    file2 = "file2.txt"
    file3 = "index.html"
    folder1 = "folder1"

    sentOK = True

    ########### send file1
    try:
        ftp.cwd('/path') ########### EDIT PATH HERE
    except:
        print(colored(255, 0, 0, f"Folder not found! \n"))
        sentOK = False
    try:
        with open(file1, "rb") as file:
            ftp.storbinary(f"STOR {file1}", file)
            print(colored(0, 255, 0, f"{file1} sent successfully!"))
    except:
        print(colored(255, 0, 0, f"ERROR !!!!!!!! {file1} cannot be uploaded!!"))
        sentOK = False

    ########### send file2
    try:
        ftp.cwd('/path')  ########### EDIT PATH HERE
    except:
        print(colored(255, 0, 0, f"Folder not found! \n"))
        sentOK = False
    try:
        with open(file2, "rb") as file:
            ftp.storbinary(f"STOR {file2}", file)
            print(colored(0, 255, 0, f"{file2} sent successfully!"))
    except:
        print(colored(255, 0, 0, f"ERROR !!!!!!!! {file2} cannot be uploaded!!"))
        sentOK = False

    ########### send file3
    try:
        ftp.cwd('/path/dir')  ########### EDIT PATH HERE
    except:
        print(colored(255, 0, 0, f"Folder not found! \n"))
        sentOK = False
    try:
        with open(file3, "rb") as file:
            ftp.storbinary(f"STOR {file3}", file)
            print(colored(0, 255, 0, f"{file3} sent successfully!"))
    except:
        print(colored(255, 0, 0, f"ERROR !!!!!!!! {file3} cannot be uploaded!!"))
        sentOK = False

    # send a entire folder # IMPORTANT: CANNOT ALREADY HAVE IN THE SERVER
    try:
        ftp.mkd(f"/path/dir/{folder1}") ########### EDIT PATH HERE
        ftp.cwd(f'/path/dir/{folder1}') ########### EDIT PATH HERE

        for root, dirs, files in os.walk(folder1, topdown=True):
            relative = root[len(folder1):].lstrip(os.sep)
            for d in dirs:
                ftp.mkd(os.path.join(relative, d))

            for f in files:
                filePath = os.path.join(folder1, relative, f)
                ftp.cwd(relative)
                with open(filePath, 'rb') as fileObj:
                    ftp.storbinary('STOR ' + f, fileObj)
                    
                ftp.cwd(f"/path/dir/{folder1}") ########### EDIT PATH HERE
                
        print(colored(0, 255, 0, f"Folder {folder1} sent successfully!"))
    except:
        print(colored(255, 0, 0, f"Could not send folder!"))
        sentOK = False

    return True

if sendFiles():
    print("\nFiles uploaded successfully!")
else:
    print("\nCould not upload all files!")

ftp.quit()
