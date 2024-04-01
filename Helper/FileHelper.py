from os import path, mkdir, remove, listdir,rmdir
from CertGenerate import generateCert


def checkCert():
    if path.exists("cert"):
        file = listdir("cert")
        if "privatekey.pem" in file and "cert.pem" in file:
            return
        print("Cert folder exists but not all files are present. Regenerating...")
        print("Removing old files...")
        for i in file:
            print(f"Removing {i}")
            remove(f"cert/{i}")
        rmdir("cert")
    mkdir("cert")
    generateCert()
    print("Certificate generated successfully.")

def checkdir():
    if not path.exists("ota"):
        mkdir("ota")
