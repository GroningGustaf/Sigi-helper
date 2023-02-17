from numpy import empty
import time
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
import os
import argparse
import urllib3
import csv
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Is this a problem?

#------------------------#
# EXAMPLE WITH DIAGNOSIS 83
#------------------------#
# Company - in-SITU consult (ID 682)
# C22 106250
# Inuti syslog finns “Diagnosis, 83”

if __name__ == '__main__':

#------------------------# 
# USER INPUT
#------------------------#

    parser = argparse.ArgumentParser(description='Search script',
            add_help=True)

    parser.add_argument('--company_id', dest='company_id', required=True)
    parser.add_argument('--device_type', dest='device_type', required=True, nargs='+')                     
    parser.add_argument('--date', dest='date', required=True)               # "YYYY/MM/DD" format for the URL
    parser.add_argument('--timespan', dest='timespan', required=True)       # (expressed in weeks from --date 
                                                                            # --timespan 8 = 2 months after args.date)
    parser.add_argument('--u', dest='u', required=True)
    parser.add_argument('--p', dest='p', required=True)
    args = parser.parse_args()

#------------------------# 
# FIND ID'S FOR DEVICES
#------------------------# 

def getDeviceId(company_id, deviceType):
    print('----- finding device serials for {} ----- \n'.format(deviceType))
    list_of_devices = []
    
    url = 'https://sigicom.infralogin.com/boapi/v0/company/{}/device/all'.format(company_id)

    r = requests.get(url=url, headers={'accept': 'application/json'}, 
    verify=False, auth=HTTPBasicAuth(args.u, args.p)) 
    
    data = json.dumps(r.json(), indent=4)
    jsonData = json.loads(data)

    for i in jsonData:
        if i['type'] in deviceType:
            list_of_devices.append(i['serial'])
        
    return list_of_devices

#------------------------# 
# CREATE LIST OF DATES
#------------------------# 
def createDatesFromTimespan():
    list_of_dates = []
    # Convert the input date string to a datetime object
    start_date = datetime.strptime(args.date, '%Y/%m/%d').date()

    # Calculate the end date by adding the number of weeks specified by the user
    end_date = start_date + timedelta(weeks=int(args.timespan))

    # Loop over each day between the start and end dates
    for date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):

        date_str = date.strftime('%Y/%m/%d')
        list_of_dates.append(date_str)

    return list_of_dates

#------------------------# 
# LOOK FOR DIAGNOSIS
#------------------------# 
def findDiagnosis(company_id, list_of_device_ids, deviceType, date):
    print('\n')
    print('----- searching Syslogs for {} ----- \n'.format(deviceType))
    devices_with_diagnosis = []
    for i in list_of_device_ids:
        
        # This needs to stop taking date, going off of the loop instead
        url = "https://sigicom.infralogin.com/boapi/v0/company/{}/device/{}/{}/syslog/{}".format(
            company_id, deviceType, i, date)
        print(url)

        r = requests.get(url=url, headers={'accept': 'application/json'}, 
        verify=False, auth=HTTPBasicAuth(args.u, args.p))

        if r.status_code != 200:    # Some devices don't have any Syslogs for the interval selected and will return 404
            continue
        
        data = json.dumps(r.json(), indent=4)

        jsonData = json.loads(data)

        for j in jsonData['data']:
            if len(j['data']) > 1 and j['data'][0]['data'] == 'DIAGNOSIS' and j['data'][1]['data'] == 83:
                print("found a device!")
                device = [i, j['infra_timestamp']]
                devices_with_diagnosis.append(device)

    return devices_with_diagnosis

#------------------------# 
# WRITE CSV FILE
#------------------------#
def writeCsvFile(list_of_devices_with_diagnosis):
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['device type', 'serial', 'timestamp'])
        writer.writerows(list_of_devices_with_diagnosis)

#------------------------# 
# TESTS (PROBABLE DELETE)
#------------------------#

def writeJsonFile(url):
        jsonFile = "json_data.json"

        # URL = "https://sigicom.infralogin.com/boapi/v0/company/682/device/C22/106250/syslog/2023/01/05"
        URL = url

        r = requests.get(url=URL, headers={'accept': 'application/json'}, verify=False, auth=HTTPBasicAuth(args.u, args.p))
        json_object = json.dumps(r.json(), indent=4)

        with open(jsonFile, "a") as file:
            file.write(json_object)


#------------------------# 
# MAIN
#------------------------#
start_time = time.time() # For logging how long the execution time is

print('----- CompanyID: {} ----- \n'.format(args.company_id))
print('----- Analyzing device types: {} ----- \n'.format(args.device_type))

deviceTypes = []
deviceListForCSV = []   # final list that will be written to CSV


# testList = [107000, 106263, 107073, 106229, 107006, 108589, 106099, 106341, 106999, 108527, 107001, 107008, 106073, 106808, 106325, 
# 107047, 105931, 106061, 106975, 106333, 106250] 

for device in args.device_type:
    deviceTypes.append(device)

listOfDates = createDatesFromTimespan()
print(listOfDates)

for day in listOfDates:
    print('\n')
    print('----- analyzing date {} ----- \n'.format(day))

    for item in deviceTypes:
        deviceList = getDeviceId(args.company_id, item)
        print("Serials for {} ".format(item), deviceList)
        devicesWithDiagnosis = findDiagnosis(args.company_id, deviceList, item, day)
        print("devicesWithDiagnosis", devicesWithDiagnosis)
        for i in devicesWithDiagnosis:
            CSVDevice = [item, i[0], i[1]]
            deviceListForCSV.append(CSVDevice)
    print('***********************************************************************')

writeCsvFile(deviceListForCSV)
print("--- %s seconds total runtime ---" % (time.time() - start_time))



