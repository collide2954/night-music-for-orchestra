# The engraving: standards and how the project follows them

This document gives the rules for the printed music of *Night Music for Orchestra*.
The owner of the project asked for engraving of high quality, and for research first:
"What a full score needs. What every part needs. Legibility. Typography. Paper sizes. Interpretation markings. Cover page. Orchestra layout diagram."

The rules come from the people who use the music: the librarians of orchestras.
The table [`research/tables/engraving.csv`](../research/tables/engraving.csv) has each rule with its source.

| Source | What it is |
| --- | --- |
| MOLA Guidelines for Music Preparation (revision of 2017) | The rules of the Major Orchestra Librarians' Association for scores and parts. |
| Singapore Symphony Orchestra, Guidelines for Music Preparation (2025) | The rules of one orchestra for a new score: sizes in millimetres and in points. |
| Scoring Notes, two articles | Notes of music engravers on the production of scores and on the names of instruments. |
| Alex Clark, Score and Part Preparation for Orchestra (2021) | A seminar of an orchestra librarian. |
| Elaine Gould, *Behind Bars* (2011) | The reference book of the two guidelines. The project did not read the book: it uses what the guidelines say. |

The engraving program is LilyPond. The code that writes its input is in these modules of [`src/nightmusic/notation`](../src/nightmusic/notation):

| Module | Function |
| --- | --- |
| `lilypond.py` | The score file and the part files. |
| `frontmatter.py` | The pages before the music. |
| `combine.py` | The staves of the score that two players share. |
| `cues.py` | The cues in the parts. |
| `turns.py` | The bar lines at which a page turn of a part is possible. |

## The documents

| Document | Paper | Height of a staff | Use |
| --- | --- | --- | --- |
| Conductor score in C | 11 x 17 inches (279 x 432 mm), portrait | 4.6 mm | For the conductor. Each instrument has the real sound, but an instrument that plays in a different octave keeps its usual octave. |
| Conductor score, transposed | The same | The same | For a conductor or an orchestra that wants the notes of the parts in the score. One orchestra asks for this type of score. |
| Parts (44) | 9 x 12 inches (229 x 305 mm) | 7.1 mm; 7.4 mm for the strings | One part for each player or string section. Transposing instruments are transposed. |

The names of the files are those that the guidelines ask for: the composer, the title, a number in the sequence of the score, and the instrument.
The two scores have the number 00, and the parts have the numbers 01 to 44.

The sizes are those of North America: the owner of the project is there.
The guidelines permit them: a score of 11 x 17 inches or less, and parts of 9 x 12 inches or more.
9 x 12 inches is also the largest size that the guidelines recommend for a digital part.

## The score

| Rule of the guidelines | In this project |
| --- | --- |
| A cover with the title and the composer | Page 1 of the file: composer, title, the type of the score, the year. |
| The duration, the publisher or a contact, a date | The page behind the cover: duration, licence, and the address of the source. |
| The full instrumentation: doublings, keys of the transposing instruments, each percussion instrument with its range, the number of percussion players | The page "Instrumentation". The code makes it from the music: it lists only instruments that have notes, and the ranges are those that the music uses. |
| A diagram of the stage for an unusual plan | The page "Plan of the stage": the violins are on the two sides of the conductor, and six special instruments have a place. |
| Special instructions and an explanation of unusual notation | The page "Notes for the performance": the transposition, the accidentals, the quarter-tones, and each technique word that the music uses. |
| A programme note | The page "About the work", with a plan of the form: parts, rehearsal marks, and times. |
| Page 1 is the first page of music. It has the title, the composer, the copyright, and all instruments. The type of the score is in the upper left corner. | The pages before the music have no numbers. The first page of music has "Score in C" in the upper left corner, all staves, and the copyright line at the bottom. |
| Right pages have odd numbers in the upper right corner, left pages have even numbers in the upper left corner, 14 to 16 point | 14 point, in the outer corner. The title is in the middle of each header. |
| Full names of the instruments at the first system, abbreviations after it | Yes. |
| Tempo marks above the highest staff and above the first violins | A line for the marks is above the woodwinds and above the strings. It has the tempo marks and the rehearsal marks. |
| Rehearsal marks at landmarks, bold in a box, 19 to 23 point | 20 point. The marks are the letters A to Z without I, then AA to KK. A rehearsal mark and a tempo mark at the same bar line are side by side. |
| Bar numbers at the start of each system, 10 to 13 point, italic | 10 point, italic. |
| A staff of 4 mm or more | 4.6 mm. |
| Bar lines continuous in each family | Yes. |
| The usual sequence of the staves | Woodwinds, brass, timpani and percussion, harp and plucked instruments, keyboards, strings. |
| Two players of one instrument share a staff | Yes: 9 pairs of wind players. The score has 42 staves. See "Shared staves". |
| Each staff has its usual clef from the first bar | Yes, also for a staff that starts with rests. |

One rule of one orchestra is not followed:

| Rule | Why not |
| --- | --- |
| Do not hide the staves of players who do not play | The work has 42 staves. A page with all staves has very little space. The score hides empty staves after the first page (a "French score"), and it shows two systems on a page where that is possible. |

### Shared staves

These players share a staff in the score: flutes 1 and 2, oboes 1 and 2, clarinets 1 and 2, bassoons 1 and 2, horns 1 and 2, horns 3 and 4, horns 5 and 6, trumpets 1 and 2, trombones 1 and 2.
The name of the staff has the two numbers, one above the other.

For each bar, the code selects how the staff shows the two players:

| The two players | The staff shows |
| --- | --- |
| One player has notes | One line with the label "1." or "2.". |
| The same music | One line with the label "a 2". |
| The same rhythm and the same marks, different notes | One line of chords. Player 1 has the upper note. |
| All other bars | Two voices: the stems of player 1 go up, and the stems of player 2 go down. |

- A label is given again at the start of each system, and after a silence of two bars.
- A dynamic mark that the two players have shows one time. If the two players have different dynamics, the marks of player 1 are above the staff.
- A slur or a tie of player 2 does not go from one voice to the other voice: the bars before it or after it get two voices also.
- A player who changes to a second instrument (alto flute, ocarina, clarinet in E-flat) gets a staff of its own for that instrument. The score shows that staff only where it has notes. Its name has the player below it, for example "A. Fl. (Fl. 2)".
- Where the two players have chords, player 1 must have the upper note. The command `nightmusic check` finds the bars in which player 2 is above player 1 in a chord.

## The parts

| Rule of the guidelines | In this project |
| --- | --- |
| A staff of 7.0 mm or more; 7.5 mm is the best | 7.1 mm for the winds, the percussion, and the keyboards. 7.4 mm for the strings: two players read one part. |
| Margins of 20 mm | 19 mm at the binding, 17 mm at the outer edge. |
| The front of a part has the title, the composer, and the instrument with its key | The first page: the instrument on the left, the title in the middle, the composer on the right. |
| Each subsequent page has the instrument, the title, and the page number | Yes, in the header. |
| The first line is indented | Yes. |
| Clefs at the start of each line, bar numbers at the start of each line | Yes. |
| The player has the time to turn the page | A page turn is permitted only at a rest of 4 seconds or more. The rule uses the tempo: one bar of a slow tempo is sufficient. A player with two staves (piano, harp, celesta) can turn a page while one hand is free for 4 seconds. Two string players read one part, and one of them turns the page: a string part can also have a page turn at a rest of 2 seconds, and at a bar line through which the section holds a note. |
| A cue after a long rest, from an instrument that the player can hear, in the key of the part | After a rest of 8 bars or more (or of 25 seconds or more), the last bars before the entry show the notes of a different instrument in small type, with its name. See "Cues". |
| Tempo and metre changes show also in a long rest | A long rest stops at each bar with a tempo mark or a change of tempo in words. |
| A change of instrument is clear | After the last note on the old instrument, the words "to ..." tell the player to take the new instrument. At the first note on the new instrument, a box has its name. A percussion player has many instruments: the first note of the part also has the name of its instrument. |
| A percussion part lists its instruments | The part of each percussion player starts with a key: the instruments in the sequence of their use, the range of each tuned instrument, and the places on the staff of an instrument that has more than one size (for example three tom-toms). |
| An octave sign is only above or below notes | An octave sign stops at a silence of one whole note or more. |
| One part for each wind player, one part for each string section | Yes. The timpani have a separate part. |
| The pedal changes of the harp are not printed; bowings only for a special effect | Yes. |

In a part, a rehearsal mark and a tempo mark at the same bar line are side by side, as in the score.

### Cues

The code selects the instrument of each cue. The player must hear that instrument clearly.
Each instrument that plays in the bars before the entry gets points:

| Property | Points |
| --- | --- |
| The loudness of its notes | 0 to 2 |
| The number of notes that start in the cue (8 or more give all points) | 0 to 1.2 |
| It plays until the entry | 1 |
| Its family (brass and woodwinds 0.8, strings 0.7, keyboards 0.6, plucked instruments 0.5, tuned percussion 0.4) | 0.4 to 0.8 |
| It is of the same family as the player of the part | 0.4 |
| It has only a note that it holds from before the cue | -1.5 |

- A cue has 5 seconds of music or more, but not more than 4 bars. It starts with the first bar in which its instrument has a note.
- The notes of a cue are in the key of the part. They are in the octave that is best for the clef of the part: a cue is for the ear, not for the hand.
- A cue shows one note at a time (the highest note of a chord), with ties, and with no other marks.
- An instrument with no pitch is not a cue. In a staff for such instruments, a cue has its own small treble clef.
- The rests of the player stay in the bars of the cue. The notes of the cue have stems up.
- A long rest stops where a cue starts: thus a page turn can be before a cue.

## Marks for the interpretation

- A playing technique (for example "sul pont.", "con sord.") is in upright type above the staff.
- A word of expression (for example "espr.", "dolce") is in italic type below the staff, with the dynamic marks.
- A tempo mark is bold. A gradual change of tempo ("poco rit.") is italic.
- A hairpin is below sounding notes only. The code stops each hairpin at a silence, and each entry after the silence gets its own dynamic mark.
- An accidental is for one bar and one octave.

The command `nightmusic check` finds notes out of range, hairpins over a silence, chords that a hand cannot reach, and moves of a hand that are too fast.
See [`work.md`](work.md).

## How to make the documents

| Command | Result |
| --- | --- |
| `uv run nightmusic score` | The conductor score: `build/score/score.pdf`. |
| `uv run nightmusic parts` | The full set: the score in C, the transposed score, and the 44 parts. The directory `build/set` has each document with the name that a librarian expects, for example `GILIO Night Music for Orchestra 01 - Flute 1.pdf`. |
| `uv run python tools/front_pages.py DIRECTORY` | Only the pages before the music: a fast check of their layout. |
| `uv run python tools/short_score.py BARS DIRECTORY` | The score of the first bars: a fast check of the layout of the music pages. |
| `uv run python tools/one_part.py PART DIRECTORY` | One part. |
