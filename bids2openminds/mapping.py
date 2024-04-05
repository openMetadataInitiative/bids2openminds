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
        "neuroimaging"
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
    "inplaneT1": None, #TODO instance TBD
    "inplaneT2": None, #TODO instance TBD
    "R1map": None, #TODO instance TBD
    "T1map": None, #TODO instance TBD
    "MTVmap": None, #TODO instance TBD
    "MTRmap": ["magnetization transfer imaging"], #TODO instance TBD
    "MTsat": ["magnetization transfer imaging"], #TODO instance TBD
    "MWFmap": ["Myelin water fraction image"],
    "S0map": ["Observed signal amplitude (S0) image"],
    "R2starmap": ["Observed transverse relaxation rate image"],
    "T2starmap": ["Observed transverse relaxation time image"],
    "PDT2": ["PD and T2 weighted image"],
    "PDw": ["Proton density (PD) weighted image"],
    "PD": ["Proton density image"],
    "PDmap": ["Proton density image"],
    "Chimap": ["Quantitative susceptibility map (QSM)"],
    "RB1map": ["RF receive sensitivity map"],
    "TB1map": ["RF transmit field image"],
    "T1rho": ["T1 in rotating frame (T1 rho) image"],
    "T1w": ["T1 pulse sequence"],
    "T2w": ["T2 pulse sequence"],
    "T2star": ["T2* pulse sequence"], #TODO instance TBD
    "T2starw": ["T2* pulse sequence"], #TODO instance TBD
    "R2map": ["True transverse relaxation rate image"],
    "T2map": ["True transverse relaxation time image"],
    "bold": ["Blood-Oxygen-Level Dependent image"],
    "cbv": ["Cerebral blood volume image"],
    "phase": ["Phase image"],
    "defacemask": ["Defacing masks"],
    "epi": ["EPI"],
    "fieldmap": ["Fieldmap"],
    "magnitude": ["Magnitude"],
    "magnitude1": ["Magnitude"],
    "magnitude2": ["Magnitude"],
    "phase1": ["Phase"],
    "phase2": ["Phase"],
    "phasediff": ["Phase-difference"],
    "dwi": ["@id: https://openminds.ebrains.eu/instances/technique/diffusionWeightedImaging"],
    "sbref": ["Single-band reference image"],
    "asl": ["Arterial Spin Labeling"],
    "m0scan": ["M0"],
    "eeg": ["@id:https://openminds.ebrains.eu/instances/technique/electroencephalography"],
    "ieeg": ["Intracranial Electroencephalography"],
    "physio": ["Physiological continuous recordings"],
    "stim": ["stimulation continuous recordings"],
    "beh": ["Behavioral experiments"],
    "pet": ["@id:https://openminds.ebrains.eu/instances/technique/positronEmissionTomography"],
    "2PE": ["2-photon excitation microscopy"],
    "BF": ["Bright-field microscopy"],
    "CARS": ["Coherent anti-Stokes Raman spectroscopy"],
    "CONF": ["Confocal microscopy"],
    "DIC": ["Differential interference contrast microscopy"],
    "DF": ["Dark-field microscopy"],
    "FLUO": ["Fluorescence microscopy"],
    "MPE": ["Multi-photon excitation microscopy"],
    "NLO": ["Nonlinear optical microscopy"],
    "OCT": ["Optical coherence tomography"],
    "PC": ["Phase-contrast microscopy"],
    "PLI": ["Polarized-light microscopy"],
    "SEM": ["Scanning electron microscopy"],
    "SPIM": ["Selective plane illumination microscopy"],
    "SR": ["Super-resolution microscopy"],
    "TEM": ["Transmission electron microscopy"],
    "uCT": ["Micro-CT"],
    "nirs": ["Near-Infrared Spectroscopy"],
    "motion": ["Motion"]
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
#    "cell line",
#    "in vitro differentiated cells",
#    "primary cell",
#    "cell-free sample",
#    "cloning host",
#    "tissue",
#    "whole organisms",
#    "organoid",
#    "technical sample"
#}
