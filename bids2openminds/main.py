import os
import pathlib
from warnings import warn

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
        #excluding the None and non thechnique indexes
        if not (pd.isna(suffix) or (suffix in not_techniques_index)):
            openminds_techniques_cache=bids2openminds_instance(suffix, "MAP_2_TECHNIQUES")
            #Excluding the suffixs that are not in the library or flagged as non technique suffixes
            if not pd.isna(openminds_techniques_cache):
                techniques.extend(openminds_techniques_cache)
            else:
                warn(f"The {suffix} suffix is currently considered an auxiliary file for already existing techniques or a non technique file.")

    return techniques or None


def create_approaches(layout_df):
    datatypes = layout_df["datatype"].unique().tolist()
    approaches = set([])
    for datatype in datatypes:
        if not (pd.isna(datatype)):
            approaches.update(bids2openminds_instance(datatype, "MAP_2_EXPERIMENTAL_APPROACHES"))

    return list(approaches) or None


def create_openminds_age(data_subject):

    try:
        age=pd_table_value(data_subject, "age")
    except:
        return None

    if isinstance(age,float) or isinstance(age,int) or age.isnumeric():
        return omcore.QuantitativeValue(
                    value=age,
                    unit=controlled_terms.UnitOfMeasurement.year
                )
    elif age=="89+":
        return omcore.QuantitativeValueRange(
                    maxValue=None,
                    min_value=89,
                    minValueUnit=controlled_terms.UnitOfMeasurement.year
                )
    else:
        return None


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
    #   #to be completed ethics_assessment
    #   ethics_assessment=controlledTerms.EthicsAssessment.by_name("EU compliant")
    # else:
    #   ethics_assessment=None

    # creating a list containing all the Modalities used in this dataset

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
    subjects_dict = {}
    subjects_list = []
    subject_state_dict = {}

    # Find the participants files in the files table
    participants_paths = table_filter(layout_df, "participants")
    if  participants_paths.empty:
        #creating emphty subjects just based on file structure
        for subject in subject_id:
            subject_name = f"sub-{subject}"
            state_cache_dict = {}
            state_cache = []
            #dealing with condition that have no seasion
            if not sessions:
                state = omcore.SubjectState(
                    internal_identifier=f"Studied state {subject_name}".strip(),
                    lookup_label=f"Studied state {subject_name}".strip()
                )
                globals.collection.add(state)
                state_cache_dict[""] = state
                state_cache.append(state)
            else:
                #create a subject state for each state
                for session in sessions:
                    if not(table_filter(table_filter(layout_df,session,"session"),subject,"subject").empty):
                        state = omcore.SubjectState(
                            internal_identifier=f"Studied state {subject_name} {session}".strip(),
                            lookup_label=f"Studied state {subject_name} {session}".strip()
                        )
                        globals.collection.add(state)
                        state_cache_dict[f"{session}"] = state
                        state_cache.append(state)
            subject_state_dict[f"{subject}"] = state_cache_dict
            subject_cache = omcore.Subject(
                lookup_label=f"{subject_name}",
                internal_identifier=f"{subject_name}"
            )
            subjects_dict[f"{subject}"] = subject_cache
            subjects_list.append(subject_cache)
            globals.collection.add(subject_cache)


        return subjects_dict, subject_state_dict, subjects_list


    # Select the tsv file of the table
    participants_path_tsv = pd_table_value(table_filter(participants_paths, ".tsv", "extension"), "path")
    participants_path_json = pd_table_value(table_filter(participants_paths, ".json", "extension"), "path")

    participants_table = pd.read_csv(participants_path_tsv, sep="\t", header=0)
    for subject in subject_id:
        subject_name = f"sub-{subject}"
        data_subject = table_filter(participants_table, subject_name, "participant_id")
        state_cache_dict = {}
        state_cache = []
        if not sessions:
            state = omcore.SubjectState(
                age=create_openminds_age(data_subject),
                handedness=bids2openminds_instance(pd_table_value(data_subject, "handedness"), "MAP_2_HANDEDNESS", is_list=False),
                internal_identifier=f"Studied state {subject_name}".strip(),
                lookup_label=f"Studied state {subject_name}".strip()
                )
            globals.collection.add(state)
            state_cache_dict[""] = state
            state_cache.append(state)
        else:
            for session in sessions:
                if not(table_filter(table_filter(layout_df,session,"session"),subject,"subject").empty):
                    state = omcore.SubjectState(
                        age=create_openminds_age(data_subject),
                        handedness=bids2openminds_instance(pd_table_value(data_subject, "handedness"), "MAP_2_HANDEDNESS", is_list=False),
                        internal_identifier=f"Studied state {subject_name} {session}".strip(),
                        lookup_label=f"Studied state {subject_name} {session}".strip()
                    )
                    globals.collection.add(state)
                    state_cache_dict[f"{session}"] = state
                    state_cache.append(state)
            subject_state_dict[f"{subject}"] = state_cache_dict
        subject_cache = omcore.Subject(
            biological_sex=bids2openminds_instance(pd_table_value(data_subject, "sex"), "MAP_2_SEX", is_list=False),
            lookup_label=f"{subject_name}",
            internal_identifier=f"{subject_name}",
            # TODO species should default to homo sapiens
            species=bids2openminds_instance(pd_table_value(data_subject, "species"), "MAP_2_SPECIES", is_list=False),
            studied_states=state_cache
        )
        subjects_dict[f"{subject}"] = subject_cache
        subjects_list.append(subject_cache)
        globals.collection.add(subject_cache)

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
        extension = file["extension"]
        path = file["path"]
        iri=IRI(pathlib.Path(path).as_uri())
        name=os.path.basename(path)
        hashes = file_hash(path)
        storage_size = file_storage_size(path)
        if pd.isna(file["subject"]):
            if file["suffix"] == "participants":
                if extension == ".json":
                    content_description = f"A JSON metadata file of participants TSV."
                    data_types = controlled_terms.DataType.by_name("associative array")
                    file_format = omcore.ContentType.by_name("application/json")
                elif extension == [".tsv"]:
                    content_description = f"A metadata table for participants."
                    data_types = controlled_terms.DataType.by_name("table")
                    file_format = omcore.ContentType.by_name("text/tab-separated-values")
        else:
            if extension == ".json":
                content_description = f"A JSON metadata file for {file['suffix']} of subject {file['subject']}"
                data_types = controlled_terms.DataType.by_name("associative array")
                file_format = omcore.ContentType.by_name("application/json")
            elif extension in [".nii", ".nii.gz"]:
                content_description = f"Data file for {file['suffix']} of subject {file['subject']}"
                data_types = controlled_terms.DataType.by_name("voxel data")
                # file_format=omcore.ContentType.by_name("nifti")
            elif extension == [".tsv"]:
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
