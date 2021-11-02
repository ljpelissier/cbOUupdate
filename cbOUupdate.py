#!/usr/bin/env python3
"""
 author: Louis Pelssier
 
 
"""
import configparser
import os
import pandas as pd
import subprocess

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



#year offset based on grade level
YEAROFFSET = 9  #9 for 8th grade 13 for High School

config = configparser.ConfigParser()
config.read('config.ini')

#sisList =  pd.read_csv(config['hostpath']['hostPath'] + config['hostpath']['fileName'], index_col='StudentID')
sisList =  pd.read_csv(config['hostpath']['hostPath'] + \
                        config['hostpath']['fileName'], index_col='StudentID')
print(sisList.iat[0,0])
