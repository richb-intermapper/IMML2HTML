ns2sq -tn -1h -q "(CLNPORT == 67)" -c+ -s ${address} -m $Min -M $Max

# http://docs.python.org/howto/argparse.html#id1

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cmd", help="The FlowTraq command to execute")
parser.add_argument("-tn", help="Time interval specified as #Y#M#w#d#h#s, where any of the units can be left out")
parser.add_argument("-q",  help="Quoted query string (query must be in \"..\")")
parser.add_argument("-m",  help="Min threshold",type=int)
parser.add_argument("-M",  help="Max threshold",type=int)
parser.add_argument("-c+", help="Display as CSV with header/trailer", action="store_true")
parser.add_argument("-s",  help="FlowTraq Server Address")
args = parser.parse_args()
print args
