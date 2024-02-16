from openminds import core,controlledTerms
import pandas as pd
from .utility import  read_json,table_filter

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

  for subject in subject_id:







  return openMINDS_subjects
