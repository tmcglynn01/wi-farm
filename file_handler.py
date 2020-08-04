#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:14:47 2020

@author: trevor

Takes a tsv file from the USDA NASS, cleans the headers, then parses each
line of the tsv. First, it checks the source of the data, then writes that
line to a csv 

"""
import re
import os
import csv

SURVEY = '_survey.csv'
CENSUS = '_census.csv'
DATA_PATH = '/data/'


def clean_header(header, search_term='_DESC'):
  """Cleans up header names"""
  for i, field in enumerate(header):
    if field.endswith(search_term):
      idx = field.find(search_term)
      header[i] = field[:idx]
  return header
   

def create_output_files(filename):
  """Creates output files for writing csv"""
  filename = re.split('\.', filename)[1] # ['qs', 'XXX', 'txt']
  return (filename + CENSUS), (filename + SURVEY)


def read_source(row):
  source = row['SOURCE']
  if source == 'CENSUS':
    return 'census'
  elif source == 'SURVEY':
    return 'survey'
  else:
    raise Exception(f'Invalid entry: {row}')
    
    
def check_count(*args):
  for arg in args:
    if arg < 1:
      return args.index(arg)
    

def process_files():
  """
  Iteratively parses through the files of the data sets obtained through the
  USDA National Agricultural Statistics Service. Entries are checked by source
  and likewise written into a respective CSV file. The source file is cleaned
  up when complete to deal with space constraints.

  Returns 
  -------
  None.

  """
  os.chdir('data')
  for file in os.listdir():
    with open(file) as file:
      print(f'Processing file: {file.name}')
      reader = csv.DictReader(file, dialect='excel-tab')
      census_out, survey_out = create_output_files(file.name)
      fieldnames = clean_header(reader.fieldnames)
      print(f'Census file created: {census_out}')
      print(f'Survey file created: {survey_out}')
    
      with open(census_out, 'w') as census, open(survey_out, 'w') as survey:
        census_writer = csv.DictWriter(census, fieldnames=fieldnames)
        survey_writer = csv.DictWriter(survey, fieldnames=fieldnames)
        
        census_writer.writeheader()
        survey_writer.writeheader()
        
        census_rows, survey_rows = 0, 0
        
        print('Now parsing rows...')
        count = 0
        
        for row in reader:
          if not (count % 100000):
            print(f'Parsing row #{count}')
          count += 1
          if read_source(row) == 'census':
            census_writer.writerow(row)
            census_rows += 1
          else:
            survey_writer.writerow(row)
            survey_rows += 1
        else:
          print(f'Finished parsing {file.name}\nTotal Rows: {count}\n')
        if census_rows < 1:
          print('Census file empty: removing...')
          os.remove(census_out)
        elif survey_rows < 1:
          print('Survey file empty: removing...')
          os.remove(survey_out)
      
      print(f'Removing parsed file: {file.name}')
      os.remove(file.name)


if __name__ == '__main__':
  process_files()
  
  
