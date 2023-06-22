import requests
import time
import threading
import argparse

from datetime import datetime
from colorama import Fore, Back, Style

blue = Fore.LIGHTBLUE_EX
red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
reset = Fore.RESET

bold = '\033[1m'
underline = '\033[4m'
end = '\033[0m'

VERSION = "v0.0.01b"

w00ffuzz_banner = f"""
                    ._____.
          {blue},{reset}        < W00f! >
          {blue}|`-.__{reset}  . *******
          {blue}/ ' _/{reset} .*'
         {blue}****`{reset}       -- By Russian.Hzcker --
        {blue}/    }}{reset}            ___  ___  ______          
       {blue}/  \ /{reset}     _    __/ _ \/ _ \/ _/ _/_ ________
   {blue}\ /`   \\\ {reset}    | |/|/ / // / // / _/ _/ // /_ /_ /
   {blue}`\    /_\\{reset}     |__,__/\___/\___/_//_/ \_,_//__/__/
     {blue}`~~~~~``~`{reset}
"""

print(w00ffuzz_banner)

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", required=True, dest="fuzz_url", help="Specifies the URL to fuzz. (Type '{FUZZ}' at the point where you want to fuzz via dictonary)")
	parser.add_argument("-w", "--wordlist", required=True, dest="fuzz_dict", help="Specifies the wordlist to fuzz with.")
	parser.add_argument("-m", "--method", required=False, dest="fuzz_method", help="Specifies the request method. Methods: GET or POST (Default: GET)")
	parser.add_argument("-b", "--badstatus-codes", required=False, dest="fuzz_badcode", help="Specifies the bad response. Example: 404,403... (Seperated by comma) (Default: show all)")
	return parser.parse_args()

arguments = get_arguments()

print(f" {bold}{blue}[+]{reset}{end} Starting required packages by w00ffuzz...")

class W00ffuzz:
	def __init__(self, arguments:argparse.Namespace) -> None:
		try:
			self.session = requests.Session()
			self.fuzz_url = str(arguments.fuzz_url)
			self.fuzz_dict = str(arguments.fuzz_dict)
			self.fuzz_method = "GET"
			self.badstatus_codes = arguments.fuzz_badcode
			if self.badstatus_codes != None:
				if "," in self.badstatus_codes:
					self.badstatus_codes = self.badstatus_codes.split(",")

			if arguments.fuzz_method != None:
				if arguments.fuzz_method.upper() not in ["GET", "POST"]:
					exit(f" {bold}{red}[!]{reset}{end} Invalid request method specified.")
				else:
					self.fuzz_method = str(arguments.fuzz_method.upper())
			else:
				print(f" {bold}{yellow}[i]{reset}{end} No request method specified, setting to default (GET).")
		except Exception as argument_parsing_error:
				exit(f" {bold}{red}[-]{reset}{end} CRITICAL: Error while parsing arguments Error-code: 0x000002. Exception: " + str(argument_parsing_error))

	def show_table(self) -> None:
		print()
		print(" ===============================================")
		print(f" {bold}{blue}[+]{reset}{end} URL: " + self.fuzz_url)
		print(f" {bold}{blue}[+]{reset}{end} DICTIONARY: " + self.fuzz_dict)
		print(f" {bold}{blue}[+]{reset}{end} METHOD: " + self.fuzz_method)
		print(f" {bold}{blue}[+]{reset}{end} VERSION: " + VERSION)
		print(" ===============================================")
		print()
		option = input(f" {bold}{yellow}[?]{reset}{end} Information table correct? [Y/n]: ")
		option = option.lower()
		if option == "n":
			exit(f" {bold}{red}[!]{reset}{end} Change the w00ffuzz arguments in command prompt.")
		elif option == "y":
			pass
		else:
			exit(f" {bold}{red}[!]{reset}{end} Invalid input was entered!")

	def get_report(self, url:str) -> dict:
		if self.fuzz_method == "GET":
			try:
				response = self.session.get(url, allow_redirects=False)
			except requests.ConnectionError:
				response = "[CONNECTION ERROR]"
		elif self.fuzz_method == "POST":
			try:
				response = self.session.post(url, allow_redirects=False)
			except requests.ConnectionError:
				response = "[CONNECTION ERROR]"
		else:
			exit(f" {bold}{red}[-]{reset}{end} CRITICAL: There was an unexpected error. Error-code: 0x000001")

		if type(response) == str and response == "[CONNECTION ERROR]":
			return {
				"time": str(datetime.now()),
				"DETAILS": {
					"url": self.fuzz_url,
					"method": self.fuzz_method,
					"status_code": None,
					"errors": True,
					"error": "[CONNECTION ERROR]"
				}
			}
		else:
			return {
				"time": str(datetime.now()),
				"DETAILS": {
					"url": self.fuzz_url,
					"method": self.fuzz_method,
					"status_code": str(response.status_code),
					"errors": False,
					"error": None
				}
			}

print(f" {bold}{blue}[+]{reset}{end} All required packages started.")

W00ffuzz = W00ffuzz(arguments)
W00ffuzz.show_table()

try:
	file = open(W00ffuzz.fuzz_dict, "r")
except Exception as file_open_error:
	exit(f" {bold}{red}[-]{reset}{end} CRITICAL: There was an error while opening file. Error-code: 0x000003. Exception: " + str(file_open_error) + " (" + str(report["DETAILS"]["method"]) + ")")
infile = file.read()
file.close()
combinations = infile.split("\n")
combinations_length = len(combinations)
current = 1

print(f" {bold}{blue}[+]{reset}{end} Fuzzing started.")
print()

try:
	for combination in combinations:
		print(f" Progress ({current} / {combinations_length})", end="\r")
		report = W00ffuzz.get_report(W00ffuzz.fuzz_url.replace("{FUZZ}", combination))
		if report["DETAILS"]["errors"]:
			if report["DETAILS"]["error"] == "[CONNECTION ERROR]":
				print(f" {bold}{red}[!]{reset}{end} ERR |  " + "(" + str(report["DETAILS"]["method"]) + ")" + " " + "ERR" + "  | " + "Couldn't connect: " + str(report["DETAILS"]["url"]).replace("{FUZZ}", combination))
		else:
			if str(report["DETAILS"]["status_code"]) in W00ffuzz.badstatus_codes:
				pass
			if str(report["DETAILS"]["status_code"]) not in W00ffuzz.badstatus_codes or W00ffuzz.badstatus_codes == None:
				print(f" {bold}{blue}[+]{reset}{end} OK  |  " + "(" + str(report["DETAILS"]["method"]) + ")" + " " + str(report["DETAILS"]["status_code"]) + "  | " + str(report["DETAILS"]["url"]).replace("{FUZZ}", combination))
		current += 1
except KeyboardInterrupt:
	exit()