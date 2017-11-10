import urllib.request, os

file_name = "hosts.txt"
whitelist = dict()

def addToDict(d, data):
    for line in data.split('\n'):
        lineStr = ""
        lineStr += line
        # Skips unusable lines
        if not lineStr or lineStr.startswith('\n'):
            continue
        if lineStr.startswith('127.0.0.1'):
            continue
        if lineStr.startswith('255.255.255.255'):
            continue
        if lineStr.startswith('.'):
        	continue
        if '!' in lineStr:
            continue
        if ':' in lineStr:
            continue
        if '@' in lineStr:
            continue 
        if '$' in lineStr:
            continue
        if '#' in lineStr:
            continue
        if '*' in lineStr:
            continue
        if '/' in lineStr:
            continue
        if '%' in lineStr:
            continue
        if '=' in lineStr:
        	continue
       	if '?' in lineStr:
       		continue
        # Strips any whitespace
        lineStr = lineStr.strip()
        # Strips initial pipe symbols
        lineStr = lineStr.replace('||', '')
        # Strips use of 'www.'
        lineStr = lineStr.replace('www.', '')
        # Strips initial '0.0.0.0 ' from host files
        lineStr = lineStr.replace('0.0.0.0 ', '')
        # If contains '^third-party' then checks against safe filters
        is_safe = False
        if '^' in lineStr:
        	third_party_str = '^third-party'
        	if lineStr.endswith(third_party_str):
        		lineStr = lineStr.replace(third_party_str, '')
        		if lineStr in whitelist:
        			is_safe = True
        		else:
        			is_safe = False
        	else:
        		lineStr = lineStr.replace('^', '')

        if is_safe:
        	continue
        # Skips final unusables
        if '^' in lineStr:
            continue
        if lineStr.endswith('.'):
        	continue

        d[lineStr] = d.get(lineStr, 0) + 1

    return d

def downloadHosts(url_str, d):
    response = urllib.request.urlopen(url_str)
    data = response.read()
    text = data.decode('utf-8')
    return addToDict(d, text)

def downloadBetterFYITrackerList(d):
    url = "https://raw.githubusercontent.com/anarki999/Adblock-List-Archive/master/Better.fyiTrackersBlocklist.txt"
    return downloadHosts(url, d)

def downloadAdawayHosts(d):
    url = "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt"
    return downloadHosts(url, d)

def downloadYoYoHosts(d):
    url = "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&mimetype=plaintext&useip=0.0.0.0"
    return downloadHosts(url, d)

def downloadAntiMicrosoftHosts(d):
    url = "https://raw.githubusercontent.com/tyzbit/hosts/master/data/tyzbit/hosts"
    return downloadHosts(url, d)

def downloadAdguardSpywareHosts(d):
    url = "https://filters.adtidy.org/extension/chromium/filters/3.txt"
    return downloadHosts(url, d)

def downloadPersonalHosts(d):
    url = "https://pastebin.com/raw/X4G4zVJb"
    return downloadHosts(url, d)

def getWhitelist():
	url = "https://pastebin.com/raw/G7UGnpxM"
	downloadHosts(url, whitelist)

def isServerUp(key):
	response = os.system("ping -c 1 " + key)
	if response == 0:
		return True
	else:
		return False

def main():
    d = dict()
    getWhitelist()
    downloadPersonalHosts(d)
    downloadBetterFYITrackerList(d)
    downloadAdawayHosts(d)
    downloadYoYoHosts(d)
    downloadAntiMicrosoftHosts(d)
    downloadAdguardSpywareHosts(d)

    f = open(file_name, 'w')
    for key in d.keys():
    	print ("Checking " + key + "\n")
    	if isServerUp(key):
    		key = key.strip()
    		f.write(key + '\n')
    		print("Added " + key + "\n")
    	print ("--------------------------------------------------------------------------------------------------\n")


    f.close()
    print(len(d.keys()))

if __name__ == '__main__':
    main()