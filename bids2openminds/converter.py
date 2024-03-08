from warnings import warn
from bids import BIDSLayout,BIDSValidator
import json
import os
import pandas as pd
import numpy as np
import datetime

from openminds import Collection

collection = Collection()

  
if not(os.path.isdir(bids_dir)):
  raise NotADirectoryError(f"The input directory is not valid, you have specified {bids_dir} which is not a directory.")

if not(BIDSValidator().is_bids(bids_dir)):
  raise NotADirectoryError(f"The input directory is not valid, you have specified {bids_dir} which is not a BIDS directory.")

bids_layout=BIDSLayout(bids_dir)

layout_df=bids_layout.to_df()

subjects_id=bids_layout.get_subjects()

tasks=bids_layout.get_task()

#imprting the datset description file containing some of the 
dataset_description_path=table_filter(layout_df,'description')

dataset_description=read_json(dataset_description_path.iat[0,0])

dataset_version=dataset_version_create(bids_layout,dataset_description,layout_df)
