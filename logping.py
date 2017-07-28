import datetime, sched, subprocess, time 
import re

regex = re.compile(r"tempo=(.*)ms", re.IGNORECASE)

def logPing():
	process = subprocess.Popen(['ping', '8.8.8.8', '-n', '1'], encoding="850", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
	output, error = process.communicate()
	if error:
		result = 0
	else:
		result = output.split('\n', 4)[2]
		
		print(result)
		
		result = re.search(regex, result)
		
		if result:
			result = result.group(1)
		else:
			result = "0"
		
	with open("ping.txt", "a") as myfile:
		myfile.write("%s\t%s\n" % (datetime.datetime.now().strftime("%d/%m/%Y\t%H:%M:%S"), result))
	
	s.enter(10, 1, logPing)
	
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, logPing)
s.run()
