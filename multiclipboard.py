from audioop import mul
import sys
import json
import clipboard

savedData='clipboard.json'

def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            data=json.load(f)
            return(data)
    except:
        return{}

if len(sys.argv)==2:
    command=sys.argv[1]
    data=load_data(savedData)

    if command=='save':
        key=input('Enter a key:')
        if key not in data:
            data[key]=clipboard.paste()
            save_data(savedData, data)
            print("Data saved!")
        else:
            print("Key already exist. Do you want to overwrite it? If yes press Y else press any letter:")
            decision=input()
            if decision=='Y':
                data[key]=clipboard.paste()
                save_data(savedData, data)
                print("Data saved!")
            else:
                exit()


    elif command=='load':
        if data=={}:
            print("list is empty. Save some data first.")
        else:
            key=input("Enter a key:")
            if key in data:
                clipboard.copy(data[key])
                print("Data copied!")
            else:
                print("Key is not available.")

    elif command=='list':
        print(data)
    
    elif command=='clear':
        save_data(savedData, {})

    else:
        print("Enter a valid command.")
    
else:
    print("Enter exactly one command.")
