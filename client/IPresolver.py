f = open('avahi.txt', 'r')
lines = f.readlines()
f.close()
searchtxt = "=;wlan0;IPv4"
ipline = ""
for i, line in enumerate(lines):    
    if searchtxt in line and i+1 < len(lines):
        #print line
        ipline=line
        break
ipline = lines[3]
pasertxt=ipline.split(';')

print pasertxt[7]
