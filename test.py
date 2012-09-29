import sys
from ssh_exec import ssh_exec
from acelium_lib import BaseProbe

class ProcessCheck(BaseProbe):

    def probe(self):
        # connect to host via ssh and retrieve memory infos
        ret = ssh_exec(self.options.address, 22, self.options.username, self.options.password,\
            'ps -C %s -o pid --no-heading' % self.options.process)
        self.ret_values.process_name = self.options.process
        try:
            tmp = ret.split('\n')		# multiple process id's will be on separate lines
            if (len(tmp) <= 1):			# only one
                pid = int(ret.strip())  # just return the integer value of the PID
            else:
                pid = ', '.join(tmp)    # Otherwise, return PIDs separated by ", "
            self.ret_values.process_pid = pid
            self.ret_code = 0
            self.ret_msg = "Process is running"
        except:
            self.ret_values.process_pid = 'n/a'
            self.ret_code = 3
            self.ret_msg = "CRITICAL: Process is not running"

p = ProcessCheck()
p.setDescription('stdin: <login> <password>')
p.addOption('address',  '-a', requiered=True, validator='host')
p.addOption('process',  '-p', requiered=True)
p.getCredentialsFromStdin()
sys.exit(p.run())

class ProcessCheck(BaseProbe):

    def probe(self):
        # connect to host via ssh and retrieve memory infos
        ret = ssh_exec(self.options.address, 22, self.options.username, self.options.password,\
            'ps -C %s -o pid --no-heading' % self.options.process)
        self.ret_values.process_name = self.options.process
        try:
            pid = int(ret.strip())
            self.ret_values.process_pid = pid
            self.ret_code = 0
            self.ret_msg = "Process is running"
        except:
            self.ret_values.process_pid = 'n/a'
            self.ret_code = 3
            self.ret_msg = "CRITICAL: Process is not running"

p = ProcessCheck()
