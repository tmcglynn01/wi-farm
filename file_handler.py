#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:14:47 2020

@author: trevor
"""

import os
import csv


def clean_header(header, search_term):
  for i, field in enumerate(header):
    if field.endswith(clip := search_term):
      idx = name.find(clip)
      header[i] = name[:idx]

source = os.getcwd() + '/data/'
files = os.listdir(source)

with open (source + files[0]) as census2007:
  reader = csv.DictReader(census2007, dialect='excel-tab')
  
  # Cleans up some header names
  for i, name in enumerate(reader.fieldnames):
    if name.endswith(clip := '_DESC'):
      idx = name.find(clip)
      reader.fieldnames[i] = name[:idx]
      
  # Split into two files according to source
  
  
  for line in reader:
    print(line)
    break
  
  
  

