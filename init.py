# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:28:02 2023

@author: Sebastian
"""

import uuid

with open("uuid.txt", "w") as output:
    id = str(uuid.uuid4())
    output.write(id)
