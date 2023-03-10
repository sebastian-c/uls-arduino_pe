# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:28:02 2023

@author: Sebastian
"""
import random

with open("uuid.txt", "w") as output:
    id = random.randint(11, 100000)
    output.write(str(id))
