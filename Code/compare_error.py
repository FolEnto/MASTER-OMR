from musicdiff.m21utils import DetailLevel
from pathlib import Path
from generate_and_compare import PATH_PROJECT
import custom_diff
PATH_PROJECT_errors = PATH_PROJECT + "error/"

def compare_origin_and_OMR(sc1,sc2,detail):
    print("Comparing {} and {}".format(sc1,sc2))
    file_name2 = Path(sc2).stem
    file_name1 = Path(sc1).stem
    out_pdf_path1 = PATH_PROJECT_errors + file_name1 + "_" + file_name2 + '_original.pdf'
    out_pdf_path2 = PATH_PROJECT_errors + file_name1 + "_" + file_name2 + '_error.pdf'
    numDiffs, diff_list = custom_diff.diff(sc1, sc2, out_pdf_path1, out_pdf_path2, visualize_diffs=True, detail=detail)
    return numDiffs, diff_list




if __name__ == '__main__':

    original = PATH_PROJECT_errors + "BASE.musicxml"
    file = PATH_PROJECT_errors + "MODIFIED.musicxml"
    try :
        numDiffs, diff_list = compare_origin_and_OMR(original,file,detail=DetailLevel.AllObjects)

        print("-----------------------DIFFS-----------------------")

        for diff in diff_list:
            print(diff)

        print("-----------------------END DIFFS-----------------------")
    except Exception as e:
        print(e)
        pass