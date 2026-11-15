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
