from tqdm import tqdm
import sys
import os
from cloudmesh.common.Shell import Shell
import subprocess
from cloudmesh.common.systeminfo import os_is_windows

if not os_is_windows():
    sys.exit("Only Windows is supported :(")

if len(sys.argv) == 1:
    sys.exit("You need to specify the name of the nus3audio file.\n"
             "After moving it to this folder, use 'python main.py "
             "MYFILENAME.nus3audio'")

if len(sys.argv) >= 2:
    filename = sys.argv[1]

def runcommand(command):
    try:
        r = Shell.run(command)
        return r
    except subprocess.CalledProcessError as e:
        print(e.output)

try:
    r = Shell.run('rustc --version')
except subprocess.CalledProcessError:
    print('Rust not found. Installing rust...')
    r2 = Shell.run('choco install rust -y')
    if 'not found' in r2:
        print('Chocolatey not found. Please install chocolatey.')
        exit()
    else:
        print('Rust installed.')

try:
    r = Shell.run('ffmpeg -h')
except subprocess.CalledProcessError:
    print('ffmpeg not found. Installing ffmpeg...')
    r2 = Shell.run('choco install ffmpeg -y')

if not os.path.isdir('nus3audio-rs'):
    print('Installing nus3audio-rs...')
    try:
        Shell.run('git clone https://github.com/jam1garner/nus3audio-rs.git && cd nus3audio-rs && cargo build --release')
    except Exception as e:
        print(str(e.output))

if not os.path.isdir('StreamTool'):
    print('Installing streamtool...')
    try:
        Shell.run('git clone https://github.com/ActualMandM/StreamTool.git')
    except Exception as e:
        print(str(e.output))
    try:
        Shell.run(fr'cd StreamTool && .\#SETUP.bat')
    except Exception as e:
        print(str(e.output))

r = runcommand(rf'nus3audio-rs\target\release\nus3audio.exe -e idsps -- {filename}')
if not os.path.isdir('wavs'):
    Shell.mkdir('wavs')

files = os.listdir('idsps')

print('Converting idsp to wav...')
# Loop through the files and print their names
for file in tqdm(files):
    if '.idsp' in file:
        inner = fr'.\idsps\{file}'
        outer = fr'.\wavs\{file.split(".idsp")[0]}.wav'
        inner = Shell.map_filename(inner).path
        outer = Shell.map_filename(outer).path
        # print(rf'.\StreamTool\vgaudio.exe {inner} {outer}')
        r = runcommand(rf'.\StreamTool\vgaudio.exe {inner} {outer}')

print('Converting to mp3s...')
# Path to the folder containing the input files
input_folder = "wavs/"

# Create the "mp3s" folder if it doesn't exist
output_folder = "mp3s/"
os.makedirs(output_folder, exist_ok=True)

# Iterate through each file in the input folder
for filename in os.listdir(input_folder):
    input_file = os.path.join(input_folder, filename)

    # Check if the item is a file (not a subdirectory) and ends with a specific extension (e.g., ".wav")
    if os.path.isfile(input_file) and input_file.lower().endswith(".wav"):
        # Create the output filename with .mp3 extension
        output_filename = os.path.splitext(filename)[0] + ".mp3"
        output_file = os.path.join(output_folder, output_filename)

        # Run FFmpeg as a system command to convert the file
        # The command is: ffmpeg -i input_file.mp3 output_file.wav
        # cmd = ["ffmpeg", "-i", input_file, output_file]
        Shell.run(f'ffmpeg -i {input_file} {output_file}')
        # subprocess.run(cmd)

print('Done, look in mp3s folder.')


