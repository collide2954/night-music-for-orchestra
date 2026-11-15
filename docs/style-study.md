# Style study

This document gives the style parameters for *Night Music for Orchestra*.
The parameters come from the music of Arnold Schoenberg, Béla Bartók, and John Corigliano.
The composition code will use these parameters as its rules.

## Method

The study has three types of data. Each row of a table has a code for its type.

| Code | Type | Meaning |
| --- | --- | --- |
| M | Measured | The study code measured open score data or performance data. The command `make study` makes these values again. |
| R | Read | The study team read the source. The column "Source" gives the key of the source. The list of sources is at the end of this document. |
| K | Reference knowledge | The row is standard knowledge of music theory or music history. The study team did not read a source for the row. Check the row before you use it for a critical decision. |

The study measured three sets of open data:

1. Schoenberg, *Verklärte Nacht*, complete (418 bars).
   The data are the text source of a piano arrangement by Peter Billam.
   The bar numbers and the key changes of this source agree with the published analysis by Walter Frisch.
2. Bartók, *Out of Doors*, complete.
   The data are a MIDI capture of one piano performance.
   The fourth piece is "The Night's Music", the model of the night music style.
3. Bartók, *Fourteen Bagatelles* op. 6.
   The data are the note lists of the DCML corpus.

No open score data are available for the music of Corigliano.
His rows come from his own program notes and from his lists of instruments.

The second edition of the study (15 November 2026) has four more sourced tables (S12 to S15): variation, instrument techniques, notes that are not in the chord, and more devices of modern orchestral writing.
It also measures the new work itself with the methods of the study (tables M15 to M17).
The command `uv run nightmusic docs` makes the tables of the new work again after a change of the music.

## Main results

1. *Verklärte Nacht* turns from D minor to D major at 54 percent of its duration.
   The largest climax is at 77 percent. A second climax is at 91 percent.
2. Soft levels (p and softer) are in effect for 64 percent of *Verklärte Nacht*.
   The middle levels (mp and mf) are in effect for only 11 percent.
3. Before the turn to D major, vagrant chords sound for two times as long as major and minor triads.
   After the turn, the triads sound for longer than the vagrant chords.
4. Before the turn, 26 percent of the moves of the top line are semitones.
   After the turn, only 10 percent are semitones, and fourths and fifths increase.
5. The bass of *Verklärte Nacht* moves by semitone in 30 percent of its moves.
   It moves by fourth or fifth in 15 percent.
6. In "The Night's Music", 92 percent of the chord time has a semitone clash, and 77 percent has a cluster.
   In *Verklärte Nacht*, the values are 24 percent and 1 percent.
7. One cluster of five adjacent semitones sounds for 26 percent of "The Night's Music".
8. Night music is slow and soft, but it is not empty.
   "The Night's Music" has 4.7 note starts in one second.
   Its mean key velocity is 71 percent of that of "The Chase".
9. In the fugue of Bartók's *Music for Strings, Percussion and Celesta*, the far key comes at 50 percent and the climax at 63 percent.
10. Corigliano makes the shape of a work before its notes.
    His large works have a duration of 29 to 40 minutes and have 4 to 8 sections.
    They use space, layers in different tempos, and quotation.
11. *Verklärte Nacht* has almost no literal repetition: 5 percent of its bars are the same as one of the 8 bars before, and no block of 4 bars comes two times.
    Bartók said in 1937: "I never repeat one part identically".
12. The second version of the new work repeats more than its models.
    9 percent of its bars are the same as one of the 8 bars before (20 percent in part 5), and 5 percent are in a block of 4 bars that comes two times.
    In one half of the bars of a player, the player repeats one of the 8 bars before.
13. *Verklärte Nacht* has 7.6 different pitch classes in one bar. The new work has 4.8.
    After the turn, the new work has almost no vagrant chords (0.2 percent of the time; *Verklärte Nacht*: 13 percent) and almost no whole-tone chords.
14. The new work uses few techniques of its instruments: 1 in the woodwinds, 2 in the brass, and 10 in the strings.
    Ten instruments of its percussion list have no notes.

## Part 1: Measured tables

The study code made all tables of this part. The directory [`research/measured`](../research/measured) has the full data, which includes one row for each bar of *Verklärte Nacht* ([`vn_bars.csv`](../research/measured/vn_bars.csv)).

### M1. Verklärte Nacht: general numbers

This table gives the size, the tempo range, and the positions of the main events. A position is a share of the full duration.

| Measure | Value |
| --- | --- |
| bars | 418 |
| note starts in the arrangement | 8698 |
| duration with the timing of the arrangement (minutes) | 25.01 |
| slowest bar (quarter notes in a minute) | 40 |
| median bar (quarter notes in a minute) | 64.86 |
| fastest bar (quarter notes in a minute) | 132.60 |
| tempo marks | 33 |
| bars for each tempo mark | 12.67 |
| dynamic level marks | 127 |
| dynamic level marks for each 10 bars | 3.04 |
| changes of metre | 18 |
| first bar with the level fff | 175 |
| bars with the level fff in effect | 21 |
| position of bar 229 (arrival of D major), share of time | 0.54 |
| position of bar 338 (largest climax), share of time | 0.77 |
| position of bar 391 (second climax), share of time | 0.91 |
| position of bar 229, share of bars | 0.55 |
| position of bar 338, share of bars | 0.81 |

Data file: [`research/measured/vn_overview.csv`](../research/measured/vn_overview.csv)

### M2. Verklärte Nacht: the five sections

The bar numbers of the sections are from Frisch (1993). The tempo values use the timing of the arrangement. Real recordings are slower by the factor 1.12.

| Section | Content | First bar | Last bar | Minutes | Share of time | Start (share of the time) | Mean tempo (quarter notes in a minute) | Slowest bar | Fastest bar | Note starts per second | Mean loudness (MIDI volume, 0 to 127) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Stanza 1. Narrator: the walk in the cold wood | 1 | 28 | 2.55 | 10.2 % | 0.0 % | 44 | 40 | 62 | 3.2 | 58 |
| 2 | Stanza 2. The woman speaks | 29 | 187 | 8.01 | 32.0 % | 10.2 % | 76 | 52 | 123 | 6.8 | 83 |
| 3 | Stanza 3. Narrator | 188 | 228 | 2.86 | 11.5 % | 42.2 % | 56 | 48 | 65 | 2.4 | 84 |
| 4 | Stanza 4. The man speaks | 229 | 369 | 7.88 | 31.5 % | 53.7 % | 69 | 44 | 133 | 6.7 | 70 |
| 5 | Stanza 5. Narrator: the transfigured night | 370 | 418 | 3.70 | 14.8 % | 85.2 % | 52 | 41 | 71 | 6.2 | 53 |

Data file: [`research/measured/vn_parts.csv`](../research/measured/vn_parts.csv)

### M3. Verklärte Nacht: the ten segments

This table divides section 2 and section 4 into smaller segments. The loudness and the density are highest in the development (segment 2d).

| Section | Content | First bar | Last bar | Minutes | Share of time | Start (share of the time) | Mean tempo (quarter notes in a minute) | Slowest bar | Fastest bar | Note starts per second | Mean loudness (MIDI volume, 0 to 127) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Theme group 1, D minor | 1 | 28 | 2.55 | 10.2 % | 0.0 % | 44 | 40 | 62 | 3.2 | 58 |
| 2a | Theme group 2 | 29 | 49 | 1.28 | 5.1 % | 10.2 % | 66 | 59 | 67 | 4.6 | 87 |
| 2b | Theme groups 3 and 4, B-flat minor, then transition | 50 | 104 | 2.73 | 10.9 % | 15.3 % | 75 | 63 | 106 | 6.3 | 71 |
| 2c | Theme group 5, E major | 105 | 131 | 1.36 | 5.5 % | 26.2 % | 85 | 72 | 105 | 6.9 | 70 |
| 2d | Development | 132 | 180 | 2.16 | 8.6 % | 31.7 % | 83 | 68 | 123 | 9.4 | 96 |
| 2e | Return of theme 2a at the first large climax | 181 | 187 | 0.48 | 1.9 % | 40.3 % | 58 | 52 | 60 | 3.8 | 112 |
| 3 | Transition and return of theme 1, to E-flat minor | 188 | 228 | 2.86 | 11.5 % | 42.2 % | 56 | 48 | 65 | 2.4 | 84 |
| 4a | Themes 6 to 10: D major, F-sharp major, D-flat major, F major | 229 | 319 | 4.94 | 19.7 % | 53.7 % | 70 | 44 | 133 | 7.3 | 67 |
| 4b | Theme 11 in D-flat major, climax, theme 6 again in D major | 320 | 369 | 2.95 | 11.8 % | 73.5 % | 67 | 53 | 94 | 5.5 | 77 |
| 5 | Reprise of themes in D major, second climax, coda | 370 | 418 | 3.70 | 14.8 % | 85.2 % | 52 | 41 | 71 | 6.2 | 53 |

Data file: [`research/measured/vn_segments.csv`](../research/measured/vn_segments.csv)

### M4. Verklärte Nacht: tempo marks

The table shows each tempo mark with its bar number. The work has 33 tempo marks in 418 bars: one mark for each 12.7 bars.

| Bar | Tempo mark |
| --- | --- |
| 1 | Sehr langsam |
| 29 | Etwas bewegter |
| 39 | rit |
| 40 | tempo |
| 50 | mit Dämpfer |
| 69 | Lebhafter |
| 75 | Etwas belebter |
| 79 | Etwas zurückhaltend |
| 82 | Wieder belebter |
| 86 | Etwas zurückhaltend |
| 89 | dim e rit. |
| 91 | Lebhafter |
| 100 | Breiter |
| 105 | Etwas Ruhiger |
| 123 | Drängend, etwas unruhiger |
| 128 | rascher werdend |
| 132 | Lebhaft bewegt |
| 153 | Noch bewegter |
| 175 | Schneller werdend |
| 176 | Sehr breit |
| 181 | Sehr langsam |
| 201 | Schwer betont |
| 215 | Etwas zurückhaltend |
| 229 | Sehr breit und langsam |
| 266 | Etwas gedehnt |
| 270 | Wieder wie früher |
| 291 | steigernd, beschleunigend |
| 310 | Etwas bewegter |
| 320 | Etwas bewegt |
| 330 | beschleunigend |
| 367 | molto rit. |
| 370 | Sehr ruhig |
| 390 | Sehr gross |

Data file: [`research/measured/vn_marks.csv`](../research/measured/vn_marks.csv)

### M5. Verklärte Nacht: words for tempo change and expression

The table shows the words that occur two times or more. The spelling is the spelling of the source.

| Kind | Text | Count |
| --- | --- | --- |
| expression | dim | 19 |
| expression | cresc | 12 |
| expression | rit | 9 |
| expression | steigernd | 8 |
| expression | espress | 6 |
| expression | dolce | 5 |
| expression | molto rit | 4 |
| expression | immer leise | 3 |
| tempo | etwas zurückhaltend | 3 |
| expression | warm | 3 |
| expression | arpeggiando | 3 |
| tempo | sehr langsam | 2 |
| tempo | etwas bewegter | 2 |
| tempo | lebhafter | 2 |
| expression | zart | 2 |
| expression | dolciss | 2 |

Data file: [`research/measured/vn_mark_counts.csv`](../research/measured/vn_mark_counts.csv)

### M6. Verklärte Nacht: dynamic marks

A level mark stays in effect until the subsequent level mark. The soft levels (p and softer) are in effect for 64 percent of the time. The middle levels (mp and mf) are in effect for only 11 percent.

| Mark | Kind | Count of marks | Bars in effect | Share of time in effect |
| --- | --- | --- | --- | --- |
| pppp | level | 1 | 3 | 0.9 % |
| ppp | level | 11 | 21 | 6.0 % |
| pp | level | 29 | 126 | 31.7 % |
| p | level | 36 | 117 | 25.3 % |
| mp | level | 3 | 25 | 6.6 % |
| mf | level | 3 | 23 | 4.1 % |
| f | level | 20 | 15 | 3.1 % |
| ff | level | 20 | 56 | 12.4 % |
| fff | level | 4 | 21 | 5.4 % |
| fp | accent | 5 |  |  |
| sff | accent | 2 |  |  |
| sfp | accent | 1 |  |  |

Data file: [`research/measured/vn_dynamics.csv`](../research/measured/vn_dynamics.csv)

### M7. Verklärte Nacht: metres

The metres are the metres of the arrangement.

| Time signature | Bars | Share of bars |
| --- | --- | --- |
| 4/4 | 337 | 80.6 % |
| 3/4 | 36 | 8.6 % |
| 9/8 | 23 | 5.5 % |
| 6/8 | 17 | 4.1 % |
| 2/4 | 3 | 0.7 % |
| 1/2 | 2 | 0.5 % |
| (changes of metre) | 18 |  |

Data file: [`research/measured/vn_metres.csv`](../research/measured/vn_metres.csv)

### M8. Verklärte Nacht: motion of the bass

The study took the lowest note at each quarter-note beat. The table counts the interval between two different bass notes. The most frequent move of the bass is the semitone.

| Interval class | Name | Moves | Share |
| --- | --- | --- | --- |
| 0 | unison or octave | 68 | 6.9 % |
| 1 | semitone or major seventh | 297 | 30.0 % |
| 2 | whole tone or minor seventh | 187 | 18.9 % |
| 3 | minor third or major sixth | 151 | 15.2 % |
| 4 | major third or minor sixth | 91 | 9.2 % |
| 5 | fourth or fifth | 150 | 15.2 % |
| 6 | tritone | 46 | 4.6 % |

Data file: [`research/measured/vn_bass_motion.csv`](../research/measured/vn_bass_motion.csv)

### M9. Bartók, Out of Doors: the five pieces in one performance

The data come from a MIDI capture of one piano performance. The key velocity is the force of each key stroke, from 0 to 127.

| Piece | Minutes | Note starts | Note starts per second | Mean key velocity | Key velocity 5th percentile | Key velocity 95th percentile | Lowest midi pitch | Highest midi pitch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. With Drums and Pipes | 1.74 | 886 | 8.5 | 74 | 44 | 97 | 21 | 87 |
| 2. Barcarolla | 2.25 | 797 | 5.9 | 60 | 39 | 88 | 29 | 101 |
| 3. Musettes | 3.13 | 2089 | 11.1 | 65 | 34 | 95 | 32 | 95 |
| 4. The Night's Music | 5.27 | 1490 | 4.7 | 49 | 21 | 80 | 35 | 104 |
| 5. The Chase | 2.16 | 2713 | 20.9 | 69 | 35 | 99 | 24 | 101 |

Data file: [`research/measured/ood_pieces.csv`](../research/measured/ood_pieces.csv)

### M10. Bartók, Fourteen Bagatelles: metres and chords

Bagatelle no. 12 is an early form of the night music style. It has five different metres in 44 bars.

| Number | Bars | Notes | Metres with bar counts | Different metres | Chords share built from thirds | Chords share with semitone clash | Pitch class entropy bits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 18 | 135 | 4/4 (18) | 1 | 25.0 % | 75.0 % | 3.12 |
| 2 | 30 | 493 | 2/2 (28); 3/2 (2) | 2 | 66.0 % | 15.4 % | 3.29 |
| 3 | 24 | 383 | 3/4 (24) | 1 | 14.0 % | 100.0 % | 3.35 |
| 4 | 12 | 233 | 3/4 (12) | 1 | 94.4 % | 18.1 % | 2.83 |
| 5 | 90 | 1443 | 2/4 (90) | 1 | 76.2 % | 20.3 % | 2.73 |
| 6 | 25 | 154 | 2/2 (25) | 1 | 56.1 % | 24.2 % | 3.38 |
| 7 | 117 | 955 | 2/4 (115); 3/4 (2) | 2 | 21.9 % | 90.5 % | 3.52 |
| 8 | 31 | 317 | 2/4 (26); 3/4 (5) | 2 | 44.9 % | 63.5 % | 3.50 |
| 9 | 70 | 624 | 3/4 (70) | 1 |  |  | 3.50 |
| 10 | 102 | 1686 | 2/2 (95); 1/2 (4); 3/2 (3) | 3 | 31.3 % | 42.7 % | 3.49 |
| 11 | 87 | 672 | 2/4 (87) | 1 | 42.5 % | 24.6 % | 3.51 |
| 12 | 44 | 655 | 9/8 (21); 6/8 (12); 5/8 (5); 3/8 (3); 4/8 (3) | 5 | 74.7 % | 38.4 % | 3.49 |
| 13 | 26 | 422 | 4/4 (26) | 1 | 75.8 % | 39.8 % | 3.34 |
| 14 | 215 | 1297 | 3/8 (214); 3/4 (1) | 2 | 61.4 % | 12.6 % | 3.53 |

Data file: [`research/measured/bagatelles.csv`](../research/measured/bagatelles.csv)

### M13. Real orchestra recordings: loudness and stereo width

The recordings are public-domain recordings of full orchestras (Musopen). They are the reference for the sound of the audio master.

The loudness unit is the LUFS (ITU-R BS.1770). The loudness range is the difference between the loud and the soft passages (EBU Tech 3342). The short-term values are relative to the integrated loudness. The side level is the level of the difference of the two channels, relative to their sum.

| Recording | Minutes | Integrated loudness lufs | Loudness range lu | Short term 10th percentile lu | Short term median lu | Short term 95th percentile lu | Peak db | Crest factor db | Left right correlation | Side level db |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tchaikovsky, Symphony No. 6, I | 17.52 | -21.2 | 23.6 | -19.0 | -8.4 | 4.6 | -1.1 | 25.5 | 0.66 | -7.0 |
| Tchaikovsky, Symphony No. 6, IV | 10.32 | -24.1 | 21.7 | -16.3 | -7.4 | 5.4 | -4.7 | 24.3 | 0.69 | -7.3 |
| Brahms, Symphony No. 4, I | 12.68 | -16.3 | 13.6 | -9.6 | -1.9 | 4.0 | -1.0 | 18.7 | 0.55 | -5.4 |
| Smetana, Vltava | 12.85 | -12.3 | 20.5 | -16.9 | -5.0 | 3.7 | -1.0 | 16.0 | 0.53 | -5.1 |
| Borodin, In the Steppes of Central Asia | 7.64 | -20.9 | 22.7 | -15.6 | -7.4 | 7.0 | -1.0 | 24.6 | 0.39 | -3.5 |

Data file: [`research/measured/reference_recordings.csv`](../research/measured/reference_recordings.csv)

### M14. Real orchestra recordings: tone balance

The table gives the level of each third-octave band, relative to the total level, for the five recordings of table M13. The master of the project must agree with the mean values from 50 Hz to 8 kHz. Above 8 kHz, some of the recordings have no content, thus the values are not a reliable target.

| Band hz | Mean db | Lowest db | Highest db |
| --- | --- | --- | --- |
| 20 | -49.4 | -54.6 | -44.3 |
| 25 | -45.4 | -51.1 | -33.1 |
| 31 | -39.3 | -47.7 | -19.7 |
| 39 | -36.5 | -43.8 | -22.4 |
| 50 | -28.5 | -33.4 | -19.2 |
| 62 | -18.8 | -23.1 | -13.5 |
| 79 | -15.5 | -17.3 | -12.4 |
| 99 | -13.1 | -14.3 | -11.7 |
| 125 | -11.3 | -13.2 | -9.7 |
| 157 | -14.1 | -16.2 | -12.5 |
| 198 | -16.4 | -18.6 | -14.6 |
| 250 | -14.6 | -17.2 | -12.9 |
| 315 | -13.7 | -14.6 | -12.8 |
| 397 | -9.6 | -10.3 | -9.0 |
| 500 | -8.8 | -10.3 | -7.7 |
| 630 | -11.4 | -12.3 | -10.7 |
| 794 | -13.5 | -14.2 | -12.8 |
| 1000 | -12.7 | -14.1 | -10.2 |
| 1260 | -10.9 | -12.1 | -8.5 |
| 1587 | -10.8 | -11.1 | -10.6 |
| 2000 | -13.7 | -14.6 | -13.0 |
| 2520 | -17.1 | -17.9 | -16.1 |
| 3175 | -19.7 | -21.9 | -17.3 |
| 4000 | -23.7 | -26.2 | -19.5 |
| 5040 | -28.0 | -30.9 | -25.9 |
| 6350 | -31.4 | -35.5 | -29.3 |
| 8000 | -36.4 | -42.1 | -30.3 |
| 10079 | -43.5 | -53.8 | -30.0 |
| 12699 | -61.6 | -76.8 | -33.5 |
| 16000 | -70.4 | -90.7 | -36.7 |

Data file: [`research/measured/reference_tone_balance.csv`](../research/measured/reference_tone_balance.csv)

### M11. Comparison of all measured works

"Chord time" is the time in which three or more pitch classes sound together. A "semitone clash" is two notes that are a semitone apart (in all octaves). A "cluster" is three or more adjacent semitones. A "window" is four quarter notes (score data) or four seconds (performance data). The "top line" is the highest note at each note start.

Abbreviations: VN = *Verklärte Nacht*. OoD = *Out of Doors*. Bag. = Bagatelle.

| Measure | VN | VN part 1 | VN part 2 | OoD 1 | OoD 2 | OoD 3 | OoD 4 (Night) | OoD 5 | Bag. 12 | Bag. 1-14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Silence share of time | 1.8 % | 2.3 % | 1.2 % | 28.4 % | 0.3 % | 6.2 % | 2.3 % | 20.9 % | 13.8 % | 8.8 % |
| Mean pitch classes that sound together | 2.82 | 2.80 | 2.85 | 2.25 | 2.86 | 5.05 | 4.81 | 3.59 | 3.01 | 2.53 |
| Mean notes that sound together | 3.62 | 3.56 | 3.69 | 3.06 | 3.53 | 7.01 | 6.40 | 5.00 | 3.34 | 2.81 |
| Share of sounding time with 3 or more pitch classes | 65.2 % | 64.4 % | 66.0 % | 31.4 % | 39.3 % | 87.3 % | 85.0 % | 44.3 % | 71.9 % | 48.5 % |
| Chords: share built from thirds | 68.0 % | 69.1 % | 66.6 % | 8.7 % | 9.7 % | 1.7 % | 5.1 % | 6.3 % | 74.7 % | 55.6 % |
| Chords: share with a semitone clash | 23.8 % | 24.2 % | 23.2 % | 69.6 % | 72.7 % | 91.3 % | 92.5 % | 90.5 % | 38.4 % | 33.8 % |
| Chords: share with a 3-semitone cluster | 1.0 % | 1.4 % | 0.4 % | 20.9 % | 27.2 % | 68.2 % | 77.0 % | 70.0 % | 7.4 % | 3.5 % |
| Chords: share in one whole-tone scale | 12.9 % | 15.8 % | 9.5 % | 14.1 % | 6.9 % | 1.5 % | 4.5 % | 0.7 % | 11.2 % | 16.4 % |
| Chords: mean pitch classes | 3.42 | 3.45 | 3.39 | 4.23 | 4.46 | 5.56 | 5.34 | 6.45 | 3.75 | 3.69 |
| Share of sounding time: major and minor triads | 14.9 % | 11.0 % | 19.6 % | 0.0 % | 1.2 % | 0.1 % | 0.3 % | 0.7 % | 19.5 % | 6.1 % |
| Share of sounding time: vagrant chords | 17.5 % | 21.6 % | 12.8 % | 3.7 % | 2.5 % | 1.0 % | 2.0 % | 0.7 % | 15.1 % | 7.6 % |
| Share of sounding time: dominant chords | 5.7 % | 5.5 % | 6.0 % | 1.0 % | 0.1 % | 0.4 % | 0.9 % | 0.2 % | 0.8 % | 3.6 % |
| Share of sounding time: other seventh and ninth chords | 7.3 % | 7.5 % | 6.9 % | 1.7 % | 1.8 % | 0.5 % | 1.7 % | 1.4 % | 18.6 % | 11.9 % |
| Pitch-class entropy (bits, maximum 3.585) | 3.56 | 3.55 | 3.51 | 3.39 | 3.46 | 3.47 | 3.29 | 3.44 | 3.49 | 3.56 |
| Mean distinct pitch classes in one window | 7.57 | 7.38 | 7.63 | 7.48 | 9.24 | 8.53 | 7.12 | 10.24 | 8.07 | 6.85 |
| Share of windows with 10 or more pitch classes | 23.1 % | 21.8 % | 19.2 % | 28.0 % | 57.6 % | 35.6 % | 24.4 % | 69.7 % | 43.9 % | 17.5 % |
| Pitch, 5th percentile (MIDI) | 41 | 41 | 41 | 26 | 42 | 38 | 49 | 35 | 38 | 41 |
| Pitch, median (MIDI) | 62 | 61 | 63 | 54 | 58 | 62 | 68 | 52 | 65 | 64 |
| Pitch, 95th percentile (MIDI) | 87 | 86 | 89 | 79 | 74 | 82 | 91 | 88 | 82 | 82 |
| Pitch span, 5th to 95th percentile (semitones) | 46 | 45 | 48 | 53 | 32 | 44 | 42 | 53 | 44 | 41 |
| Lowest pitch (MIDI) | 36 | 36 | 36 | 21 | 29 | 32 | 35 | 24 | 33 | 24 |
| Highest pitch (MIDI) | 105 | 97 | 105 | 87 | 101 | 95 | 104 | 101 | 94 | 95 |
| Median width of simultaneous notes (semitones) | 28 | 26 | 31 | 12 | 17 | 31 | 26 | 33 | 17 | 15 |
| 90th percentile width of simultaneous notes (semitones) | 43 | 39 | 46 | 36 | 32 | 46 | 48 | 54 | 33 | 33 |
| Top line: repeated note | 2.4 % | 3.5 % | 1.6 % | 9.3 % | 0.5 % | 4.5 % | 13.1 % | 7.9 % | 24.0 % | 14.3 % |
| Top line: semitone | 16.7 % | 26.4 % | 10.2 % | 8.2 % | 16.6 % | 17.6 % | 17.9 % | 6.6 % | 39.6 % | 25.2 % |
| Top line: whole tone | 11.9 % | 10.3 % | 13.0 % | 15.4 % | 25.2 % | 17.6 % | 28.0 % | 12.8 % | 25.2 % | 17.2 % |
| Top line: minor or major third | 21.7 % | 19.5 % | 23.2 % | 13.3 % | 9.1 % | 11.3 % | 11.6 % | 14.6 % | 4.9 % | 14.1 % |
| Top line: fourth or fifth | 23.2 % | 18.4 % | 26.4 % | 10.5 % | 20.1 % | 6.5 % | 5.2 % | 7.3 % | 3.5 % | 18.9 % |
| Top line: sixth or seventh | 14.9 % | 10.6 % | 17.8 % | 2.6 % | 7.1 % | 8.4 % | 4.8 % | 10.6 % | 2.1 % | 5.6 % |
| Top line: octave or larger | 9.3 % | 11.3 % | 7.9 % | 40.8 % | 21.3 % | 34.1 % | 19.4 % | 40.1 % | 0.7 % | 4.6 % |
| Top line: tritone | 6.1 % | 7.4 % | 5.2 % | 7.0 % | 3.3 % | 2.0 % | 1.6 % | 2.3 % | 0.9 % | 3.5 % |
| Top line: descending share of moves | 54.8 % | 54.5 % | 55.0 % | 47.0 % | 52.3 % | 50.9 % | 47.1 % | 41.9 % | 43.9 % | 54.1 % |
| Top line: mean size of moves (semitones) | 5.47 | 5.22 | 5.64 | 11.10 | 6.59 | 9.85 | 7.50 | 14.27 | 2.06 | 4.09 |
| Note starts in one second | 5.80 | 5.19 | 6.52 | 8.48 | 5.89 | 11.11 | 4.71 | 20.89 | - | - |

Data file: [`research/measured/fingerprints.csv`](../research/measured/fingerprints.csv)

### M12. The most frequent sonorities

A sonority is the set of pitch classes that sound at one moment. A name of the form "set type (0 1 2 3 4)" gives the semitone steps of a set that has no chord name.

**Schoenberg: Verklärte Nacht, complete**

| Rank | Sonority | Share of the sounding time |
| --- | --- | --- |
| 1 | single pitch class | 10.3 % |
| 2 | interval: minor third or major sixth | 7.9 % |
| 3 | major triad | 7.6 % |
| 4 | minor triad | 7.3 % |
| 5 | interval: major third or minor sixth | 6.7 % |
| 6 | diminished triad | 6.4 % |
| 7 | interval: fourth or fifth | 4.5 % |
| 8 | half-diminished seventh | 3.6 % |
| 9 | diminished seventh | 3.1 % |
| 10 | dominant seventh | 2.8 % |
| 11 | interval: whole tone or minor seventh | 2.7 % |
| 12 | set type (0 3 5) | 2.3 % |

**Bartók: Out of Doors, 4. The Night's Music**

| Rank | Sonority | Share of the sounding time |
| --- | --- | --- |
| 1 | set type (0 1 2 3 4) | 25.5 % |
| 2 | set type (0 1 2 3 4 5) | 6.3 % |
| 3 | semitone cluster (0 1 2 3) | 5.6 % |
| 4 | set type (0 2 3) | 3.9 % |
| 5 | interval: semitone or major seventh | 3.9 % |
| 6 | set type (0 2 3 4 5 6) | 3.0 % |
| 7 | interval: minor third or major sixth | 2.7 % |
| 8 | interval: major third or minor sixth | 2.7 % |
| 9 | single pitch class | 2.2 % |
| 10 | set type (0 1 2 3 4 8) | 2.2 % |
| 11 | set type (0 1 2 3 4 6 7 8 9 10) | 2.0 % |
| 12 | set type (0 1 2 3 4 5 6 7) | 1.6 % |

**Bartók: Fourteen Bagatelles op. 6, complete**

| Rank | Sonority | Share of the sounding time |
| --- | --- | --- |
| 1 | single pitch class | 29.3 % |
| 2 | interval: major third or minor sixth | 6.3 % |
| 3 | minor seventh | 5.9 % |
| 4 | interval: minor third or major sixth | 4.0 % |
| 5 | minor triad | 3.9 % |
| 6 | interval: semitone or major seventh | 3.5 % |
| 7 | interval: fourth or fifth | 3.4 % |
| 8 | interval: whole tone or minor seventh | 3.4 % |
| 9 | half-diminished seventh | 2.3 % |
| 10 | major triad | 2.1 % |
| 11 | set type (0 4 6) | 2.0 % |
| 12 | dominant seventh | 1.7 % |

Data file: [`research/measured/sonorities.csv`](../research/measured/sonorities.csv)

### M15. Literal repetition: Verklärte Nacht and the new work

The table shows how frequently a bar comes again with no change. Each value is a share of the bars that have notes. "The same" means the same notes at the same positions with the same lengths. A voice is one player of the new work, or one voice of the piano arrangement of *Verklärte Nacht*. An orchestra has more voices with accompaniment figures than a piano arrangement: thus the values for one voice are not fully comparable.

| Measure | Verklärte Nacht | New work, complete | New work, part 1 | New work, part 2 | New work, part 3 | New work, part 4 | New work, part 5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Full texture: bar is the same as the bar before | 2.4 % | 1.2 % | 0.0 % | 2.8 % | 0.0 % | 0.0 % | 0.0 % |
| Full texture: bar is the same as one of the 8 bars before | 5.1 % | 8.7 % | 0.0 % | 12.7 % | 0.0 % | 0.0 % | 20.5 % |
| Full texture: bar is the same at a different pitch | 3.9 % | 0.2 % | 0.0 % | 0.0 % | 0.0 % | 0.8 % | 0.0 % |
| Full texture: bar has the same rhythm with different notes | 8.7 % | 11.3 % | 0.0 % | 16.9 % | 0.0 % | 11.5 % | 7.2 % |
| One voice: bar is the same as one of its 8 bars before | 10.2 % | 51.0 % | 26.1 % | 54.3 % | 50.7 % | 25.5 % | 63.8 % |
| One voice: bar is the same at a different pitch | 8.5 % | 18.2 % | 2.3 % | 25.0 % | 0.0 % | 12.2 % | 12.0 % |
| Bars in a block of 4 bars that is the same as an earlier block | 0.0 % | 5.2 % | 0.0 % | 6.6 % | 0.0 % | 0.0 % | 14.5 % |

Data files: [`research/measured/repetition.csv`](../research/measured/repetition.csv), [`research/measured/work_repetition.csv`](../research/measured/work_repetition.csv)

### M16. The new work: harmony

The table measures the new work with the method of table M11. "The turn" is the change from the dark half to the light half of the work (the start of part 4). Part 3 is the zone of the profile "Night": the ranges of the profile "Transfigured" do not apply to it.

| Measure | Range of the profile "Transfigured" | Verklärte Nacht | New work, complete | New work, before the turn | New work, after the turn | New work, part 1 | New work, part 2 | New work, part 3 | New work, part 4 | New work, part 5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Chords: share built from thirds | 0.62 to 0.72 | 68.0 % | 43.4 % | 38.9 % | 48.3 % | 48.4 % | 51.1 % | 6.2 % | 54.8 % | 34.2 % |
| Chords: share with a semitone clash | 0.20 to 0.28 | 23.8 % | 50.4 % | 70.0 % | 29.3 % | 59.0 % | 62.6 % | 92.0 % | 26.5 % | 35.4 % |
| Chords: share with a 3-semitone cluster | 0.00 to 0.02 | 1.0 % | 15.2 % | 26.5 % | 3.0 % | 13.3 % | 5.4 % | 81.4 % | 0.0 % | 9.6 % |
| Chords: share in one whole-tone scale | 0.09 to 0.16 | 12.9 % | 1.1 % | 2.0 % | 0.1 % | 2.8 % | 2.6 % | 0.0 % | 0.2 % | 0.0 % |
| Chords: mean pitch classes | - | 3.42 | 4.36 | 4.69 | 4.00 | 4.19 | 4.21 | 6.02 | 3.98 | 4.06 |
| Share of sounding time: major and minor triads | - | 14.9 % | 15.7 % | 9.2 % | 24.9 % | 13.2 % | 10.7 % | 2.0 % | 27.9 % | 19.6 % |
| Share of sounding time: vagrant chords | - | 17.5 % | 4.7 % | 7.9 % | 0.2 % | 11.8 % | 9.6 % | 0.0 % | 0.3 % | 0.2 % |
| Share of sounding time: dominant chords | 0.05 to 0.07 | 5.7 % | 7.7 % | 6.4 % | 9.7 % | 1.0 % | 9.4 % | 0.0 % | 12.6 % | 4.6 % |
| Share of sounding time: other seventh and ninth chords | - | 7.3 % | 6.6 % | 4.2 % | 10.0 % | 7.6 % | 3.7 % | 3.6 % | 14.0 % | 3.1 % |
| Mean pitch classes that sound together | - | 2.82 | 3.81 | 3.81 | 3.81 | 3.36 | 3.33 | 5.58 | 3.97 | 3.54 |
| Mean distinct pitch classes in one window | 7 to 8 | 7.57 | 4.76 | 4.91 | 4.54 | 4.39 | 5.34 | 3.81 | 4.72 | 4.24 |

Data file: [`research/measured/work_harmony.csv`](../research/measured/work_harmony.csv)

### M17. The new work: use of the instruments

"Range in use" is the distance from the lowest note to the highest note of the player, as a part of the range of the instrument. The three subsequent columns divide the range of the instrument into three equal parts. The column "Techniques" lists each way to play that is not the usual way.

| Player | Share of the time | Range in use | Notes in the low third | Notes in the middle third | Notes in the high third | Techniques |
| --- | --- | --- | --- | --- | --- | --- |
| fl1 | 39.1 % | 94.6 % | 2.6 % | 44.1 % | 53.3 % | - |
| fl2 | 31.8 % | 75.7 % | 1.0 % | 45.9 % | 53.1 % | grace notes |
| fl3 | 22.7 % | 70.6 % | 39.6 % | 59.9 % | 0.5 % | - |
| ob1 | 35.0 % | 81.8 % | 20.5 % | 61.6 % | 17.9 % | - |
| ob2 | 28.3 % | 81.8 % | 16.6 % | 63.0 % | 20.4 % | grace notes |
| ob3 | 6.7 % | 78.1 % | 26.5 % | 65.3 % | 8.2 % | grace notes |
| cl1 | 38.3 % | 75.0 % | 21.2 % | 63.7 % | 15.1 % | grace notes |
| cl2 | 28.1 % | 68.2 % | 5.8 % | 69.4 % | 24.8 % | - |
| cl3 | 26.8 % | 58.3 % | 63.8 % | 36.2 % | 0.0 % | grace notes |
| cbcl | 25.7 % | 62.8 % | 16.7 % | 81.5 % | 1.8 % | grace notes |
| bn1 | 43.3 % | 73.8 % | 25.5 % | 70.4 % | 4.1 % | - |
| bn2 | 41.9 % | 64.3 % | 29.6 % | 68.5 % | 1.9 % | grace notes |
| bn3 | 34.0 % | 81.8 % | 6.4 % | 65.0 % | 28.6 % | - |
| hn1 | 53.5 % | 64.3 % | 0.2 % | 49.3 % | 50.5 % | desk: solo; mute: on |
| hn2 | 47.8 % | 64.3 % | 2.2 % | 73.5 % | 24.3 % | mute: on |
| hn3 | 49.7 % | 61.9 % | 0.2 % | 72.7 % | 27.1 % | mute: on |
| hn4 | 46.3 % | 83.3 % | 12.7 % | 68.1 % | 19.2 % | mute: on |
| hn5 | 15.9 % | 50.0 % | 0.0 % | 47.5 % | 52.5 % | - |
| hn6 | 15.9 % | 50.0 % | 0.0 % | 60.2 % | 39.8 % | - |
| tpt1 | 23.3 % | 68.8 % | 7.5 % | 76.0 % | 16.5 % | mute: on |
| tpt2 | 21.8 % | 68.8 % | 16.2 % | 75.9 % | 8.0 % | - |
| tpt3 | 18.2 % | 71.9 % | 29.6 % | 62.5 % | 7.9 % | - |
| tbn1 | 27.7 % | 79.4 % | 39.2 % | 54.0 % | 6.8 % | - |
| tbn2 | 27.5 % | 79.4 % | 46.5 % | 47.0 % | 6.5 % | - |
| btbn | 25.0 % | 64.1 % | 50.8 % | 48.7 % | 0.5 % | - |
| tuba | 26.3 % | 66.7 % | 55.6 % | 43.0 % | 1.5 % | - |
| timp | 31.4 % | 81.8 % | 55.8 % | 37.2 % | 7.0 % | mallet: soft; tremolo |
| perc1 | 9.3 % | - | - | - | - | tremolo |
| perc2 | 42.6 % | 58.1 % | 23.5 % | 75.7 % | 0.8 % | motor: on |
| perc3 | 14.3 % | - | - | - | - | tremolo |
| perc4 | 18.4 % | - | - | - | - | tremolo |
| perc5 | 7.6 % | - | - | - | - | - |
| perc6 | 11.7 % | - | - | - | - | tremolo |
| harp.rh | 33.5 % | 56.2 % | 0.0 % | 32.6 % | 67.3 % | - |
| harp.lh | 5.9 % | 32.5 % | 67.1 % | 32.9 % | 0.0 % | - |
| cimb.rh | 3.5 % | 36.8 % | 0.0 % | 46.0 % | 54.0 % | tremolo |
| cimb.lh | 18.3 % | 42.1 % | 65.3 % | 34.7 % | 0.0 % | tremolo |
| mand | 11.9 % | 68.4 % | 23.8 % | 57.0 % | 19.2 % | tremolo |
| cel.rh | 13.1 % | 46.7 % | 0.0 % | 30.4 % | 69.6 % | - |
| cel.lh | 0.0 % | - | - | - | - | no notes |
| pno.rh | 58.5 % | 64.4 % | 3.6 % | 87.5 % | 8.9 % | - |
| pno.lh | 35.9 % | 40.2 % | 92.0 % | 8.0 % | 0.0 % | grace notes; tremolo |
| acc.rh | 64.2 % | 45.8 % | 0.0 % | 73.6 % | 26.4 % | - |
| acc.lh | 0.0 % | - | - | - | - | no notes |
| vn1 | 81.5 % | 74.0 % | 8.6 % | 83.4 % | 8.0 % | desk: solo; harmonic; mute: on; sul ponticello; tremolo |
| vn2 | 94.0 % | 72.0 % | 58.6 % | 41.0 % | 0.3 % | mute: on; spiccato; sul ponticello; sul tasto; tremolo; vibrato: none |
| va | 133.8 % | 80.0 % | 43.9 % | 52.3 % | 3.8 % | mute: on; sul ponticello; sul tasto; tremolo; vibrato: none |
| vc | 125.4 % | 85.4 % | 48.1 % | 48.4 % | 3.5 % | desk: solo; glissando; mute: on; pizzicato; spiccato; sul ponticello; sul tasto; tremolo; vibrato: none |
| cb | 85.3 % | 62.8 % | 52.8 % | 46.3 % | 0.9 % | mute: on; pizzicato; sul tasto; tremolo |

Instruments in the list of the orchestra that have no notes: marimba, crotales, singing bowls, triangle, temple blocks, claves, guiro, cowbells, finger cymbals, wind chimes, waterphone.

Data file: [`research/measured/work_instruments.csv`](../research/measured/work_instruments.csv)

## Part 2: Sourced tables

The study team wrote the tables of this part from the sources. The directory [`research/tables`](../research/tables) has the data files.

### S1. Reference works

The table lists the works that the study uses, and the reason for each work.

| Composer | Work | Year | Forces | Minutes | Use in this study | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg | Verklärte Nacht op. 4 | 1899 (string orchestra 1917; revised 1943) | String sextet; later string orchestra | 27.1 to 29.3 (five recordings) | Primary model: harmony, theme work, form in one movement | frisch1993; imslp-vn; ia-vn1924 |
| Schoenberg | Pelleas und Melisande op. 5 | 1902 to 1903 | Very large orchestra |  | Model for a very large late-Romantic orchestra | wiki-pelleas |
| Schoenberg | Gurre-Lieder | 1900 to 1911 | Soloists, choruses, about 150 players |  | Upper limit of orchestra size; unusual percussion (iron chains) | wiki-gurre |
| Schoenberg | Chamber Symphony No. 1 op. 9 | 1906 | 15 solo players |  | Harmony built from fourths; motto theme of fourths | wiki-op9 |
| Schoenberg | Five Pieces for Orchestra op. 16 | 1909 (revised 1949) | Very large orchestra |  | No. 3 "Farben": change of tone colour as the musical event | wiki-op16 |
| Bartók | Bagatelle op. 6 no. 12 | 1908 | Piano |  | Early form of the night music style | wiki-nightmusic; dcml-bagatelles |
| Bartók | Out of Doors, no. 4: The Night's Music | 1926 | Piano | 4.7 (from the metronome marks); 5.3 (measured performance) | First complete night music piece; it gave the style its name | wiki-ood; bednarek2026 |
| Bartók | String Quartet No. 4 | 1928 | String quartet | About 24 (movements about 6-3-6-3-6) | Arch form in five movements; night music in the centre | wiki-sq4 |
| Bartók | String Quartet No. 5 | 1934 | String quartet |  | Arch form; two night music movements; Bulgarian metres | wiki-sq5 |
| Bartók | Music for Strings, Percussion and Celesta | 1936 | Two string groups, percussion, celesta, harp, piano |  | Fugue with proportion plan (I); night music with percussion colour (III) | wiki-mspc; solomon1973; roberts2021 |
| Bartók | Sonata for Two Pianos and Percussion | 1937 | 2 pianos, 2 percussion players (7 instruments) |  | Night music (II); exact percussion directions | wiki-son2p |
| Bartók | Divertimento for String Orchestra | 1939 | String orchestra with solo group |  | Slow movement with very flexible tempo | wiki-div |
| Bartók | Concerto for Orchestra | 1943 (revised 1945) | Large orchestra | About 38 | Night music for full orchestra (I introduction and III Elegia) | wiki-cfo; wiki-nightmusic |
| Bartók | Piano Concerto No. 3 | 1945 | Piano and orchestra |  | Night music with real bird calls (II) | wiki-pc3; wiki-nightmusic |
| Corigliano | Concerto for Clarinet and Orchestra | 1977 | Clarinet and large orchestra | 29 | Full orchestra as a group of soloists; players around the hall | cor-clarinet |
| Corigliano | Three Hallucinations | 1981 | Large orchestra | 13 | Trance music: quotation, tritone, blurred cadences, orchestra glissando | cor-halluc |
| Corigliano | Pied Piper Fantasy | 1982 | Flute, large orchestra, children's group | 38 | Theatre in the concert hall; two groups in different tempos | cor-piper |
| Corigliano | Symphony No. 1 | 1988 | Very large orchestra | 40 | Rage and memory: offstage piano, brass around the orchestra, layered accelerations | cor-sym1 |
| Corigliano | String Quartet | 1995 | String quartet | 33 | Arch form after Bartók; Nocturne from the night calls of Fez | cor-quartet |
| Corigliano | The Red Violin: Chaconne | 1997 | Violin and orchestra | 17 | Chaconne chords and one lyric theme hold a long form together | cor-chaconne |
| Corigliano | Vocalise | 1999 | Soprano, orchestra, electronics | 20 | Acoustic sound that changes into amplified, looped sound | cor-vocalise |
| Corigliano | Symphony No. 2 | 2000 | String orchestra (minimum 6-5-4-4-2) | 35 | The quartet as string symphony; divided sections; solo calls | cor-sym2 |
| Corigliano | Circus Maximus (Symphony No. 3) | 2004 | Three wind bands: stage, surround, marching | 35 | Space as form; "Night Music I" (nature) and "Night Music II" (city) | cor-circus; wiki-circus |
| Corigliano | Conjurer | 2007 | Percussion solo and string orchestra | 35 | Percussion in three families: wood, metal, skin | cor-conjurer |
| Corigliano | Chiaroscuro | 1997 | Two pianos tuned a quarter-tone apart | 12 | Quarter-tones as expression | cor-chiaroscuro |

Data file: [`research/tables/works.csv`](../research/tables/works.csv)

### S2. Orchestra sizes

Each number is the number of players. A note in parentheses shows the auxiliary instruments.

| Work | Flutes | Oboes | Clarinets | Bassoons | Horns | Trumpets | Trombones | Tubas | Timpani and percussion | Keyboards and harp | Strings | Special | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Schoenberg: Pelleas und Melisande (1903) | 4 (piccolo, 3 flutes; flute 3 = piccolo 2) | 4 (3 oboes, English horn; oboe 3 = English horn 2) | 5 (E-flat, 3 clarinets, bass; clarinet 3 = bass 2) | 4 (3 bassoons, contrabassoon) | 8 | 4 | 5 (1 alto + 4 tenor-bass) | 1 | 2 timpani players; triangle, cymbals, tam-tam, large tenor drum, bass drum, glockenspiel | 4 harps (number as in the article) | Full sections |  | wiki-pelleas |
| Schoenberg: Five Pieces op. 16 (1909 version) | 4 (piccolo, 3 flutes; flute 3 = piccolo 2) | 4 (3 oboes, English horn) | 5 (D clarinet, 3 clarinets, bass; clarinet 3 = contrabass clarinet) | 4 (3 bassoons, contrabassoon) | 6 | 3 | 4 | 1 | Timpani; bass drum, crash cymbals, suspended cymbal, triangle, tam-tam, xylophone | Celesta, harp | Full sections | Contrabass clarinet | wiki-op16 |
| Schoenberg: Gurre-Lieder (1911) | 8 (4 piccolos + 4 flutes) | 5 (3 oboes + 2 English horns) | 7 (3 clarinets, 2 E-flat, 2 bass) | 5 (3 bassoons, 2 contrabassoons) | 10 (4 play Wagner tubas also) | 7 (6 + bass trumpet) | 7 (alto, 4 tenor, bass, contrabass) | 1 contrabass tuba | 6 timpani (2 players); tenor drum, snare drum, bass drum, cymbals, triangle, ratchet, tam-tam, glockenspiel, xylophone | Celesta, 4 harps | 20-20-16-16-12 | 2 large iron chains; Wagner tubas; about 150 players and 200 singers | wiki-gurre |
| Schoenberg: Chamber Symphony No. 1 (1906) | 1 (also piccolo) | 2 (oboe + English horn) | 3 (E-flat, clarinet, bass) | 2 (bassoon, contrabassoon) | 2 | 0 | 0 | 0 | None | None | 1-1-1-1-1 | 15 solo players: 10 winds and 5 strings | wiki-op9 |
| Bartók: Music for Strings, Percussion and Celesta (1936) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Timpani; xylophone, snare drum, cymbals, tam-tam, bass drum | Celesta, piano (celesta player joins for four hands), harp | Two full string groups, on opposite sides of the stage | No winds; timpani glissandi | wiki-mspc |
| Bartók: Concerto for Orchestra (1943) | 3 (flute 3 = piccolo) | 3 (oboe 3 = English horn) | 3 (clarinet 3 = bass) | 3 (bassoon 3 = contrabassoon) | 4 | 3 | 3 | 1 | Timpani; side drum, bass drum, cymbals, triangle, tam-tam | 2 harps | Full sections | Each section has solo work | wiki-cfo |
| Bartók: Piano Concerto No. 2 (1931) | 2 (flute 2 = piccolo) | 2 | 2 | 2 (bassoon 2 = contrabassoon) | 4 | 3 | 3 | 1 | Timpani; snare drum, bass drum, triangle, cymbals | Solo piano | Full sections |  | wiki-pc2 |
| Corigliano: Concerto for Clarinet (1977) | 4 (3 flutes + piccolo) | 4 (3 oboes + English horn) | 3 (2 clarinets + bass) | 4 (3 bassoons + contrabassoon) | 6 | 4 | 3 | 1 | Timpani; 3 percussion players | Harp, piano | Minimum 14-14-12-12-6 | Solo clarinet | cor-clarinet |
| Corigliano: Three Hallucinations (1981) | 3 (with piccolo) | 3 | 3 (with E-flat and bass) | 3 (with contrabassoon) | 4 | 3 | 3 | 1 | 2 timpani players (2 sets of 4 drums); 5 percussion players | Harp, 2 pianos, electronic organ | Minimum 12-10-8-8-6 |  | cor-halluc |
| Corigliano: Pied Piper Fantasy (1982) | 3 (2 flutes + piccolo) | 3 | 3 (with E-flat and bass) | 3 (with contrabassoon) | 4 | 3 | 3 | 1 | Timpani; 4 percussion players | Harp, piano (also celesta) | Minimum 14-12-10-8-6 | Solo flute (also tin whistle); children's group: 9 to 18 flutes and 2 drums | cor-piper |
| Corigliano: Symphony No. 1 (1988) | 4 (3 play piccolo also) | 4 (3 oboes + English horn) | 4 (with E-flat, bass, contrabass) | 4 (3 bassoons + contrabassoon) | 6 | 5 | 4 | 2 | Timpani; minimum 5 percussion players | Harp, piano (offstage) | Full sections | Brass in a half-circle around the orchestra | cor-sym1 |
| Corigliano: The Red Violin: Chaconne (1997) | 3 (2 play piccolo also) | 2 | 2 | 2 | 4 | 2 | 3 (2 tenor + bass) | 1 | Timpani; 3 percussion players | Harp, piano or celesta | Full sections | Solo violin | cor-chaconne |
| Corigliano: Vocalise (1999) | 3 (1 plays piccolo also) | 2 | 3 (1 plays bass also) | 2 | 4 | 4 (1 plays piccolo trumpet also) | 3 | 1 (optional) | Timpani; 4 percussion players | Harp, piano (also celesta) | Full sections | Soprano; microphones, loudspeakers around the hall, live looping; 3 offstage trumpets play crotales and glockenspiel also | cor-vocalise |
| Corigliano: Phantasmagoria (2000) | 3 (2 play piccolo also) | 3 (1 plays English horn also) | 3 (with E-flat and bass) | 3 (1 plays contrabassoon also) | 4 | 4 | 3 | 1 | Timpani; 4 percussion players | Harp, piano (also celesta and harmonium or synthesizer) | Full sections |  | cor-site |
| Corigliano: Mr. Tambourine Man (2000) | 3 (2 play piccolo also) | 3 (1 plays English horn also) | 3 (with E-flat and bass) | 3 (1 plays contrabassoon also) | 4 | 4 | 3 (2 tenor + bass) | 1 | Timpani; 3 percussion players | Harp, piano | Full sections | Soprano; alto saxophone (also baritone saxophone) | cor-site |
| Corigliano: Circus Maximus (2004) | 5 (stage 4; marching piccolo) | 4 (stage) | 8 (stage 3 + 2 bass + contrabass; surround 1; marching E-flat) | 4 (stage 3 + contrabassoon) | 6 (stage 4; surround 2) | 15 (stage 4; surround 11, 2 of them march also) | 6 (stage 4; marching 2) | 2 tubas + 2 euphoniums | Timpani; 4 to 5 percussion players on stage; 3 surround (1 of them marches also) | Piano, harp | 1 double bass (surround) | 4 saxophones (surround); 12-gauge shotgun fired at the end | wiki-circus; cor-circus |

Data file: [`research/tables/forces.csv`](../research/tables/forces.csv)

### S3. Form and proportion

The table gives the plan of each reference work and the positions of its events.

| Work | Parameter | Value | Note | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| Schoenberg: Verklärte Nacht | Length | 418 bars in one movement | The parsed source has the same count | frisch1993; billam2013 | R |
| Schoenberg: Verklärte Nacht | Plan | Five sections: A B A' C A'' | One section for each stanza of the poem. A sections: narrator. B: the woman. C: the man | wellesz1925; frisch1993 | R |
| Schoenberg: Verklärte Nacht | Section bars | 1-28; 29-187; 188-228; 229-369; 370-418 | Part 1 = bars 1-228 (minor). Part 2 = bars 229-418 (major) | pfannkuch1963; frisch1993 | R |
| Schoenberg: Verklärte Nacht | Sub-sections of section 2 | 29-49; 50-104; 105-131; 132-180; 181-187 | Themes 2; themes 3 and 4; theme 5; development; climax return of theme 2a | pfannkuch1963; frisch1993 | R |
| Schoenberg: Verklärte Nacht | Key plan | D minor (1); B-flat minor (50); E major (105); E-flat minor (to 228); D major (229); F-sharp major (249-265); D-flat major (dominant pedal from 270); F major (291); D-flat major (320); D major (343 and 370 to the end) | The key signatures of the parsed source change at the same bars | frisch1993; billam2013 | R |
| Schoenberg: Verklärte Nacht | Approach to the tonic | By semitone from above (E-flat minor) and from below (D-flat major) | Schoenberg wrote that he knew of this plan. The dominant is not a large key area | schoenberg1932; swift1977; frisch1993 | R |
| Schoenberg: Verklärte Nacht | Number of themes | 11 theme groups; 5 groups in part 1 | Many short themes, in pairs (a and b). Later themes come from earlier themes | frisch1993 | R |
| Schoenberg: Verklärte Nacht | Theme unit | 1 bar | Pattern: unit, unit again at the same pitch, then a longer continuation (1 + 1 + 2) | frisch1993 | R |
| Schoenberg: Verklärte Nacht | Section breaks | Ritardando (28); fermata (49); change of metre (74-75); dominant preparation (100-104) | Each new theme group has a clear signal | frisch1993 | R |
| Schoenberg: Verklärte Nacht | Climax points | Bars 175-181; 338-340 (largest, fff); 391-393 ("Sehr gross") | The two late climaxes are almost the same music. Each leads to different music | frisch1993; billam2013 | R |
| Schoenberg: Verklärte Nacht | Reprise | Bar 370 | Themes 1a, 7a, and 10 sound together in D major. Coda from bar 401 | frisch1993 | R |
| Schoenberg: Verklärte Nacht | Cut that the composer refused | 54 bars (13 percent) | Bruno Walter asked for the cut in 1943. Schoenberg kept all bars | frisch1993 | R |
| Bartók: Music for Strings, Percussion and Celesta, I | Length | 88 bars | Lendvai counts 89 (he adds one silent bar) | roberts2021; howat1983 | R |
| Bartók: Music for Strings, Percussion and Celesta, I | Fugue entries | A, then E (fifth up), D (fifth down), B, G, and so on | Entries go out in fifths in two directions. They meet at E-flat, a tritone from A | solomon1973 | R |
| Bartók: Music for Strings, Percussion and Celesta, I | Events by bar | End of exposition 20 or 21; canon 26; mutes off 33 to 35; percussion in 34; subject on E-flat 44; fff climax 55 to 56; inverted stretto 65; mutes on 68 to 69; subject with its inversion and celesta 78; coda 82 | Authors count some bars differently | solomon1973; roberts2021; howat1983; lendvai1971 | R |
| Bartók: Music for Strings, Percussion and Celesta, I | Climax position | 0.63 (bar 55.5 of 88) | Golden section = 0.618. The subject comes to E-flat at 0.50 | roberts2021; howat1983 | R |
| Bartók: Music for Strings, Percussion and Celesta, I | Shape | pp to fff to ppp | After the climax the subject is inverted and the entry order goes backward | solomon1973; roberts2021 | R |
| Bartók: Music for Strings, Percussion and Celesta, III | Shape | Arch: A B C B' A' | Climax and inversion in the centre | roberts2021; howat1983 | R |
| Bartók: Music for Strings, Percussion and Celesta | Tonal plan | I: A, E-flat, A. II: C, F-sharp, C | The middle of a movement is a tritone from its start | wiki-axis; wiki-mspc | R |
| Bartók: The Night's Music | Length | 71 bars |  | wiki-ood | R |
| Bartók: The Night's Music | Materials | A (night noises): bars 1-17, 34-37, 48, 67-71. B (chorale in G): 17-34, 58-66. C (flute melody, Dorian on C-sharp): 37-58, 61-67, 70-71 | Form: loose rondo or three parts. B and C sound together in bars 61-66, with different tempos and key centres | wiki-ood; schneider2006 | R |
| Bartók: The Night's Music | Key centres | G and C-sharp | A tritone apart | wiki-ood | R |
| Bartók: String Quartet No. 4 | Plan | Five movements in arch form: I and V related; II and IV related; III alone | Lengths about 6, 3, 6, 3, 6 minutes. III is night music | wiki-sq4 | R |
| Bartók: String Quartet No. 5 | Plan | Five movements in arch form | I: keys go up by whole tones: B-flat, C, D; E; F-sharp, A-flat, B-flat. The reprise gives the themes in reverse order and inverted | wiki-sq5 | R |
| Bartók: Piano Concerto No. 2 | Plan | Fast - slow - fast - slow - fast | II = Adagio - Presto - Adagio. Night music with a fast centre | wiki-pc2; wiki-ood | R |
| Bartók: Sonata for Two Pianos and Percussion | Plan | Three movements. I takes half of the full duration | I starts in F-sharp and ends in C major (a tritone). II is night music in three parts (A B A) | wiki-son2p | R |
| Bartók: Sonata for Two Pianos and Percussion, I | Reprise position | Bar 274 of 443 (0.618) | Claim by Lendvai. Not checked in this study | reference | K |
| Corigliano: method | First step | The shape ("architecture") of the work, before all notes | His statement: he has worked in this sequence for three decades | cor-circus | R |
| Corigliano: method | Second step | A problem to solve, taken from the occasion, the player, or the hall | Examples: full orchestra with a solo wind instrument; a percussion soloist who carries the melodies | cor-clarinet; cor-conjurer; cor-piper | R |
| Corigliano: Symphony No. 1 | Plan | Four parts. I: A B A (rage, memory, rage). II: tarantella. III: chaconne. IV: epilogue | 40 minutes. The A to G-sharp motive from the start comes back in III | cor-sym1 | R |
| Corigliano: String Quartet and Symphony No. 2 | Plan | Five movements in arch form: Prelude, Scherzo, Nocturne, Fugue, Postlude | 33 to 35 minutes. I and V related; II and IV related; III is night music | cor-quartet; cor-sym2 | R |
| Corigliano: Circus Maximus | Plan | Eight sections with no pause: Introitus; Screen/Siren; Channel Surfing; Night Music I; Night Music II; Circus Maximus; Prayer; Coda: Veritas | 35 minutes. The peak (VI) uses the material of all earlier sections | cor-circus | R |
| Corigliano: The Red Violin: Chaconne | Plan | One movement on a repeated chord pattern | 17 minutes. Slow start; solo studies that go faster; high slow melody; cadenza; large final statement; fast coda | cor-chaconne | R |
| Corigliano: Vocalise | Plan | One arc: voice alone; voice and orchestra; amplified voice; loops at the peak; echoes at the end | 20 minutes. The end is the opening melody, now through the loudspeakers | cor-vocalise | R |

Data file: [`research/tables/form.csv`](../research/tables/form.csv)

### S4. Tempo

The table gives metronome marks and durations from the scores and the recordings.

| Work | Section | Mark | Value | Note | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg: Verklärte Nacht | Full work (five recordings) |  | 27 min 07 s; 27 min 41 s; 27 min 45 s; 27 min 50 s; 29 min 18 s | Mean 27.9 minutes. The 27 min 50 s recording is from 1924 | imslp-vn; ia-vn1924 | R |
| Schoenberg: Verklärte Nacht | Full work (timing in the arrangement) |  | 25.0 minutes | The timing of the arrangement is 1.12 times faster than the mean recording | billam2013 | M |
| Bartók: The Night's Music | Full piece | Lento - (Un poco) più andante | Quarter note = 72 in 3/2 | 4 min 40 s from the metronome marks. Bartók's estimate: about 4.5 minutes. Measured performance: 5 min 16 s | wiki-ood; bednarek2026 | R |
| Bartók: With Drums and Pipes | Full piece | Pesante | Quarter note = 132 in 2/4 | 1 min 45 s | wiki-ood | R |
| Bartók: Musettes | Full piece | Moderato | Quarter note = 96 | 2 min 35 s | wiki-ood | R |
| Bartók: The Chase | Full piece | Presto | Dotted quarter note = 160 in 6/8 | 2 min to 2 min 12 s | wiki-ood | R |
| Bartók: Music for Strings, Percussion and Celesta | III | Adagio | Eighth note = 66 | Night music | roberts2021 | R |
| Bartók: Concerto for Orchestra | II | Allegro scherzando | Quarter note = 94 | The first printed score had 74 in error | wiki-cfo | R |
| Bartók: Divertimento | II | Molto adagio | 14 metronome marks in 74 bars | Bars 50 to 54 have one mark each. Bartók gives timings to the second | wiki-div | R |
| Corigliano: String Quartet | IV (Fugue) | Severe | 60 against 72 beats in a minute | Two voices with the same theme in two tempos | cor-quartet | R |
| Corigliano: Symphony No. 1 | I | Ferocious |  | Character words in English. No tempo number in the program note | cor-sym1 | R |

Data file: [`research/tables/tempo.csv`](../research/tables/tempo.csv)

### S5. Harmony

The column "Set type" gives the prime form of the pitch-class set. The numbers are semitones above the lowest note of the most compact form.

| Composer | Item | Content | Set type | Where | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg | Half-diminished seventh on scale step 2 | E G B-flat D in D minor. The most important chord that is not the tonic in section 1 | 0 2 5 8 | Verklärte Nacht bars 5-6, 11-12, 18-20, 24-27, 34-38 | frisch1993 | R |
| Schoenberg | "Vagrant" chords | Augmented triad, diminished seventh, half-diminished seventh, French sixth, whole-tone chords. Schoenberg's name for chords that can go to many keys |  | Dehmel songs of 1899 and Verklärte Nacht | frisch1993 | R |
| Schoenberg | First note from outside the key | C-sharp in the bass, as part of an augmented triad (C-sharp F A). It is not part of a dominant chord | 0 4 8 | Verklärte Nacht bar 9 | frisch1993 | R |
| Schoenberg | Inverted ninth chord | Ninth chord on A-flat (A-flat C E-flat G-flat B-flat) with the ninth, B-flat, in the bass. A Vienna society refused the work because of this chord | 0 2 4 6 9 | Verklärte Nacht bar 42 | frisch1993; schoenberg1978; wiki-vn | R |
| Schoenberg | Strong bass below vagrant chords | The bass moves by step or by fifth on the notes of the key. The chords above it are vagrant chords. This gives direction to chromatic harmony |  | Jesus bettelt; Verklärte Nacht bars 17-28 | frisch1993 | R |
| Schoenberg | Cadence plan with a weak dominant | Root motion 1 - 2 - 5, stop; 2 - 5, stop; 2 - 5 - 1. Step 2 has more weight than step 5. In bar 28 the dominant is only the bare note A |  | Verklärte Nacht bars 1-29 | frisch1993 | R |
| Schoenberg | Deceptive resolution by semitone | The bass of the dominant goes up one semitone (A to B-flat). The new bass note later becomes a key (B-flat minor) |  | Verklärte Nacht bars 41-50 | frisch1993 | R |
| Schoenberg | Cadence with no dominant | The tonic comes directly from a chord that normally comes before the dominant (French sixth, German sixth, or the dominant of the dominant) |  | Mannesbangen; Jesus bettelt; Erhebung; Verklärte Nacht bars 319-320 | frisch1993 | R |
| Schoenberg | German sixth as a link between keys | The chord A C-sharp E G is the dominant seventh of D. It is also the German sixth of D-flat. It goes directly to D-flat major | 0 2 5 8 | Verklärte Nacht bars 316-320, 322, 324, 332-336 | frisch1993 | R |
| Schoenberg | Plagal cadences after the climax | Soft cadences from the subdominant to the tonic release the tension |  | Verklärte Nacht bars 342-343 and 349-352 | frisch1993 | R |
| Schoenberg | Keys a major third apart | D, F-sharp, B-flat: the octave in three equal parts | 0 4 8 | Verklärte Nacht part 2 | frisch1993 | R |
| Schoenberg | Whole-tone chord | Five of the six notes of a whole-tone scale in one chord, on a strong bass note | 0 2 4 6 8 | Jesus bettelt bar 16 | frisch1993 | R |
| Schoenberg | Chords of fourths | Harmony and a motto theme built from fourths | 0 2 4 5 7 9 (six fourths) | Chamber Symphony No. 1 | wiki-op9 | R |
| Schoenberg | One chord in changing colours | The chord C G-sharp B E A stays. The instruments that play it change | 0 1 3 4 8 | Five Pieces op. 16 no. 3, "Farben" | reference | K |
| Bartók | Cluster as background | E-sharp F-sharp G G-sharp A, arpeggiated, on each slow beat. Five adjacent semitones | 0 1 2 3 4 | The Night's Music | wiki-ood | R |
| Bartók | Cluster with the palm of the hand | E F F-sharp G G-sharp A B-flat C-flat. Eight adjacent semitones | 0 1 2 3 4 5 6 7 | The Night's Music (footnote 4 of the score) | wiki-ood | R |
| Bartók | Two clusters a semitone apart | The chord G A C D and the same chord one semitone higher sound together at the end | 0 2 5 7 | Mikrokosmos no. 107, Melody in the Mist | wiki-nightmusic | R |
| Bartók | Tritone poles | The middle or the contrast section is a tritone from the start. Examples: A and E-flat; C and F-sharp; G and C-sharp; F-sharp and C |  | Music for Strings I and II; The Night's Music; Sonata for Two Pianos I | wiki-axis; wiki-ood; wiki-son2p | R |
| Bartók | Axis system (Lendvai) | Tonic axis: C E-flat F-sharp A. Subdominant axis: F A-flat B D. Dominant axis: G B-flat D-flat E. Notes of one axis can replace each other. Later authors do not all accept this theory | 0 3 6 9 for each axis | Analysis of many works | wiki-axis; lendvai1971 | R |
| Bartók | Polymodal chromaticism | Different modes on the same tonic, together or one after the other. Phrygian and Lydian together give all 12 notes | All 12 | Bartók's Harvard lectures of 1943 | wiki-polymodal | R |
| Bartók | Acoustic scale chord | Major triad with raised fourth and minor seventh: C E G B-flat F-sharp | 0 1 3 4 6 8 10 (full scale) | Concerto for Orchestra finale | wiki-acoustic | R |
| Bartók | Tritone and major seventh chord | Root, tritone, major seventh: F B E | 0 1 6 | The Miraculous Mandarin; The Chase | wiki-ood | R |
| Bartók | Parallel pairs at fixed intervals | Bassoons in minor sixths; oboes in minor thirds; clarinets in minor sevenths; flutes in fifths; muted trumpets in major seconds |  | Concerto for Orchestra II | wiki-cfo | R |
| Bartók | Tristan chord that resolves to a pentatonic set | A chord related to the Tristan chord resolves to a pentatonic mode on C | 0 2 5 8 to 0 2 4 7 9 | Piano Concerto No. 3 II | wiki-pc3 | R |
| Bartók | Interval cells x y z | x: four adjacent semitones. y: four adjacent whole tones. z: two tritones a semitone apart | 0 1 2 3; 0 2 4 6; 0 1 6 7 | String Quartet No. 4 and other works. Names from Perle and Treitler | reference | K |
| Bartók | Major-minor chord | A triad with its major third and its minor third together | 0 3 4 7 | Many works | reference | K |
| Corigliano | Chord that functions as a tonic | E-flat D A E, held by the strings below fast solo passages. The chord comes from the solo melody | 0 1 2 7 | Concerto for Clarinet I | cor-clarinet | R |
| Corigliano | Four pitch centres | C, C-sharp, G, G-sharp come back through the full work | 0 1 5 6 | String Quartet; Symphony No. 2 | cor-quartet | R |
| Corigliano | Semitone motive on one note | The open-string note A in unison, held, then pulled down to G-sharp |  | Symphony No. 1 I and III | cor-sym1 | R |
| Corigliano | Chaconne on 12 pitches | A chord sequence made from 12 pitches goes through the full movement. The chords dissolve into each other | All 12 | Symphony No. 1 III | cor-sym1 | R |
| Corigliano | Chaconne as the form of a long work | A repeated chord pattern below a lyric theme and fast solo studies |  | The Red Violin: Chaconne | cor-chaconne | R |
| Corigliano | Plagal cadences through all keys | Cadences from chord 4 to chord 1 go through all keys below a long rising melody |  | Circus Maximus VII, Prayer | cor-circus | R |
| Corigliano | Blurred cadences | "Amen" cadences (4 to 1) float around a hymn fragment |  | Three Hallucinations II | cor-halluc | R |
| Corigliano | Accidental major chord | Many independent calls hold one note each at the same time. The result is a major chord | 0 4 7 | String Quartet III; Symphony No. 2 III (Nocturne) | cor-quartet | R |
| Corigliano | Chord waves | Four chords in a slow pattern. Each chord grows from one high trumpet note that goes out through the brass |  | Symphony No. 1 IV (Epilogue) | cor-sym1 | R |
| Corigliano | Quarter-tones | Semitone sighs divided into quarter-tones; two tunings that fight to be the tonic | 24 notes in the octave | Chiaroscuro; Pied Piper Fantasy (star music); Altered States | cor-chiaroscuro | R |
| Corigliano | One interval for a full work | The fifth is in all three movements | 0 7 | Conjurer | cor-conjurer | R |

Data file: [`research/tables/harmony.csv`](../research/tables/harmony.csv)

### S6. Scales and modes

The steps are distances from the tonic. The unit is the semitone, or the cent for tunings that are not equal-tempered. One semitone is 100 cents.

| Name | Family | Steps from tonic | Unit | Size | Use | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chromatic segment (x cell) | Bartók | 0 1 2 3 | semitones | 4 | Small chromatic cells. The fugue subject of Music for Strings uses all semitones from A to E | solomon1973 | R |
| Whole-tone scale | Schoenberg and Bartók | 0 2 4 6 8 10 | semitones | 6 | Vagrant chords in Schoenberg. First movement of Bartók's String Quartet No. 4 | frisch1993; wiki-sq4 | R |
| Octatonic scale (semitone first) | Bartók | 0 1 3 4 6 7 9 10 | semitones | 8 | A subset scale of the chromatic scale in the quartets. One octatonic scale = two axes of the axis system | wiki-sq4 | R |
| Octatonic scale (whole tone first) | Bartók | 0 2 3 5 6 8 9 11 | semitones | 8 | Same scale from its second note | wiki-sq4 | R |
| Acoustic scale (Lydian with minor seventh) | Bartók | 0 2 4 6 7 9 10 | semitones | 7 | From the overtone series. Finale of the Concerto for Orchestra. Mode 4 of the melodic minor scale | wiki-acoustic | R |
| Dorian mode | Folk and Bartók | 0 2 3 5 7 9 10 | semitones | 7 | The flute melody of The Night's Music (on C-sharp) | wiki-ood | R |
| Phrygian mode | Folk and Bartók | 0 1 3 5 7 8 10 | semitones | 7 | Half of the Phrygian-Lydian polymode. Also the cadence mode of Andalusian music | wiki-polymodal | R |
| Lydian mode | Folk and Bartók | 0 2 4 6 7 9 11 | semitones | 7 | Half of the Phrygian-Lydian polymode | wiki-polymodal | R |
| Phrygian-Lydian polymode | Bartók | 0 1 2 3 4 5 6 7 8 9 10 11 | semitones | 12 | Two modes on one tonic. All 12 notes, but with a tonic | wiki-polymodal | R |
| Model 1:3 | Bartók | 0 3 4 7 8 11 | semitones | 6 | Minor third and semitone in alternation. It has the major and minor third and the major and minor sixth | wiki-polymodal | R |
| Pentatonic scale without semitones (minor form) | Hungarian old style | 0 3 5 7 10 | semitones | 5 | Old-style Hungarian peasant song. Melody in the Mist: G A C D F | wiki-nightmusic | R |
| Pentatonic scale without semitones (major form) | General | 0 2 4 7 9 | semitones | 5 | End of the slow movement of Bartók's Piano Concerto No. 3 | wiki-pc3 | R |
| Fourths stack | Schoenberg | 0 5 10 3 8 1 | semitones | 6 | Motto theme and chords of the Chamber Symphony No. 1 | wiki-op9 | R |
| Minor scale with raised 4 and 7 (Hungarian minor) | Central Europe | 0 2 3 6 7 8 11 | semitones | 7 | Verbunkos style. Two augmented seconds | reference | K |
| Phrygian with major third (Hijaz type) | Balkan, Arab, Jewish, Andalusian | 0 1 4 5 7 8 10 | semitones | 7 | One augmented second between steps 2 and 3 | reference | K |
| Maqam Rast | Arab | 0 200 350 500 700 900 1050 | cents | 7 | Neutral third and neutral seventh (between major and minor). Values are the 24-tone approximation | reference | K |
| Maqam Bayati | Arab | 0 150 300 500 700 800 1000 | cents | 7 | Neutral second. A common maqam for song and for the call to prayer | reference | K |
| Maqam Saba | Arab | 0 150 300 400 700 800 1000 1100 | cents | 8 | Neutral second and lowered fourth. The top note is lower than the octave. Mood: grief. In the Turkish tradition, the maqam of the dawn call to prayer | reference | K |
| Maqam Hijaz | Arab | 0 100 400 500 700 800 1000 | cents | 7 | Augmented second in the lower part. Real tuning makes the step smaller than 300 cents | reference | K |
| Raga Yaman | Hindustani | 0 2 4 6 7 9 11 | semitones | 7 | First quarter of the night. Same notes as the Lydian mode. Main note: step 3. Second main note: step 7. Steps 1 and 5 are weak in the ascent. Typical phrase (steps): low 7, 2, 3, 2, 1; 5, raised 4, 3, 2, 1 | wiki-yaman | R |
| Raga Bageshri | Hindustani | 0 2 3 5 7 9 10 | semitones | 7 | Middle of the night. Main note: step 4. Second main note: step 1. The ascent has no step 2 and no step 5 (five notes up, seven notes down) | wiki-bageshri | R |
| Raga Malkauns | Hindustani | 0 3 5 8 10 | semitones | 5 | Late night, 24:00 to 03:00. No step 2 and no step 5. Main note: step 4. Second main note: step 1. Serious and meditative; low octave; slow tempo. Slides and a slow oscillation on the minor third and the minor sixth. Typical phrase (steps): 3, 4, 6, 4, 3, 4, 3, 1 | wiki-malkauns | R |
| Raga Darbari Kanada | Hindustani | 0 2 3 5 7 8 10 | semitones | 7 | Midnight, deep in the night. A grave raga, mostly in the low octave. Main note: step 2. Second main note: step 5. Slow slides, and a slow oscillation on the minor third. The line stays for some time on the low minor sixth | wiki-darbari | R |
| Slendro | Javanese gamelan | 0 240 480 720 960 | cents | 5 | Five pitches at almost equal distances in the octave. Each gamelan has its own tuning. The values are the equal-step model | wiki-slendro | R |
| Pelog | Javanese gamelan | 0 133 267 533 667 800 933 | cents | 7 | Seven unequal steps; the music uses five of them at a time. Each gamelan has its own tuning. The values are 7 of the 9 steps of an equal scale of 9 notes (measurement of 27 gamelans by Surjodiningrat, 1972) | wiki-pelog | R |
| In scale (miyako-bushi) | Japanese | 0 1 5 7 8 | semitones | 5 | Koto and shamisen music. Semitones above steps 1 and 5 | reference | K |
| Yo scale | Japanese | 0 2 5 7 9 | semitones | 5 | Folk song and shakuhachi music. No semitones | reference | K |

Data file: [`research/tables/scales.csv`](../research/tables/scales.csv)

### S7. Themes and motives

The table gives the shapes of themes and the methods that change them.

| Composer | Item | Shape | Parameters | Where | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg | Walking theme (theme 1a) | Step by step down from scale step 6 to step 1, above a held tonic note | Notes B-flat A G F E D. Upbeat. Dotted rhythm on beats 2 and 4. Low register | Verklärte Nacht bars 1-4 | frisch1993 | R |
| Schoenberg | Semitone and tritone | A semitone down, then a leap of a tritone | Intervals -1, then 6. It is the start of themes 2b, 4a, and 5a | Verklärte Nacht bars 34; 75; 105 | frisch1993; schoenberg1932 | R |
| Schoenberg | Paired semitones | Two semitone steps a fourth apart | Example: the semitone above step 5 and the semitone below step 1 | Verklärte Nacht themes 2a; 2b; 3a | frisch1993; schoenberg1932 | R |
| Schoenberg | Short theme unit | A unit of 1 bar, said two times at the same pitch, then a longer continuation | Proportion 1 : 1 : 2. The second statement is not on the dominant | Verklärte Nacht themes 2a; 3a; 5a | frisch1993 | R |
| Schoenberg | Register that rises | The first theme of a group starts low. The range goes up as the section continues | Themes 1a; 2a; 3a start in the low register | Verklärte Nacht part 1 | frisch1993 | R |
| Schoenberg | Developing variation | Each new theme is a changed form of an earlier theme: same contour, new intervals or new rhythm | Rhythm of the upbeat: present (1a); empty (2a; 4a); present again (5a) | Verklärte Nacht | frisch1993 | R |
| Schoenberg | Theme transformation | The same theme with a new character | Same contour; intervals adjusted; arpeggio inverted | Warnung bars 1 and 17 | frisch1993 | R |
| Schoenberg | Linkage | The last motive of a phrase starts the next phrase | The new phrase starts before the cadence is complete | Im Reich der Liebe bars 6-7 | frisch1993 | R |
| Schoenberg | Themes that sound together | Three earlier themes at the same time in the tonic major | Themes 1a, 7a, and 10 | Verklärte Nacht bar 370 | frisch1993 | R |
| Schoenberg | Diatonic theme with a chromatic inner voice | A melody that goes up by diatonic steps, with an inner voice that goes down by semitones | Contrary motion | Verklärte Nacht themes 6 and 7a (bars 230; 255) | frisch1993 | R |
| Bartók | Fugue subject in a narrow range | Four phrases. Each phrase fills a block of adjacent semitones. The line goes up to the centre and back | Range A to E-flat in the first statement; all semitones from A to E in the subject | Music for Strings I | solomon1973 | R |
| Bartók | Interval expansion | The same theme later with larger intervals: chromatic steps become diatonic steps | Example: I bars 1-5 and IV bars 204-209 | Music for Strings I and IV | wiki-mspc | R |
| Bartók | Inversion as a goal | After the climax, the subject is always inverted. At the end, the subject and its inversion sound together | Both lines start on A and end on A | Music for Strings I bars 56-88 | solomon1973; roberts2021 | R |
| Bartók | Nature call | Short motive at an irregular time in the bar | Six different imitations: birds, cicadas, frog. Bartók: the player can put them at any point and play as many as he likes | The Night's Music | wiki-ood | R |
| Bartók | Repeated note that becomes a melody | Repeated notes that start as noise and change into the shepherd's melody | The note G-sharp, from bar 37 | The Night's Music | wiki-nightmusic; schneider2006 | R |
| Bartók | Call with built-in acceleration | A A A C A A: five notes in the time of four, then one more | Latent rhythm 3 + 2 + 1. It sounds like an acceleration that stops suddenly | Sonata for Two Pianos II | wiki-nightmusic | R |
| Bartók | Lonely melody | One line, no accompaniment, sometimes doubled one or two octaves apart | Pentatonic (G A C D F), old Hungarian style | Mikrokosmos no. 107 | wiki-nightmusic | R |
| Bartók | Peasant flute melody | A melody "shown" as a sound of the place, not as the voice of the composer | Strict Dorian mode on C-sharp | The Night's Music bars 37-58 | wiki-ood; wiki-nightmusic | R |
| Bartók | Real bird calls | The calls of real birds that the composer wrote down | Tufted titmouse and wood thrush, heard in North Carolina in 1945 | Piano Concerto No. 3 II | wiki-nightmusic | R |
| Bartók | Fourths theme | A theme of rising fourths in the low strings | Cellos and basses; answered by string tremolo and flutes | Concerto for Orchestra I (introduction) | wiki-nightmusic | R |
| Bartók | Folk motive | A short part of a real folk song as the main motive | Three notes: E F-sharp G | With Drums and Pipes | wiki-ood | R |
| Corigliano | Motto of the string quartet | One note repeated in even values, and a chain of minor thirds that are not adjacent | The thirds go up in the Prelude and down in the Fugue | String Quartet; Symphony No. 2 | cor-quartet | R |
| Corigliano | Decorated single note | One repeated note with ornaments | The note C, played by oboes "in a highly primitive manner" | Three Hallucinations I and III | cor-halluc | R |
| Corigliano | Quotation as memory | A known piece of music that comes from far away | Offstage piano: the Albéniz-Godowsky Tango. Hymn: Rock of Ages. Bach chorale | Symphony No. 1; Three Hallucinations; Chiaroscuro | cor-sym1; cor-halluc; cor-chiaroscuro | R |
| Corigliano | Words changed into melody | Short sentences about friends, set as melodies for solo instruments. Then the words are removed | Melodies above the chaconne chords | Symphony No. 1 III | cor-sym1 | R |
| Corigliano | All material from the first solo | The full movement comes from the first solo passage | Also the chord that functions as the tonic | Concerto for Clarinet I | cor-clarinet | R |
| Corigliano | Calls that answer | Many solo players echo the calls of the others | Calls made from repeated notes and minor thirds | Symphony No. 2 III | cor-sym2 | R |

Data file: [`research/tables/motifs.csv`](../research/tables/motifs.csv)

### S8. Rhythm and metre

The table gives metres, rhythm patterns, and methods for layers in different tempos.

| Composer | Item | Content | Parameters | Where | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg | Phrases across the bar line | Phrases do not agree with the metre. Each phrase lies differently against the bar line | In the first bars of Erwartung, each of three phrases starts at a different point of the bar | Verklärte Nacht; Erwartung op. 2 no. 1 | frisch1993; wiki-vn | R |
| Schoenberg | Metre that expands and contracts | The written 4/4 sounds as 3/2 (phrases of six quarter notes). Then it goes back to 4/4 through one bar of 2/4 | Bars 331-336 | Verklärte Nacht | frisch1993 | R |
| Schoenberg | Walking rhythm | Dotted eighth and sixteenth on beats 2 and 4 | Present in the full theme 1 family | Verklärte Nacht bars 1-28 | frisch1993 | R |
| Schoenberg | Tempo in constant change | Many marks to go faster or slower in a short time | Marks: steigernd, beschleunigend, drängend, zurückhaltend, breiter. See the measured table of tempo marks | Verklärte Nacht | billam2013 | R |
| Bartók | Bulgarian (aksak) metres | Fast metres made of groups of 2 and 3 | 2+3; 3+2; 2+2+3; 2+3+2; 3+2+2; 2+2+2+3 | Turkish and Balkan folk music | wiki-aksak | R |
| Bartók | Bulgarian metres in a scherzo | Scherzo: 4+2+3 eighths. Trio: 3+2+2+3 eighths | 9/8 and 10/8 | String Quartet No. 5 III | wiki-sq5 | R |
| Bartók | Six Dances in Bulgarian Rhythm | 4+2+3; 2+2+3; 2+3; 3+2+3; 2+2+2+3; 3+3+2 (eighths) | Mikrokosmos nos. 148 to 153 | Mikrokosmos | reference | K |
| Bartók | Fibonacci rhythm | One note repeated: 1, 1, 2, 3, 5, 8, 5, 3, 2, 1, 1 notes for each beat | A written acceleration and deceleration. Xylophone. Adagio, eighth = 66 | Music for Strings III | wiki-mspc; roberts2021 | R |
| Bartók | Change of metre at each bar | The fugue has a time signature that changes constantly |  | Music for Strings I | wiki-mspc | R |
| Bartók | Slow pulse with free events | A soft dissonant sound on each beat of a slow tempo. Short motives at irregular times above it | The pulse becomes background | Night music style | wiki-nightmusic | R |
| Bartók | Two tempos together | Chorale and flute melody together, with different characters, tempos, and key centres | Bars 61-66 | The Night's Music | wiki-ood; schneider2006 | R |
| Bartók | Fast section in a slow movement | A presto in the centre of the slow movement | Adagio - Presto - Adagio | Piano Concerto No. 2 II | wiki-pc2 | R |
| Bartók | Clash of 2 against 3 | Chords in groups of two against a 6/8 metre | Returns between the episodes | The Chase | wiki-ood | R |
| Bartók | Parlando rubato and tempo giusto | Two types of folk rhythm: free speech rhythm, and strict dance rhythm | Slow lonely melodies use the first type | Bartók's folk music classes | reference | K |
| Corigliano | Layered accelerations | A slow steady drum beat starts a series of accelerations that overlap | Final stage: a slow steady melody against a drum that accelerates | Symphony No. 1 I | cor-sym1 | R |
| Corigliano | Machine that stops | The full orchestra repeats one dissonant chord. The pattern slows down and stops, but stays loud | No decrease of loudness during the slow-down | Symphony No. 1 I | cor-sym1 | R |
| Corigliano | Voices in different tempos | Each voice has even notes with no rhythm profile. Each voice has its own tempo. The parts are written in one common metre | Example: 60 against 72 beats in a minute (ratio 5 : 6) | String Quartet IV (Fugue) | cor-quartet | R |
| Corigliano | Out of phase | One player's quarter note = the other player's dotted eighth note | Tempo ratio 4 : 3 | Chiaroscuro III | cor-chiaroscuro | R |
| Corigliano | Space-time notation | No beats to count. The players align at given points and are free between them | Three of five movements of the quartet. Rewritten for 50 strings in the symphony | String Quartet; Symphony No. 2 | cor-sym2 | R |
| Corigliano | Small delay between players | Each player is a very small time out of step with the others | Result: threads of sound with no clear focus | String Quartet I (Prelude) | cor-quartet | R |
| Corigliano | Two groups in two tempos | A march group and the orchestra play in very different tempos | The march group goes out through the hall | Pied Piper Fantasy | cor-piper | R |
| Corigliano | Acceleration to madness | A dance that goes faster and faster | Tarantella in 6/8; the end is a scream | Symphony No. 1 II | cor-sym1 | R |

Data file: [`research/tables/rhythm.csv`](../research/tables/rhythm.csv)

### S9. Texture and orchestration

The table gives the orchestration devices of the three composers.

| Composer | Device | Content | Parameters | Where | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Bartók | Night music: layer 1 | A soft dissonant sound that repeats on each slow beat | Cluster of adjacent semitones; arpeggiated; the listener hears it as background | The Night's Music | wiki-nightmusic; wiki-ood | R |
| Bartók | Night music: layer 2 | Short imitations of animal sounds at irregular times | Repeated notes, trills, grace notes; high register; they ignore the metre and the key | The Night's Music (frog from bar 6 to bar 70) | wiki-nightmusic; wiki-ood | R |
| Bartók | Night music: layer 3 | A lonely melody that seems to come from the place | One line; no chords; sometimes doubled at one or two octaves | The Night's Music; Melody in the Mist | wiki-nightmusic | R |
| Bartók | Night music: space | Very wide distances: glissandi, leaps, and doublings across many octaves, against clusters of adjacent notes | The contrast gives the effect of space and of a person alone | Night music style | wiki-nightmusic; schneider2006 | R |
| Bartók | Night music: layers that do not agree | Different materials overlap. One material can cut into a different material | Each layer keeps its own tempo, key centre, and character | The Night's Music bars 61-66 | wiki-nightmusic; wiki-ood | R |
| Bartók | Night music: mood | Hushed, still, full of expectation. In the last works: calm, bright | Bartók got the idea on summer nights on the Great Hungarian Plain (from 1921) | Night music style | wiki-nightmusic | R |
| Bartók | Night music for orchestra | Low strings with a theme of fourths; string tremolo; flutes that flutter; soft trumpets with a short chorale |  | Concerto for Orchestra I (introduction) | wiki-nightmusic | R |
| Bartók | Percussion colour | Timpani glissandi; xylophone solo; celesta arpeggios; harp; piano | The timpani glissando was unusual in 1936 | Music for Strings III | wiki-mspc | R |
| Bartók | Exact percussion directions | The score tells which part of the cymbal to hit and with which stick. It gives the stage plan for the players | Snare drum with snares on and off; cymbal played with the fingernail; thin sticks on the edge of the drum | Sonata for Two Pianos and Percussion | wiki-son2p; lendvai-web | R |
| Bartók | Two groups in space | Two string orchestras on opposite sides of the stage | Antiphonal effects in the fast movements | Music for Strings II and IV | wiki-mspc | R |
| Bartók | String techniques | Mutes for a full movement; pizzicato for a full movement; snap (Bartók) pizzicato; glissandi; held notes with no vibrato | Movement II all muted; movement IV all pizzicato; movement III with the non-vibrato notes | String Quartet No. 4 | wiki-sq4 | R |
| Bartók | Fugue that grows | Muted strings. Each new voice adds sound. The texture and the loudness grow together to the climax | pp to fff in 55 bars; then fast decrease as instruments stop | Music for Strings I | wiki-mspc; solomon1973 | R |
| Bartók | Solo group against the full group | A small group of soloists against the full string orchestra | As in the Baroque concerto grosso | Divertimento | wiki-div | R |
| Bartók | Piano as percussion | The piano gets its real character when it is used as a percussion instrument | Bartók's statement of 1927 | Works of 1926 | wiki-ood | R |
| Schoenberg | Mutes for a new region | The mutes go on at the start of a new theme group and key | Bar 50 ("mit Dämpfer"), B-flat minor | Verklärte Nacht | billam2013; frisch1993 | R |
| Schoenberg | Low start | Each of the first three theme groups starts in the low register and goes up | Bars 1, 29, and 50 | Verklärte Nacht | frisch1993 | R |
| Schoenberg | Collapse to one note | The texture falls to octaves and then to one low unison note. The development starts here | Octave D at bar 132; then the low E | Verklärte Nacht | frisch1993 | R |
| Schoenberg | Web of motives | A web of theme and motive relations covers the simple five-part plan. The web becomes tighter as the work continues | Statement by Carl Dahlhaus | Verklärte Nacht | frisch1993 | R |
| Schoenberg | Voice in the web | The solo line is doubled or followed closely by one line of the accompaniment |  | Erhebung op. 2 no. 3; Jesus bettelt | frisch1993 | R |
| Schoenberg | Colour chord | A chord of five notes made from the tonic and four neighbour notes. It comes back in changed forms as a "colour" |  | Erwartung op. 2 no. 1 | frisch1993 | R |
| Schoenberg | Tone colour as melody | The same chord goes from one group of instruments to the next |  | Five Pieces op. 16 no. 3, "Farben" | reference | K |
| Corigliano | Brass around the orchestra | 5 trumpets behind the orchestra, first trumpet in the centre. 6 horns (3 on each side), 4 trombones (2 on each side), 1 tuba at each end | A chord starts as one high trumpet note and goes out to the two sides: a "wave" | Symphony No. 1 | cor-sym1 | R |
| Corigliano | Offstage instrument as memory | A piano far away plays a known piece through the orchestra sound | The orchestra holds a quiet high violin note | Symphony No. 1 I and IV | cor-sym1 | R |
| Corigliano | Change of string tone on one note | Open-string A ("nasal"); then the same note on stopped strings in more and more instruments | The sound becomes harder and more intense | Symphony No. 1 I | cor-sym1 | R |
| Corigliano | Violins at the top of their range | The peak of the accelerations is a violin line in the highest register | It then becomes quiet and starts the memory section | Symphony No. 1 I | cor-sym1 | R |
| Corigliano | Low strings alone | Violas, cellos, and basses only, for the first minutes of the movement | The chaconne chords dissolve into each other | Symphony No. 1 III | cor-sym1 | R |
| Corigliano | Two types of mute | A practice mute (the sound is a whisper) for the outer parts. A normal mute for the centre |  | String Quartet I; Symphony No. 2 I | cor-quartet | R |
| Corigliano | Divided string sections | Sections divided to make thicker chords. Fast passages divided between players. Many solo players for calls | 50 players in place of 4 | Symphony No. 2 | cor-sym2 | R |
| Corigliano | Strength from effort | Strings have a small loudness range. A string fortissimo comes from intensity, not from volume | His reason to keep the symphony for strings only | Symphony No. 2 | cor-sym2 | R |
| Corigliano | Players around the audience | Trumpets and percussion around the hall; a saxophone quartet and a double bass in the boxes; a band that marches down the aisles | The audience is in the centre of the sound | Circus Maximus | cor-circus | R |
| Corigliano | Night music of nature | Calm. Sounds of the forest stop time. Animals call to each other | Section IV | Circus Maximus | cor-circus | R |
| Corigliano | Night music of the city | A pulse with hidden energy and sudden flashes. Sirens. Distant battles | Section V | Circus Maximus | cor-circus | R |
| Corigliano | Solo as a light that comes and goes | The soloist plays as fast as possible and very softly. Parts of the line stay in the orchestra as held notes | Subtitle: "Ignis fatuus" (will-o'-the-wisp) | Concerto for Clarinet I | cor-clarinet | R |
| Corigliano | Glissando contest | Solo clarinet and trombones in canons of glissandi with sharp edges |  | Concerto for Clarinet I | cor-clarinet | R |
| Corigliano | Orchestra glissando | All the materials together end in one very large glissando of the full orchestra |  | Three Hallucinations I | cor-halluc | R |
| Corigliano | Wood of the bow | String chords made brittle by hard attacks with the wood of the bow | Used for the chaconne chords before the last climax | The Red Violin: Chaconne | cor-chaconne | R |
| Corigliano | Very high slow melody | A solo line in the highest register, very slow, above string sounds that change slowly | After the fast climax | The Red Violin: Chaconne | cor-chaconne | R |
| Corigliano | Percussion families | Wood: xylophone, marimba, and a row of wood instruments with no pitch. Metal: chimes, tam-tams, cymbals, bowed vibraphone. Skin: talking drum, kick drum, timpani played with the hands | One family for each movement | Conjurer | cor-conjurer | R |
| Corigliano | Amplified and looped sound | The singer goes to a microphone when the orchestra becomes too loud. At the peak, the electronics repeat a phrase again and again | Loudspeakers around the hall | Vocalise | cor-vocalise | R |
| Corigliano | Folk and toy instruments | Tin whistle for the soloist; flutes and drums played by children | The children go out through the hall with the soloist | Pied Piper Fantasy | cor-piper | R |
| Corigliano | Light as part of the score | Stage lights go down; a spotlight follows the players; a start in the dark | Added in performances after the premiere | Pied Piper Fantasy | cor-piper | R |

Data file: [`research/tables/texture.csv`](../research/tables/texture.csv)

### S10. Bartók's night music: list of works

The list is from the Wikipedia article "Night music (Bartók)" (source key `wiki-nightmusic`). The article uses the list of Danchenka (1987).

| Year | Work | Part | Marking |
| --- | --- | --- | --- |
| 1905 | Second Suite for small orchestra op. 4 | III | Andante |
| 1908 | Fourteen Bagatelles op. 6 | No. 12 |  |
| 1911 | Duke Bluebeard's Castle | Parts of sections and moods |  |
| 1916 | Five Songs op. 15 | No. 5, "Here down in the valley" |  |
| 1918 to 1924 | The Miraculous Mandarin | The body of the mandarin shines in the dark |  |
| 1920 | Eight Improvisations on Hungarian Peasant Songs op. 20 | No. 3 |  |
| 1923 | Dance Suite | IV |  |
| 1924 | Village Scenes | Lullaby |  |
| 1926 | Out of Doors | IV, "The Night's Music" | Lento - (Un poco) più andante |
| 1926 | Piano Concerto No. 1 | II | Andante |
| 1927 | String Quartet No. 3 | I | Moderato |
| 1928 | String Quartet No. 4 | III | Non troppo lento |
| 1931 | Piano Concerto No. 2 | II | Adagio - Più adagio - Presto - Tempo I |
| 1934 | String Quartet No. 5 | II and IV | Adagio molto; Andante |
| 1936 | Music for Strings, Percussion and Celesta | III | Adagio |
| 1937 | Sonata for Two Pianos and Percussion | II | Lento, ma non troppo |
| 1940 (published) | Mikrokosmos | No. 107, "Melody in the Mist"; No. 144, "Minor Seconds, Major Sevenths" | Tranquillo; Lento |
| 1943 | Concerto for Orchestra | I (introduction) and III, "Elegia" | Andante non troppo |
| 1945 | Piano Concerto No. 3 | II (centre section) | Adagio religioso |
| 1945 | Viola Concerto (sketches) | II | Adagio religioso |

Data file: [`research/tables/night_list.csv`](../research/tables/night_list.csv)

### S12. Variation: how an idea comes again

The table gives the methods of the reference composers for the return of an idea. No row permits a return with no change.

| Composer | Method | Content | Parameters | Where | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Schoenberg | Developing variation | New material comes from changes of the material before it. Schoenberg: "variation of the features of a basic unit produces all the thematic formulations" | The changes are in the pitch (vertical) and in the rhythm and the order (horizontal) | Essay "Bach" (1950) in Style and Idea, page 397. Schoenberg gave the method its name | wiki-devvar | R |
| Schoenberg | All themes from the first phrase | "All main themes had to be transformations of the first phrase". The repetition of the relations between the notes holds the work together | One common factor produces forms that are more and more remote | Die Jakobsleiter. Essay "Composition with Twelve Tones" (about 1948), page 248 | wiki-devvar | R |
| Schoenberg | Variation keeps some features | "The use of the motive requires variation". But a change of all features "produces something foreign, incoherent, illogical" | Change one or two of these: rhythm, intervals, contour, harmony. Keep the others | Fundamentals of Musical Composition, the chapter on the motive (read in a course summary) | fmc-summary | R |
| Schoenberg | Ways to change a motive | Rhythm: different note lengths, repeated notes, a move to different beats, an added upbeat, a different metre. Intervals: a different direction or order, added or removed notes, a leap filled with steps, a larger or smaller leap. Harmony: an inversion, a different chord, added chords. Melody: a transposition, added passing harmony | A list for the composer: each repetition uses one or more items | Fundamentals of Musical Composition, the chapter on the motive | reference | K |
| Schoenberg | Liquidation | The characteristic features of a motive go away step by step. Only notes with no character stay. Thus a section can end with no hard stop | Each repetition is shorter or has fewer characteristic intervals | Fundamentals of Musical Composition | reference | K |
| Schoenberg | Brahms as the model | Schoenberg found developing variation in its "most advanced state" in the music of Brahms |  | Frisch (1982), page 216 | wiki-devvar | R |
| Bartók | No idea two times in the same way | "I never present the same musical thought twice in the same way". "I never repeat one part identically - which shows my great love for variation and the transformation of themes" | A rule for each return of a theme and of a section | Interview with Denijs Dille, Brussels, 2 February 1937 | dille1937 | R |
| Bartók | Return in retrograde | At the end of the Second Piano Concerto, "the first subject comes back in retrograde" | The notes of the theme in the opposite order | Piano Concerto No. 2. Interview with Denijs Dille (1937) | dille1937 | R |
| Bartók | Return in inversion | The fugue ends with the second phrase of its subject, played softly above its inversion. The subject comes back "in different guises" in the later movements | The theme and its mirror form at the same time | Music for Strings, Percussion and Celesta I to IV | wiki-mspc | R |
| Bartók | The same game with a new interval and a new colour | Five pairs of instruments play in turn. Each pair has its own interval: bassoons a minor sixth, oboes minor thirds, clarinets minor sevenths, flutes fifths, muted trumpets major seconds | 5 statements; 5 intervals; 5 colours. A short brass chorale comes before the return | Concerto for Orchestra II ("Game of Pairs") | wiki-cfo | R |
| Corigliano | Returning material gets longer | The fast brass motives of the first section come back in the slow section for longer and longer times, until they take over | Each return is longer than the return before it | Symphony No. 1 I | wiki-corsym1 | R |
| Corigliano | A theme comes back with a different sound | At the end, the soloist plays the opening material again "with a purer and richer sound" than at the start | Same notes; a different tone quality | Pied Piper Fantasy VII | cor-piper | R |
| Corigliano | A pattern becomes more ornate | The repeated patterns become more and more ornate. The player decides how long a pattern repeats | Second part of the work | Fantasia on an Ostinato (1985) | cor-fantasia | R |
| Corigliano | The chords come back with a different attack | The chords of the chaconne come back in the strings, "rendered brittle by sharp attacks with the wood of the bow" | Same harmony; a different playing technique | The Red Violin: Chaconne | cor-chaconne | R |
| Corigliano | A theme comes back very high and very slow | The theme returns as "a stratospherically high, gravely slow melody" "against slowly shifting string sonorities". The first line of the work comes back "in determined accents this time" | Same notes; a different register, tempo, and articulation | The Red Violin: Chaconne | cor-chaconne | R |
| Present-day view | Repetition needs surprise | "Usually composers repeat elements with some variation". The important question is which part of an idea repeats and when. Variation changes the texture more frequently than the melody | Literal repetition gives the listener a fixed point, but no surprise. Music with no repetition that the ear can find makes the listener tired | Essay by the composer Joseph Sowa | sowa-repetition | R |

Data file: [`research/tables/variation.csv`](../research/tables/variation.csv)

### S13. Instrument techniques

The table lists ways to play that give an instrument more colours. Table S9 gives the orchestration devices of the three composers.

| Family | Technique | Content | Example | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| Strings | Sul ponticello | The bow is near the bridge. The sound is glassy and has much noise |  | rush-techniques | R |
| Strings | Sul tasto | The bow is above the fingerboard. The sound is softer |  | rush-techniques | R |
| Strings | Col legno | The wood of the bow hits the string (battuto) or moves across it (tratto) | Berlioz, Symphonie fantastique. Gubaidulina, Perception (1983) | rush-techniques; wiki-exttech | R |
| Strings | Snap pizzicato | The string hits the fingerboard. Also called Bartók pizzicato | Bartók | wiki-exttech | R |
| Strings | Pizzicato chords, strummed | The player strums a chord across the strings | Bartók, Music for Strings, Percussion and Celesta IV | wiki-mspc | R |
| Strings | Harmonics | Natural harmonics (a light touch on an open string) and artificial harmonics (one firm finger and one light finger) |  | rush-techniques | R |
| Strings | Harmonic glissando | A slide of the light finger gives a chain of harmonics ("seagull" effect) |  | wiki-exttech | R |
| Strings | Behind the bridge | The bow is between the bridge and the tailpiece. The pitch is high and not exact |  | wiki-exttech; rush-techniques | R |
| Strings | Different string, same note | The same note on an open string and then on stopped strings, in more and more players. The sound becomes harder | Corigliano, Symphony No. 1 I | wiki-corsym1; cor-sym1 | R |
| Strings | Two groups, left and right | Two string orchestras on the two sides of the stage answer each other | Bartók, Music for Strings, Percussion and Celesta II and IV | wiki-mspc | R |
| Woodwinds | Flutter-tongue | The player rolls the tongue. The sound goes from a soft cooing to a growl. It needs more air than a normal note. Notation: tremolo strokes and a word (flz., frull.) | Tchaikovsky, The Nutcracker (flutes). Corigliano, Pied Piper Fantasy (a high, shrill flutter-tongued note of the soloist) | wiki-flutter; cor-piper | R |
| Woodwinds | Key slaps | The player hits the keys with no air. A soft percussion sound at the pitch of the fingering |  | rush-techniques | R |
| Woodwinds | Multiphonics | Two or more notes at the same time, from special fingerings |  | wiki-exttech | R |
| Woodwinds | Breath sounds | Air through the instrument with no tone, or with a small part of the tone |  | wiki-exttech | R |
| Woodwinds | Pitch bend | The player moves the pitch with the lips or the fingers |  | wiki-exttech | R |
| Woodwinds | Reed alone | The player blows the reed in a special way to get a raw sound | Corigliano, Oboe Concerto (1975): the sound of the North African rhaita | rush-techniques | R |
| Woodwinds | A second instrument of the same player | The soloist changes to a tin whistle for the march | Corigliano, Pied Piper Fantasy | cor-piper | R |
| Brass | Flutter-tongue | As on woodwinds. On horns it can sound like animals | Strauss, Don Quixote, variation 2 (horns: the sheep) | wiki-flutter | R |
| Brass | Mutes and objects in the bell | Each mute type gives a different colour | Bartók, Concerto for Orchestra II (muted trumpets in major seconds) | wiki-exttech; wiki-cfo | R |
| Brass | Glissando | Trombones slide between notes | Bartók, Concerto for Orchestra IV (trombones and woodwinds interrupt the theme). Corigliano, Clarinet Concerto I ("glissandi of jagged canons") | wiki-cfo; cor-clarinet | R |
| Brass | Half valve, pitch bend, double buzz | Sounds between the notes and sounds with noise |  | wiki-exttech | R |
| Brass | Players in the hall | Five horns behind the stage, two trumpets at the rear of the hall, two clarinets high at the sides. The music for them "specifically shouldn't be synchronized" | Corigliano, Clarinet Concerto III | cor-clarinet | R |
| Percussion | Bowed metal | A bow on the edge of a vibraphone bar, a cymbal, or a gong. A long note with no attack | Thorvaldsdottir, Aura (2015) | rush-techniques; wiki-exttech | R |
| Percussion | Timpani glissando | The player moves the pedal while the drum sounds | Bartók, Music for Strings, Percussion and Celesta III. Concerto for Orchestra IV: 10 pitches in about 20 seconds | wiki-mspc; wiki-cfo | R |
| Percussion | Cymbal on a timpani head | The cymbal sounds through the drum. The pedal changes the colour |  | wiki-exttech | R |
| Percussion | Water gong | The player lowers a gong into water after the stroke. The pitch slides |  | rush-techniques; wiki-exttech | R |
| Percussion | Side drum as a frame | A side drum alone starts and ends the movement | Bartók, Concerto for Orchestra II | wiki-cfo | R |
| Piano | Inside the piano | The player plucks the strings, hits them with a mallet, or slides a finger along a string | Cowell, The Banshee (1925) | rush-techniques | R |
| Piano | Silent keys | The player holds keys down with no sound. The open strings ring when other notes sound |  | rush-techniques; wiki-exttech | R |
| Piano | Clusters | The palm or the arm plays all keys of an area | Cowell | wiki-exttech | R |
| Piano | Piano as percussion | The piano is a member of the percussion group. The celesta player also plays the piano with four hands | Bartók, Music for Strings, Percussion and Celesta | wiki-mspc | R |
| Harp | Harmonics | A light touch at the middle of the string. The note is one octave higher and has a bell sound |  | reference | K |
| Harp | Near the soundboard | The player plucks the string at its low end. The sound is dry, as a guitar |  | reference | K |
| Harp | Bisbigliando | A soft tremolo of the two hands on some notes: a whisper |  | reference | K |
| Harp | Pedal slide and glissando | A change of the pedal while the string sounds moves the pitch by a semitone. A glissando across the strings gives the scale of the pedal setting |  | reference | K |

Data file: [`research/tables/techniques.csv`](../research/tables/techniques.csv)

### S14. Notes that are not in the chord

The table gives the types of notes outside the chord, and the chords that keep such notes.

| Type | Movement | Effect or use | Example | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| Passing tone | Step from a chord tone, then a step in the same direction to a chord tone. Accented or not accented | Connects two chord tones. Two in sequence are double passing tones |  | wiki-nct | R |
| Neighbour tone | Step away from a chord tone, then a step back to the same tone | Decorates one note. An upper form and a lower form |  | wiki-nct | R |
| Escape tone | Step from a chord tone, then a leap in the opposite direction | An incomplete neighbour tone. Not accented |  | wiki-nct | R |
| Anticipation | A note of the subsequent chord comes early | Not accented. It makes the arrival softer |  | wiki-nct | R |
| Suspension | A note stays from the chord before, then goes down one step | Accented. The dissonance is on the strong beat. A suspension that goes up is a retardation |  | wiki-nct | R |
| Appoggiatura | Leap to a note outside the chord, then a step to a chord tone | Accented. The strongest type for expression: the dissonance has the accent and the chord tone comes late |  | wiki-nct | R |
| Changing tones | Step to a note outside the chord, leap to a second such note, step to a chord tone | Two notes around the chord tone |  | wiki-nct | R |
| Pedal point | One note stays while the chords change | Usually the tonic or the dominant in the lowest voice. The chords above it become dissonant against it |  | wiki-nct | R |
| Bass note outside the chord | The bass has a note that is not in the chord above it | The most elementary form of pandiatonic harmony | Stravinsky; the Elektra chord of Strauss | wiki-nct; wiki-pandiatonic | R |
| Chromatic note outside the chord | A note outside the key that moves by a semitone | More frequent from the Romantic period on |  | wiki-nct | R |
| Note that does not resolve | A note outside the chord stays to the subsequent change of harmony | It makes a seventh chord or an extended chord. Nadeau: each such note "became frozen into the chordal mass"; ninth, eleventh, and thirteenth chords became normal |  | wiki-nct | R |
| Added second or ninth | A major second or ninth above the root of a triad, with the third in the chord | Added notes are "more intense substitutes for traditional chords" | C D E G | wiki-addtone | R |
| Added fourth | A perfect fourth above the root of a triad, with the third in the chord |  |  | wiki-addtone | R |
| Added sixth | A major or minor sixth above the root of a triad | The chord with a sixth and a ninth is "not a tense chord requiring resolution" |  | wiki-addtone | R |
| Mixed third | The major third and the minor third of one root, an octave or more apart | Usually the minor third is above the major third | Many symphonies of William Schuman | wiki-addtone | R |
| Pandiatonic harmony | All seven notes of a scale are free to sound together. No rules of resolution | Triads with an added sixth, seventh, or second are the most frequent chords. A strong sense of key, "with a distinct preference for major keys" | Stravinsky, Symphony of Psalms III. Copland, Appalachian Spring. Prokofiev, start of Piano Concerto No. 3 | wiki-pandiatonic | R |
| Polymodal chromaticism | Two or more modes on one tonic at the same time or in sequence. Example: the Phrygian mode and the Lydian mode on C give all twelve notes | Each chromatic note is a member of a mode on the tonic (Bartók: a "diatonic ingredient"). The key centre stays | Bartók, Mikrokosmos No. 80. Bartók, Harvard lectures (1943) | wiki-polymodal | R |
| Chord from two interval types | A chord of many notes (to all twelve) that has only two interval types between adjacent notes | Lutosławski keeps the dense chords for climaxes. They are not clusters: each chord has its own colour | Lutosławski, Musique funèbre (tritones and semitones); Symphony No. 2 (major seconds and fourths) | wiki-lutoslawski | R |

Data file: [`research/tables/colour.csv`](../research/tables/colour.csv)

### S15. More devices of modern orchestral writing

The table gives devices of composers after 1900. The first edition of the study did not have them.

| Device | Content | Parameters | Example | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| Tone-colour melody (Klangfarbenmelodie) | A change of the instruments has the effect of a melody, even on one pitch. In later use: one line goes from instrument to instrument | Webern: frequently one note for each instrument | Schoenberg, Five Pieces op. 16 no. 3 (1909). Webern, Five Pieces op. 10 (1913) | wiki-klang | R |
| One chord in changing colours | The chord C, G-sharp, B, E, A stays. The instruments that play it change: "a kaleidoscopically rotating array of instrumental colors" | Schoenberg to the conductor: "There are no motives in this piece which have to be brought to the fore" | Schoenberg, Five Pieces op. 16 no. 3 ("Farben") | wiki-op16 | R |
| Heterophony | "The simultaneous variation of a single melodic line": some players have the plain line, others have it with ornaments or in a different rhythm | Usual in gamelan, gagaku, and Arab classical music | Britten, Curlew River. Boulez, Rituel | wiki-hetero | R |
| Micropolyphony | Many lines in canon at different speeds. The ear cannot follow one line: the result is a cluster that moves | Cope: it differs from a cluster "in its use of moving rather than static lines" | Ligeti, Apparitions; Atmosphères; Lontano | wiki-micro | R |
| Limited aleatory | All notes are written. The players do not play exactly together: each player goes at his own speed until the conductor gives a sign | The composer controls the harmony and the form. Lutosławski: "I do not presuppose any improvised parts" | Lutosławski, Jeux vénitiens (1960-61). Hovhaness (1958): "Repeat and repeat ad lib, but not together" | wiki-lutoslawski; wiki-aleatoric | R |
| Chain form | Two strands of music overlap as the links of a chain: one strand starts before the other stops | The sections do not start and stop together | Lutosławski, Chain 1 to 3 (about 1983 to 1986) | wiki-lutoslawski | R |
| Sound mass | Texture, tone colour, and loudness are more important than the single pitches | Clusters, glissandi, extreme registers, flutter-tongue, mutes | Penderecki, Threnody (1959). Ligeti, Atmosphères (1961) | wiki-soundmass | R |
| Tempo modulation | A new tempo comes from a note value of the old tempo: the pivot note value is the same in the two tempos | New tempo = old tempo x (number of pivot notes in the new bar / number in the old bar). Example: 84 x 3/2 = 126 | Carter, Cello Sonata (1948) | wiki-metricmod | R |
| Written change of speed | The number of notes for each beat grows and then becomes smaller again | 1 1 2 3 5 8 5 3 2 1 1 (a Fibonacci pattern) | Bartók, Music for Strings, Percussion and Celesta III (xylophone) | wiki-mspc | R |
| Spectral orchestration | Each instrument plays one partial of a sound. The pitches come from the harmonic series and can be microtones | "Additive instrumental synthesis" | Grisey, Partiels (1975). Murail, Gondwana (1980) | wiki-spectral | R |
| Night that becomes sunrise | "Sunrise is represented by an orchestral tutti beginning with pointillistic night sounds". A very large crescendo breaks off. Then "a soft, warm string chord" is the risen sun | Points of sound; one crescendo; a sudden stop; one soft chord | Corigliano, Pied Piper Fantasy I | cor-piper | R |
| Each player has a solo | The orchestra part is as difficult as the solo part: the work "approaches being a concerto for orchestra" | Each section and many single players get a display passage | Corigliano, Clarinet Concerto. Bartók, Concerto for Orchestra | cor-clarinet; wiki-cfo | R |
| Section borders that are not sharp | The parts of the form go into each other. The listener does not hear the exact moment of the change |  | John Luther Adams, Become Ocean | sowa-repetition | R |

Data file: [`research/tables/devices.csv`](../research/tables/devices.csv)

### S11. Night music and melody from different regions of the world

The table lists possible material from different regions. Most rows have the code K: the study did not read a source for them. The design stage must check the selected rows with primary sources.

Each tradition has its own meaning and context. The new work must use this material with respect and with exact knowledge.

| Tradition | Region | Item | Parameters | Link to the reference composers | Source | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Hungarian peasant song (old style) | Hungary | Descending pentatonic melody | Scale 0 3 5 7 10. Four lines of equal length. The second half repeats the first half a fifth lower | Bartók's base material. The lonely melody of Melody in the Mist is in this style | wiki-nightmusic; reference | R, K |
| Hungarian folk instruments | Hungary | Instruments of the peasant tradition | Citera (zither), cimbalom (hammered strings), duda (bagpipe), tárogató (reed), kaval (flute), doromb (jaw harp), tekerő (hurdy-gurdy) | Possible colours for the orchestra. Bartók imitates the bagpipe in Musettes | wiki-hunfolk; wiki-ood | R |
| Romanian long song (hora lungă, doina) | Maramureș and other regions | Free, decorated solo melody | Free rhythm. Many ornaments. The singer improvises on a more or less fixed pattern that usually descends. The long notes are the fourth or the fifth above the lowest note | Bartók found it in 1912. He found related types in Ukraine, Albania, Algeria, the Middle East, and North India, and he linked it to the maqam system. Thus the long song connects three of the four selected traditions | wiki-doina | R |
| Bulgarian and Turkish dance | Balkans and Anatolia | Aksak metres | Groups of 2 and 3 at fast tempo: 2+2+3; 2+2+2+3; 3+2+2; 2+3 | Bartók's "Bulgarian rhythm": String Quartet No. 5, Mikrokosmos | wiki-aksak; wiki-sq5 | R |
| Shepherd flute | Hungarian plain | Flute melody heard from far away at night | Dorian mode. Narrow range. The melody grows out of repeated notes | The Night's Music (material C) | wiki-ood; wiki-nightmusic | R |
| Night call to prayer | Fez, Morocco | Many callers who do not agree in time | About 4 o'clock at night. First one voice, then tens of voices. At one moment all hold one note: a major chord. Then silence, a cock, a dog, dawn | Corigliano heard it and wrote the Nocturne of the String Quartet and Symphony No. 2 | cor-quartet | R |
| Call to prayer by time of day | Turkey | A different maqam for each of the five calls | The maqam agrees with the time of day | A model for modes that change with the hours. This is sacred music: the new work must not imitate the call itself | wiki-adhan | R |
| Arab maqam | Middle East and North Africa | Melody type and method of improvisation | No fixed metre. The maqam gives the tonic, the dominant note, and the notes to emphasize. Scales have 7 notes with microtones. Notation rounds them to quarter-tones; the frequent half-flat notes are E, B, and A. The melody starts low, goes up by stages to a climax, then comes down. Violin, nay, qanun, and clarinet can play the intervals | Bartók linked the Romanian long song to the maqam system. Corigliano uses quarter-tones for expression | wiki-maqam; wiki-doina; cor-chiaroscuro | R |
| Hindustani raga | North India | Ragas for the hours of the night | Yaman: first quarter of the night (about 21:00 to 24:00). Bageshri: middle of the night. Malkauns: 24:00 to 03:00. Darbari Kanada: midnight, deep in the night. The opening (alap) has no metre, is improvised above a drone, and starts slowly. In one method the notes come one at a time, and the first note in a new octave is a strong event. Then a pulse starts (jor), then the tempo becomes fast (jhala) | Same idea as night music: a slow, free line above a still background. Same process as Schoenberg's themes that go up in register | wiki-yaman; wiki-bageshri; wiki-malkauns; wiki-darbari; wiki-alap | R |
| Javanese shadow play (wayang kulit) | Java | Music for a full night in three stages | The mode (pathet) changes through the night. Slendro: nem, then sanga, then manyura. Pelog: lima, then nem, then barang. Each pathet has its cadence. Slendro nem: 6 5 3 2. Sanga: 2 1 6 5. Manyura: 3 2 1 6 | A model for a large form that follows the hours of the night | wiki-pathet; wiki-slendro | R |
| Javanese gong cycle (colotomy) | Java | Gongs that mark nested cycles of time | Lancaran: a cycle of 16 beats. The large gong sounds 1 time. The kenong divides the cycle into 4. The kempul divides each of these parts into 2. The ketuk divides again into 2. Groups of 4 are most frequent at all levels | A fixed slow cycle below free layers: a way to show time in the night music | wiki-colotomy | R |
| Paired tuning | Bali | Two instruments tuned a small interval apart | The pair makes beats. The speed of the beats is the same for all notes in all registers | Same idea as Bartók's badly tuned pair of bagpipes (Musettes) and Corigliano's two pianos a quarter-tone apart: a shimmer | wiki-slendro; wiki-pelog; wiki-ood; cor-chiaroscuro | R |
| Japanese court music (gagaku) | Japan | Cluster chords of the mouth organ (shō) | The shō has 17 bamboo pipes with free reeds; 15 of them sound. The reeds sound when the player breathes in and breathes out, thus the sound does not stop. The standard chords have 5 or 6 notes and are held with a slow change | Cluster harmony as a still background, much older than Bartók. The accordion is a free-reed instrument of the same family | wiki-sho; reference | R, K |
| Japanese bamboo flute (shakuhachi) | Japan | Solo pieces in breath rhythm | One phrase = one breath. Silence (ma) is part of the music. Pitch bends, air noise | A model for a lonely melody with silence | reference | K |
| Shona mbira | Zimbabwe | Music for a ceremony that continues through the night | Cycles of 12 or 48 pulses. Two or more interlocked parts. The listener hears melodies that no single player plays | Layers that make new patterns together | reference | K |
| West African drum ensemble | Ghana and neighbours | Bell time-line | 12 pulses: 2 2 1 2 2 2 1. All other parts align to the bell | A fixed cycle below free layers | reference | K |
| Andalusian song (flamenco) | Spain | Phrygian cadence and 12-beat cycle | Chords A minor, G, F, E. Cycle of 12 beats with accents on 3, 6, 8, 10, 12 (soleá) | Night as a subject in Spanish music (Falla) | reference | K |
| Lullaby | World | Rocking song for a child at night | Small range. Falling minor third. Slow 6/8 or 2/4. Many repeats | Bartók: Lullaby from Village Scenes is on the night music list | wiki-nightmusic; reference | R, K |
| Animal sounds at night | Hungary and North America | Sounds that composers wrote down | Fire-bellied toad (Bombina bombina), cicada, birds; tufted titmouse, wood thrush | The Night's Music; Piano Concerto No. 3 | wiki-nightmusic | R |

Data file: [`research/tables/world.csv`](../research/tables/world.csv)

## Part 3: Style profiles

A style profile is a set of target ranges for the new work. Each range has a low value and a high value. The study team set each range around a measured value or a sourced value. The column "Basis" gives that value.

The profile "All" applies to the full work. The other three profiles apply to zones of the work. The design stage will decide the sequence and the mix of the zones.

### P1. Profile "All": the full work

| Group | Parameter | Low | High | Unit | Basis | Code |
| --- | --- | --- | --- | --- | --- | --- |
| Form | Position of the turn from dark to light | 0.52 | 0.56 | share of the duration | Verklärte Nacht: D major comes at 0.54 of the time and 0.55 of the bars | M |
| Form | Position of the far point of the key plan | 0.42 | 0.54 | share of the duration | Music for Strings I: the subject is on E-flat at 0.50. Verklärte Nacht: section 3 (0.42 to 0.54) ends in E-flat minor | R |
| Form | Position of the largest climax | 0.62 | 0.81 | share of the duration | Music for Strings I: 0.63. Verklärte Nacht: 0.77 of the time and 0.81 of the bars | M |
| Form | Position of a second climax | 0.88 | 0.94 | share of the duration | Verklärte Nacht bar 391: 0.91 of the time | M |
| Form | Number of sections | 4 | 8 | sections | Verklärte Nacht 5. Bartók arch forms 5. Corigliano 4, 5, and 8 | R |
| Form | Time for each theme group | 2 | 3 | minutes | Verklärte Nacht: 11 theme groups in 28 minutes | R |
| Form | Duration of a large one-movement or multi-part work | 28 | 40 | minutes | Verklärte Nacht 28. Concerto for Orchestra 38. Corigliano 29, 35, 35, 38, 40 | R |
| Dynamics | Time with a level of p or softer | 0.60 | 0.70 | share of the duration | Verklärte Nacht: 0.64 marked. The first bars (0.05) have no level mark and are soft | M |
| Dynamics | Time with a level of mp or mf | 0.08 | 0.14 | share of the duration | Verklärte Nacht: 0.11 | M |
| Dynamics | Time with a level of f or louder | 0.15 | 0.25 | share of the duration | Verklärte Nacht: 0.21 | M |
| Dynamics | Time with the level fff | 0.03 | 0.06 | share of the duration | Verklärte Nacht: 0.05 (21 bars) | M |
| Dynamics | Softest and loudest level | pppp | fff | mark | Verklärte Nacht | M |
| Dynamics | Dynamic level marks | 2.5 | 3.5 | marks for each 10 bars | Verklärte Nacht (arrangement): 3.0. Orchestra parts need more marks | M |
| Tempo | Bars for each tempo mark | 5 | 13 | bars | Bartók, Divertimento II: 5.3. Verklärte Nacht: 12.7 | M |
| Tempo | Fastest bar divided by slowest bar | 2.5 | 3.5 | ratio | Verklärte Nacht: 133 and 40 quarter notes in a minute (ratio 3.3) | M |
| Tempo | Mean tempo of a section | 39 | 76 | quarter notes in a minute | Verklärte Nacht sections: 44 to 85 in the arrangement, divided by 1.12 for real recordings | M |
| Metre | Changes of metre | 4 | 10 | changes for each 100 bars | Verklärte Nacht: 4.3. Bartók's Bagatelle no. 12 has 5 metres in 44 bars | M |
| Repetition | Returns of a theme or of a section with no change | 0 | 0 | returns | Bartók (1937): "I never repeat one part identically". Schoenberg: developing variation | R |
| Repetition | Bars of the full texture that are the same as one of the 8 bars before | 0.00 | 0.06 | share of the bars | Verklärte Nacht: 0.05 | M |
| Repetition | Bars in a block of 4 bars that is the same as an earlier block | 0.00 | 0.00 | share of the bars | Verklärte Nacht: 0.00 | M |
| Repetition | Bars of one voice that are the same as one of its 8 bars before | 0.10 | 0.30 | share of the bars of the voices | Verklärte Nacht: 0.10 (voices of a piano arrangement). An orchestra has more voices with accompaniment figures: thus the high value is larger | M |

### P2. Profile "Transfigured": the Schoenberg zone

| Group | Parameter | Low | High | Unit | Basis | Code |
| --- | --- | --- | --- | --- | --- | --- |
| Harmony | Chords built from thirds | 0.62 | 0.72 | share of the chord time | Verklärte Nacht: 0.68 (parts 0.69 and 0.67) | M |
| Harmony | Chords with a semitone clash | 0.20 | 0.28 | share of the chord time | Verklärte Nacht: 0.24 | M |
| Harmony | Chords with a cluster of 3 semitones | 0.00 | 0.02 | share of the chord time | Verklärte Nacht: 0.01 | M |
| Harmony | Chords in one whole-tone scale | 0.09 | 0.16 | share of the chord time | Verklärte Nacht: 0.13 (parts 0.16 and 0.10) | M |
| Harmony | Vagrant chords divided by major and minor triads, before the turn | 1.8 | 2.2 | ratio | Verklärte Nacht part 1: 0.216 and 0.110 of the sounding time (ratio 2.0) | M |
| Harmony | Vagrant chords divided by major and minor triads, after the turn | 0.55 | 0.75 | ratio | Verklärte Nacht part 2: 0.128 and 0.196 of the sounding time (ratio 0.65) | M |
| Harmony | Dominant chords | 0.05 | 0.07 | share of the sounding time | Verklärte Nacht: 0.057. The dominant is not a key area | M |
| Bass | Bass moves by semitone | 0.27 | 0.33 | share of the bass moves | Verklärte Nacht: 0.30 | M |
| Bass | Bass moves by fourth or fifth | 0.13 | 0.18 | share of the bass moves | Verklärte Nacht: 0.15 | M |
| Melody | Semitone moves, before the turn | 0.22 | 0.30 | share of the moves | Verklärte Nacht part 1: 0.26 | M |
| Melody | Semitone moves, after the turn | 0.08 | 0.13 | share of the moves | Verklärte Nacht part 2: 0.10 | M |
| Melody | Moves of a fourth or fifth, before and after the turn | 0.18 | 0.26 | share of the moves | Verklärte Nacht: 0.18 in part 1 and 0.26 in part 2 | M |
| Melody | Moves of a sixth or larger | 0.20 | 0.28 | share of the moves | Verklärte Nacht: 0.24 | M |
| Melody | Mean size of a move | 5.0 | 5.8 | semitones | Verklärte Nacht: 5.5 | M |
| Melody | Repeated notes | 0.01 | 0.04 | share of the moves | Verklärte Nacht: 0.02 | M |
| Pitch | Different pitch classes in one bar of 4/4 | 7 | 8 | pitch classes | Verklärte Nacht: 7.6 | M |
| Theme | Length of the theme unit | 1 | 2 | bars | Verklärte Nacht: unit, unit, continuation (1 + 1 + 2) | R |

### P3. Profile "Night": the Bartók zone

| Group | Parameter | Low | High | Unit | Basis | Code |
| --- | --- | --- | --- | --- | --- | --- |
| Harmony | Chords with a semitone clash | 0.88 | 0.95 | share of the chord time | The Night's Music: 0.92 | M |
| Harmony | Chords with a cluster of 3 semitones | 0.68 | 0.80 | share of the chord time | The Night's Music: 0.77 | M |
| Harmony | Chords built from thirds | 0.00 | 0.08 | share of the chord time | The Night's Music: 0.05 | M |
| Harmony | Time with the background cluster | 0.20 | 0.30 | share of the sounding time | The Night's Music: one cluster of 5 semitones sounds for 0.26 | M |
| Harmony | Size of the background cluster | 5 | 8 | adjacent semitones | The Night's Music: 5 notes (arpeggio) and 8 notes (palm) | R |
| Harmony | Distance between the key centres of two layers | 6 | 6 | semitones | The Night's Music: G and C-sharp | R |
| Melody | Repeated notes | 0.12 | 0.25 | share of the moves | The Night's Music: 0.13. Bagatelle no. 12: 0.24 | M |
| Melody | Whole-tone moves | 0.25 | 0.30 | share of the moves | The Night's Music: 0.28. Bagatelle no. 12: 0.25 | M |
| Melody | Moves of an octave or larger | 0.15 | 0.22 | share of the moves | The Night's Music: 0.19 (events in far registers) | M |
| Texture | Number of materials | 3 | 3 | layers | The Night's Music: night noises, chorale, flute melody | R |
| Texture | Types of nature call | 6 | 6 | types | The Night's Music | R |
| Texture | Full pitch range | 60 | 69 | semitones | The Night's Music: MIDI 35 to 104 | M |
| Texture | Width of simultaneous notes (90th percentile) | 44 | 48 | semitones | The Night's Music: 48 (four octaves) | M |
| Rhythm | Note starts | 4.0 | 5.5 | starts in one second | The Night's Music: 4.7. Fast pieces of the same set: 8.5 to 20.9 | M |
| Rhythm | Slow pulse | 60 | 72 | beats in a minute | The Night's Music: quarter note = 72. Music for Strings III: eighth note = 66 | R |
| Dynamics | Mean loudness divided by the mean loudness of fast movements | 0.65 | 0.75 | ratio of key velocity | The Night's Music 49; The Chase 69; With Drums and Pipes 74 | M |

### P4. Profile "Theatre": the Corigliano zone

| Group | Parameter | Low | High | Unit | Basis | Code |
| --- | --- | --- | --- | --- | --- | --- |
| Form | Design sequence | shape | notes | sequence | Corigliano: the shape of the work comes before the notes | R |
| Tempo | Ratio of two tempos that sound together | 1.2 | 1.33 | ratio | String Quartet, Fugue: 72 and 60. Chiaroscuro: 4 to 3 | R |
| Space | Brass players around the orchestra | 17 | 17 | players | Symphony No. 1: 5 trumpets, 6 horns, 4 trombones, 2 tubas | R |
| Space | Offstage instruments | 1 | 3 | players | Symphony No. 1: 1 piano. Vocalise: 3 trumpets | R |
| Orchestra | Woodwind players in each family | 3 | 4 | players | Corigliano's scores for large orchestra | R |
| Orchestra | Horns | 4 | 6 | players | Corigliano's scores for large orchestra | R |
| Orchestra | Trumpets | 3 | 5 | players | Corigliano's scores for large orchestra | R |
| Orchestra | Percussion players (without timpani) | 3 | 5 | players | Corigliano's scores for large orchestra | R |
| Pitch | Pitch centres of a full work | 4 | 4 | notes | String Quartet: C, C-sharp, G, G-sharp | R |
| Pitch | Pitches of the chaconne sequence | 12 | 12 | pitches | Symphony No. 1 III | R |
| Material | Quotations of other music | 1 | 1 | for each work | Symphony No. 1: a tango. Three Hallucinations: a hymn. Chiaroscuro: a Bach chorale | R |
| Tuning | Smallest interval | 50 | 50 | cents | Quarter-tones in Chiaroscuro, Pied Piper Fantasy, and Altered States | R |

Data file: [`research/tables/profiles.csv`](../research/tables/profiles.csv)

## Limits of the study

- The *Verklärte Nacht* data come from a piano arrangement.
  The arrangement keeps the harmony and the main lines.
  It does not keep the six separate parts, and it changes some octaves.
- The "top line" is the highest note of the upper stave. It is not always the main melody.
- The tempo values of *Verklärte Nacht* use the timing of the arrangement.
  The mean of five recordings is slower by the factor 1.12.
- The dynamic marks of *Verklärte Nacht* are the marks of the arrangement.
- The *Out of Doors* data come from one performance.
  The sustain pedal holds notes, thus the measured chords are larger than the written chords.
- The study did not measure the music of Corigliano.
- The study measured audio recordings of full orchestras for the sound of the master
  (tables M13 and M14). These recordings are not works of the three reference composers:
  no free recordings of their works were available.
- The rows with the code K are not checked.
- The repetition values of *Verklärte Nacht* are for the voices of a piano arrangement. The values of the new work are for the players of an orchestra.
- The harmony values of the new work come from all notes of the score. They do not show which notes the ear hears as melody and which as harmony.
- The table of the instrument techniques (S13) lists what the sources name. It is not a full list, and it does not show how difficult a technique is.

## Sources

| Key | Source | Access |
| --- | --- | --- |
| `frisch1993` | Frisch, Walter. The Early Works of Arnold Schoenberg, 1893-1908. University of California Press, 1993. Chapters 4 and 5. <http://publishing.cdlib.org/ucpressebooks/view?docId=ft5t1nb3gn> | read |
| `wellesz1925` | Wellesz, Egon. Arnold Schönberg. 1925. Five-part plan of Verklärte Nacht. | through frisch1993 |
| `pfannkuch1963` | Pfannkuch, Wilhelm. Zu Thematik und Form in Schönbergs Streichsextett. 1963. Bar numbers added by Frisch. | through frisch1993 |
| `swift1977` | Swift, Richard. 1/XII/99: Tonal Relations in Schoenberg's Verklärte Nacht. 19th-Century Music 1 (1), 1977. <https://doi.org/10.2307/746766> | through frisch1993 |
| `schoenberg1932` | Schoenberg, Arnold. Konstruktives in der Verklärten Nacht. Manuscript, 1932. | through frisch1993 |
| `schoenberg1978` | Schoenberg, Arnold. Theory of Harmony. Translated by Roy E. Carter. 1978. Page 346: the inverted ninth chord. | through frisch1993 |
| `billam2013` | Billam, Peter. Verklärte Nacht by Arnold Schoenberg, arranged for piano. 2013, edition of 15 February 2014. Score and muscript text source. Licence CC BY 4.0. <https://peterbillam.gitlab.io/pjb_arrangements/> | read and measured |
| `muscript` | Billam, Peter. Muscript: format manual. <https://peterbillam.gitlab.io/muscript/> | read |
| `imslp-vn` | IMSLP. Verklärte Nacht, Op.4 (Schoenberg, Arnold). List of scores and recordings with durations. <https://imslp.org/wiki/Verkl%C3%A4rte_Nacht,_Op.4_(Schoenberg,_Arnold)> | read |
| `ia-vn1924` | Internet Archive. Schoenberg, Verklärte Nacht. Spencer Dyke Sextet, National Gramophonic Society, 1924. Item data. <https://archive.org/details/ngs-h-l-schoenberg-verklarte-nacht> | read |
| `wiki-vn` | Wikipedia. Verklärte Nacht. Read 2026-11-14. <https://en.wikipedia.org/wiki/Verkl%C3%A4rte_Nacht> | read |
| `wiki-pelleas` | Wikipedia. Pelleas und Melisande (Schoenberg). Read 2026-11-14. <https://en.wikipedia.org/wiki/Pelleas_und_Melisande_(Schoenberg)> | read |
| `wiki-op16` | Wikipedia. Five Pieces for Orchestra. Read 2026-11-14. <https://en.wikipedia.org/wiki/Five_Pieces_for_Orchestra> | read |
| `wiki-gurre` | Wikipedia. Gurre-Lieder. Read 2026-11-14. <https://en.wikipedia.org/wiki/Gurre-Lieder> | read |
| `wiki-op9` | Wikipedia. Chamber Symphony No. 1 (Schoenberg). Read 2026-11-14. <https://en.wikipedia.org/wiki/Chamber_Symphony_No._1_(Schoenberg)> | read |
| `wiki-nightmusic` | Wikipedia. Night music (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Night_music_(Bart%C3%B3k)> | read |
| `schneider2006` | Schneider, David E. Bartók, Hungary, and the Renewal of Tradition. University of California Press, 2006. Pages 81-116. | through wiki-nightmusic and wiki-ood |
| `danchenka1987` | Danchenka, Gary. Diatonic Pitch-Class Sets in Bartók's Night Music. Indiana Theory Review 8 (1), 1987. | through wiki-nightmusic |
| `wiki-ood` | Wikipedia. Out of Doors (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Out_of_Doors_(Bart%C3%B3k)> | read |
| `wiki-mspc` | Wikipedia. Music for Strings, Percussion and Celesta. Read 2026-11-14. <https://en.wikipedia.org/wiki/Music_for_Strings,_Percussion_and_Celesta> | read |
| `solomon1973` | Solomon, Larry J. Symmetry as a Compositional Determinant. 1973, revised 2002. Chapter VII. <https://web.archive.org/web/20060827021555/http://solomonsmusic.net/diss7.htm> | read |
| `roberts2021` | Roberts, Gareth E. Bartók, Fibonacci, and the Golden Ratio: Fact or Fiction. Handout, Joint Mathematics Meetings 2021. <https://meetings.ams.org/math/jmm2021/mediafile/Handout/Paper3109/Bartok_JMM2021_Roberts.pdf> | read |
| `lendvai1971` | Lendvai, Ernő. Béla Bartók: An Analysis of His Music. Kahn and Averill, 1971. | through roberts2021 and solomon1973 |
| `lendvai-web` | Lendvai, Ernő. Text on the Sonata for Two Pianos and Percussion (dimensions and overall form). Web edition. <https://www.mi.sanu.ac.rs/vismath/lend/b12.htm> | read |
| `howat1983` | Howat, Roy. Bartók, Lendvai and the Principles of Proportional Analysis. Music Analysis 2 (1), 1983. | through roberts2021 |
| `wiki-cfo` | Wikipedia. Concerto for Orchestra (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Concerto_for_Orchestra_(Bart%C3%B3k)> | read |
| `wiki-sq4` | Wikipedia. String Quartet No. 4 (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/String_Quartet_No._4_(Bart%C3%B3k)> | read |
| `wiki-sq5` | Wikipedia. String Quartet No. 5 (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/String_Quartet_No._5_(Bart%C3%B3k)> | read |
| `wiki-son2p` | Wikipedia. Sonata for Two Pianos and Percussion. Read 2026-11-14. <https://en.wikipedia.org/wiki/Sonata_for_Two_Pianos_and_Percussion> | read |
| `wiki-pc2` | Wikipedia. Piano Concerto No. 2 (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Piano_Concerto_No._2_(Bart%C3%B3k)> | read |
| `wiki-pc3` | Wikipedia. Piano Concerto No. 3 (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Piano_Concerto_No._3_(Bart%C3%B3k)> | read |
| `wiki-div` | Wikipedia. Divertimento for String Orchestra (Bartók). Read 2026-11-14. <https://en.wikipedia.org/wiki/Divertimento_for_String_Orchestra_(Bart%C3%B3k)> | read |
| `wiki-axis` | Wikipedia. Axis system. Read 2026-11-14. <https://en.wikipedia.org/wiki/Axis_system> | read |
| `wiki-acoustic` | Wikipedia. Acoustic scale. Read 2026-11-14. <https://en.wikipedia.org/wiki/Acoustic_scale> | read |
| `wiki-polymodal` | Wikipedia. Polymodal chromaticism. Read 2026-11-14. <https://en.wikipedia.org/wiki/Polymodal_chromaticism> | read |
| `wiki-aksak` | Wikipedia. Aksak. Read 2026-11-14. <https://en.wikipedia.org/wiki/Aksak> | read |
| `wiki-circus` | Wikipedia. Symphony No. 3 (Corigliano). Read 2026-11-14. <https://en.wikipedia.org/wiki/Symphony_No._3_(Corigliano)> | read |
| `cor-sym1` | Corigliano, John. Symphony No. 1 (1988). Work page with forces, duration, and program note. <https://johncorigliano.com/works/symphony-no-1-1988> | read |
| `cor-circus` | Corigliano, John. Circus Maximus (2004). Work page with program note. <https://johncorigliano.com/works/circus-maximus-2004> | read |
| `cor-sym2` | Corigliano, John. Symphony No. 2 (2000). Work page with forces, duration, and program note. <https://johncorigliano.com/works/symphony-no-2-2000> | read |
| `cor-quartet` | Corigliano, John. String Quartet (1995). Work page with program note. <https://johncorigliano.com/works/string-quartet-1995> | read |
| `cor-clarinet` | Corigliano, John. Concerto for Clarinet and Orchestra (1977). Work page with forces and program note. <https://johncorigliano.com/works/concerto-for-clarinet-and-orchestra-1977> | read |
| `cor-piper` | Corigliano, John. Pied Piper Fantasy (1982). Work page with forces and program note. <https://johncorigliano.com/works/pied-piper-fantasy-1982> | read |
| `cor-conjurer` | Corigliano, John. Conjurer (2007). Work page with program note. <https://johncorigliano.com/works/conjurer-concerto-for-percussionist-and-string-orchestra-2007> | read |
| `cor-chaconne` | Corigliano, John. The Red Violin: Chaconne for Violin and Orchestra (1997). Work page with forces and program note. <https://johncorigliano.com/works/the-red-violin-chaconne-for-violin-and-orchestra-1997> | read |
| `cor-halluc` | Corigliano, John. Three Hallucinations (1981). Work page with forces and program note. <https://johncorigliano.com/works/three-hallucinations-1981> | read |
| `cor-vocalise` | Corigliano, John. Vocalise (1999). Work page with forces and program note. <https://johncorigliano.com/works/vocalise-1999> | read |
| `cor-chiaroscuro` | Corigliano, John. Chiaroscuro. Work page with program note. <https://johncorigliano.com/works/chiaroscuro> | read |
| `cor-site` | Corigliano, John. Other work pages: forces and durations. <https://johncorigliano.com/work/works-by-category> | read |
| `bednarek2026` | Bednarek, Michael. Béla Bartók, Out of Doors Suite, Sz 81. MIDI capture of a piano performance. Wikimedia Commons, 2026. Licence CC0 1.0. <https://commons.wikimedia.org/wiki/File:B%C3%A9la_Bart%C3%B3k,_Out_of_Doors_Suite,_Sz_81.mid> | measured |
| `dcml-bagatelles` | Digital and Cognitive Musicology Lab. bartok_bagatelles: Béla Bartók, Fourteen Bagatelles op. 6. Annotated score corpus. Licence CC BY-NC-SA 4.0. <https://github.com/DCMLab/bartok_bagatelles> | measured |
| `wiki-doina` | Wikipedia. Doina. Read 2026-11-15. <https://en.wikipedia.org/wiki/Doina> | read |
| `wiki-hunfolk` | Wikipedia. Hungarian folk music. Read 2026-11-15. <https://en.wikipedia.org/wiki/Hungarian_folk_music> | read |
| `wiki-maqam` | Wikipedia. Arabic maqam. Read 2026-11-15. <https://en.wikipedia.org/wiki/Arabic_maqam> | read |
| `wiki-adhan` | Wikipedia. Adhan. Read 2026-11-15. <https://en.wikipedia.org/wiki/Adhan> | read |
| `wiki-yaman` | Wikipedia. Yaman (raga). Read 2026-11-15. <https://en.wikipedia.org/wiki/Yaman_(raga)> | read |
| `wiki-malkauns` | Wikipedia. Malkauns. Read 2026-11-15. <https://en.wikipedia.org/wiki/Malkauns> | read |
| `wiki-darbari` | Wikipedia. Darbari Kanada. Read 2026-11-15. <https://en.wikipedia.org/wiki/Darbari_Kanada> | read |
| `wiki-bageshri` | Wikipedia. Bageshri. Read 2026-11-15. <https://en.wikipedia.org/wiki/Bageshri> | read |
| `wiki-alap` | Wikipedia. Alap. Read 2026-11-15. <https://en.wikipedia.org/wiki/Alap> | read |
| `wiki-pathet` | Wikipedia. Pathet. Read 2026-11-15. <https://en.wikipedia.org/wiki/Pathet> | read |
| `wiki-slendro` | Wikipedia. Slendro. Read 2026-11-15. <https://en.wikipedia.org/wiki/Slendro> | read |
| `wiki-pelog` | Wikipedia. Pelog. Read 2026-11-15. <https://en.wikipedia.org/wiki/Pelog> | read |
| `wiki-colotomy` | Wikipedia. Colotomy. Read 2026-11-15. <https://en.wikipedia.org/wiki/Colotomy> | read |
| `wiki-sho` | Wikipedia. Shō (instrument). Read 2026-11-15. <https://en.wikipedia.org/wiki/Sh%C5%8D_(instrument)> | read |
| `wiki-devvar` | Wikipedia. Developing variation. Read 2026-11-15. Quotes Schoenberg, Style and Idea (1975), pages 248 and 397, and Frisch (1982). <https://en.wikipedia.org/wiki/Developing_variation> | read |
| `fmc-summary` | Course module with quotations from Schoenberg, Fundamentals of Musical Composition (1967). Read 2026-11-15. <https://tambien.github.io/InteractiveMusic/module/fundamentals_of_music_composition> | read |
| `dille1937` | Bartók, Béla. Interview with Denijs Dille, Brussels, 2 February 1937. In Dille, Béla Bartók. Regard sur le passé (Louvain-la-Neuve, 1990), page 28. Read on the exhibition pages of the Bartók Archives, 2026-11-15. <https://zti.hu/bartok/exhibition/en_P8.htm> | read |
| `sowa-repetition` | Sowa, Joseph. Why don't modern composers like repetition? Essay on the web site of the composer. Read 2026-11-15. <https://josephsowa.com/why-dont-modern-composers-like-repetition/> | read |
| `wiki-corsym1` | Wikipedia. Symphony No. 1 (Corigliano). Read 2026-11-15. <https://en.wikipedia.org/wiki/Symphony_No._1_(Corigliano)> | read |
| `cor-fantasia` | Corigliano, John. Fantasia on an Ostinato (1985). Work page of the publisher with the program note. Read 2026-11-15. <https://www.wisemusicclassical.com/composer/work/24479> | read |
| `wiki-nct` | Wikipedia. Nonchord tone. Read 2026-11-15. <https://en.wikipedia.org/wiki/Nonchord_tone> | read |
| `wiki-addtone` | Wikipedia. Added tone chord. Read 2026-11-15. <https://en.wikipedia.org/wiki/Added_tone_chord> | read |
| `wiki-pandiatonic` | Wikipedia. Pandiatonicism. Read 2026-11-15. <https://en.wikipedia.org/wiki/Pandiatonicism> | read |
| `wiki-lutoslawski` | Wikipedia. Witold Lutosławski. Read 2026-11-15 (the first part of the article). <https://en.wikipedia.org/wiki/Witold_Lutos%C5%82awski> | read |
| `wiki-exttech` | Wikipedia. Extended technique. Read 2026-11-15. <https://en.wikipedia.org/wiki/Extended_technique> | read |
| `rush-techniques` | Rush, Toby. Extended Techniques. Chapter of an online text book on music of the twentieth century. Read 2026-11-15. <https://tobyrush.com/book/text/twc/twc03.html> | read |
| `wiki-flutter` | Wikipedia. Flutter-tonguing. Read 2026-11-15. <https://en.wikipedia.org/wiki/Flutter-tonguing> | read |
| `wiki-klang` | Wikipedia. Klangfarbenmelodie. Read 2026-11-15. <https://en.wikipedia.org/wiki/Klangfarbenmelodie> | read |
| `wiki-hetero` | Wikipedia. Heterophony. Read 2026-11-15. <https://en.wikipedia.org/wiki/Heterophony> | read |
| `wiki-micro` | Wikipedia. Micropolyphony. Read 2026-11-15. <https://en.wikipedia.org/wiki/Micropolyphony> | read |
| `wiki-aleatoric` | Wikipedia. Aleatoric music. Read 2026-11-15. <https://en.wikipedia.org/wiki/Aleatoric_music> | read |
| `wiki-soundmass` | Wikipedia. Sound mass. Read 2026-11-15. <https://en.wikipedia.org/wiki/Sound_mass> | read |
| `wiki-metricmod` | Wikipedia. Metric modulation. Read 2026-11-15. <https://en.wikipedia.org/wiki/Metric_modulation> | read |
| `wiki-spectral` | Wikipedia. Spectral music. Read 2026-11-15. <https://en.wikipedia.org/wiki/Spectral_music> | read |
| `reference` | Standard reference knowledge. The study did not read a source for these rows. Check each row before critical use. | not read |
