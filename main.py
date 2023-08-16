from tqdm import tqdm
import sys
import requests
import os
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
import subprocess
from cloudmesh.common.systeminfo import os_is_windows

def runner(filename):

    # if not os_is_windows():
    #     sys.exit("Only Windows is supported :(")

    # if len(sys.argv) == 1:
    #     sys.exit("You need to specify the name of the nus3audio file.\n"
    #              "After moving it to this folder, use 'python main.py "
    #              "MYFILENAME.nus3audio'")
    #
    # if len(sys.argv) >= 2:
    #     filename = sys.argv[1]
    #
    # if filename == 'MYNUS3FILE.nus3audio':
    #     sys.exit('\nYou silly goose! You have to run the command '
    #              'with the name of your file at the end.\n'
    #              'If you are confused, just run the command "start ." in '
    #              'your Powershell.\nThe folder that comes up, is where you have '
    #              'to drop your nus3audio file.\nThen run the command but '
    #              'change "MYFILENAME.nus3audio" to the actual name of your '
    #              'file.\n\n')
    #
    # if not os.path.isfile(filename):
    #     sys.exit(f'\n{filename} was not found :(\nMaybe you are missing '
    #                 '.nus3audio at the end? Maybe you are in the wrong folder?\n'
    #                 'Type the command "start ." into your powershell and run it, '
    #                 'and move the file\ninto this folder that shows up.\n\n')

    def runcommand(command):
        try:
            r = Shell.run(command)
            return r
        except subprocess.CalledProcessError as e:
            print(e.output)
            return str(e.output)

    # try:
    #     r = Shell.run('rustc --version')
    # except subprocess.CalledProcessError:
    #     print('Rust not found. Installing rust...')

    try:
        Shell.run('choco --version')
    except subprocess.CalledProcessError:
        Console.error('Chocolatey not found. Please install chocolatey.\n'
                      'If you are confused, just install the install.bat file\n'
                      'provided by right clicking it and Run as Admin.')
        exit()

    # try:
    #     r = Shell.run('ffmpeg -h')
    # except subprocess.CalledProcessError:
    #     print('ffmpeg not found. Installing ffmpeg...')
    #     r2 = Shell.run('choco install ffmpeg -y')

    if not os.path.isdir('nus3express'):
        Shell.mkdir('nus3express')

    if not os.path.isfile('nus3audio.exe'):
        print('Downloading nus3audio...')
        url = "https://github.com/jam1garner/nus3audio-rs/releases/download/v1.1.7/nus3audio.exe"
        file_name = "nus3express/nus3audio.exe"

        response = requests.get(url)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name} successfully.")
        else:
            print("Failed to download the file.")

    if not os.path.isdir('nus3express/StreamTool'):
        print('Installing streamtool...')
        try:
            Shell.run('cd nus3express && git clone https://github.com/ActualMandM/StreamTool.git')
        except Exception as e:
            print(str(e.output))
        try:
            Shell.run(fr'cd nus3express/StreamTool && .\#SETUP.bat')
        except Exception as e:
            print(str(e.output))

    for folder_path in ['nus3express/mp3s', 'nus3express/idsps', 'nus3express/wavs']:
        if os.path.exists(folder_path):
            print(f"Deleting {folder_path}...")
            Shell.rmdir(folder_path)
        else:
            print(f"{folder_path} does not exist.")
        Shell.mkdir(folder_path)


    r = runcommand(rf'cd nus3express && nus3audio.exe -e idsps -- "{filename}"')

    if 'is not recognized as an internal' in r:
        Shell.rm('nus3express/nus3audio.exe')
        Console.error('nus3audio-rs was not installed properly by nus3express.\n'
                      'Perhaps this was due to an early stoppage.\n'
                      'Please rerun the program which will reinstall nus3audio-rs.\n')

    files = os.listdir('nus3express/idsps')

    print('Converting idsp to wav...')
    # Loop through the files and print their names
    for file in tqdm(files):
        if '.idsp' in file:
            inner = fr'.\nus3express\idsps\{file}'
            outer = fr'.\nus3express\wavs\{file.split(".idsp")[0]}.wav'
            inner = Shell.map_filename(inner).path
            outer = Shell.map_filename(outer).path
            # print(rf'.\StreamTool\vgaudio.exe {inner} {outer}')
            r = runcommand(rf'.\nus3express\StreamTool\vgaudio.exe "{inner}" "{outer}"')

    print('Converting to mp3s...')
    # Path to the folder containing the input files
    input_folder = rf"nus3express\wavs"

    output_folder = rf"nus3express\mp3s"

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
            Shell.run(f'ffmpeg -i "{input_file}" "{output_file}"')
            # subprocess.run(cmd)

    os.system(r'start nus3express\mp3s')
    print('Done, look in mp3s folder.')


