# Regular and alternative Abaqus job running methods

## Regular methods
Running Abaqus from the command line is quite common not only on Linux machines. It's much more flexible and convenient than using Abaqus/CAE or other GUI apps in many situations. In some cases like HPC servers, cloud services it's prefered or even obvious method. 
Abaqus job can be start from command line in three modes:
```
abaqus -j job_name -ba[ckground]
```
This option will submit the job to run in the background (default mode). It's the default method when mode is not specific directly. In this mode the log file output will be saved in the file job-name.log in the current directory.
```
abaqus -j job_name -int[eractive]
```
This option will cause the job to run in the foreground. For Abaqus/Standard the log file and for Abaqus/Explicit the status file and the log file will be output to the stdout (terminal).
```
abaqus -j job_name -seq[uential]
```
This option will submit the job to run in the foreground. However the log/sta files will not be output to the stdout. The output info will be saved in the file job-name.log in the current directory like in the case of background mode.

To start Abaqus' job manually or even with simple scripts the three above modes are effective enough in regular work for most users. However alternative Abaqus job running methods can be useful for sysadmins or devops to manage abaqus processes more effectively.

## Running Abaqus job using \*.com file directly

When abaqus command is invoked in the terminal the SMALauncher (ABQLauncher in 2021 and earlier versions) program is run. Next SMALuncher starts the sequence of subprocesses. The sequence depends on which phases of an analysis is performed (see Abaqus manual Abaqus/Standard and Abaqus/Explicit execution). Each stage is driven by Python script run by SMAPython - Python distributions delivered with Abaqus. The driver script creates the job_name.com file based on parameter given with abaqus command (e.g. number of cpus, user subroutines, etc), Abaqus settings (set of \*.env files) and input file. The \*.com file is in fact a Python script.

The \*.com file can be also created separately using command:

$ abaqus createComOnly -j job_name

The simple Python script can used to run job using \*.com file:
```
$ cat runComFile.py
import os, sys, subprocess, driverUtils

jobName = os.path.splitext(sys.argv[1])[0]
print '[*] Job %s is running ...' % jobName

cmd = [driverUtils.getPython(),'-u','%s.com' % jobName]

logFile = open('%s.log' % jobName,'wb')

p = subprocess.Popen(cmd,stdout=logFile,stderr=logFile)
retCode = p.wait()

logFile.close()

if retCode:
    print '[*] Job %s aborted with status: %s' % (jobName, retCode)
else:
    print '[*] Job %s finished successfully' % jobName

sys.exit(retCode)

$ abaqus python runComFile.py job_name.com
```
Direct usage of Python popen method enables to get and to use ID of the process, to redirect stdout and stderr in any way, to check if the running process has terminated, to send the signal to the process, to terminate or kill the process and much more e.g. read Abaqus files (\*.dat, \*.msg, \*.sta, \*.odb) during process execution and control process based on results.

Happy running Abaqus jobs! 

