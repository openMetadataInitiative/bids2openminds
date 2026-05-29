import re
import os
import pathlib
from warnings import warn

import pandas as pd
from nameparser import HumanName

from openminds import IRI

from .utility import table_filter, pd_table_value, file_hash, file_storage_size, detect_nifti_version
from . import mapping
from . import openminds_version as om


def create_openminds_person(full_name):
    # Regex for detecting any unwanted characters.
    name_regex = re.compile(
        r"^[\w'\-, .][^0-9_!¡?÷?¿/\\+=@#$%^&*(){}|~<>;:[\]]{1,}$")
    alternate_names = []
    person = HumanName(full_name)
    given_name = person.first
    family_name = person.last

    # Handle the situation in which there is no given name or the given name consists of unwanted characters.
    if not (given_name and name_regex.match(given_name)):
        if not (len(family_name) > 0 and len(given_name) == 1):
            return None

    # Handle the situation in which the family name consists of unwanted characters.
    if not (name_regex.match(family_name)):
        family_name = None

    if person.middle:
        given_name = f"{given_name} {person.middle}"

    if person.nickname:
        alternate_names.append(person.nickname)

    if not alternate_names:
        alternate_names = None

    person_kwargs = dict(
        alternate_names=alternate_names, given_name=given_name, family_name=family_name)
    if om.version == "v5":
        # In v5 `preferred_name` is the required identifying property of a Person;
        # use the original full name string as supplied in the BIDS metadata.
        person_kwargs["preferred_name"] = full_name
    openminds_person = om.core.Person(**person_kwargs)

    return openminds_person


def create_persons(dataset_description, collection):

    if "Authors" in dataset_description:
        person_list = dataset_description["Authors"]
    else:
        return None

    if not (isinstance(person_list, list)):
        # handel's only one name
        if isinstance(person_list, str):
            openminds_person = create_openminds_person(person_list)
            if openminds_person is not None:
                collection.add(openminds_person)
            return openminds_person
        else:
            return None

    openminds_list = []
    for person in person_list:
        openminds_person = create_openminds_person(person)
        if openminds_person is not None:
            openminds_list.append(openminds_person)
            collection.add(openminds_person)

    return openminds_list


def create_behavioral_protocol(layout, collection):
    behavioral_protocols_dict = {}
    behavioral_protocols = []
    tasks = layout.get_tasks()

    if not tasks:
        return None, None

    for task in tasks:

        behavioral_protocol = om.core.BehavioralProtocol(name=task,
                                                        internal_identifier=task,
                                                        description="To be defined")
        behavioral_protocols.append(behavioral_protocol)
        behavioral_protocols_dict[task] = behavioral_protocol
        collection.add(behavioral_protocol)

    return behavioral_protocols, behavioral_protocols_dict


def techniques_openminds(suffix):
    # TODO "MRIPulseSequence" and "MRIWeighting" should be added as soon as openMINDS v4 becomes available.
    possible_types = ["Technique", "AnalysisTechnique", "StimulationApproach",
                      "StimulationTechnique"]

    if suffix in mapping.MAP_2_TECHNIQUES:
        items_openminds = mapping.MAP_2_TECHNIQUES[suffix]
    else:
        return []

    if items_openminds is None:
        return []

    openminds_techniques_list = []
    for item_openminds in items_openminds:
        for possible_type in possible_types:
            openminds_type = getattr(om.controlled_terms, possible_type)
            openminds_obj = None
            try:
                openminds_obj = openminds_type.by_name(item_openminds)
                break
            except KeyError:
                pass
        if openminds_obj:
            openminds_techniques_list.append(openminds_obj)
    return openminds_techniques_list


def create_techniques(layout_df):
    suffixs = layout_df["suffix"].unique().tolist()
    techniques = []
    not_techniques_index = ["description", "participants", "events"]
    for suffix in suffixs:
        # excluding the None and non thechnique indexes
        if not (pd.isnull(suffix) or (suffix in not_techniques_index)):
            openminds_techniques_cache = techniques_openminds(suffix)
            techniques.extend(openminds_techniques_cache)

    techniques_set = set(techniques)
    techniques_list = list(techniques_set)
    return techniques_list or None


def approaches_openminds(datatype):

    if datatype in mapping.MAP_2_EXPERIMENTAL_APPROACHES:
        items_openminds = mapping.MAP_2_EXPERIMENTAL_APPROACHES[datatype]

    approches_list = []

    for item in items_openminds:
        approches_list.append(
            om.controlled_terms.ExperimentalApproach.by_name(item))

    return approches_list


def create_approaches(layout_df):
    datatypes = layout_df["datatype"].unique().tolist()
    approaches = set([])
    for datatype in datatypes:
        if not (pd.isnull(datatype)):
            approaches.update(approaches_openminds(datatype))

    return list(approaches) or None


def create_openminds_age(data_subject):

    try:
        age = pd_table_value(data_subject, "age")
    except:
        return None

    if age is None or pd.isna(age):
        return None
    elif isinstance(age, float) or isinstance(age, int) or age.isnumeric():
        age_value = om.core.QuantitativeValue(
            value=age,
            unit=om.controlled_terms.UnitOfMeasurement.year
        )
    elif age == "89+":
        age_value = om.core.QuantitativeValueRange(
            max_value=None,
            min_value=89,
            min_value_unit=om.controlled_terms.UnitOfMeasurement.year
        )
    else:
        return None

    if om.version == "v4":
        return age_value
    # In v5, SubjectState.age expects a SpecimenAge wrapping the quantitative value;
    # BIDS records age since birth.
    return om.core.SpecimenAge(
        age=age_value,
        reference=om.controlled_terms.AgeReference.by_name("birth")
    )


def create_dataset_version(bids_layout, dataset_description, layout_df, studied_specimens, file_repository, behavioral_protocols, collection):

    # Fetch the dataset type from dataset description file

    # dataset_type=bids2openminds_instance(dataset_description.get("DatasetType",None))

    # Fetch the digitalIdentifier from dataset description file

    if "DatasetDOI" in dataset_description:
        digital_identifier = om.core.DOI(
            identifier=dataset_description["DatasetDOI"])
    else:
        digital_identifier = None

    authors = create_persons(dataset_description, collection)

    if "Acknowledgements" in dataset_description:
        other_contribution = dataset_description["Acknowledgements"]
    else:
        other_contribution = None

    if "HowToAcknowledge" in dataset_description:
        how_to_cite = dataset_description["HowToAcknowledge"]
    else:
        how_to_cite = None

    if ("DatasetType" in dataset_description) and (dataset_description == "derivative"):
        dataset_type = om.controlled_terms.SemanticDataType.derived_data
    else:
        dataset_type = om.controlled_terms.SemanticDataType.raw_data

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

    common_properties = dict(
        digital_identifier=digital_identifier,
        experimental_approaches=experimental_approaches,
        short_name=dataset_description["Name"],
        full_name=dataset_description["Name"],
        studied_specimens=studied_specimens,
        techniques=techniques,
        how_to_cite=how_to_cite,
        repository=file_repository,
        data_types=dataset_type
        # other_contributions=other_contribution  # needs to be a Contribution object
        # version_identifier
    )
    if om.version == "v4":
        dataset_version = om.core.DatasetVersion(
            authors=authors,
            behavioral_protocols=behavioral_protocols,
            **common_properties
        )
    else:
        # v5 replaced `authors` with `contributions` and merged the v4
        # `behavioral_protocols` property into the general `protocols` property
        # (openMINDS_core #377), which now accepts both BehavioralProtocol and Protocol.
        # `or None` avoids passing an empty list, which would trip the schema's
        # minItems=1 constraint on `protocols` for datasets with no task labels.
        dataset_version = om.core.DatasetVersion(
            contributions=_authors_to_contributions(authors),
            protocols=behavioral_protocols or None,
            **common_properties
        )

    collection.add(dataset_version)

    return dataset_version


def _authors_to_contributions(authors):
    """Wrap author Persons in an openMINDS v5 Contribution with the "authoring" role.

    In v5 the `DatasetVersion`/`Dataset` `authors` property was replaced by
    `contributions`, a list of `Contribution` objects each pairing one or more
    contributors with a `ContributionType`. BIDS only records who the authors are,
    so they are all mapped to a single contribution of type "authoring".

    Parameters:
    - authors: a list of Person objects, a single Person, or None (as returned by
      :func:`create_persons`).

    Returns:
    - list[Contribution] or None: None when there are no authors.
    """
    if not authors:
        return None
    if not isinstance(authors, list):
        authors = [authors]
    return [
        om.core.Contribution(
            contributors=authors,
            type=om.controlled_terms.ContributionType.by_name("authoring")
        )
    ]


def create_dataset(dataset_description, dataset_version, collection):

    if om.version == "v4":
        dataset = om.core.Dataset(
            digital_identifier=dataset_version.digital_identifier,
            authors=dataset_version.authors,
            full_name=dataset_version.full_name,
            short_name=dataset_version.short_name,
            has_versions=dataset_version
        )
    else:
        # v5 replaced `authors` with `contributions` and removed `has_versions`;
        # the version-to-dataset link is expressed on the DatasetVersion instead.
        dataset = om.core.Dataset(
            digital_identifier=dataset_version.digital_identifier,
            contributions=dataset_version.contributions,
            full_name=dataset_version.full_name,
            short_name=dataset_version.short_name
        )
        dataset_version.is_version_of = dataset

    collection.add(dataset)

    return dataset


def spices_openminds(data_subject: pd.DataFrame):
    bids_species = pd_table_value(data_subject, "species")
    if bids_species is None:
        # In BIDS the default species is homo sapiens.
        return om.controlled_terms.Species.homo_sapiens
    if bids_species in mapping.MAP_2_SPECIES:
        openminds_species = mapping.MAP_2_SPECIES[bids_species]
        return om.controlled_terms.Species.by_name(openminds_species[0])
    else:
        try:
            openminds_species = om.controlled_terms.Species.by_name(bids_species)
            warn(
                f"You have specified {bids_species} as species, we have autodetected {openminds_species.name}, please verify it.")
            return openminds_species
        except KeyError:
            warn(
                f"You have specified {bids_species} we currently don't support this species.")
        return None


def handedness_openminds(data_subject: pd.DataFrame):
    bids_handedness = pd_table_value(data_subject, "handedness")
    if bids_handedness is None:
        return None
    if bids_handedness in mapping.MAP_2_HANDEDNESS:
        openminds_handedness = mapping.MAP_2_HANDEDNESS[bids_handedness]
        return om.controlled_terms.Handedness.by_name(openminds_handedness[0])
    else:
        warn(
            f"You have specified {bids_handedness} which is not a allowed value for handedness defined by BIDS standard.")
        return None


def sex_openminds(data_subject: pd.DataFrame):
    bids_sex = pd_table_value(data_subject, "sex")
    if bids_sex is None:
        return None
    if bids_sex in mapping.MAP_2_BIOLOGICALSEX:
        bids_sex = mapping.MAP_2_BIOLOGICALSEX[bids_sex]
        return om.controlled_terms.BiologicalSex.by_name(bids_sex[0])
    else:
        warn(
            f"You have specified {bids_sex} which is not a allowed value for handedness defined by BIDS standard.")
        return None


def create_subjects(subject_id, layout_df, layout, collection):

    sessions = layout.get_sessions()
    subjects_dict = {}
    subjects_list = []
    subject_state_dict = {}

    # Find the participants files in the files table
    participants_paths = table_filter(layout_df, "participants")
    if participants_paths.empty:
        # creating emphty subjects just based on file structure
        for subject in subject_id:
            subject_name = f"sub-{subject}"
            state_cache_dict = {}
            state_cache = []
            # dealing with condition that have no seasion
            if not sessions:
                state = om.core.SubjectState(
                    internal_identifier=f"Studied state {subject_name}".strip(
                    ),
                    lookup_label=f"Studied state {subject_name}".strip()
                )
                collection.add(state)
                state_cache_dict[""] = state
                state_cache.append(state)
            else:
                # create a subject state for each state
                for session in sessions:
                    if not (table_filter(table_filter(layout_df, session, "session"), subject, "subject").empty):
                        state = om.core.SubjectState(
                            internal_identifier=f"Studied state {subject_name} {session}".strip(
                            ),
                            lookup_label=f"Studied state {subject_name} {session}".strip(
                            )
                        )
                        collection.add(state)
                        state_cache_dict[f"{session}"] = state
                        state_cache.append(state)
            subject_state_dict[f"{subject}"] = state_cache_dict
            subject_cache = om.core.Subject(
                lookup_label=f"{subject_name}",
                internal_identifier=f"{subject_name}",
                studied_states=state_cache
            )
            subjects_dict[f"{subject}"] = subject_cache
            subjects_list.append(subject_cache)
            collection.add(subject_cache)

        return subjects_dict, subject_state_dict, subjects_list

    # Select the tsv file of the table
    participants_path_tsv = pd_table_value(table_filter(
        participants_paths, ".tsv", "extension"), "path")

    participants_table = pd.read_csv(participants_path_tsv, sep="\t", header=0)
    for subject in subject_id:
        subject_name = f"sub-{subject}"
        data_subject = table_filter(
            participants_table, subject_name, "participant_id")
        state_cache_dict = {}
        state_cache = []
        if not sessions:
            state = om.core.SubjectState(
                age=create_openminds_age(data_subject),
                handedness=handedness_openminds(data_subject),
                internal_identifier=f"Studied state {subject_name}".strip(),
                lookup_label=f"Studied state {subject_name}".strip()
            )
            collection.add(state)
            state_cache_dict[""] = state
            state_cache.append(state)
        else:
            for session in sessions:
                if not (table_filter(table_filter(layout_df, session, "session"), subject, "subject").empty):
                    state = om.core.SubjectState(
                        age=create_openminds_age(data_subject),
                        handedness=handedness_openminds(data_subject),
                        internal_identifier=f"Studied state {subject_name} {session}".strip(
                        ),
                        lookup_label=f"Studied state {subject_name} {session}".strip(
                        )
                    )
                    collection.add(state)
                    state_cache_dict[f"{session}"] = state
                    state_cache.append(state)
            subject_state_dict[f"{subject}"] = state_cache_dict
        subject_cache = om.core.Subject(
            biological_sex=sex_openminds(data_subject),
            lookup_label=f"{subject_name}",
            internal_identifier=f"{subject_name}",
            # TODO species should default to homo sapiens
            species=spices_openminds(data_subject),
            studied_states=state_cache
        )
        subjects_dict[f"{subject}"] = subject_cache
        subjects_list.append(subject_cache)
        collection.add(subject_cache)

    return subjects_dict, subject_state_dict, subjects_list


def create_file_bundle(BIDS_path, path, collection, parent_file_bundle=None, is_file_repository=False):

    if is_file_repository:
        openminds_file_bundle = om.core.FileRepository(format=om.core.ContentType.by_name("application/vnd.bids"),
                                                      iri=IRI(pathlib.Path(BIDS_path).absolute().as_uri()))
    else:
        relative_path = os.path.relpath(path, BIDS_path)
        name = str(relative_path).replace("\\", "/")
        if name[0] == "_":
            name = name[1:]
        openminds_file_bundle = om.core.FileBundle(content_description=f"File bundle created for {relative_path}",
                                                  name=name,
                                                  is_part_of=parent_file_bundle)

    files = {}
    files_size = 0
    all = os.listdir(path)

    for item in all:

        item_path = str(pathlib.PurePath(path, item))

        if os.path.isfile(item_path) and os.path.basename(item_path) != "openminds.jsonld":

            if is_file_repository:
                files[item_path] = None
            else:
                files[item_path] = [openminds_file_bundle]

            files_size += os.stat(item_path).st_size

        if os.path.isdir(item_path) and os.path.basename(item_path) != "openminds":

            child_files, child_filesizes, _ = create_file_bundle(
                BIDS_path, item_path, collection, parent_file_bundle=openminds_file_bundle, is_file_repository=False)

            for child_file_path in child_files.keys():
                if child_file_path not in files:
                    files[child_file_path] = []

                files[child_file_path].extend(child_files[child_file_path])

            files_size += child_filesizes

    openminds_file_bundle.storage_size = om.core.QuantitativeValue(value=files_size,
                                                                  unit=om.controlled_terms.UnitOfMeasurement.by_name(
                                                                      "byte")
                                                                  )
    collection.add(openminds_file_bundle)

    if is_file_repository:
        openminds_file_repository = openminds_file_bundle
    else:
        openminds_file_repository = None

    return files, files_size, openminds_file_repository


def create_file(layout_df, BIDS_path, collection):

    BIDS_path_absolute = pathlib.Path(BIDS_path).absolute()

    file2file_bundle_dic, _, file_repository = create_file_bundle(
        BIDS_path_absolute, BIDS_path_absolute, collection, is_file_repository=True)

    files_list = []
    for index, file in layout_df.iterrows():
        file_format = None
        content_description = None
        data_types = None
        extension = file["extension"]
        path = file["path"]
        iri = IRI(pathlib.Path(path).absolute().as_uri())
        name = os.path.basename(path)
        hashes = file_hash(path)
        storage_size_obj, file_size = file_storage_size(path)
        if pd.isna(file["subject"]):
            if file["suffix"] == "participants":
                if extension == ".json":
                    content_description = f"A JSON metadata file of participants TSV."
                    data_types = om.controlled_terms.DataType.by_name(
                        "associative array")
                    file_format = om.core.ContentType.by_name(
                        "application/json")
                elif extension == [".tsv"]:
                    content_description = f"A metadata table for participants."
                    data_types = om.controlled_terms.DataType.by_name("table")
                    file_format = om.core.ContentType.by_name(
                        "text/tab-separated-values")
        else:
            if extension == ".json":
                content_description = f"A JSON metadata file for {file['suffix']} of subject {file['subject']}"
                data_types = om.controlled_terms.DataType.by_name(
                    "associative array")
                file_format = om.core.ContentType.by_name("application/json")
            elif extension in [".nii", ".nii.gz"]:
                content_description = f"Data file for {file['suffix']} of subject {file['subject']}"
                data_types = om.controlled_terms.DataType.by_name("voxel data")
                file_format = detect_nifti_version(path, extension, file_size)
            elif extension == [".tsv"]:
                if file["suffix"] == "events":
                    content_description = f"Event file for {file['suffix']} of subject {file['subject']}"
                    data_types = om.controlled_terms.DataType.by_name(
                        "event sequence")
                    file_format = om.core.ContentType.by_name(
                        "text/tab-separated-values")

        file = om.core.File(
            iri=iri,
            content_description=content_description,
            data_types=data_types,
            file_repository=file_repository,
            format=file_format,
            hashes=hashes,
            is_part_of=file2file_bundle_dic[str(
                pathlib.Path(path))],
            name=name,
            # special_usage_role
            storage_size=storage_size_obj,
        )
        collection.add(file)
        files_list.append(file)

    return files_list, file_repository
