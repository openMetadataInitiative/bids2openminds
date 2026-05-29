import os


def create_report(dataset, dataset_version, collection, dataset_description, input_path, output_path, openminds_version="v4"):
    subject_number = 0
    subject_state_numbers = []
    file_bundle_number = 0
    files_number = 0
    content_type_list = ""

    for item in collection:
        if item.type_.endswith("Subject"):

            subject_number += 1
            subject_state_numbers.append(len(item.studied_states))

        if item.type_.endswith("File"):

            files_number += 1

        if item.type_.endswith("FileBundle"):

            file_bundle_number += 1

        if item.type_.endswith("ContentType"):

            content_type_list += f"{item.name}\n"

    # In v5, DatasetVersion no longer carries `authors`: they live inside
    # `contributions`. Derive them version-agnostically.
    authors = getattr(dataset_version, "authors", None)
    if authors is None and getattr(dataset_version, "contributions", None):
        authors = []
        for contribution in dataset_version.contributions:
            authors.extend(contribution.contributors or [])

    # Behavioral protocols are linked on the DatasetVersion: in v4 via the dedicated
    # `behavioral_protocols` property, in v5 merged into the general `protocols`
    # property (which may also hold non-behavioral Protocols), see openMINDS_core #377.
    behavioral_protocols = getattr(dataset_version, "behavioral_protocols", None)
    if not behavioral_protocols:
        protocols = getattr(dataset_version, "protocols", None) or []
        behavioral_protocols = [
            p for p in protocols if p.type_.endswith("BehavioralProtocol")
        ]
    behavioral_protocols = behavioral_protocols or None
    behavioral_protocols_numbers = len(behavioral_protocols or [])

    experimental_approaches_list = ""
    if dataset_version.experimental_approaches is not None:
        for approache in dataset_version.experimental_approaches:
            experimental_approaches_list += f"{approache.name}\n"

    data_types_list = ""
    if dataset_version.data_types is not None:
        if isinstance(dataset_version.data_types, list):
            for data_type in dataset_version.data_types:
                data_types_list += f"{data_type.name}\n"
        else:
            data_types_list = f"{dataset_version.data_types.name}\n"

    techniques_list = ""
    if dataset_version.techniques is not None:
        for technique in dataset_version.techniques:
            techniques_list += f"{technique.name}\n"
    else:
        techniques_list = "No techniques were detected. Please follow the BIDS recommendations for suffixes, as bids2openminds detects techniques based on suffixes."

    behavioral_protocols_list = ""
    if behavioral_protocols is not None:
        for behavioral_protocol in behavioral_protocols:
            behavioral_protocols_list += f"{behavioral_protocol.name}\n"
    else:
        behavioral_protocols_list = "No behavioral protocols were detected. Please follow the BIDS recommendations for task labels, as bids2openminds detects behavioral protocols based on task labels."

    author_list = ""
    i = 1
    if authors is not None:
        for author in authors:
            if author.family_name is not None:
                author_list += f"  {i}. {author.family_name}, {author.given_name}\n"
                i += 1
            else:
                author_list += f"  {i}. ___, {author.given_name}\n"
                i += 1

    min_subject_state_numbers = min(subject_state_numbers)
    max_subject_state_numbers = max(subject_state_numbers)
    if min_subject_state_numbers == max_subject_state_numbers:
        text_subject_state_numbers = str(min_subject_state_numbers)
    else:
        text_subject_state_numbers = f"min={min_subject_state_numbers}, max={max_subject_state_numbers}"

    report = f"""
Conversion Report
=================
Conversion was successful, the openMINDS file is in {output_path}
openMINDS schema version: {openminds_version} (load it back with Collection.load(..., version="{openminds_version}"))

Dataset title : {dataset.full_name}


The following elements were converted:
------------------------------------------
+ number of authors : {len(authors or [])}
+ number of converted subjects: {subject_number}  
+ number of states per subject: {text_subject_state_numbers}
+ number of files: {files_number} 
+ number of file bundles: {file_bundle_number}
+ number of techniques: {len(dataset_version.techniques or [])}
+ number of behavioral protocols: {behavioral_protocols_numbers}


Experimental approaches detected:
------------------------------------------ 
{experimental_approaches_list}

Detected data types:
------------------------------------------
{data_types_list}

Detected content types:
------------------------------------------
{content_type_list}

Detected techniques:
------------------------------------------
{techniques_list}

Detected behavioral protocols:
------------------------------------------
{behavioral_protocols_list}



**Important Notes**
------------------------------------------ 

Authors:
    The conversion of authors is not reliable due to missing source convention.
    The converter may fail in detecting family vs given name.
    The converter will fail in detecting organizations.
    The following persons (family name, given name) were converted, : 
{author_list}

Subject States:
    There are as many subject states as sessions for each subject.
    Please modify to your needs (divide into more or merge into fewer subject states).

Behavioral protocols:
    The conversion of behavioral protocols is incomplete.
    Only the task-label is extracted as name and internal identifier of a behavioral protocol.
    Please adjust to your needs.
 
"""
    if "GeneratedBy" in dataset_description:
        report = report+"+Dataset is derivative, derivative data are ignored for now\n"

    derivatives_path = os.path.join(
        input_path, "derivatives")
    if os.path.isdir(derivatives_path):
        report = report+"+ Dataset contains derivative, derivative data are ignored for now\n"

    return report
