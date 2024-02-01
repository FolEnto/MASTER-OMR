import time
import random
import shutil
import datetime
import logging
import glob
import os
from PyPDF2 import PdfWriter, PdfReader

from pathlib import Path

from generate_and_compare import compare_origin_and_OMR
from apply_trueskill import evaluate_teams_weights
from musicdiff.m21utils import DetailLevel

from generate_and_compare import PATH_PROJECT
TEST_FOLDER = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/Test_PrIMuS_data"
DROPBOX_for_ScanScore = "/home/jerome/Dropbox/PrIMus"
Audiveris_folder = "/home/jerome/.local/share/AudiverisLtd/audiveris"

""" We tried to automate the OMR recognition but was unstable and often resulted with empty files. We do it by hand.
def execute_OMR_for_PrIMuS(file):
    cmd = 'java -cp "'+PATH_PROJECT+'audiveris/Audiveris-5.3.1/lib/*" Audiveris -batch -output '+TEST_FOLDER+' -export '+ file
    print("CMD : " + cmd)
    file_name = Path(file).stem
    os.system(cmd)
    file_path = TEST_FOLDER+'/'+file_name+'.mxl'
    print("Executed omr, result in :" + file_path)
    return file_path
"""

def copy_mei_and_png_in_test_folder(nbr):
    dst = TEST_FOLDER
    mypath = "/home/jerome/Téléchargements/primusCalvoRizoAppliedSciences2018/*/*"
    print("-- retreiving and enumerating PrIMuS dataset --")
    files = glob.glob(mypath + "/*.mei")
    print("-- shuffle the filenames to pick at random --")
    random.shuffle(files)
    count = 0
    print("-- Let's pick {} data --".format(nbr))
    for file in files[0:nbr]:
        count+=1
        filename = Path(file).stem
        dir = os.path.dirname(os.path.realpath(file))
        path_original = dir + "/" + filename + ".mei"
        path_png = dir + "/" + filename + ".png"

        path_dst_original = dst+"/"+filename+".mei"
        path_dst_png = dst+"/"+filename+".png"
        path_dst_pdf = dst + "/" + filename + ".pdf"

        path_dropbox_png = DROPBOX_for_ScanScore + "/" + filename + ".png"

        shutil.copyfile(path_original, path_dst_original)
        shutil.copyfile(path_png, path_dst_png)
        shutil.copyfile(path_png, path_dropbox_png)

        """
        writer = PdfWriter()
        page = writer.add_blank_page(width=8.27 * 72, height=11.7 * 72)
        with open(path_dst_pdf, 'wb') as fp:
            writer.write(fp)
        """
        print(path_dst_original)
        print(path_dst_png)
        print(path_dropbox_png)

    print("-- copied {} data --".format(count))


if __name__ == "__main__":
    copy_mei_and_png_in_test_folder(5)
