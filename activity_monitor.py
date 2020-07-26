import psutil
import git

from time import sleep
from datetime import datetime, time
from json import dumps
from kafka import KafkaProducer
from random import randrange

git_dir = "C:\_programy\say-that-i-am-up"
g = git.cmd.Git(git_dir)

def send_to_kafka(text):
    producer = KafkaProducer(bootstrap_servers=['192.168.1.167:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    
    send_to_kafka = {'send_time' : datetime.now().replace(microsecond=0).isoformat(), 'text' : str(text)}
    producer.send('activity_monitor', value=send_to_kafka)



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
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       # Append dict of process detail in list
       listOfProcessNames.append(pInfoDict)
    # Iterate over the list of dictionary and print each elem
    for elem in listOfProcessNames:
        #print(elem)
        pass
    print('*** Top 5 process with highest memory usage ***')
    listOfRunningProcess = getListOfProcessSortedByMemory()
    
    for elem in listOfRunningProcess[:5] :
        print(elem)
        send_to_kafka(str(elem['username']) + " " + str(elem['name']))

        


    

print("Hllo World")
print("OMG this is cool")

send_to_kafka("Hello there")

time_start = datetime.now()
do_git_pull = True
while True:
    main()
    sleep(5)
    time_now = datetime.now()
    seconds_since_start = (time_now - time_start).seconds
    print(f"Program is running for: {seconds_since_start} seconds.")

    # execute this once at the start
    if do_git_pull == True:
        print("Running git pull")
        g.pull()
        do_git_pull = False

    # randomly set the flag to run git pull
    random_number = randrange(10)
    print(f"Random number: {random_number}")
    if random_number%5 == 0:
        do_git_pull = True
