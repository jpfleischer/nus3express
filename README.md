# 🍫 nus3express

This tool converts files in nus3audio to mp3s.

## But How Do I Use it?!?!?!?

You need: 
* chocolatey

To know whether you have chocolatey, run Powershell as administrator.

Type the following and press Enter.

```bash
choco --version
```

If it says `The term 'choco' is not recognized as the name of a cmdlet...`
then you don't have it. Follow these instructions: https://chocolatey.org/install

Now that you have chocolatey, close and reopen Powershell as administrator,
and install Python and Git:

```bash
choco install python git -y
```

Then, after closing and reopening Powershell as admin, download nus3express.
By the way, it is usually a good idea to copy and paste each line individually.
Copying all the commands at once may lead to unknown behavior.

```bash
# maybe go to your downloads folder?
cd ~/Downloads
git clone https://github.com/jpfleischer/nus3express.git
cd nus3express 
```

Finally, run these commands:

```bash
pip install -r requirements.txt
python nus3express.py
```

## I want to update my nus3express!

Assuming you downloaded it to your Downloads folder, as above, do the
following in **Powershell as administrator**:

```bash
cd ~/Downloads
Remove-Item -Recurse -Force nus3express
git clone https://github.com/jpfleischer/nus3express.git
cd nus3express 
pip install -r requirements.txt
python nus3express.py
```