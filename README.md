# Night Music for Orchestra

Night Music for Orchestra is a new work for large orchestra.
Code makes all parts of the work: the score, the parts, the audio, and the score video.

The work takes its style from three sources:

- Arnold Schoenberg, and primarily *Verklärte Nacht*.
- Béla Bartók, and primarily his "night music" style.
- John Corigliano.

The work also uses musical material from different regions of the world.

## Project status

The project is in its first stage. This stage is the style study.

| Stage | Result | Status |
| --- | --- | --- |
| 1. Style study | Tables of measured and sourced style parameters | In work |
| 2. Design | Form, orchestra, and material of the work | Not started |
| 3. Composition | The music, written as code | Not started |
| 4. Engraving | Conductor score and parts | Not started |
| 5. Audio | Realistic audio from free sample libraries | Not started |
| 6. Video | Score video with part tracking | Not started |

## Style study

The style study is in the [`research`](research/README.md) directory.
The full report is [`docs/style-study.md`](docs/style-study.md).

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
