
import os
import io
import sys
import math
import argparse
import subprocess
import configparser

from json import loads

def round_of_rating(number):
    return round(number * 2) / 2

def get_supported_programs():
    ftparser = subprocess.run([sys.executable, sys.path[0] + '/ftparser/ftparser.py', '--spn'], stdout=subprocess.PIPE)
    return ftparser.stdout.decode('ascii')

def get_frametimes(logfile, programname):
    ftparser = subprocess.run([sys.executable, sys.path[0] + '/ftparser/ftparser.py', '-f', logfile, '-p', programname, '--allframes'], stdout=subprocess.PIPE)
    content = ftparser.stdout.decode('ascii')
    parser = configparser.ConfigParser()
    parser.read_file(io.StringIO(content))
    return parser['statistics']['all frames times']

# error output function
def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

argParser = argparse.ArgumentParser(description='frame analyzer tool')

# script arguments
argParser.add_argument('-f', '--logfile', dest='logfile', help='frame time recording program output file', default=None)
argParser.add_argument('-p', '--programname', dest='pname', help='frame time recording program name', choices=get_supported_programs(), default=None)
argParser.add_argument('-o', '--output', dest='outputfilename', help='output filename. if not specified then the output is in stdout', nargs='?', default=None)
argParser.add_argument('--version', dest='showversion', help='show version', action='store_true', default=False)
argParser.add_argument('--spn', dest='supportedprograms', help='supported recording programs names', action='store_true', default=False)
argParser.add_argument('--ftg', dest='isframetiminggraph', help='generate frame timing graph data', action='store_true', default=False)
argParser.add_argument('--pdensg', dest='isprobabilitydensitygraph', help='generate probability density graph data', action='store_true', default=False)
argParser.add_argument('--pdistg', dest='isprobabilitydistributiongraph', help='generate probability distribution graph data', action='store_true', default=False)

argslist = argParser.parse_args()

# if user want to get version
if argslist.showversion is True:
    print("{name} 0.1".format(name=sys.argv[0]))
    sys.exit()

# if user want to get supported recording programs names
if argslist.supportedprograms is True:
    print(get_supported_programs(), end='')
    sys.exit()

# if the arguments are not specified together
if argslist.logfile is None or argslist.pname is None:
    errprint("Argument error: params 'logfile' and 'programname' must be specified together")
    sys.exit()

# if file does not exist
if not os.path.isfile(argslist.logfile):
    errprint("Argument error: {filepath} does not exist. ".format(filepath=os.path.abspath(argslist.logfile)), end='')

    # if output file was specified, then print, else nothing
    if argslist.outputfilename is not None:
        errprint("File '{outputfile}' does not created".format(outputfile=argslist.outputfilename))
    else:
        errprint()

    sys.exit()

# if no one graph data not specified
if not argslist.isframetiminggraph and not argslist.isprobabilitydensitygraph and not argslist.isprobabilitydistributiongraph:
    errprint("Argument error: no one graph data specified")
    sys.exit()

frametimes = loads(get_frametimes(argslist.logfile, argslist.pname))
graphs_data = configparser.ConfigParser()

# if user want to get frame timing graph
if argslist.isframetiminggraph:
    graph_data = list()
    time_from_start = 0.0

    for frametime in frametimes[1:]:
        time_from_start += frametime
        graph_data.append((time_from_start, frametime))

    graphs_data['frame timing graph'] = dict(data=graph_data)

# if user want to get probability density graph
if argslist.isprobabilitydensitygraph:
    values = {}

    for frametime in frametimes[(1 if frametimes[0] == 0 else 0):]:
        frametime_rating = round_of_rating(frametime)

        if frametime_rating in values:
            values[frametime_rating] += frametime_rating
        else:
            values[frametime_rating] = frametime_rating

    graph_data = list((0 if k == 0 else 1000.0 / k, v) for k, v in sorted(values.items(), key=lambda kv: kv[0], reverse=True))
    min = min(graph_data)[0]

    graph_data = [(min - 1.0, 0)] + graph_data
    graphs_data['probability density graph'] = dict(data=graph_data)

# if user want to get probability distribution graph
if argslist.isprobabilitydistributiongraph:
    graph_data = list()
    time_from_start = 0.0
    total_test_time = sum(frametimes)

    for frametime in sorted(frametimes):
        if frametime == 0:
            continue

        time_from_start + frametime
        graph_data.append((1000.0 / frametime, time_from_start / total_test_time / 10.0))

    graphs_data['probability distribution graph'] = dict(data=graph_data)

# write to file or stdout
if argslist.outputfilename is not None:
    with open(argslist.outputfilename, 'w') as output_file:
        graphs_data.write(output_file)
else:
    graphs_data.write(sys.stdout)
