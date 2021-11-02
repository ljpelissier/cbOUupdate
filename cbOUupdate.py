#!/usr/bin/env python3
"""
 author: Louis Pelssier
 
 
"""
import configparser
import os
import pandas as pd
import subprocess

#year offset based on grade level
YEAROFFSET = 9  #9 for 8th grade 13 for High School

config = configparser.ConfigParser()
config.read('config.ini')

print(config['hostpath']['hostpath'])
