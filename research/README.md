# Style study

This directory contains the style study for *Night Music for Orchestra*.
The study gives the style of the reference composers as numbers and tables.
The composition code will use these tables as its rules.

The full report is [`docs/style-study.md`](../docs/style-study.md).

## Contents

| Path | Contents | How it is made |
| --- | --- | --- |
| [`tables/`](tables) | Sourced tables: works, orchestra sizes, form, tempo, harmony, scales, themes, rhythm, texture, world sources, variation, instrument techniques, notes that are not in the chord, more devices | Written by the study team from the sources |
| [`tables/profiles.csv`](tables/profiles.csv) | Style profiles: target ranges for the new work | Written by the study team from the measured and sourced values |
| [`measured/`](measured) | Measured tables | Made by the study code |
| [`measured/work_*.csv`](measured) | Measured tables of the new work: repetition, harmony, use of the instruments | Made by the command `uv run nightmusic docs` |
| [`sources.csv`](sources.csv) | List of all sources | Written by the study team |
| [`corpus.sha256`](corpus.sha256) | Checksums of the open data files | Made with `sha256sum` |
| [`text/`](text) | Text sections of the report | Written by the study team |

## Evidence codes

Each row of a sourced table has an evidence code.

| Code | Meaning |
| --- | --- |
| M | The study code measured the value. |
| R | The study team read the source. The row gives the key of the source. |
| K | The row is standard reference knowledge. The study team did not read a source for the row. |

## Open data

The study measures three sets of open data.
The repository does not contain these files.
The study code downloads them into the directory `.cache/corpus`.

| Data | Author | Licence |
| --- | --- | --- |
| Schoenberg, *Verklärte Nacht*, piano arrangement, text source | Peter Billam | CC BY 4.0 |
| Bartók, *Out of Doors*, MIDI capture of a piano performance | Michael Bednarek | CC0 1.0 |
| Bartók, *Fourteen Bagatelles* op. 6, note lists | Digital and Cognitive Musicology Lab (DCML) | CC BY-NC-SA 4.0 |
| Five recordings of full orchestras (for loudness and tone balance) | Musopen | Public domain |

The study code verifies the checksum of each file after the download.
If a file changed at its source, the code stops and shows a message.

## How to build the study

1. Install the Python environment:

   ```bash
   uv sync
   ```

2. Build the study:

   ```bash
   make study
   ```

The command does these steps:

1. It downloads the open data files (`make fetch`).
2. It measures the data and writes the files in `measured/` (`make measure`).
3. It checks the sourced tables for errors (`make check`).
4. It writes the report `docs/style-study.md` (`make report`).

## How to add a row to a sourced table

1. Read the source.
2. If the source is new, add it to `sources.csv` with a new key.
3. Add the row to the applicable file in `tables/`.
4. Put the key of the source in the column `source`.
5. Put the evidence code in the column `evidence`.
6. Run `make check`.
7. Run `make report`.

## Rules for the tables

- Each value must have a source or a measurement.
- A row with the code K must cite the key `reference`.
- A row with the code R must not cite the key `reference`.
- Do not copy music notation or audio from sources that have a copyright.
  Facts, numbers, and short descriptions are permitted.
