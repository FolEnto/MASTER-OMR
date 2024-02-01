from music21 import *
# Specify usage of MuseScore 3 as converter
converterPath = '/usr/bin/mscore3'  # Replace by the path to musescore
environment.set("musicxmlPath", converterPath)

# Early tests
"""
def music21_test():
    stream1 = stream.Stream()
    noteStringList = ["C4","E4","G4","B4","rest","B#4", "Bb4","B4"]
    for n in noteStringList :
        if n == "rest" :
            stream1.append(note.Rest())
        else :
            stream1.append(note.Note(n))


    stream1.write('musicxml', fp=PATH_GENERATED+"file.mxl")
    stream1.write('musicxml.pdf', fp =PATH_GENERATED+'file.pdf')
    stream1.show()

def example_show(file):
    piece = converter.parse(file)
    piece.show('text')
    print("----------------------------------------------------------------------")
    s_score = piece
    p_part = s_score.recurse()
    for el in p_part:
        print(el.offset, el, el.activeSite)
    print("----------------------------------------------------------------------")
    for el in s_score.flatten():
        print(el.offset, el, el.activeSite)
    print("----------------------------------------------------------------------")
    for el in p_part:
        print(el, el.quarterLength)
    print("----------------------------------------------------------------------")

    rest_note_Iterator = p_part.notesAndRests

    for el in rest_note_Iterator:
        print(el, el.quarterLength)



def compare_mxml(file1,file2):
    print("-----------------------FILE1-----------------------")
    example_show(file1)
    print("-----------------------FILE2-----------------------")
    example_show(file2)



def generate_measures(stream):
    noteStringList = ["G4", "rest", "B#4", "Bb4"]
    for n in noteStringList:
        if n == "rest":
            stream.append(note.Rest())
        else:
            stream.append(note.Note(n))
    stream.makeMeasures()
    stream.makeBeams(inPlace=True, setStemDirections=True, failOnNoTimeSignature=False)
"""

# Random generation

import random
import math
from music21.duration import Duration
import datetime

PATH_PROJECT = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/"
PATH_GENERATED="/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/"


MAX_MEASURE = 4.0
def place_note_in_stream(s, note_name, dura, offset) :
    if note_name == "rest":
        object = note.Rest(dura)
    else:
        object = note.Note(note_name)

    object.duration = Duration(dura)
    object.offset=offset
    print("insertion {} of length {} with offset {} in measure : {} " .format(str(object),str(object.duration),str(object.offset),str(s)))
    s.append(object)

def formatMeasure(m):
    offsetList = []
    for n in m :
        if not isinstance(n, meter.TimeSignature) :
            print(n.offset, n.name)

            if not n.offset.is_integer() and math.ceil(n.offset) != int(MAX_MEASURE)  :
                offsetList.append(math.ceil(n.offset))
    print(offsetList)
    # remove duplicates
    offsetList = list(dict.fromkeys(offsetList))
    print(offsetList)

    m.sliceAtOffsets(offsetList,inPlace=True)
    m.splitAtDurations()

    m.makeBeams(inPlace=True)

    beams_list = []
    for n in m:
        if not isinstance(n, note.Rest) and not isinstance(n, meter.TimeSignature) and not isinstance(n, clef.Clef):
            beams_list.append(n.beams)

    for b in beams_list:
        if b is not None:
            for be in b:
                print(be.type)
        else:
            print("None")

    beam.Beams.sanitizePartialBeams(beams_list)
    m.makeAccidentals(inPlace=True)



def generate_random_measures(s):
    noteStringList = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B','rest']
    durations = [.25,.5,.75,1,1.25,1.5,2,3,4]
    measure_total = MAX_MEASURE
    measure_nbr = 1
    m = stream.Measure(number=measure_nbr)
    tc = clef.TrebleClef() #TODO: Adapt to other Clefs
    # TODO : Add other KeySignatures
    ts44 = meter.TimeSignature('4/4') #TODO: Adapt to other time signatures
    ts44.beamSequence.partition(4)
    ts44.beatSequence.partition(4)
    ts44.beatCount = [1, 1, 1, 1] #TODO: Adapt to other time signatures

    m.append(tc)
    m.append(ts44)

    offset = 0.0

    for i in range(0,55):
        print("measure TOTAL {}".format(measure_total))
        index_note = random.randint(0, len(noteStringList)-1)
        index_duration = random.randint(0, len(durations) - 1)
        note_name = noteStringList[index_note]
        dura = durations[index_duration]
        # Manage duration of last note of measure to not exceed. Trying to avoid some "changed flags" error of comparison
        if dura > measure_total :
            dura = measure_total
        measure_total = measure_total-dura

        # if there is no place anymore in the measure, complete it and create a new Measure
        if measure_total == 0 :
            measure_total = MAX_MEASURE
            place_note_in_stream(m, note_name, dura, offset)
            measure_nbr += 1
            offset = 0.0
            s.append(m)
            formatMeasure(m)
            m = stream.Measure(number=measure_nbr)
        else :
            place_note_in_stream(m, note_name, dura, offset)
            offset += dura

    ## finish the pièce with adapted length of note
    if measure_total != 0.0 :
        index_note = random.randint(0, len(noteStringList) - 1)
        note_name = noteStringList[index_note]
        place_note_in_stream(m,note_name,measure_total, offset)
        s.append(m)
        formatMeasure(m)
        m.rightBarline = bar.Barline('final')

def generate_file_xml_and_pdf(random):
    stream1 = stream.Score()
    stream1.insert(0, metadata.Metadata())
    stream1.metadata.title = 'Random Piece'
    stream1.metadata.composer = 'Random Generator'
    p0 = stream.Part()
    now = datetime.datetime.now()
    filename=str(now.strftime("%Y_%m_%d_%H_%M_%S")) + "_TEST" + str()
    if random :
        generate_random_measures(p0)
    else :
        generate_custom_measures(p0)

    stream1.insert(0, p0)

    file_xml = PATH_GENERATED + "mxl/" + filename + ".musicxml"
    file_pdf = PATH_GENERATED + "pdf/" + filename + ".pdf"
    # Export musicxml file
    stream1.write('musicxml', fp=file_xml, makeNotation=False)
    # Export PDF file
    stream1.write('musicxml.pdf', file_pdf, makeNotation=False)

    return file_pdf, file_xml

import os
from pathlib import Path


def show_file(file):
    piece = converter.parse(file)
    s_score = piece
    p_part = s_score.recurse()
    rest_note_Iterator = p_part.notesAndRests

    for el in rest_note_Iterator:
        print(el, el.quarterLength)


def show(file1, file2):
    print("-----------------------FILE1-----------------------")
    show_file(file1)
    print("-----------------------FILE2-----------------------")
    show_file(file2)
    print("-----------------------END-----------------------")


def execute_OMR(file):
    cmd = 'java -cp "'+PATH_PROJECT+'audiveris/Audiveris-5.3.1/lib/*" Audiveris -batch -output '+PATH_PROJECT+'output_OMR/ -export '+ file
    print("CMD : " + cmd)
    file_name = Path(file).stem
    os.system(cmd)
    file_path = PATH_PROJECT+'output_OMR/'+file_name+'.mxl'
    print("Executed omr, result in :" + file_path)
    return file_path


# Not used
def write_file_to_compare(file):
    piece = converter.parse(file)
    #piece.show('text')
    print("-- file : "+file +" --")
    print("----------------------------------------------------------------------")
    s_score = piece
    p_part = s_score.recurse()
    #for el in p_part:  print(el.offset, el, el.activeSite)
    #print("----------------------------------------------------------------------")
    #for el in s_score.flatten(): print(el.offset, el, el.activeSite)
    #print("----------------------------------------------------------------------")
    #for el in p_part: print(el, el.quarterLength)
    #print("----------------------------------------------------------------------")

    rest_note_Iterator = p_part.notesAndRests

    for el in rest_note_Iterator:
        print(el, el.quarterLength)

import music21 as m21
from pathlib import Path
import sys
sys.path.append('music-score-diff')
from musicdiff.m21utils import DetailLevel
import custom_diff
import logging
import musicdiff
import csv

def compare_origin_and_OMR(sc1,sc2,detail, weights):
    logging.info("Comparing {} and {}".format(sc1,sc2))
    print("Comparing {} and {}".format(sc1,sc2))
    file_name = Path(sc2).stem
    out_pdf_path1 = PATH_PROJECT + 'output_pdf/' + file_name + '___1_original.pdf'
    out_pdf_path2 = PATH_PROJECT + 'output_pdf/' + file_name + '___2_omr.pdf'
    #musicdiff.diff(sc1, sc2, out_pdf_path1, out_pdf_path2, visualize_diffs=True, detail=detail)
    numDiffs, diff_list = custom_diff.diff(sc1, sc2, out_pdf_path1, out_pdf_path2, visualize_diffs=True, detail=detail, weights=weights)

    return numDiffs, diff_list

def example_run():
    # create_random_music_sheet(4)
    music21()
    # example_show(PATH_GENERATED+"file.mxl")
    # compare_mxml("/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test.mxl","/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test.mxl")
    show("/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/file.mxl",
         "/home/jerome/Documents/MASTER/MASTER-OMR/Code/test_auto/test.mxl")

def example_diff():
    example_path_1 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/mxl/2023_10_04_16_18_20_TEST.mxl"
    example_path_2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_OMR/2023_10_04_16_18_20_TEST.mxl"

    # compare_origin_and_OMR(file1_xml, file2_xml)
    numDiffs, diff_list = compare_origin_and_OMR(example_path_1, example_path_2, DetailLevel.AllObjects, [])
    show(example_path_1, example_path_2)

    print("-----------------------DIFFS-----------------------")

    for diff in diff_list:
        print(diff)

    print("-----------------------END DIFFS-----------------------")

def real_run():
    file1_pdf, file1_xml = generate_file_xml_and_pdf(random=True)
    file2_xml = execute_OMR(file1_pdf)

    numDiffs, diff_list = compare_origin_and_OMR(file1_xml, file2_xml, DetailLevel.AllObjects, {})

    show(file1_xml, file2_xml)

    for diff in diff_list:
        print(diff)

def test_compare():

    example_path_1 = "/home/jerome/Téléchargements/primusCalvoRizoAppliedSciences2018/package_ab/230001461-1_1_1/230001461-1_1_1.mei"
    example_path_2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_OMR/230001461-1_1_1.mxl"

    # compare_origin_and_OMR(file1_xml, file2_xml)
    numDiffs, diff_list = compare_origin_and_OMR(example_path_1, example_path_2, detail=DetailLevel.AllObjects,weights={})
    show(example_path_1, example_path_2)

    print("-----------------------DIFFS-----------------------")

    for diff in diff_list:
        print(diff)

    print("-----------------------END DIFFS-----------------------")

from PyPDF2 import PdfWriter, PdfReader
def test_errors_visu(file1,file2) :
    #file1 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/mxl/2023_12_13_16_01_22_TEST.musicxml"
    #file2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_pdf/2023_12_13_16_01_22_TEST___2_omr.musicxml"

    source = converter.parse(file1)
    piece = converter.parse(file2)
    s_score = piece
    p_part = s_score.recurse()
    flag = False
    for el in p_part:
        print(el)
        try :
            if isinstance(el, stream.Measure)  :
                #print("---content---" )
                try :
                    for i in el :
                        if isinstance(i, expressions.TextExpression) :
                            flag = True
                except TypeError :
                    print("---TypeError -")

        except AttributeError :
            pass
        if flag :
            mes = el.measureNumber

            stream1 = source.parts[0].measure(mes)
            stream2 = el

            print("STREAM1")
            stream1.show('text')
            print("STREAM2")
            stream2.show('text')
            print("END --- STREAM")

            out_pdf_path = PATH_PROJECT + 'error/' + Path(file1).stem +str(mes) + '.pdf'

            biggerStream = stream.Score()
            p1 = stream.Part()
            p2 = stream.Part()
            p1.append(stream1)
            p2.append(stream2)
            p1.append(bar.Barline('final'))

            biggerStream.append(p1)
            biggerStream.append(p2)

            biggerStream.write('musicxml.pdf', out_pdf_path, makeNotation=False)

            flag = False

            out_pdf_path_cropped = PATH_PROJECT + 'error/' + Path(file1).stem + str(mes) + '_cropped.pdf'
            reader = PdfReader(out_pdf_path)
            writer = PdfWriter()

            for page in reader.pages:

                print(page.cropbox.lower_left)
                print(page.cropbox.lower_right)
                print(page.cropbox.upper_left)
                print(page.cropbox.upper_right)

                x1 = 0
                x2 = 360
                y1 = 620
                y2 = 750

                lower_right_new_x_coordinate = x2
                lower_right_new_y_coordinate = y1
                lower_left_new_x_coordinate = x1
                lower_left_new_y_coordinate = y1
                upper_right_new_x_coordinate = x2
                upper_right_new_y_coordinate = y2
                upper_left_new_x_coordinate = x1
                upper_left_new_y_coordinate = y2

                page.mediabox.lower_right = (lower_right_new_x_coordinate, lower_right_new_y_coordinate)
                page.mediabox.lower_left = (lower_left_new_x_coordinate, lower_left_new_y_coordinate)
                page.mediabox.upper_right = (upper_right_new_x_coordinate, upper_right_new_y_coordinate)
                page.mediabox.upper_left = (upper_left_new_x_coordinate, upper_left_new_y_coordinate)

                writer.add_page(page)

            with open(out_pdf_path_cropped, 'wb') as fp:
                writer.write(fp)


from apply_trueskill import evaluate_teams_weights

def test_compare_dropbox(path, file_name):
    weights = evaluate_teams_weights()

    _Original = path + "/" + file_name + ".musicxml"
    _SmartScore = path + "/" + file_name + "_ScanScore.xml"
    _Audiveris = path + "/" + file_name + "_Audiveris.mxl"
    _Audiveris_modified = path + "/" + file_name + "_Audiveris_modified.mxl"
    _fake_OMR = path + "/" + file_name + "_fake_OMR.mxl"
    _small_errors = path + "/" + file_name + "_small_errors.mxl"
    _big_errors = path + "/" + file_name + "_big_errors.mxl"

    print("---- Audiveris -----")
    try :
        compare_origin_and_OMR(_Original, _Audiveris, DetailLevel.AllObjects, weights)
    except Exception as e: print(e)
    print("---- Audiveris - End -----")

    """
    print("---- Audiveris Modified -----")
    compare_origin_and_OMR(_Original, _Audiveris_modified, DetailLevel.AllObjects, weights)
    print("---- Audiveris Modified End -----")
    """

    print("---- ScanScore -----")
    try:
        compare_origin_and_OMR(_Original, _SmartScore,DetailLevel.AllObjects, weights)
    except Exception as e:
        print(e)
    print("---- ScanScore - End -----")

    """
    print("---- FAKE OMR -----")
    compare_origin_and_OMR(_Original, _fake_OMR, DetailLevel.AllObjects, weights)
    print("---- FAKEOMR - End -----")
    """
    """
    print("---- Small Errors -----")
    compare_origin_and_OMR(_Original, _small_errors, DetailLevel.AllObjects, weights)
    print("---- Small Errors - End -----")
"""
    """
    print("---- Big Errors -----")
    compare_origin_and_OMR(_Original, _big_errors, DetailLevel.AllObjects, weights)
    print("---- Big Errors - End -----")
    """

from os import listdir
from os.path import isfile, join


import os
import glob

def run_multiple_OMR():
    mypath = "/home/jerome/Dropbox/Ground_Truth/to_OMR/*/"
    files = glob.glob(mypath+"/*.pdf")
    for file in files:
        print(file)
        execute_OMR(file)
        print("OMF for {} ended".format(file))

if __name__ == '__main__':
    real_run()



