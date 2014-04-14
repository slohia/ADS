import commands
import re


class SystemMonitor:

    def __init__(self, ads):
        pass

    def number_of_processes(self):
        cmd = "top -n 1 -b | grep -Po 'Tasks:\K \d*'"
        return int(commands.getoutput(cmd))

    def system_time(self):
        cmd = "top -n 1 -b | grep -Po '\d*.?\d*(?=%sy,)'"
        return commands.getoutput(cmd)

    def user_time(self):
        cmd = "top -n 1 -b | grep -Po '\d*.?\d*(?=%us,)'"
        return commands.getoutput(cmd)

    def memory_utilization(self):
        #~ This command is for measuring the used memory
        cmd1 = "free -t | grep -Po '\d*(?= \d*  \d*  \d*      )'"
        #
        # #~ This command is for measuring the total memory in the system
        cmd2 = "free -t | grep -Po '\d*(?=\d* \d*  \d*  \d+     \d*      )'"

        #~ This variable stores the value of the used memory
        var1 = float(commands.getoutput(cmd1))

        #~ This variable stores the value of the total memory
        var2 = float(commands.getoutput(cmd2))

        #~ This variable is used for storing the percentage of memory that is being used
        var3 = (var1/var2) * 100

        #~ Final output with upto 2 decimal places
        output = float("%.2f" %var3)
        return output

    def page_faults(self):
        cmd = "ps -eo maj_flt | grep -Po '\d*'"
        var1 = commands.getoutput(cmd)
        var2 = re.split('\n', var1)
        #~ Now, we will convert each element, which is a string, into integer element
        var2 = [int(i) for i in var2]
        #~ Now, we have to add each element of the list to get toal number of major page faults
        # #~ First, we initialize a variable to 0, to help in adding all the elements of the list
        var3 = 0
        #~ Adding each element of the list
        for j in var2:
            var3 = var3 + j
        return var3

    def read_bytes(self):
        cmd = "hdparm -tT /dev/sda | grep -Po '\d*.?\d*(?= MB/sec)'"
        var = commands.getoutput(cmd)
        return re.split('\n', var)

    def write_bytes(self):
        cmd = "dd if=/dev/zero of=test bs=20485 count=2048 2>&1 > /dev/null | grep -Po '\d+.?\d*(?= MB/s)'"
        return commands.getoutput(cmd)

    def used_disk_percent(self):
        cmd = "df -h / | awk '{print $5}' | grep -Po '\d+.?\d+'"
        return commands.getoutput(cmd)

    def total_files(self):
        cmd = "df --inodes / | grep -Po '\d*(?= \d\d* \d*  \d\d*)'"
        return int(commands.getoutput(cmd))