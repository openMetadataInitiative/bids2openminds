import os
import pathlib

import pandas as pd

import openminds.latest.core as omcore
import openminds.latest.controlled_terms as controlled_terms
from openminds import IRI

from .utility import table_filter, pd_table_value, file_hash, file_storage_size
from .mapping import bids2openminds_instance
from . import globals


def create_techniques(layout_df):
    suffixs = layout_df["suffix"].unique().tolist()
    techniques = []
    not_techniques_index = ["description", "participants", "events"]
    for suffix in suffixs:
        if not (pd.isna(suffix) or (suffix in not_techniques_index)):
            techniques.extend(bids2openminds_instance(suffix, "MAP_2_TECHNIQUES"))

    return techniques or None


def create_approaches(layout_df):
    datatypes = layout_df["datatype"].unique().tolist()
    approaches = set([])
    for datatype in datatypes:
        if not (pd.isna(datatype)):
            approaches.update(bids2openminds_instance(datatype, "MAP_2_EXPERIMENTAL_APPROACHES"))

    return list(approaches) or None


def create_dataset_version(bids_layout, dataset_description, layout_df, studied_specimens, file_repository):

    # Fetch the dataset type from dataset description file

    # dataset_type=bids2openminds_instance(dataset_description.get("DatasetType",None))

    # Fetch the digitalIdentifier from dataset description file

    if "DatasetDOI" in dataset_description:
        digital_identifier = omcore.DOI(identifier=dataset_description["DatasetDOI"])
    else:
        digital_identifier = None

    # TODO extract person
    # author=person_create(dataset_description["Authors"])

    if "Acknowledgements" in dataset_description:
        other_contribution = dataset_description["Acknowledgements"]
    else:
        other_contribution = None

    if "HowToAcknowledge" in dataset_description:
        how_to_cite = dataset_description["HowToAcknowledge"]
    else:
        how_to_cite = None

    # TODO funding
    # if "Funding" in dataset_description:
    #   funding=funding_openMINDS(dataset_description["Funding"])
    # else:
    #   funding=None

    # if "EthicsApprovals" in dataset_description:
    #   #to be compleated ethics_assessment
    #   ethics_assessment=controlledTerms.EthicsAssessment.by_name("EU compliant")
    # else:
    #   ethics_assessment=None

    # creating a list containig all the Modalities used in this dataset

    techniques = create_techniques(layout_df)

    experimental_approaches = create_approaches(layout_df)

    dataset_version = omcore.DatasetVersion(
        digital_identifier=digital_identifier,
        experimental_approaches=experimental_approaches,
        short_name=dataset_description["Name"],
        studied_specimens=studied_specimens,
        techniques=techniques,
        how_to_cite=how_to_cite,
        repository=file_repository,
        #other_contributions=other_contribution  # needs to be a Contribution object
        # version_identifier
    )

    globals.collection.add(dataset_version)

    return dataset_version


def create_dataset(dataset_description, dataset_version):

    if "DatasetDOI" in dataset_description:
        digital_identifier = omcore.DOI(identifier=dataset_description["DatasetDOI"])
    else:
        digital_identifier = None

    dataset = omcore.Dataset(
        digital_identifier=digital_identifier, full_name=dataset_description["Name"], has_versions=dataset_version
    )

    globals.collection.add(dataset)

    return dataset


def create_subjects(subject_id, layout_df, layout):
    
    sessions = layout.get_sessions()
    if not sessions:
        sessions = [""]
    subjects_dict = {}
    subjects_list = []
    subject_state_dict = {}

    # Find the participants files in the files table
    participants_paths = table_filter(layout_df, "participants")
    if  participants_paths.empty:
        #creating emphty subjects just based on file structure
        for subject in subject_id:
            subject_name = f"sub-{subject}"
            state_cash_dict = {}
            state_cash = []
            for session in sessions:
                state = omcore.SubjectState(
                    internal_identifier=f"Studied state {subject_name} {session}".strip(),
                    lookup_label=f"Studied state {subject_name} {session}".strip()
                )
                globals.collection.add(state)
                state_cash_dict[f"{session}"] = state
                state_cash.append(state)
            subject_state_dict[f"{subject}"] = state_cash_dict
            subject_cash = omcore.Subject(
                lookup_label=f"{subject_name}",
                internal_identifier=f"{subject_name}"
            )
            subjects_dict[f"{subject}"] = subject_cash
            subjects_list.append(subject_cash)
            globals.collection.add(subject_cash)


        return subjects_dict, subject_state_dict, subjects_list


    # Select the tsv file of the table
    participants_path_tsv = pd_table_value(table_filter(participants_paths, ".tsv", "extension"), "path")
    participants_path_json = pd_table_value(table_filter(participants_paths, ".json", "extension"), "path")

    participants_table = pd.read_csv(participants_path_tsv, sep="\t", header=0)
    for subject in subject_id:
        subject_name = f"sub-{subject}"
        data_subject = table_filter(participants_table, subject_name, "participant_id")
        state_cash_dict = {}
        state_cash = []
        for session in sessions:
            state = omcore.SubjectState(
                age=omcore.QuantitativeValue(
                    value=pd_table_value(data_subject, "age"),
                    unit=controlled_terms.UnitOfMeasurement.year
                ),
                handedness=bids2openminds_instance(pd_table_value(data_subject, "handedness"), "MAP_2_HANDEDNESS"),
                internal_identifier=f"Studied state {subject_name} {session}".strip(),
                lookup_label=f"Studied state {subject_name} {session}".strip()
            )
            globals.collection.add(state)
            state_cash_dict[f"{session}"] = state
            state_cash.append(state)
        subject_state_dict[f"{subject}"] = state_cash_dict
        subject_cash = omcore.Subject(
            biological_sex=bids2openminds_instance(pd_table_value(data_subject, "sex"), "MAP_2_SEX", is_list=False),
            lookup_label=f"{subject_name}",
            internal_identifier=f"{subject_name}",
            # TODO species should be defulted to homo sapiens
            species=bids2openminds_instance(pd_table_value(data_subject, "species"), "MAP_2_SPECIES"),
            studied_states=state_cash
        )
        subjects_dict[f"{subject}"] = subject_cash
        subjects_list.append(subject_cash)
        globals.collection.add(subject_cash)

    return subjects_dict, subject_state_dict, subjects_list


def create_file(layout_df, BIDS_path):

    BIDS_directory_path = os.path.dirname(BIDS_path)
    file_repository = omcore.FileRepository()
    globals.collection.add(file_repository)
    files_list = []
    for index, file in layout_df.iterrows():
        file_format = None
        content_description = None
        data_types = None
        extention = file["extension"]
        path = file["path"]
        name = path[path.rfind("/") + 1 :]
        iri=IRI(pathlib.Path(path).as_uri())
        hashes = file_hash(path)
        storage_size = file_storage_size(path)
        if pd.isna(file["subject"]):
            if file["suffix"] == "participants":
                if extention == ".json":
                    content_description = f"A JSON metadata file of participants TSV."
                    data_types = controlled_terms.DataType.by_name("associative array")
                    file_format = omcore.ContentType.by_name("application/json")
                elif extention == [".tsv"]:
                    content_description = f"A metadata table for participants."
                    data_types = controlled_terms.DataType.by_name("table")
                    file_format = omcore.ContentType.by_name("text/tab-separated-values")
        else:
            if extention == ".json":
                content_description = f"A JSON metadata file for {file['suffix']} of subject {file['subject']}"
                data_types = controlled_terms.DataType.by_name("associative array")
                file_format = omcore.ContentType.by_name("application/json")
            elif extention in [".nii", ".nii.gz"]:
                content_description = f"Data file for {file['suffix']} of subject {file['subject']}"
                data_types = controlled_terms.DataType.by_name("voxel data")
                # file_format=omcore.ContentType.by_name("nifti")
            elif extention == [".tsv"]:
                if file["suffix"] == "events":
                    content_description = f"Event file for {file['suffix']} of subject {file['subject']}"
                    data_types = controlled_terms.DataType.by_name("event sequence")
                    file_format = omcore.ContentType.by_name("text/tab-separated-values")
        file = omcore.File(
            iri=iri,
            content_description=content_description,
            data_types=data_types,
            file_repository=file_repository,
            format=file_format,
            hashes=hashes,
            # is_part_of=file_bundels
            name=name,
            # special_usage_role
            storage_size=storage_size,
        )
        globals.collection.add(file)
        files_list.append(file)

    return files_list, file_repository
