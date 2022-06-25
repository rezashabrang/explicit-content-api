#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov explicit_content_api tests/ >>.logs/coverage.txt
