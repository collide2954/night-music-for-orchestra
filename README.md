# Night Music for Orchestra

Night Music for Orchestra is a new work for large orchestra.
Code makes all parts of the work: the score, the parts, the audio, and the score video.

The work takes its style from three sources:

- Arnold Schoenberg, and primarily *Verklärte Nacht*.
- Béla Bartók, and primarily his "night music" style.
- John Corigliano.

The work also uses musical material from different regions of the world.

## Project status

The first edition of the style study is complete. The subsequent stage is the design of the work.

| Stage | Result | Status |
| --- | --- | --- |
| 1. Style study | Tables of measured and sourced style parameters | First edition complete |
| 2. Design | Form, orchestra, and material of the work | Subsequent stage |
| 3. Composition | The music, written as code | Not started |
| 4. Engraving | Conductor score and parts | Not started |
| 5. Audio | Realistic audio from free sample libraries | Not started |
| 6. Video | Score video with part tracking | Not started |

## Style study

The style study is in the [`research`](research/README.md) directory.
The full report is [`docs/style-study.md`](docs/style-study.md).

The study measured the complete *Verklärte Nacht* (418 bars) and two sets of piano works by Bartók.
It also contains sourced tables for form, harmony, rhythm, orchestration, and orchestra sizes.
The style profiles in the report give the target ranges for the new work.

## Design

The directory [`design`](design) contains the decisions and the plan of the work.

| File | Contents |
| --- | --- |
| [`brief.toml`](design/brief.toml) | The decisions of the owner of the project |
| [`form.toml`](design/form.toml) | The five parts, the positions of the main events, and the targets |
| [`pitch.toml`](design/pitch.toml) | The motto, its four states, the key centres, and the processes |
| [`orchestra.toml`](design/orchestra.toml) | The players, the instruments, and their ranges |

## Requirements

- [uv](https://docs.astral.sh/uv/) 0.5 or later
- GNU Make

## How to build the style study

1. Install the Python environment:

   ```bash
   uv sync
   ```

2. Build the study:

   ```bash
   make study
   ```

The `make study` command downloads the open data files, measures them, and writes the report.

## Licence

- The code is under the MIT License. See [`LICENSE`](LICENSE).
- The music, the score, the parts, the audio, the video, and the documents are under the
  Creative Commons Attribution 4.0 International licence (CC BY 4.0).
  See [`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0).
- The style study measures open data from other authors. These data have their own licences.
  See [`research/README.md`](research/README.md).
