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
