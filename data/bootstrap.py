import sys
import os

# Add the directory containing awkde to sys.path
sys.path.append('/usr/src/app')

# Now run your main script
if __name__ == '__main__':
    os.system("pipenv run python ./script.py")
