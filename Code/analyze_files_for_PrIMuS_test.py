import time
import random
import shutil
import datetime
import logging
import glob
import os

from pathlib import Path

from generate_and_compare import compare_origin_and_OMR
from apply_trueskill import evaluate_teams_weights
from musicdiff.m21utils import DetailLevel

from generate_and_compare import PATH_PROJECT


from copy_files_for_PrIMuS_test import TEST_FOLDER, DROPBOX_for_ScanScore, Audiveris_folder


def compare_OMR_with_original():
    files = glob.glob(DROPBOX_for_ScanScore + "/*.xml")
    print("-- take one ScanScore mxl file from the DropBox and analyses it--")
    try :
        file = files[0]
    except IndexError as e:
        print("No ScanScore file to analyze")
        return None
    filename = Path(file).stem
    dir = os.path.dirname(os.path.realpath(file))

    path_dst_original = TEST_FOLDER + "/" + filename + ".mei"
    path_Audiveris = TEST_FOLDER + "/" + filename + "_Audiveris.mxl"
    path_dst_Audiveris = Audiveris_folder + "/" + filename + "/" + filename + ".mxl"
    path_dst_ScanScore = TEST_FOLDER + "/" + filename + "_ScanScore.xml"

    shutil.copyfile(path_dst_Audiveris, path_Audiveris)
    shutil.copyfile(file, path_dst_ScanScore)

    weight = evaluate_teams_weights()

    compare_origin_and_OMR(sc1=path_dst_original,sc2=path_dst_Audiveris,detail=DetailLevel.AllObjects,weights=weight)
    compare_origin_and_OMR(sc1=path_dst_original, sc2=path_dst_ScanScore, detail=DetailLevel.AllObjects,weights=weight)

    #os.remove(file)
    #os.remove(dir + "/" + filename + ".png")

if __name__ == "__main__":
    compare_OMR_with_original()
