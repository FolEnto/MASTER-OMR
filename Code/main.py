# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import mingus.core
from mingus.containers import Bar, Composition, Track
import mingus.extra.lilypond as LilyPond
from mingus.extra.musicxml import write_Composition
import datetime


PATH_PROJECT = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/"
PATH_GENERATED="/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/"
def create_random_music_sheet(bars_number):
    """
    bars = bars_number
    if bars > 5 :
        bars = 5
    elif bars < 0 :
        bars = 0
    """

    c = Composition()
    c.set_author('Jérôme Vonlanthen', 'jerome.vonlanthen@unifr.ch')
    c.set_title('Random Mingus Composition')
    t = Track()
    b = Bar()
    b.place_notes("C",4)
    b.place_notes("E",4)
    b.place_notes("G",4)
    b.place_notes("B",4)
    t.add_bar(b)
    b = Bar()
    b.place_notes(None, 4)
    b.place_notes("B#", 4)
    b.place_notes("Bb", 4)
    b.place_notes("Bb", 4)
    t.add_bar(b)
    c.add_track(t)
    LilyPond.to_pdf(LilyPond.from_Composition(c),"test.pdf")
    write_Composition(c, "test", zip=False)


from music21 import *
# Spécifiez l'utilisation de MuseScore 3 comme convertisseur
converterPath = '/usr/bin/mscore3'  # Remplacez par le chemin complet vers MuseScore 3
environment.set("musicxmlPath", converterPath)

def music21():
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



    #b.show()  # I've altered this so it's much shorter than it should be...
def demo_show(file):
    piece = converter.parse(file)
    s_score = piece
    p_part = s_score.recurse()
    rest_note_Iterator = p_part.notesAndRests

    for el in rest_note_Iterator:
        print(el, el.quarterLength)



def compare_mxml(file1,file2):
    print("-----------------------FILE1-----------------------")
    example_show(file1)
    print("-----------------------FILE2-----------------------")
    example_show(file2)

def demo(file1,file2):
    print("-----------------------FILE1-----------------------")
    demo_show(file1)
    print("-----------------------FILE2-----------------------")
    demo_show(file2)
    print("-----------------------END-----------------------")

def generate_measures(stream):
    noteStringList = ["G4", "rest", "B#4", "Bb4"]
    for n in noteStringList:
        if n == "rest":
            stream.append(note.Rest())
        else:
            stream.append(note.Note(n))
    stream.makeMeasures()
    stream.makeBeams(inPlace=True, setStemDirections=True, failOnNoTimeSignature=False)

import random
from music21.duration import Duration
MAX_MEASURE = 4.0


def place_note_in_stream(s, note_name, dura,offset) :
    if note_name == "rest":
        object = note.Rest(dura)
    else:
        object = note.Note(note_name)

    object.duration = Duration(dura)
    object.offset=offset
    print("insertion {} of length {} with offset {} in measure : {} " .format(str(object),str(object.duration),str(object.offset),str(s)))
    #print(splitted)
    s.append(object)

    """
    if round(offset) != int(offset) :
        print(round(offset), offset)
        s.sliceByBeat(inPlace=True)
    """


import math
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
    # ts44.displaySequence.partition(4)
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
        generate_measures(p0)

    stream1.insert(0, p0)

    file_xml = PATH_GENERATED + "mxl/" + filename + ".musicxml"
    file_pdf = PATH_GENERATED + "pdf/" + filename + ".pdf"
    # Export musicxml file
    stream1.write('musicxml', fp=file_xml, makeNotation=False)
    # Export PDF file
    """
    cmd = "mscore "+ file_xml +" --export-to "+ file_pdf
    print(cmd)
    os.system(cmd)
    """
    stream1.write('musicxml.pdf', file_pdf, makeNotation=False)

    return file_pdf, file_xml

import os
from pathlib import Path


def execute_OMR(file):
    cmd = 'java -cp "'+PATH_PROJECT+'audiveris/Audiveris-5.3.1/lib/*" Audiveris -batch -output '+PATH_PROJECT+'output_OMR/ -export '+file
    print(cmd)
    file_name = Path(file).stem
    os.system(cmd)
    file_path = PATH_PROJECT+'output_OMR/'+file_name+'.mxl'
    print(file_path)
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
def compare_origin_and_OMR(sc1,sc2,detail):
    file_name = Path(sc1).stem
    out_pdf_path1 = PATH_PROJECT + 'output_pdf/' + file_name + '___1_original.pdf'
    out_pdf_path2 = PATH_PROJECT + 'output_pdf/' + file_name + '___2_omr.pdf'
    numDiffs, diff_list = custom_diff.diff(sc1, sc2, out_pdf_path1, out_pdf_path2, force_parse=False, visualize_diffs =True, detail=detail)
    return numDiffs, diff_list

def example_run():
    # create_random_music_sheet(4)
    music21()
    # example_show(PATH_GENERATED+"file.mxl")
    # compare_mxml("/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test.mxl","/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test.mxl")
    demo("/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/file.mxl",
         "/home/jerome/Documents/MASTER/MASTER-OMR/Code/test_auto/test.mxl")

def example_diff():
    example_path_1 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/mxl/2023_10_04_16_18_20_TEST.mxl"
    example_path_2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_OMR/2023_10_04_16_18_20_TEST.mxl"

    # compare_origin_and_OMR(file1_xml, file2_xml)
    numDiffs, diff_list = compare_origin_and_OMR(example_path_1, example_path_2, detail=DetailLevel.AllObjects)
    demo(example_path_1, example_path_2)

    print("-----------------------DIFFS-----------------------")

    for diff in diff_list:
        print(diff)

    print("-----------------------END DIFFS-----------------------")

def real_run():
    file1_pdf, file1_xml = generate_file_xml_and_pdf(random=True)
    file2_xml = execute_OMR(file1_pdf)

    numDiffs, diff_list = compare_origin_and_OMR(file1_xml, file2_xml, detail=DetailLevel.AllObjects)

    demo(file1_xml, file2_xml)

    for diff in diff_list:
        print(diff)

def example_generate():
    generate_file_xml_and_pdf(random=True)


def test_compare():
    example_path_1 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/generated/mxl/2023_10_18_16_31_15_TEST.mxl"
    example_path_2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_OMR/2023_10_18_16_31_15_TEST.mxl"

    # compare_origin_and_OMR(file1_xml, file2_xml)
    numDiffs, diff_list = compare_origin_and_OMR(example_path_1, example_path_2, detail=DetailLevel.GeneralNotesOnly)
    demo(example_path_1, example_path_2)

    print("-----------------------DIFFS-----------------------")

    for diff in diff_list:
        print(diff)

    print("-----------------------END DIFFS-----------------------")


def test_errors_visu() :
    """[('accidentdel', [('F4', 'sharp', False)], 4, 0, ['stop', 'partial'], [], 140220965260352, [], [], [], {}, [('F4', 'None', False)], 4, 0, ['stop', 'partial'], [], 140220964493680, [], [], [], {}, 1, (0, 0)),
    ('extrains', None, "TX:", "off=0.0", "dur=0.0, 1")]
    """
    file1 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_pdf/2023_12_06_14_02_05_TEST___1_original.pdf"
    file2 = "/home/jerome/Documents/MASTER/MASTER-OMR/Code/output_pdf/2023_12_06_14_02_05_TEST___2_omr.musicxml"

    piece = converter.parse(file2)
    s_score = piece
    p_part = s_score.recurse()
    flag = False
    for el in p_part:
        try :
            if isinstance(el, stream.Measure)  :
                #print("---content---" )
                try :
                    for i in el :
                        if isinstance(i, expressions.TextExpression) :
                            flag = True
                except TypeError :
                    pass
                #print("---end content---")
        except AttributeError :
            pass
        if flag :
            el.show(fmt="musicxml.pdf")
            print("SHOWING MEASURE {}", el)
            flag = False




if __name__ == '__main__':
    #example_run()
    #example_diff()
    #example_generate()


    real_run()

    #test_errors_visu()

    #test_compare()






