import os


def create_report(dataset, dataset_version, collection, dataset_description, input_path):
    print(f"Dataset title : {dataset.full_name}")
    print("Authors : ")
    for author in dataset_version.authors:
        print(f"{author.given_name} {author.family_name}")

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

    print("This dataset contains following items:")
    print(f"Number of subjects : {subject_number}")
    print(f"Number of files : {files_number}")
#    print(f"Number of file bundles : {file_bundle_number}")

    if "GeneratedBy" in dataset_description:
        print("This dataset is derivative. The derivative section of BIDS specification is not final yet, so conversion is not complete. The generated openMINDS file should be treated carefully.")

    derivatives_path = os.path.join(
        input_path, "derivatives")
    if os.path.isdir(derivatives_path):
        print("This dataset contains derivative. The derivative section of BIDS specification is not final yet, so conversion is not complete. The generated openMINDS file should be treated carefully.")
