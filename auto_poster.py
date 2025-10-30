import os
import random
import time
import subprocess

# Add a small random delay (to make posts look natural)
offset = random.randint(10, 120)
print(f"⏱ Waiting {offset} seconds before posting...")
time.sleep(offset)

# Run your deal posting script once
print("🚀 Running deal posting script...")
exit_code = subprocess.call(["python", "run_once.py"])

if exit_code == 0:
    print("✅ Deal posted successfully!")
else:
    print("❌ Error running run_once.py")

print("⏰ Next run will be triggered automatically by GitHub Actions.")
