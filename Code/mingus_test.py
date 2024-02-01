import mingus.core
from mingus.containers import Bar, Composition, Track
import mingus.extra.lilypond as LilyPond
from mingus.extra.musicxml import write_Composition

def create_music_sheet():
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