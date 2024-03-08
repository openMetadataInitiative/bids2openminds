from openminds.latest import core as omcore
import pandas as pd
from .utility import  read_json,table_filter,pd_table_value
from .mapping import bids2openminds_instance


def create_techniques(layout_df):
  suffixs=layout_df['suffix'].unique().tolist()
  techniques=[]
  not_techniques_index=['description', 'participants','events']
  for suffix in suffixs:
    if not(pd.isna(suffix) or (suffix in not_techniques_index)):
      techniques.extend(bids2openminds_instance(suffix,'MAP_2_TECHNIQUES'))
  return techniques

def dataset_version_create (bids_layout,dataset_description,layout_df):
  
  

  #Fetch the dataset type from dataset description file 

  dataset_type=bids2openminds_instance(dataset_description.get("DatasetType",None))
  

  #Fetch the digitalIdentifier from dataset description file 

  if "DatasetDOI" in dataset_description:
    digital_identifier=omcore.DOI(
      identifier=dataset_description["DatasetDOI"])
  else:
    digital_identifier=None
    
    
  #TODO extract person
  #author=person_create(dataset_description["Authors"])

  if "Acknowledgements" in dataset_description:
    other_contribution=dataset_description["Acknowledge"]
  else:
    other_contribution=None

  if "HowToAcknowledge" in dataset_description:
    how_to_cite=dataset_description["HowToAcknowledge"]
  else:
    how_to_cite=None

  #TODO funding
  # if "Funding" in dataset_description:
  #   funding=funding_openMINDS(dataset_description["Funding"])
  # else:
  #   funding=None
  
  # if "EthicsApprovals" in dataset_description:
  #   #to be compleated ethics_assessment
  #   ethics_assessment=controlledTerms.EthicsAssessment.by_name("EU compliant")
  # else:
  #   ethics_assessment=None



  #creating a list containig all the Modalities used in this dataset

  techniques=create_techniques(layout_df)


  dataset_version=omcore.DatasetVersion(
    
  )  

  return dataset_version


def dataset_create ():
  
  return dataset

def subjects_creation (subject_id,layout_df,layout):

  #Find the participants files in the files table
  participants_paths=table_filter(layout_df,'participants')
  #Select the tsv file of the table
  participants_path_tsv=table_filter(participants_paths,'.tsv','extension').iat[0,0]
  participants_path_json=table_filter(participants_paths,'.json','extension').iat[0,0]

  participants_table=pd.read_csv(participants_path_tsv, sep='\t', header=0)

  sessions=layout.get_sessions()
  if not sessions:
    sessions=[""]
  subjects_dict={}
  subject_state_dict={}
  for subject in subject_id:
    subject_name=f"sub-{subject}"
    data_subject=table_filter(participants_table,subject_name,"participant_id")
    state_cash={}
    for sesion in sessions:
        state=omcore.SubjectState(age=pd_table_value(data_subject,"age"),
                            handedness=bids2openminds_instance(pd_table_value(data_subject,"handedness"),"MAP_2_HANDEDNESS"),
                            internal_identifier=f"{subject_name}",
                            lookup_label=f"Studied state {subject_name} {sesion}")
        collection.add(state)
        state_cash[f"{sesion}"]=state
    subject_state_dict[f"{subject}"]=state_cash
    subject_cash=omcore.Subject(biological_sex=bids2openminds_instance(pd_table_value(data_subject,"sex"),"MAP_2_SEX"),
                           lookup_label=f"{subject_name}",
                           internal_identifier=f"{subject_name}",
                           #TODO species should be defulted to homo sapiens
                           species=bids2openminds_instance(pd_table_value(data_subject,"species"),"MAP_2_SPECIES"),
                           studied_state=state_cash)
    subjects_dict[f"{subject}"]=subject_cash
    collection.add(subject_cash)

  return subjects_dict,subject_state_dict
