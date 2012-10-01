<!-- 
	LPR (com.dartware.tcp.lpr)
	Copyright © 2001 Dartware, LLC. All rights reserved.
-->

<header>
	type			= 	"tcp-script"
	package			= 	"com.dartware"
	probe_name		=	"tcp.lpr"
	human_name		=	"LPR"
	version			= 	"1.7"
	address_type	= 	"IP"
	port_number		=	"515"
	display_name	=	"Servers-Standard/LPR"
	
</header>

<description>

\GB\Line Printer Daemon Protocol\P\

The print server protocol used to print over a TCP/IP network, as defined in \U2=http://www.ietf.org/rfc/rfc1179.txt\RFC 1179\P0\. The default TCP port number for LPR connections is port 515.

</description>

<parameters>

"Queue Name"	= 	""

</parameters>

<script>

CONN #60 (connect timeout in secs)
WAIT #30 @IDLE (idle timeout in secs)
SEND "\x03${Queue Name}\n"
EXPT m".+" else goto @DISCONNECT
DONE OKAY

@IDLE:
DONE DOWN "[LPR] No data for ${_IDLETIMEOUT} seconds.  Was expecting \"${_STRINGTOMATCH}\". [Line ${_IDLELINE}]"

@DISCONNECT:
DONE DOWN "[LPR] Connection disconnected while expecting \"${_STRINGTOMATCH}\"."

</script>
