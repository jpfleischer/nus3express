import os
import subprocess
import sys

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        return str(e.output)

def install_vgmstream():
    run_command("wget https://github.com/vgmstream/vgmstream/releases/download/r1879/vgmstream-linux.zip")
    run_command("unzip vgmstream-linux.zip")
    run_command("rm vgmstream-linux.zip")
    run_command("mv vgmstream-cli vgmstream")
    run_command("chmod +x vgmstream")
    run_command("sudo mv vgmstream /usr/bin/")
    run_command("sudo apt-get -y update")
    run_command("sudo apt-get install gcc g++ make build-essential git cmake")
    run_command("sudo apt-get install libmpg123-dev libvorbis-dev libspeex-dev")
    run_command("sudo apt-get install libavformat-dev libavcodec-dev libavutil-dev libswresample-dev")
    run_command("sudo apt-get install yasm libopus-dev")
    run_command("sudo apt-get install -y libao-dev audacious-dev")

def check_vgmstream():
    if not os.path.isfile("/usr/bin/vgmstream"):
        install_vgmstream()

def convert_idsp_to_wav(input_file, output_file):
    if os.path.isfile(input_file) and input_file.lower().endswith(".idsp"):
        run_command(f'vgmstream -o "{output_file}" "{input_file}"')
        print('The file `' + sys.argv[1] + '` has been converted to WAV format.')
    else:
        exit('The file `' + sys.argv[1] + '` has not been found or is not in the IDSP format')

def runner(input_file):
    output_file = os.path.splitext(input_file)[0] + ".wav"
    convert_idsp_to_wav(input_file, output_file)

if __name__ == '__main__':
    # Have the arguments been provided?
    if len(sys.argv) != 2:
        print('Usage: python3 linux.py <input_file>')
        sys.exit(0)
    runner(sys.argv[1])
