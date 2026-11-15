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
2. MuseScore changes the MusicXML file into its own format.
3. The code changes two items in that file ([`audio/musescore.py`](../src/nightmusic/audio/musescore.py)):
   - The words of the playing techniques (for example "sul pont.") become marks that MuseScore plays.
   - The master control of the mixer goes down by 18 dB. Without this, a loud passage of the full orchestra has distortion.
4. MuseScore renders the file to a WAV file (32-bit floating point).
5. The sampler of this project renders the instruments that Muse Sounds do not have: cimbalom, accordion, ocarina, mandolin, and frame drum.
   A measurement with the timpani gives the two sources the same level.
6. The master step sets the loudness. It does not change the tone balance of this mix.

MuseScore renders five groups of the orchestra as five files (stems): woodwinds, brass, percussion, keyboards with harp, and strings.

- Three MuseScore programs run at the same time. Thus the render is faster.
- A stem stays from the last render if its music did not change.
- The table `STEM_GAIN_DB` in the code gives the level of each stem. A change of the balance between the groups needs no new render.

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
