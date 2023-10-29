import subprocess

# List of dependencies
dependencies = [
    'json',
    'concurrent.futures',
    'asyncio',
    'os',
    're',
    'shutil',
    'subprocess',
    'urllib',
    'argparse',
    'pandas',
    'collections',
    'transformers'
]

# Activate the virtual environment
subprocess.run(['.\env\Scripts\activate'], shell=True)

# Install the dependencies
for dependency in dependencies:
    subprocess.run(['pip', 'install', dependency])

# Deactivate the virtual environment
subprocess.run(['deactivate'], shell=True)

print("Dependencies installed successfully!")