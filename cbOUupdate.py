#!/usr/bin/env python3
"""
 author: Louis Pelssier

   This makes sure serial numbers associated with students is 
   updated in the correct OU in the google admin panel
   To be run every 15 minutes.
   
   Separate script will remove unassociated chomebooks from
   class OUs.
 
"""
import configparser
import os
import pandas as pd
from io import StringIO
import subprocess

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import shlex


#year offset based on grade level
YEAROFFSET = 9  #9 for 8th grade 13 for High School

config = configparser.ConfigParser()
config.read('config.ini')

#load in data from SIS with student serial numbers
sisList =  pd.read_csv(config['hostpath']['hostPath'] + \
                        config['hostpath']['fileName'], index_col='StudentID')
sisList['GradeLevel'] = sisList['GradeLevel'].replace('KF','00')

header_list = ['id','sn','grade']
googleList = pd.DataFrame(columns = header_list)


CurrentYearWithOffset = int(sisList.iat[0,0][:4]) + YEAROFFSET

#get lists of serial numbers in class ou structures
for (gradeLevel, ouRoot) in config.items('ouRoot'):
    ouForGradeLevel = CurrentYearWithOffset - int(gradeLevel)
    gamCommand = f"/home/administrator/bin/gamadv-xtd3/gam print cros limit_to_ou {ouRoot}ClassOf{ouForGradeLevel} serialnumber"
    args = shlex.split(gamCommand)
    googleOutput = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT   )
    standerdout,standarderr = googleOutput.communicate()
    standerdout = standerdout.decode("utf-8")
    standerdout = '\n'.join(standerdout.split("\n")[3:-2])
    try:
        thisClass = pd.DataFrame([cb.split(',') for cb in standerdout.split('\n')])
        thisClass.columns=["id","sn"]
        thisClass['grade'] = gradeLevel
        googleList = googleList.append(thisClass)
    except:
        pass
 
 
 
#trim out any rows where chromebook has not been scanned.
sisList = sisList[sisList['CBSerialNumber'].notna()]
sisList['CurrentSerialNumber'] = sisList['CBSerialNumber'].str[:22]


count = 0
for ind in sisList.index:
    if googleList['sn'].str.contains(sisList['CurrentSerialNumber'][ind].upper()).any():
        pass
    else:
        ouForGradeLevel = CurrentYearWithOffset - int(sisList['GradeLevel'][ind])
        print(f"put sn {sisList['CurrentSerialNumber'][ind]} in ou {sisList['OUroot'][ind]}ClassOf{ouForGradeLevel}")
        count +=1

        gamCommand = f"/home/administrator/bin/gamadv-xtd3/gam cros_sn {sisList['CurrentSerialNumber'][ind]} update ou {sisList['OUroot'][ind]}ClassOf{ouForGradeLevel}"
        print(gamCommand)
        #args = shlex.split(gamCommand)
        #googleOutput = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT   )
        #standerdout,standarderr = googleOutput.communicate()
        #standerdout = standerdout.decode("utf-8")
        print("cb move attempted")




print(sisList)
print(count)
