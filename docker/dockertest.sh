#!/bin/bash
coverage run -m pytest
coverage report -i --fail-under=90