import json
import pandas as pd

def camel_to_snake(name):
  import re
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def read_json(file_path: str) -> dict:
  """
  Reads the content of a JSON file and returns it as a Python dictionary.

  Parameters:
  - file_path (str): The path to the JSON file.

  Returns:
  - dict: A Python dictionary containing the content of the JSON file.

  Example:
  >>> data = read_json('example.json')
  >>> print(data)
  {"Name": "The mother of all experiments" , "BIDSVersion": "1.6.0", "DatasetType": "raw" , "License": "CC0" , "Authors": ["Paul Broca" , "Carl Wernicke" ]}
  """
  try:
    # Open the JSON file
    with open(file_path, 'r') as file:
      # Load the JSON content into a dictionary
      json_dic = json.load(file)
    return json_dic
  except FileNotFoundError:
    # Handle file not found error
    print(f"Error: File not found at {file_path}")
    return {}
  except json.JSONDecodeError:
    # Handle JSON decoding error
    print(f"Error: Unable to decode JSON content from {file_path}")
    return {}



def table_filter (dataframe:pd.DataFrame,filter_str:str,column:str="suffix"):
  """
  Filters a Pandas DataFrame based on a specified condition.

  Parameters:
  - dataframe (pd.DataFrame): The DataFrame to be filtered.
  - filter_str (str): The value to filter the DataFrame on.
  - column (str, optional): The column name to apply the filter on. Default is "suffix".

  Returns:
  - pd.DataFrame: A filtered DataFrame containing only the rows that satisfy the condition.
  """
  try:
    # Apply the filter condition on the specified column
    filtered_dataframe = dataframe[dataframe[column] == filter_str]
    return filtered_dataframe
  except KeyError:
    # Handle the case where the specified column is not present in the DataFrame
    KeyError(f"Error: Column '{column}' not found in the DataFrame.")


def openminds_instance(list:list, Terminologie :str =None):
  openminds_list=[]
  import openminds.latest.controlled_terms as controlled_terms
  for item in list:
    if item.replace(" ","")[0:32]=="@id:https://openminds.ebrains.eu":
      slash_location=item.rfind("/")
      item_name=item[slash_location+1:]
      item_name_snake=camel_to_snake(item_name)
      if not(Terminologie):
          Terminologie=item[item[:slash_location].rfind("/")+1:slash_location]
          Terminologie=Terminologie[0].upper()+Terminologie[1:]
      controlled_class=getattr(controlled_terms,Terminologie)
      openminds_item=getattr(controlled_class,item_name_snake)
      openminds_list.append(openminds_item)
    else:
      from warnings import warn
      warn(f"{item}is not a proper openMINDS instance")
  return openminds_list

def pd_table_value(data_frame,column_name,not_list:bool=True):
  try:
    if column_name in data_frame.columns:
      value=data_frame[column_name].to_list()
      if not_list:
        return value[0]
      else:
        return value
    else:
      return None
  except IndexError:
      from warnings import warn
      warn(f"The data frame dosen't contain {column_name}")
      return None



# def file_hash(file_path:str,hash_type:str="md5"):
#     import io, hashlib, hmac
#     with open(hashlib.__file__, file_path) as file:
#         digest = hashlib.file_digest(file, hash_type)
#
#     file.close
#     return digest.hexdigest()  


def file_hash(file_path:str,hash_type:str="md5"):
    import hashlib
    file=open(file_path, "rb")
    file_content=file.read()
    hash_object=hashlib.new(hash_type)
    hash_object.update(file_content)
    #add algorithm to hash return (the name opper case)
    return hash_object.hexdigest()

def file_storage_size(file_path:str):
    from openminds.latest.core import QuantitativeValue
    from openminds.latest.controlled_terms import UnitOfMeasurement
    import os
    file_stats = os.stat(file_path)
    file_size=QuantitativeValue(
        value=file_stats.st_size,
        unit=UnitOfMeasurement.by_name("byte")
    )
    return file_size
