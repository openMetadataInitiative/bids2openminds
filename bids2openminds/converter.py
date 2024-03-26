from warnings import warn
from bids import BIDSLayout,BIDSValidator
import os
import main
import utility

from openminds import Collection

collection = Collection()

bids_dir=input("Enter the BIDS directory path: ")

def converter(bids_dir):

  if not(os.path.isdir(bids_dir)):
    raise NotADirectoryError(f"The input directory is not valid, you have specified {bids_dir} which is not a directory.")

  #if not(BIDSValidator().is_bids(bids_dir)):
  #  raise NotADirectoryError(f"The input directory is not valid, you have specified {bids_dir} which is not a BIDS directory.")

  bids_layout=BIDSLayout(bids_dir)

  layout_df=bids_layout.to_df()

  subjects_id=bids_layout.get_subjects()

  tasks=bids_layout.get_task()

  #imprting the datset description file containing some of the 
  dataset_description_path=utility.table_filter(layout_df,'description')

  dataset_description=utility.read_json(dataset_description_path.iat[0,0])

  [subjects_dict,subject_state_dict,subjects_list]=main.subjects_creation (subjects_id,layout_df,bids_layout)

  [files_list,file_repository]=main.file_creation(layout_df,bids_dir)

  dataset_version=main.dataset_version_create (bids_layout,dataset_description,layout_df,subjects_list,file_repository)

  dataset=main.dataset_creation(dataset_description,dataset_version)
