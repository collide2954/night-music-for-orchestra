# Night Music for Orchestra: build commands.
# Each target calls a command of the project. Run "make help" for the list.

.PHONY: help study fetch measure report check test lint format score parts audio video all

help: ## Show the targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/'

study: ## Build the full style study (download, measure, check, report)
	uv run nightmusic-study all

fetch: ## Download the open data files into the cache
	uv run nightmusic-study fetch

measure: ## Measure the data and write research/measured
	uv run nightmusic-study measure

report: ## Write docs/style-study.md from the tables
	uv run nightmusic-study report

check: ## Check the tables for errors
	uv run nightmusic-study check

test: ## Run the tests
	uv run pytest -q

lint: ## Check the code style
	uv run ruff check .
	uv run ruff format --check .

format: ## Format the code
	uv run ruff format .

score: ## Build the conductor score (build/score/score.pdf)
	uv run nightmusic score

parts: ## Build the two conductor scores and all parts (build/set)
	uv run nightmusic parts

audio: ## Render the audio master (build/audio)
	uv run nightmusic audio

video: ## Render the score video (build/video); the audio must exist
	uv run nightmusic video

all: ## Build the score, the parts, the audio, and the video
	uv run nightmusic all
