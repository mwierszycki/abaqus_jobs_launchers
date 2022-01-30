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
