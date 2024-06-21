MAP_2_EXPERIMENTAL_APPROACHES = {
    "func": ["neuroimaging"],
    "dwi": [
        "neuroimaging",
        "neural connectivity",
        "anatomy"
    ],
    "fmap": ["neuroimaging"],
    "anat": [
        "neuroimaging",
        "anatomy"
    ],
    "perf": [
        "neuroimaging",
        "anatomy"
    ],
    "meg": ["neuroimaging"],
    "eeg": ["electrophysiology"],
    "ieeg": ["electrophysiology"],
    "beh": ["behavior"],
    "pet": [
        "neuroimaging",
        "radiology"
    ],
    "micr": [
        "microscopy",
        "anatomy",
        "histology"
    ],
    "nirs": ["neuroimaging"]
}

MAP_2_TECHNIQUES = {
    "angio": ["angiography"],
    "M0map": ["equilibrium magnetization mapping"],
    "FLASH": ["fast-low-angle-shot pulse sequence"], #TODO instance TBD
    "FLAIR": ["fluid attenuated inversion recovery pulse sequence"], #TODO instance TBD
    "UNIT1": None, #TODO instance TBD
    "inplaneT1": [
        "T1 pulse sequence", 
        "structural magnetic resonance imaging"
    ], #TODO sMRI
    "inplaneT2": [
        "T2 pulse sequence", 
        "structural magnetic resonance imaging"
    ], #TODO sMRI
    "R1map": None, #TODO instance TBD
    "T1map": None, #TODO instance TBD
    "MTVmap": [
        "quantitative magnetic resonance imaging",
        "macromolecular tissue volume image processing"
    ], #TODO other?
    "MTRmap": [
        "magnetization transfer imaging",
        "magnetization transfer ratio image processing",
        "magnetization transfer pulse sequence"
    ], #TODO instances
    "MTsat": [
        "magnetization transfer imaging",
        "magnetization transfer saturation image processing",
        "magnetization transfer pulse sequence"
    ], #TODO instances
    "MWFmap": [
        "myelin water imaging",
        "T2 pulse sequence",
        "myelin water fraction image processing"
    ], #TODO instances
    "S0map": None, #TODO instances
    "R2starmap": None, #TODO instance TBD
    "T2starmap": None, #TODO instance TBD
    "PDT2": None, #TODO instance TBD
    "PDw": None, #TODO instance TBD
    "PD": None, #TODO instance TBD
    "PDmap": None, #TODO instance TBD
    "Chimap": None, #TODO instance TBD
    "RB1map": None, #TODO instance TBD
    "TB1map": None, #TODO instance TBD
    "T1rho": None, #TODO instance TBD
    "T1w": None, #TODO instance TBD
    "T2w": None, #TODO instance TBD
    "T2star": None, #TODO instance TBD
    "T2starw": None, #TODO instance TBD
    "R2map": None, #TODO instance TBD
    "T2map": None, #TODO instance TBD
    "bold": None, #TODO instance TBD
    "cbv": None, #TODO instance TBD
    "phase": None, #TODO instance TBD
    "defacemask": None, #TODO instance TBD
    "epi": None, #TODO instance TBD
    "fieldmap": None, #TODO instance TBD
    "magnitude": None, #TODO instance TBD
    "magnitude1": None, #TODO instance TBD
    "magnitude2": None, #TODO instance TBD
    "phase1": None, #TODO instance TBD
    "phase2": None, #TODO instance TBD
    "phasediff": None, #TODO instance TBD
    "dwi": ["diffusion-weighted imaging"],
    "sbref": None, #TODO instance TBD
    "asl": None, #TODO instance TBD
    "m0scan": None, #TODO instance TBD
    "eeg": ["electroencephalography"],
    "ieeg": ["intracranial electroencephalography"],
    "physio": None, #TODO instance TBD
    "stim": None, #TODO instance TBD
    "beh": None, #TODO instance TBD
    "pet": ["positron emission tomography"],
    "2PE": ["two-photon fluorescence microscopy"],
    "BF": None, #TODO instance TBD
    "CARS": None, #TODO instance TBD
    "CONF": ["confocal microscopy"],
    "DIC": None, #TODO instance TBD
    "DF": None, #TODO instance TBD
    "FLUO": None, #TODO instance TBD
    "MPE": None, #TODO instance TBD
    "NLO": None, #TODO instance TBD
    "OCT": None, #TODO instance TBD
    "PC": None, #TODO instance TBD
    "PLI": ["polarized light microscopy"],
    "SEM": None, #TODO instance TBD
    "SPIM": None, #TODO instance TBD
    "SR": None, #TODO instance TBD
    "TEM": ["transmission electron microscopy"],
    "uCT": None, #TODO instance TBD
    "nirs": None, #TODO instance TBD
    "motion": None, #TODO instance TBD
}

MAP_2_UNITS = {
    "year": ["year"]
}

MAP_2_BIOLOGICALSEX = {
    "male": ["male"],
    "m": ["male"],
    "M": ["male"],
    "MALE": ["male"],
    "Male": ["male"],
    "female": ["female"],
    "f": ["female"],
    "F": ["female"],
    "FEMALE": ["female"],
    "Female": ["female"]
}

MAP_2_HANDEDNESS = {
    "left": ["left handedness"],
    "l": ["left handedness"],
    "L": ["left handedness"],
    "LEFT": ["left handedness"],
    "Left": ["left handedness"],
    "right": ["right handedness"],
    "r": ["right handedness"],
    "R": ["right handedness"],
    "RIGHT": ["right handedness"],
    "Right": ["right handedness"],
    "ambidextrous": ["ambidextrous handedness"],
    "a": ["ambidextrous handedness"],
    "A": ["ambidextrous handedness"],
    "AMBIDEXTROUS": ["ambidextrous handedness"],
    "Ambidextrous": ["ambidextrous handedness"]
}

MAP_2_SPECIES = {
    "homo sapiens": ["Homo sapiens"],
    "mus musculus": ["Mus musculus"],
    "rattus norvegicus": ["Rattus norvegicus"]
}


#sample_types = {
#    "cell line": None, #TODO instance TBD
#    "in vitro differentiated cells": None, #TODO instance TBD
#    "primary cell": None, #TODO instance TBD
#    "cell-free sample": None, #TODO instance TBD
#    "cloning host": None, #TODO instance TBD
#    "tissue": None, #TODO instance TBD
#    "whole organisms": None, #TODO instance TBD
#    "organoid": None, #TODO instance TBD
#    "technical sample": None #TODO instance TBD
#}
