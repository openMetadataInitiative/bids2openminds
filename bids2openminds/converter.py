from warnings import warn
from bids import BIDSLayout, BIDSValidator
import os
import click
from . import main
from . import utility
from . import globals


@click.command()
@click.argument('input_path', type=click.Path(file_okay=False,exists=True))
@click.option('-o','--output_path',default=None,type=click.Path(file_okay=True,writable=True),help="The output path or file name for openMINDS file/files.")
@click.option('--single-file','output_type',flag_value=True,default=False,help="Save the entire collection into a single file (default)")
@click.option('--multiple-file','output_type',flag_value=True,help="Each node is saved into a separate file within that directory, `output_path` must be a directory.")
@click.option("--include_empty_properties/--no-include_empty_properties",default=False)
def convert(input_path,output_path,output_type,include_empty_properties):
    #bids_dir, output_filename=None
    print(input_path)
    if not (os.path.isdir(input_path)):
        raise NotADirectoryError(
            f"The input directory is not valid, you have specified {input_path} which is not a directory."
        )
    # if not(BIDSValidator().is_bids(input_path)):
    #  raise NotADirectoryError(f"The input directory is not valid, you have specified {input_path} which is not a BIDS directory.")

    bids_layout = BIDSLayout(input_path)

    layout_df = bids_layout.to_df()

    subjects_id = bids_layout.get_subjects()

    tasks = bids_layout.get_task()

    # imprting the dataset description file containing some of the
    dataset_description_path = utility.table_filter(layout_df, "description")

    dataset_description = utility.read_json(dataset_description_path.iat[0, 0])

    [subjects_dict, subject_state_dict, subjects_list] = main.create_subjects(subjects_id, layout_df, bids_layout)

    [files_list, file_repository] = main.create_file(layout_df, input_path)

    dataset_version = main.create_dataset_version(
        bids_layout, dataset_description, layout_df, subjects_list, file_repository
    )

    dataset = main.create_dataset(dataset_description, dataset_version)
    
    failures = globals.collection.validate(ignore=["required", "value"])
    assert len(failures) == 0

    if output_path is None:
        if output_type:
            output_path=os.path.join(input_path, "openminds")
        else:
            output_path = os.path.join(input_path, "openminds.jsonld")

    globals.collection.save(output_path,individual_files=output_type,include_empty_properties=include_empty_properties)

    print(f"Convertion was succesfull, the openMINDS file is in {output_path}")


if __name__ == "__main__":
    input_path = input("Enter the BIDS directory path: ")
    convert(input_path)
