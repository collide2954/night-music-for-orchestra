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

The engraving program is LilyPond. The code that writes its input is in [`notation/lilypond.py`](../src/nightmusic/notation/lilypond.py) and [`notation/frontmatter.py`](../src/nightmusic/notation/frontmatter.py).

## The documents

| Document | Paper | Height of a staff | Use |
| --- | --- | --- | --- |
| Conductor score in C | 11 x 17 inches (279 x 432 mm), portrait | 4.6 mm | For the conductor. Each instrument has the real sound, but an instrument that plays in a different octave keeps its usual octave. |
| Parts (44) | 9 x 12 inches (229 x 305 mm) | 7.1 mm; 7.4 mm for the strings | One part for each player or string section. Transposing instruments are transposed. |

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
| Rehearsal marks at landmarks, bold in a box, 19 to 23 point | 20 point. The marks are the letters A to Z without I, then AA to KK. |
| Bar numbers at the start of each system, 10 to 13 point, italic | 10 point, italic. |
| A staff of 4 mm or more | 4.6 mm. |
| Bar lines continuous in each family | Yes. |
| The usual sequence of the staves | Woodwinds, brass, timpani and percussion, harp and plucked instruments, keyboards, strings. |

Two rules of one orchestra are not followed at this time:

| Rule | Why not |
| --- | --- |
| Do not hide the staves of players who do not play | The work has 51 staves. A page with all staves has very little space. The score hides empty staves after the first page (a "French score"), and it shows two systems on a page where that is possible. |
| Two players of one instrument share a staff | Each wind player has a staff at this time. Shared staves are planned: they make the pages less full, and the first page will be easier to read. |

## The parts

| Rule of the guidelines | In this project |
| --- | --- |
| A staff of 7.0 mm or more; 7.5 mm is the best | 7.1 mm for the winds, the percussion, and the keyboards. 7.4 mm for the strings: two players read one part. |
| Margins of 20 mm | 19 mm at the binding, 17 mm at the outer edge. |
| The front of a part has the title, the composer, and the instrument with its key | The first page: the instrument on the left, the title in the middle, the composer on the right. |
| Each subsequent page has the instrument, the title, and the page number | Yes, in the header. |
| The first line is indented | Yes. |
| Clefs at the start of each line, bar numbers at the start of each line | Yes. |
| The player has the time to turn the page | A page turn is permitted only where the player has a rest of three whole notes or more. |
| Tempo and metre changes show also in a long rest | A long rest stops at each bar with a tempo mark or a change of tempo in words. |
| A change of instrument is clear | A box with the name of the new instrument is at the change. |
| One part for each wind player, one part for each string section | Yes. The timpani have a separate part. |
| The pedal changes of the harp are not printed; bowings only for a special effect | Yes. |

Not done at this time: cues after long rests, an advance notice before a change of instrument, and a key of the notation at the start of a percussion part.

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
| `uv run nightmusic parts` | The score and the 44 parts: `build/parts/part-*.pdf`. |
| `uv run python tools/front_pages.py DIRECTORY` | Only the pages before the music: a fast check of their layout. |
| `uv run python tools/short_score.py BARS DIRECTORY` | The score of the first bars: a fast check of the layout of the music pages. |
| `uv run python tools/one_part.py PART DIRECTORY` | One part. |
