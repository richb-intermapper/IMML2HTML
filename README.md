# ReadMe file for InterMapper Probe Reference

[InterMapper](http://intermapper.com) has a set of built in *probes* (software plug-ins) that control how a device can be tested.

This repository contains programs and scripts that create an HTML document that displays the <definition> section of each of the builtin probes to provide a reference to that probe's use. This file, ProbeReference.html, can be diff'd to see what probes have changed from version to version. The repository also contains the current set of built-in probes.

ProvisionalProbeReference.html lists each of the probes according to their Category, in the order of their apperance in the Set Probe window. Its time stamp shows when the file was created.

To update the ProbeReference.html:

- Expand the BuiltinProbes.zip file (from InterMapper Settings/Probes) for a new version of the InterMapper server. Copy these files into the "Builtin Probes" directory of this repository

- Run the updatesprobes.sh script ("sh updateprobes.sh") with no arguments to create the new ProbeReference.html based on the built-in probes included in this repository.

- The updateprobes.sh script takes an argument of a single file or a directory containing files. 

## Requirements

- Unix-like shell command with sed, sort, etc.

- Reasonably modern Python (tested with Python 2.7.1)
