import sys
import pexpect
from gpiozero import Button
from signal import pause

running=0

button = Button(2)

def notPrinting(port):
    child.sendline('M27')
    a = child.expect(['Not SD printing', 'SD printing byte'])
    if a==0:
        return True
    elif a==1:
        return False
    else:
        print("Unknown Printer State")
        return False

def levelBed(port):
    if notPrinting(port):
        child.expect(port)
        child.sendline('G28')
        child.expect(port)
        child.sendline('G29')
        child.expect(port)
        child.sendline('disconnect')
    else:
        print(port + 'is printing')
        child.sendline('disconnect')

def bytesToStrings(list):
    convertList = []
    count=0
    for x in list:
        convertList.append(x.decode("utf-8"))
        count +=1
    return convertList

def autoLevel():
    if running==0:
        running=1
        child = pexpect.spawn('./Printrun/pronsole.py')
        child.logfile = sys.stdout.buffer
        child.expect('offline>')
        child.sendline('help connect')
        child.expect('Available ports: ')
        child.expect('\r\n')
        printers = child.before.split()
        printerString = bytesToStrings(printers)

        for x in printerString:
            child.expect('offline>')
            printerTitle = x.split('/')[-0]
            child.sendline('connect ' + x)
            i = child.expect(['Printer is now online\r\n', 'Could not connect'])
            if i==0:
                levelBed(printerTitle)
            else:
                print('Could not connect to printer')

        child.sendline('exit')
        running=0

button.when_pressed = autoLevel