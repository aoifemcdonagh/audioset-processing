# Set of scripts for downloading raw audio files (WAV) from AudioSet.

## Quick start:

To download raw audio for class "bird" 
```	
python procas.py download -c "bird"
```
Downloads raw audio to a folder `./output` in current directory.

Uses CSV files found in `./data`. Therefore execute `procas.py` in its' own directory.
