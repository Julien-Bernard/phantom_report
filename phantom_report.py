#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'julien.bernard <julien.bernard@gmail.com>'
# __description__ = 'Python script to create a timeline PDF report from Phantom.us'

"""
This scripts creates a report for a specific Phantom container
"""

import logging
import json
import requests
from weasyprint import HTML,CSS

