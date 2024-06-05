import os


def create_report(dataset, dataset_version, collection, dataset_description, input_path):
    subject_number = 0
    file_bundle_number = 0
    files_number = 0

    for item in collection:
        match item.type_:

            case "https://openminds.ebrains.eu/core/Subject":

                subject_number += 1

            case "https://openminds.ebrains.eu/core/File":

                files_number += 1

# TODO to be activated after merging the FileBundle pull request
#            case "https://openminds.ebrains.eu/core/FileBundle":
#
#                file_bundle_number += 1

    report = f"""Conversion Report
=================  

Dataset title : {dataset.full_name}

The following elements were converted:  
--------------------------------------  
+ number of converted subjects: {subject_number}  
+ number of state for each subject: XX-YY  
+ number of files: {files_number} 
+ number of files: {file_bundle_number}

The following elements were not converted:  
------------------------------------------  
"""
    if "GeneratedBy" in dataset_description:
        report = report+"\n"+"+ Dataset is derivative, derivative data are ignored for now\n"

    derivatives_path = os.path.join(
        input_path, "derivatives")
    if os.path.isdir(derivatives_path):
        report = report+"\n"+"+ Dataset contains derivative, derivative data are ignored for now\n"

    print(report)
