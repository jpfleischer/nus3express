from tqdm import tqdm
import requests
import os
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
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
        except RuntimeError as e:
            Console.error(e)
            return str(e)

    # try:
    #     r = Shell.run('rustc --version')
    # except subprocess.CalledProcessError:
    #     print('Rust not found. Installing rust...')
    
    # check for git
    git = ffmpeg = False
    try:
        Shell.run('git --version')
        git = True
    except RuntimeError:
        pass

    try:
        Shell.run('ffmpeg -version')
        ffmpeg = True
    except RuntimeError:
        pass

    if not git or not ffmpeg:
        try:
            Shell.run('choco --version')
        except RuntimeError:
            Console.error('Oh no! chocolatey not found. installing...')
            Shell.install_chocolatey()

            Console.info('Installing git and/or ffmpeg...')
            if not git:
                try:
                    Shell.run('choco install git -y')
                except RuntimeError:
                    pass
            if not ffmpeg:
                try:
                    Shell.run('choco install ffmpeg -y')
                except RuntimeError:
                    pass
    # try:
    #     r = Shell.run('ffmpeg -h')
    # except RuntimeError:
    #     print('ffmpeg not found. Installing ffmpeg...')
    #     r2 = Shell.run('choco install ffmpeg -y')

    if not os.path.isdir('nus3-program'):
        Shell.mkdir('nus3-program')

    if not os.path.isfile('nus3audio.exe'):
        Console.info('Downloading nus3audio...')
        url = "https://github.com/jam1garner/nus3audio-rs/releases/download/v1.1.7/nus3audio.exe"
        file_name = "nus3-program/nus3audio.exe"

        response = requests.get(url)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            Console.ok(f"Downloaded {file_name} successfully.")
        else:
            Console.error("Failed to download the file.")

    vg_name = r".\nus3-program\StreamTool\vgmstream.exe"
    
    if not os.path.isfile(vg_name):
        Console.info('Installing streamtool...')
        runcommand('cd nus3-program && git clone https://github.com/ActualMandM/StreamTool.git')
        runcommand(fr'cd nus3-program/StreamTool && .\#SETUP.bat')

    if not os.path.isfile(vg_name):
        Console.warning('Your setup.bat failed')
        Console.warning(r"...F@$% it, we're doing it live!")
        Console.warning('Downloading vgmstream...')
        url = "https://github.com/vgmstream/vgmstream-releases/releases/download/nightly/vgmstream-win64.zip"
        # download file
        file_name = "nus3-program/vgmstream.zip"
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            Console.ok(f"Downloaded {file_name} successfully.")
        else:
            Console.error("Failed to download the file.")
        # unzip file
        Console.info('Unzipping vgmstream...')
        Shell.unzip(file_name, r"nus3-program\vgmstream-win64")
        vg_name = r'nus3-program\vgmstream-win64\vgmstream-cli.exe'
        
    for folder_path in ['nus3-program/mp3s', 'nus3-program/idsps', 'nus3-program/wavs']:
        if os.path.exists(folder_path):
            Console.info(f"Deleting {folder_path} probably from a previous run...")
            Shell.rmdir(folder_path)
        else:
            Console.ok(f"{folder_path} does not exist, so proceeding as normal.")
        Shell.mkdir(folder_path)


    r = runcommand(rf'cd nus3-program && nus3audio.exe -e idsps -- "{filename}"')

    if 'is not recognized as an internal' in r:
        Shell.rm('nus3-program/nus3audio.exe')
        Console.error('nus3audio-rs was not installed properly by nus3express.\n'
                      'Perhaps this was due to an early stoppage.\n'
                      'Please rerun the program which will reinstall nus3audio-rs.\n')

    files = os.listdir('nus3-program/idsps')

    Console.info('Converting idsp to wav...')
    # Loop through the files and print their names
    for file in tqdm(files):
        if '.idsp' in file:
            inner = fr'.\nus3-program\idsps\{file}'
            outer = fr'.\nus3-program\wavs\{file.split(".idsp")[0]}.wav'
            inner = Shell.map_filename(inner).path
            outer = Shell.map_filename(outer).path
            # print(rf'.\StreamTool\vgaudio.exe {inner} {outer}')
            vga = rf'.\nus3-program\StreamTool\vgaudio.exe'
            if not os.path.isfile(vga):
                Shell.warning("WE'RE DOIN' IT LIVE, F(*% IT!")
                Shell.download("https://github.com/Thealexbarney/VGAudio/releases/download/v2.2.1/VGAudioCli.exe",
                               vga)
                
            
            r = runcommand(rf'{vga} "{inner}" "{outer}"')
        elif '.lopus' in file:
            inner = fr'.\nus3-program\idsps\{file}'
            outer = fr'.\nus3-program\wavs\{file.split(".lopus")[0]}.wav'
            inner = Shell.map_filename(inner).path
            outer = Shell.map_filename(outer).path
            # print(rf'.\StreamTool\vgaudio.exe {inner} {outer}')
            r = runcommand(rf'{vg_name} "{inner}" -o "{outer}"')

    Console.info('Converting to mp3s...')
    # Path to the folder containing the input files
    input_folder = rf"nus3-program\wavs"

    output_folder = rf"nus3-program\mp3s"

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
            runcommand(f'ffmpeg -i "{input_file}" "{output_file}"')
            # subprocess.run(cmd)

    os.system(r'start nus3-program\mp3s')
    Console.ok('Done, look in mp3s folder.')


