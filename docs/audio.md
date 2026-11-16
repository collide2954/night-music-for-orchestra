# The audio: two sources of sound

The project can make the audio from two sources of sound.

| Source | Command | Where it can run | Result |
| --- | --- | --- | --- |
| Open sample libraries, with the sampler of this project | `uv run nightmusic audio` | On each computer and on the build server | The sound is not realistic. The owner of the project found it not sufficient. |
| MuseScore Studio with Muse Sounds | `uv run nightmusic audio --engine musescore` | On a computer that has the official MuseScore Studio and the Muse Sounds libraries | Much more realistic. The libraries are free, but they are not open. |

## Why there are two sources

- The open libraries (VSCO 2 Community Edition, Sonatina Symphonic Orchestra, VCSL) are the only orchestra samples that a build server can download and use freely. They have few dynamic levels and few recordings for each note.
- Muse Sounds are free sample libraries of Muse Group. Only MuseScore Studio can play them. The Muse Sounds Manager program installs them. A build server cannot do this.

## How the MuseScore source works

1. The code writes the work as a MusicXML file ([`notation/musicxml.py`](../src/nightmusic/notation/musicxml.py)).
   - Each instrument of each player is one part, at sounding pitch.
   - The file gives the tempo at each bar line. Thus the time of each bar is the same as in the tempo plan.
   - The file changes some notes, to make the start and the end of the sounds more natural (see "How the notes start and stop").
2. MuseScore changes the MusicXML file into its own format.
3. The code changes three items in that file ([`audio/musescore.py`](../src/nightmusic/audio/musescore.py)):
   - The words of the playing techniques (for example "sul pont.") become marks that MuseScore plays.
   - The master control of the mixer goes down by 18 dB. Without this, a loud passage of the full orchestra has distortion.
   - The mixer gets the levels of some instruments (the table `TRIM_DB` in the code). A measurement of each instrument alone gave these levels. For example, one stroke of the taiko of Muse Sounds was 8 dB louder than one stroke of the bass drum.
4. MuseScore renders the file to a WAV file (32-bit floating point).
5. The sampler of this project renders the instruments that Muse Sounds do not have: cimbalom, accordion, ocarina, mandolin, and frame drum.
   A measurement with the timpani gives the two sources the same level.
6. The master step sets the loudness (see "How the master sets the loudness"). It does not change the tone balance of this mix.

MuseScore renders five groups of the orchestra as five files (stems): woodwinds, brass, percussion, keyboards with harp, and strings.

- Three MuseScore programs run at the same time. Thus the render is faster.
- A stem stays from the last render if its music did not change.
- The table `STEM_GAIN_DB` in the code gives the level of each stem. A change of the balance between the groups needs no new render.

## How the notes start and stop

A score gives the length of a note, but a player does not stop each sound at that moment.
The MusicXML file is for the audio only. Thus it can give MuseScore the sound that a player makes:

| Item in the score | Item in the MusicXML file | Effect |
| --- | --- | --- |
| A note of an instrument that rings (harp, piano, celesta, bells, gongs, cymbals, drums, timpani) | The note continues to the subsequent note of that player, or for the ring time of the instrument | The sound decays. It does not stop at the end of the written note. |
| A soft long note before a rest (mf or softer, two quarter notes or longer) | Two tied notes. The second note is the last second of the sound: it has a decrease of loudness. Then the dynamic mark comes again. | The end of a phrase becomes soft (5 to 10 dB at mf). It does not stop suddenly. |
| A short bow stroke (spiccato) | A staccato note | The stroke is short and has a clear start. |
| A roll on a percussion instrument | A tremolo note | The instrument plays a roll. |
| A rolled chord (harp, piano) | The mark of a rolled chord on each note | The notes of the chord start one after the other. |
| A slide between two notes (one cello in part 3) | A slide, with the play style "portamento" in the MuseScore file | The pitch changes continuously. Without the play style, MuseScore plays a sequence of semitones. |
| A long note with an accent or a marcato mark (tenor trombone, violins, double basses) | The note has no such mark | The note sounds to its end. In Muse Sounds, the sound of an accent has a fixed length: 4.6 s for the trombone, 6.5 s for the double basses, and 7.4 s for the violins. A longer note with such a mark stops before its end. |
| A fermata | More time for the last quarter note of the bar, in the tempo plan | The sound, the score video, and the times in the documents agree. |

The table `RING_SECONDS` in the code gives the ring time of each instrument.
The table `ACCENT_SECONDS` gives the longest note that keeps its accent.
Measurements of test renders gave the values of the two tables.

## How the dynamic marks get balanced levels

Muse Sounds do not play all dynamic marks and articulations at balanced levels.
The owner of the project heard two faults: one instrument had no sound (the cellos at the mark G), and the loud brass had a hard "splat".

The command `uv run nightmusic calibrate` measures the sound source.
For each wind, brass, and string instrument, it renders a test score: each dynamic mark from ppp to fff as a long note, a staccato note, a note with an accent, a note with a marcato mark, and (for the strings) a pizzicato note.
The table [`audio/muse_levels.csv`](../src/nightmusic/audio/muse_levels.csv) has the level of each case.
The harp, the celesta, and the percussion instruments with a pitch (glockenspiel, crotales, vibraphone, marimba, xylophone, tubular bells) have one test: one stroke at each dynamic mark.

| Fault that the table shows | Example |
| --- | --- |
| The steps between the marks are not regular | Bass clarinet: 17 dB from mf to f. Oboe: 2 dB from mp to fff. |
| A mark is softer than the mark below it | Clarinet: mp is 10 dB softer than p. |
| A soft staccato note is almost silent | Trumpet: 25 dB below a long note at pp. |
| A marcato mark is much louder than its dynamic mark | Trumpet: 12 dB at mp. |
| The loud marks of the brass are very bright | Trombone: from mf to f, the share of the sound above 2 kHz goes up by 26 dB. |
| The soft marks of the instruments that a player strikes or plucks are much too soft | Celesta: the mark p is 27 dB below the mark f. Xylophone: 40 dB. Harp: 30 dB, with a step of 23 dB from mp to mf. |

The module [`notation/playback.py`](../src/nightmusic/notation/playback.py) uses the table. For each note, it selects the dynamic mark and the articulation that the audio file gets:

1. The level of the mark f of the instrument is the anchor. Each written mark has a target level in relation to the anchor: about 5 to 6 dB for each mark below f, and less above f.
2. A note gets the mark whose measured level is nearest to the target.
3. A brass instrument plays no mark louder than ff.
4. A note with an articulation gets a level near that of a note with no articulation (staccato 3 dB below, accent 3 dB above, marcato 5 dB above). If no mark gives such a level, the note gets a different articulation, or none.

The printed score and the parts do not change.

Muse Sounds do not play some very high notes (for example the violins above F7). The table `HIGHEST_NOTE` has these limits, and a test makes sure that the work has no such note.

## How the loud brass gets a round tone

The owner of the project heard that the loud brass had a "splat" that "cuts against the texture".
Measurements of Muse Sounds showed the cause:

| Measurement | Result |
| --- | --- |
| The level of the marks f, ff, and fff of each brass instrument | The same in a range of 3 dB. |
| The tone of these three marks (the share of the sound above 2 kHz) | The same in a range of 4 dB: very bright. |
| The step from mf to f | Trombone: 11 dB louder, and 26 dB more of its sound above 2 kHz. Trumpet: 6 dB louder, and 10 dB more above 2 kHz. |
| The start of a brass note | No fault: the first 30 ms are not louder than the held note (2.5 dB or less). |
| The start of a loud note of the violins | Slow: a quarter note at ff stays 8 dB below its loudest level for 0.4 s. A slur or a tenuto mark does not change this. |
| The groups in the loud passages | In most loud passages, the brass was not louder than the strings. In the main climax and in the last chords, where all brass players hold loud chords, the brass was 5 to 6 dB louder than the strings. |

Thus a written f of the brass sounded as loud and as hard as a written fff.
A real brass section at f has a full, round tone. Only at fff it has a hard edge.

The mix repairs this in two steps ([`audio/stemtone.py`](../src/nightmusic/audio/stemtone.py)).

Step 1 is the tone. The mix knows the written dynamic marks of the brass at each moment.
In relation to the loudest written mark of the brass, the brass group becomes less bright:

| Written mark of the brass | Change above 2 kHz |
| --- | --- |
| mf and softer | none |
| f | 8 dB softer |
| ff | 6 dB softer |
| fff | 4 dB softer |

Between two marks (for example in a crescendo), the change moves smoothly.

Step 2 is the level. Where the brass group is very loud (the main climax and the last chords), the mix moves its level down slowly, as an engineer moves a fader.
Only the part of the level above a threshold becomes smaller (ratio 2.5). The largest change is 3 dB. The other loud passages change by 1 dB or less.

The mix also has an equalization (`MASTER_EQ` in [`audio/musescore.py`](../src/nightmusic/audio/musescore.py)).
Its values come from a comparison of the loud passages of the mix with the loud passages of the five reference recordings.
The microphones of Muse Sounds are near the instruments: the mix had too much sound above 8 kHz and between 125 and 250 Hz, and not sufficient sound between 1 and 4 kHz.

| Filter | Change |
| --- | --- |
| Bell filter at 170 Hz | 2 dB softer |
| Bell filter at 2 kHz | 2 dB louder |
| High shelf filter at 6 kHz | 4 dB softer |

The owner of the project must make the decision about the result: a measurement does not show if the brass sounds correct.

## How the piano gets its sound

The owner of the project asked for a better piano sound: the piano is the soloist of the interlude.
A measurement compared two free pianos with one chord at each dynamic mark.

| Piano | Size | Level from ppp to fff | Change of the tone from mp to fff (the share of the sound above 2 kHz) |
| --- | --- | --- | --- |
| Muse Keys, grand piano | 190 MB | 28 dB. The marks f, ff, and fff are in a range of 2 dB. | 0.7 dB: a loud note has the tone of a medium note. |
| Salamander Grand Piano V3 (Yamaha C5, 16 dynamic levels for each sampled key, 48 kHz, 24 bit) | 1.2 GB | 22 dB in the samples; 33 dB with the level table of this project | 3.4 dB from mp to ff, and 20 dB from ppp to mp: a soft note is dark, a loud note is bright. |

The audio uses the Salamander Grand Piano. Its author is Alexander Holm. Its licence is Creative Commons Attribution 3.0.
The module [`audio/piano.py`](../src/nightmusic/audio/piano.py) plays the samples:

- The loudness of a note selects one of the 16 dynamic levels of its key.
- The pedal marks of the score hold the notes. With no pedal, the damper stops the string when the key goes up. The highest keys have no dampers.
- A staccato note is short. A new stroke on a key stops the old sound of that key.
- The noise of a key that goes up and the noise of the pedal are in the sound at a low level.
- Each stroke has a small difference of time (some milliseconds) and of loudness, as the strokes of a pianist have. The owner of the project heard the exact fast lines of the last chord as "rigid".

The piano has two roles, and each role has its place in the hall:

| Role | Where | Place | Level |
| --- | --- | --- | --- |
| The soloist | The interlude (from the mark W to the mark BB) | In the middle of the stage, at the front. The stereo picture is narrower than that of the samples. Some reverberation of the hall. | A chord at f is 6 dB louder than the same chord of the piano of Muse Keys: the balance of a concerto recording. |
| An instrument of the orchestra | All other sections | At its seat: on the left, at the back. The hall model of the project gives it the direct sound, the first reflections, and the reverberation for that seat. | The level of the piano of Muse Keys. |

A measurement showed why the two roles are necessary: with the level of the soloist, the piano in the heavy section of part 5 was as loud as the woodwinds, the brass, and the strings together. The owner of the project heard that the piano lines of the last chord did not blend.

If the samples are not on the computer, the piano of Muse Keys plays. The variable `NIGHTMUSIC_PIANO=muse` selects that piano for a comparison.
To get the samples: `git clone --depth 1 https://github.com/sfzinstruments/SalamanderGrandPiano.git .cache/samples/salamander`.

## How the master sets the loudness

In the render of MuseScore, the soft passages are about 50 dB below the loudest passages.
The reference recordings of real orchestras have a loudness range of 14 to 24 LU.
Thus the master moves the level slowly, as the engineer of a classical recording does it: the soft passages go up.

- Each passage of the music gets one level change. A passage is a part of the music that has one dynamic mark in effect for 6 seconds or more ([`compose/stats.py`](../src/nightmusic/compose/stats.py)).
- The level is constant in a passage. Thus it does not follow the decay of a note: a bell or a gong in a soft passage dies away as the instrument does it.
- Between two passages, the level changes in some seconds.
- The loudness range of the master is 20 LU. The integrated loudness is -20 LUFS, and the largest sample is below -1 dBFS.

## How the build server gets the audio

A build server cannot install Muse Sounds. Thus the audio master goes through a release of the repository.

1. Make the master on the computer that has Muse Sounds:

   ```bash
   uv run nightmusic audio --engine musescore
   ```

2. Put the master in the release `audio`:

   ```bash
   uv run nightmusic publish-audio
   ```

   The command also writes a checksum of the music (all notes and the tempo plan) into the release.
3. The build workflow runs `uv run nightmusic fetch-audio`.
   - If the checksum of the release is the same as the checksum of the music of the commit, the build uses the master of the release.
   - If not, the build makes the audio with the open sample libraries.

## How to install the MuseScore source (Fedora 45)

1. Install the official MuseScore Studio. The MuseScore of the Fedora repository cannot play Muse Sounds: the Muse sampler accepts only the official build.
   1. Download the AppImage file from <https://github.com/musescore/MuseScore/releases>.
   2. Make sure that its SHA-256 checksum is the same as in the file `checksums.sha256.txt` of the release.
   3. Extract it into the directory `~/.local/opt/musescore-studio`:

      ```bash
      cd ~/.local/opt/musescore-studio && chmod +x MuseScore-Studio-*.AppImage && ./MuseScore-Studio-*.AppImage --appimage-extract
      ```

2. Install the OpenSSL 3 libraries. Muse Sounds Manager needs them, and Fedora 45 has OpenSSL 4.

   ```bash
   sudo dnf install openssl3-libs
   ```

3. Download Muse Sounds Manager (the TAR package) from <https://musescore.org/en/download> and extract it.
4. Start `bin/muse-sounds-manager`.
5. Download these libraries: Muse Strings, Muse Woodwinds, Muse Brass, Muse Percussion, Muse Harp, Muse Keys (14 GB).
6. Render the audio:

   ```bash
   uv run nightmusic audio --engine musescore
   ```

The environment variable `NIGHTMUSIC_MUSESCORE` can give the path of a different MuseScore program.

## Limits of the MuseScore source

- A build server cannot make this audio.
- Muse Sounds have no sound for some instruments of the work. For these, the audio uses the open samples.
- Muse Sounds have no contrabass clarinet. The contrabassoon sound plays its notes.
- After a change of the music, the master of the release is not valid until a new render.
- The audio is not a recording of an orchestra.
