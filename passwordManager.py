'''
This is a password manager that stores your password and uses a master password to encrypt and decrypt the given password.
The master password you choose will be used to encrypt your password so choose it clearfully.
In order to view your password you need the master password. 
If the master password is not correct then still the program runs but you will get gibberish letters.
I have used cryptography library to encrypt and decrypt the password
'''

import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

saved='password.json'

def loadData(filepath):
    try:
        with open(filepath, 'r') as f:
            data=json.load(f)
            return(data)
    except:
        return {}

def view(filepath, data, fer):
    with open(filepath, 'r') as f:
        website=input("Enter the website name: ").rstrip()
        if website in data.keys():
            username, password=data[website].split('|')
            try:
                print("Username: ",username, " | Password: ",fer.decrypt(password.encode()).decode())
            except:
                print("Username: ",username, " | Password: ",password)
        else:
            print("You havent saved password for this website.")

def add(filepath, data, fer):
    website=input("Enter the website of which you want to save password of: ").rstrip()
    if website not in data.keys():
        username=input('Enter the username: ').rstrip()
        password=input('Enter the password: ')
        content=str(username)+'|'+fer.encrypt(password.encode()).decode()
        data[website]=content
        with open(filepath, 'w') as f:
            json.dump(data, f)
    else:
        print("You have already saved password of this website.")

def list_password(data,fer):
    if data=={}:
        print("You havenot saved any password yet")
    else:  
        try:
            for key, value in data.items():
                username, password=value.split('|')
                password=fer.decrypt(password.encode()).decode()
                print(key,":",username," | ",password)
        except:
            [print(key,':',value) for key, value in data.items()]

def about():
    print('''
This is a password manager that stores your password and uses a master password to encrypt and decrypt the given password.
The master password you choose will be used to encrypt your password so choose it clearfully.
In order to view your password you need the master password. 
If the master password is not correct then still the program runs but you will get gibberish letters.
''')

def manager(fer):
    print('''Following are the commands: (Press one of the below)
    view: If you want to view a password.
    add: If you want to add a new password.
    list: If you want to see all the passwords.
    help: To help.
    q: To quit''')

    while True:
        mode=input("Enter your choice: ").lower()
        data=loadData(saved)
        if mode=='view':
            view(saved, data, fer)
        elif mode=='add':
           add(saved, data, fer)
        elif mode=='list':
            list_password(data,fer)
        elif mode=='q':
            exit()
        elif mode=='help':
            about()
        else:
            print("Invalid command.")



while True:
    masterPassword=input("Enter the master password: ").rstrip()
    if masterPassword=='q':
        exit()
    confirmPassword=input("Confirm the password: ").rstrip()
    if masterPassword==confirmPassword:
        mysalt=b'\x80p\xabg\x13\xf9h\xad\x94\x1e\x05\xea0\xe5\xa6\xed'

        kdf= PBKDF2HMAC (
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend())

        key=base64.urlsafe_b64encode(kdf.derive(masterPassword.encode()))
        fer=Fernet(key)
        manager(fer)
    else:
        print("Password doesnot matched. Re-enter the password or press q to quit.")