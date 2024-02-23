from openminds import core,controlledTerms
import pandas as pd
from .utility import  read_json,table_filter,data_frame_value

def dataset_version_create (bids_layout,dataset_description,layout_df):
  
  dataset_version=core.DatasetVersion()

  #Fetch the dataset type from dataset description file 
  if "DatasetType" in dataset_description:
    dataset_type=controlledTerms.SemanticDataType.by_name(dataset_description["DatasetType"])
  else:
    dataset_type=None
  
  #Fetch the digitalIdentifier from dataset description file 
  if "DatasetDOI" in dataset_description:
    digital_identifier=core.DOI(
      identifier=dataset_description["DatasetDOI"])
  else:
    digital_identifier=None
    
    
  author=person_create(dataset_description["Authors"])

  if "Acknowledgements" in dataset_description:
    other_contribution=dataset_description["Acknowledge"]
  else:
    other_contribution=None

  if "HowToAcknowledge" in dataset_description:
    how_to_cite=dataset_description["HowToAcknowledge"]
  else:
    how_to_cite=None

  if "Funding" in dataset_description:
    funding=funding_openMINDS(dataset_description["Funding"])
  else:
    funding=None
  
  if "EthicsApprovals" in dataset_description:
    #to be compleated ethics_assessment
    ethics_assessment=controlledTerms.EthicsAssessment.by_name("EU compliant")
  else:
    ethics_assessment=None
  #Detect th
  experimental_approach




  #creating a list containig all the Modalities used in this dataset
  suffixs=layout_df['suffix'].unique()
  techniques=tequniques_openmind(suffixs)



    

  return dataset_version



def dataset_create ():
  
  return dataset

def subjects_creation (subject_id,layout_df):

  #Find the participants files in the files table
  participants_paths=table_filter(layout_df,'participants')
  #Select the tsv file of the table
  participants_path_tsv=table_filter(participants_paths,'.tsv','extension').iat[0,0]
  participants_path_json=table_filter(participants_paths,'.json','extension').iat[0,0]

  participants_table=pd.read_csv(participants_path_tsv, sep='\t', header=0)

  sessions=layout_df.get_sessions()
  if not sessions:
    sessions=[""]
  subjects_dict={}
  subject_state_dict={}
  for subject in subject_id:
    subject_name=f"sub-{subject}"
    data_subject=table_filter(participants_table,subject_name,"participant_id")
    state_cash={}
    for sesion in sessions:
        state=core.SubjectState(age=data_frame_value(data_subject,"age"),
                            handedness=data_frame_value(data_subject,"handedness"),
                            lookup_label=f"Studied state {subject_name} {sesion}")
        collection.add(state)
        state_cash[f"{sesion}"]=state
    subject_state_dict[f"{subject}"]=state_cash
    subject_cash=core.Subject(biological_sex=data_frame_value(data_subject,"sex"),
                           lookup_label=f"{subject_name}",
                           internal_identifier=f"{subject_name}",
                           species=data_frame_value(data_subject,"sex"),
                           studied_state=state_cash)
    subjects_dict[f"{subject}"]=subject_cash
    collection.add(subject_cash)

  return subjects_dict,
