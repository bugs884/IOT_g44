import subprocess
from picamera import PiCamera

def recognise():

	cmd = "raspistill -o cam.jpg"
	cmd1= "alpr -c eu -p nl cam.jpg >dump.txt"
	subprocess.call(cmd, shell=True)
	subprocess.call(cmd1,shell=True)

	fin = open('dump.txt', 'r')
	fout = open('PIPE.txt','w+')


	with open('dump.txt') as f:
	  a = sum(1 for _ in f)
	fin.close()
        fout.close()
	return a

def main():
	a=recognise()
	fcam= open('cam.txt', 'rw')
	clines=fcam.readlines()
	cline=clines[0]
	while a<=1:
		print ("No License plate found")
		fout = open('PIPE.txt','w+')
	        fout.write("UNKNOWN")
	        a=recognise()

        fin = open('dump.txt', 'r')
	fout = open('PIPE.txt','w+')
	lines = fin.readlines()
	line = lines[1]
	lp = line.split(" ")
	fout.write(lp[5])
	print "LICENSE PLATE FOUND!!"
	fin.close()
        fout.close()

if __name__=='__main__':
	main()
