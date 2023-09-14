# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import mingus.core
from mingus.containers import Bar, Composition, Track
import mingus.extra.lilypond as LilyPond
from mingus.extra.musicxml import write_Composition


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
def music21():
    stream1 = stream.Stream()
    noteStringList = ["C4","E4","G4","B4","rest","B#4", "Bb4","B4"]
    for n in noteStringList :
        if n == "rest" :
            stream1.append(note.Rest())
        else :
            stream1.append(note.Note(n))

    stream1.write('musicxml', fp=PATH_GENERATED+"file.mxl")
    #stream1.show()

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


def compare_mxml(file1,file2):
    f1 = converter.parse(file1, format='musicxml')
    f2 = converter.parse(file2, format='musicxml')




if __name__ == '__main__':
    #create_random_music_sheet(4)
    music21()
    example_show(PATH_GENERATED+"file.mxl")
    #compare_mxml("/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test.mxl","/home/jerome/Documents/MASTER/MASTER-OMR/Code/results_mxl/test_after_OCR.mxl")
