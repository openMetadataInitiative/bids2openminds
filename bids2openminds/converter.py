from warnings import warn
from bids import BIDSLayout, BIDSValidator
import os
from . import main
from . import utility
from . import globals



def convert(bids_dir, output_filename=None):

    if not (os.path.isdir(bids_dir)):
        raise NotADirectoryError(
            f"The input directory is not valid, you have specified {bids_dir} which is not a directory."
        )

    # if not(BIDSValidator().is_bids(bids_dir)):
    #  raise NotADirectoryError(f"The input directory is not valid, you have specified {bids_dir} which is not a BIDS directory.")

    bids_layout = BIDSLayout(bids_dir)

    layout_df = bids_layout.to_df()

    subjects_id = bids_layout.get_subjects()

    tasks = bids_layout.get_task()

    # imprting the dataset description file containing some of the
    dataset_description_path = utility.table_filter(layout_df, "description")

    dataset_description = utility.read_json(dataset_description_path.iat[0, 0])

    [subjects_dict, subject_state_dict, subjects_list] = main.create_subjects(subjects_id, layout_df, bids_layout)

    [files_list, file_repository] = main.create_file(layout_df, bids_dir)

    dataset_version = main.create_dataset_version(
        bids_layout, dataset_description, layout_df, subjects_list, file_repository
    )

    dataset = main.create_dataset(dataset_description, dataset_version)

    failures = globals.collection.validate(ignore=["required", "value"])
    assert len(failures) == 0

    if output_filename is None:
        output_filename = os.path.join(bids_dir, "openminds.jsonld")
    globals.collection.save(output_filename)


if __name__ == "__main__":
    bids_dir = input("Enter the BIDS directory path: ")
    convert(bids_dir)
