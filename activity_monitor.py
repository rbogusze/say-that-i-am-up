import psutil

from time import sleep
from datetime import datetime
from json import dumps
from kafka import KafkaProducer

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
        send_to_kafka(elem['name'])

        


    

print("Hllo World")
print("OMG this is cool")

send_to_kafka("Hello there")
while True:
    main()
    sleep(10)
