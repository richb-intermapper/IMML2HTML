<!-- 
	FTP (Login) (com.dartware.tcp.ftp.login)
	Copyright � 2000 Dartware, LLC. All rights reserved.
-->

<header>
	type			= 	"tcp-script"
	package			= 	"com.dartware"
	probe_name		=	"tcp.ftp.login"
	human_name		=	"FTP (Login)"
	version			= 	"1.8"
	address_type	= 	"IP"
	port_number		=	"21"
	
	old_protocol	= 	"8"			# Backward compat. with old numbering scheme.
	old_script		= 	"8002"

	display_name	=	"Servers-Standard/FTP/FTP (Login)"
	url_hint		=	"ftp://${ADDRESS}:${PORT}"
</header>

<description>

\GB\File Transfer Protocol (Login)\P\

The standard protocol for transferring files on TCP/IP internets, as defined in \U2=http://www.ietf.org/rfc/rfc0959.txt\RFC 959\P0\.  The default TCP port number for FTP control connections is port 21.

This TCP probe connects to the FTP server's control port (21), logs in using the specified UserID and Password, and then issues a NOOP command.  The probe concludes by issuing the QUIT command.

\i\User ID\p\ is the account name used to login to the FTP server.

\i\Password\p\ is the account password used to verify the User ID's identity.

Note:  If this probe queries the FTP server often at regular intervals, it will appear in your FTP server's log files as a succession of "Login"  and "Logout" log lines.

</description>

<parameters>

"User ID"		=	"anonymous"
"Password*"		=	""

</parameters>

<script>

CONN #60 (connect timeout in secs)
WAIT #30 @IDLE (idle timeout in secs)
MTCH "220" else goto @UNEXPECTED_GREETING
EXPT "220 " else goto @DISCONNECT
SEND "USER ${User ID}\r\n"
MTCH "331" else goto @BAD_USER_RESPONSE
EXPT "331 " else goto @DISCONNECT
SEND "PASS ${Password*}\r\n"
MTCH "230" else goto @BAD_PASS_RESPONSE
EXPT "230 " else goto @DISCONNECT
SEND "NOOP\r\n"
MTCH "2[0-9][0-9]"r else goto @BAD_NOOP_RESPONSE
EXPT "2[0-9][0-9] "r else goto @DISCONNECT
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
DONE OKAY

@UNEXPECTED_GREETING:
STAT DOWN "[FTP] Unexpected greeting from port ${_REMOTEPORT}. (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@BAD_USER_RESPONSE:
MTCH "500" else goto @UNEXP_USER_RESPONSE
STAT ALRM "[FTP] Port ${_REMOTEPORT} did not recognize the \"USER\" command. (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@UNEXP_USER_RESPONSE:
STAT ALRM "[FTP] Unexpected response to USER command. (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@BAD_PASS_RESPONSE:
MTCH "530" else goto @UNEXP_PASS_RESPONSE
STAT WARN "[FTP] Incorrect login for \"${User ID}\". (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@UNEXP_PASS_RESPONSE:
STAT ALRM "[FTP] Unexpected response to PASS command. (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@BAD_NOOP_RESPONSE:
STAT ALRM "[FTP] Unexpected response to NOOP command. (${_LINE:50})"
SEND "QUIT\r\n"
MTCH "221" #+2
EXPT "221 " #+1
EXIT

@IDLE:
DONE DOWN "[FTP] No data for ${_IDLETIMEOUT} seconds.  Was expecting \"${_STRINGTOMATCH}\". [Line ${_IDLELINE}]"

@DISCONNECT:
DONE DOWN "[FTP] Connection disconnected while expecting \"${_STRINGTOMATCH}\"."

</script>
