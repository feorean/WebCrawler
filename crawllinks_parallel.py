import json
import os
import subprocess
import time


input_json_file = "seed.json"

file_address = './'+input_json_file
scrapy_proj_dir='./'
out_folder = 'out/'

#Change dir to scrapy Jumpon Crawler
os.chdir(scrapy_proj_dir)

#Open json file and read all URLs 
with open(file_address, 'r') as links_file:
	
	#Load json stream
	rows = json.load(links_file)
	
	#Keep track of batch runs
	i = 1
	
	print("Started")
	#Loop every item
	for row in rows:
		#print(os.getcwd()) 
		#Check if file does not exists before starting. Otherwise move to next one
		if os.path.isfile(out_folder+row['url']+".json")==False:	
			os.system("> "+out_folder+"jumpcrw.log")
			subprocess.Popen(["scrapy", "crawl", "jumpcrw", "-a", "WPAGE=http://"+row['url']+"", "--logfile="+out_folder+"/jumpcrw.log", "-o", out_folder+row['url']+".json"])
			print("scrapy crawl jumpcrw -a WPAGE=http://"+row['url']+" --logfile="+out_folder+"jumpcrw.log -o "+out_folder+row['url']+".json")
			if i==150:
				time.sleep(100)
				i=0
			i+=1
		else:
			print "file exists in the output directory"	

print("Finished")
