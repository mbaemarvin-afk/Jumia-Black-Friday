import os
import time
import random

offset = random.randint(10, 120)
time.sleep(offset)

while True:
    os.system("python run_once.py")
    time.sleep(3600)
