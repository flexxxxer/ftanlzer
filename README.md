# Ftanlzer
Frametime analyzer tool 

# This analyzer tool allows you:
- generate frame timing graph data
- generate probability density graph data
- generate probability distribution graph data

## Getting Started
### Prerequisites
This project based on [ftparser](https://github.com/FlexxxerAlex/ftparser) project, hence all prerequisites are equivalent (ftparser prerequisites: [link](https://github.com/FlexxxerAlex/ftparser#prerequisites))

### Installing
For installation you just need to download the [ftanlzer.py](https://github.com/FlexxxerAlex/ftanlzer/blob/master/ftanlzer.py) file (which is located in the root directory of the repository) and do not forget the location of the downloaded file :grinning:

## Usage
##### Script execution
In order to run the [ftanlzer.py](https://github.com/FlexxxerAlex/ftanlzer/blob/master/ftanlzer.py) script, you need to write the following to console/terminal:

`$> python ftanlzer.py [args]`, where `[args]` - script arguments

**What arguments can be passed?**
Show help info and supported arguments list:

`$> python ftanlzer.py --help` or `python ftanlzer.py -h`

#### FAQ
**How can I get frame timing graph data?**
For processing, you need to have a frame time log file and know what kind of program it created, and specify this information as parameters `-f` and `-p`. For get frame timing graph data you need to specify `--ftg` parameter, for example frameview logs:

`$> python ftanlzer.py -f frameviewlog.csv -p frameview --ftg`, where `frameviewlog.csv` - FrameView log file.

**How can I get probability density graph data?**
You need to specify `--pdensg` parameter:

`$> python ftanlzer.py -f frapslog.csv -p fraps --pdensg`

**How can I write the processing results to a file?**
You should append `-o filename` after the main part with `-f [file] -p [program]`, e.g. for FrameView:

`$> python ftanlzer.py -f fvlog.csv -p frameview -o results.txt --pdensg`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
