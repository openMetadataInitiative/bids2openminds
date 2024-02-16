import json
import pandas as pd

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
