import psutil
import git
import socket
import analytics
import sys
import csv

from time import sleep
from datetime import datetime, time
from json import dumps
from kafka import KafkaProducer
from random import randrange

print(sys.platform)

if sys.platform == "linux" or platform == "linux2":
    # linux
    git_dir = "/opt/say-that-i-am-up"
    token_file = "/opt/segment_token.txt"
elif sys.platform == "darwin":
    # OS X
    print("Not implemented. Exiting")
    sys.exit()
elif sys.platform == "win32":
    # Windows...
    git_dir = "C:\_programy\say-that-i-am-up"
    token_file = "C:\_programy\segment_token.txt"
else:
    print(sys.platform)
    print("Unknown platform. Exiting")
    sys.exit()

g = git.cmd.Git(git_dir)

hostname = socket.gethostname()

# get Segemnt writekey from the file

try:
    f = open(token_file, 'r')
except OSError:
    print("Could not open/read file:", token_file)
    sys.exit()
with f:
    reader = csv.reader(f)
    for read in reader:
        segment_write_key = ''.join(read)
    
print(f"segment_write_key: {segment_write_key}")
analytics.write_key = segment_write_key

def send_to_kafka(text):
    producer = KafkaProducer(bootstrap_servers=['192.168.1.104:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    
    send_to_kafka = {'send_time' : datetime.now().replace(microsecond=0).isoformat(), 'text' : str(text)}
    producer.send('activity_monitor', value=send_to_kafka)


def send_to_segment(content):

    send_this = {}
    send_this['name'] = hostname
    send_this['created_at'] = datetime.now()
    send_this['process'] = content
    analytics.track(str(hostname), 'active', send_this)


# from https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/    
def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects
def main():
    #print("*** Iterate over all running process and print process ID & Name ***")
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            #print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    #print('*** Create a list of all running processes ***')
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
       # Get process detail as dictionary
       #pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'cmdline'])
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'cmdline'])
       # Append dict of process detail in list
       listOfProcessNames.append(pInfoDict)
    # Iterate over the list of dictionary and print each elem
    for elem in listOfProcessNames:
        #print(elem)
        pass
    print('*** Top 5 process with highest memory usage ***')
    listOfRunningProcess = getListOfProcessSortedByMemory()

    list_for_kafka = []
    list_for_segment = []
    trash_processes = ["MsMpEng.exe","SearchUI.exe","Skype.exe","svchost.exe"]
    for elem in listOfRunningProcess[:5] :
        print(elem)
        if str(elem['name']) not in trash_processes:
            list_for_kafka.append(str(hostname) + " " + str(elem['name']))
            list_for_segment.append(str(elem['name']))

    list_for_kafka_unique = set(list_for_kafka)
    list_for_segment_unique = set(list_for_segment)
    for kafka_unique in list_for_kafka_unique:
        print(kafka_unique)
        send_to_kafka(kafka_unique)


    #for segment_unique in list_for_segment_unique:
    #    print(f"To segment: {segment_unique}")
    #    send_to_segment(segment_unique)
    # just send top program running, so I can use it easily to measure time online
    print("To segment: {}".format(list_for_segment[0]))
    send_to_segment(list_for_segment[0])


print("Hllo World")
print("OMG this is cool")

send_to_kafka("Hello there from: " + hostname)

time_start = datetime.now()
do_git_pull = True
while True:
    main()
    sleep(60)
    time_now = datetime.now()
    seconds_since_start = (time_now - time_start).seconds
    print(f"Program is running for: {seconds_since_start} seconds.")

    # execute this once at the start
    if do_git_pull == True:
        print("Running git pull")
        g.pull()
        do_git_pull = False

    # randomly set the flag to run git pull
    random_number = randrange(20)
    print(f"Random number: {random_number}")
    if random_number%19  == 0:
        do_git_pull = True
