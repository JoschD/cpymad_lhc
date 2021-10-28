"""
Coupling Knob
------------------

Creates a coupling knob from current optics.
Not implemented yet. TODO!
"""

from operator import itemgetter
from typing import Sequence

# from optics_functions.coupling import coupling_via_cmatrix
import pandas as pd
from cpymad.madx import Madx
import numpy as np

import logging

LOG = logging.getLogger(__name__)

COL_REFERENCE = "Reference"

def create(madx: Madx, knobs: Sequence[str], dependant_knobs:dict):
    # get F1001, F1010 from cmatrix
    # define varying parameters: knob = knob_init + vary
    #
    pass

def replace_k0(attribute):
    replacements_map = {"k0l": "angle", "k0sl": "tilt"}
    if attribute in replacements_map.keys():
        new_attribute = replacements_map[attribute]
        LOG.info(f"Attribute {attribute} is being replaced with {new_attribute}")
        attribute = new_attribute


def get_attribute_response(madx: Madx, sequence: str, variables: Sequence[str], attribute: str) -> pd.DataFrame:
    """ Creates the linear response matrix of the given `variables` for the desired `attributed`. """
    # find elements in sequence that have the attribute defined
    valid_elements = {e.name: idx for idx, e in enumerate(madx.sequence[sequence].elements) if attribute in e}
    if not len(valid_elements):
        raise AttributeError(f"No elements found in sequence '{sequence}' with attribute '{attribute}'.")

    get_valid_elements = itemgetter(*valid_elements.values())

    def get_attribute_values():
        return np.array([e[attribute] for e in get_valid_elements(madx.sequence[sequence].elements)])

    # create DataFrame
    df = pd.DataFrame(index=valid_elements.keys(), columns=variables)

    # all-zero reference
    for var in variables:
        madx.globals[var] = 0
    reference = get_attribute_values()

    # responses
    for var in variables:
        madx.globals[var] = 1
        df[var] = get_attribute_values() - reference
        madx.globals[var] = 0

    # drop all-zero rows
    df = df.loc[(df!=0).any(axis=1)]
    return df
