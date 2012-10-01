# ReadMe file for InterMapper Probe Reference

[InterMapper](http://intermapper.com) has a set of built in *probes* (software plug-ins) that control how a device can be tested.

This repository lists the built-in probes, and creates an HTML documentation page that displays the current set of probes. This file, ProbeReference.html, can be diff'd to see what probes have changed from version to version.

ProbeReference lists each of the probes according to their Category, in the order of their apperance in the Set Probe window. Its time stamp shows when the file was created.

To update the ProbeReference.html:

- Expand the BuiltinProbes.zip file (from InterMapper Settings/Probes) for a new version of the InterMapper server. Copy these files into the "Builtin Probes" directory of this repository

- Run the updatesprobes.sh script ("sh updateprobes.sh") to create the new ProbeReference.html

## Requirements

- Unix-like shell command with sed, sort, etc.

- Reasonably modern Python (tested with Python 2.7.1)
