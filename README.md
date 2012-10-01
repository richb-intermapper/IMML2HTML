ReadMe file for InterMapper Probe Reference

[InterMapper](http://intermapper.com) has a set of built in *probes* (software plug-ins) that control how a device can be tested.

This repository lists the built-in probes, and creates an HTML documentation page that displays the current set of probes. This file, ProbeReference.html can be diff'd to see what probes have changed from version to version.

To update the ProbeReference.html:

- Expand the BuiltinProbes.zip file (from InterMapper Settings/Probes) for a new version of the InterMapper server. Copy these files into the "Builtin Probes" directory of this repository

- Run the updatesprobes.sh script ("sh updateprobes.sh")
