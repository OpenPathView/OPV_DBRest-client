#!/bin/bash

pytest --cov-report html --cov=opv_api_client --cov-config .conf_coverage.conf .
