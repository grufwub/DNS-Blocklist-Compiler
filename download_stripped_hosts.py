import urllib.request, tldextract, os

# Ensures we are using the correct code page in windows console!
os.system("chcp 65001")

hosts_header = '# grufwubs combined hosts\n127.0.0.1 localhost\n::1 localhost\n\n# Start of entries generated by download_stripped_hosts.py\n'
file_name = "hosts.txt"
whitelist = dict()
TYPE_STANDARD = "standard"
TYPE_BLACKLIST = "blacklist"
hosts_type = dict()

def setHostsType():
	while True:
		t = input("Please enter hosts file type (standard / blacklist)\n")
		if t == TYPE_STANDARD:
			hosts_type.setdefault(TYPE_STANDARD, 0)
			print("Hosts file type set to standard")
			break
		if t == TYPE_BLACKLIST:
			hosts_type.setdefault(TYPE_BLACKLIST, 0)
			print("Hosts file type set to blacklist")
			break
		else:
			print("Unrecognised hosts file type")
			continue

def getHostsType():
	if TYPE_STANDARD in hosts_type:
		return TYPE_STANDARD
	if TYPE_BLACKLIST in hosts_type:
		return TYPE_BLACKLIST

def addToDict(d, data):
	# Returns a sorted, stripped dictionary of hosts, with the registered domain as the key
	print('Adding hosts to dictionary')
	for line in data.split('\n'):
		lineStr = ""
		lineStr += line
		# Skip unusable lines
		if not lineStr:
			continue
		if lineStr.startswith('127.0.0.1'):
			continue
		if lineStr.startswith('255.255.255.255'):
			continue
		if '!' in lineStr:
			continue
		if ':' in lineStr:
			continue
		if '@' in lineStr:
			continue
		if '#' in lineStr:
			if lineStr.startswith('#'):
				continue
			else:
				endList = lineStr.split('#')[1:]
				end = ''.join(endList)
				if '/' in end or '(' in end or ')' in end or '[' in end or ']' in end or '?' in end or '!' in end or '=' in end or ';' in end or '%' in end or '$' in end or '{' in end or '}' in end:
					continue
				else:
					lineStr = lineStr.split('#')[0]
		if '$' in lineStr:
			if '^$important' in lineStr:
				lineStr.replace('^$important', '')
				lineStr.replace('$important', '')
			else:
				continue
		if '*' in lineStr:
			continue
		if '?' in lineStr:
			continue
		if '=' in lineStr:
			continue
		if '[' in lineStr:
			continue
		if ']' in lineStr:
			continue
		if ',' in lineStr:
			continue
        # Strips any whitespace
		lineStr = lineStr.strip()
        # Strips initial pipe symbols
		lineStr = lineStr.replace('||', '')
        # Strips use of 'www.'
		lineStr = lineStr.replace('www.', '')
        # Strips initial '0.0.0.0 ' from host files
		lineStr = lineStr.replace('0.0.0.0 ', '')
        # Strips use of '^third-party'
		lineStr = lineStr.replace('^third-party', '')
		# Strips use of ^important
		lineStr = lineStr.replace('^important', '')
        # Strips extra '^'
		lineStr = lineStr.replace('^', '')
        # Removes unusable information after first '/'
		if '/' in lineStr:
			lineStr = lineStr.split('/')[0]
        # Checks values against whitelist and skips safe hosts
		is_safe = False
		for key in whitelist:
			if lineStr == key:
				is_safe = True
		if is_safe:
			continue
        # Skips final unusables
		if lineStr.startswith('.') or lineStr.endswith('.') or lineStr.endswith('.js'):
			continue
		# Adds the host to a dictionary which serves as the value to a parent dictionary (passed in the method argument), with the registered domain as the key
		ext = tldextract.extract(lineStr)
		base_domain = ext.registered_domain
		# Skips those with an invalid base-domain
		if base_domain == '' or base_domain == '\n' or base_domain == ' ':
			continue
		td = d.get(base_domain, dict())
		td[lineStr] = td.get(lineStr, 0) + 1
		d[base_domain] = td
	return d

def downloadHosts(url_str, d):
	# Downloads hosts and passes them to the method addToDict() which returns a sorted, stripped dict of hosts
	print('Downloading hosts from ' + url_str)
	response = urllib.request.urlopen(url_str)
	data = response.read()
	text = data.decode('utf-8')
	return addToDict(d, text)

def getWhitelist():
	# Downloads from my manually compiled whitelist on Github to prevent sites from being blacklisted
	l = list()
	l.append("https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/whitelist.txt")
	l.append("https://raw.githubusercontent.com/anudeepND/whitelist/master/Google_domains.txt")
	l.append("https://raw.githubusercontent.com/anudeepND/whitelist/master/whitelist.txt")
	print('Downloading whitelist')
	for url in l:	
		response = urllib.request.urlopen(url)
		data = response.read()
		text = data.decode('utf-8')
		for line in text.split('\n'):
			if not line or line.startswith('/') or line.startswith('\n'):
				continue
			whitelist[line] = whitelist.get(line, 0) + 1

def getOrderedKeyList(d):
	l = list()
	for i in range(0, 10):
		if d.get(i):
			l.append(i)
	return l

def getHostLengthDictionary(d):
	return_dict = dict()
	for key in d.keys():
		s = key.split('.')
		i = len(s)
		return_dict.setdefault(i, list()).append(key)
	return return_dict

def getUniqueHosts(d):
	# Returns a list of unique hosts for each registered domain, that don't overlap subdomains (e.g. stats.facebook.com and s.stats.facebook.com), keeping only the shortest.
	# For each registered domain, goes through the listed hosts and creates a dictionary with {"Number of domain levels" : List[domain, domain, domain]}
	length_dict = getHostLengthDictionary(d)
	return_list = list()
	# Creates an ordered list of keys (which are the domain level ints).
	key_list = getOrderedKeyList(length_dict)
	# BUG: another hacky fix right here to account for key_list sometimes being empty
	if len(key_list) == 0:
		return [""]
	min_length = min(key_list)
	min_length_host = length_dict[min_length][0]
	ext = tldextract.extract(min_length_host)
	# If dictionary contains the registered domain (so all traffic should be blocked), returns only this.
	if min_length_host == ext.registered_domain:
		return_list.append(min_length_host)
	else:
		# Else goes through the dictionary and finds unique non-overlapping domains
		previous = list()
		# BUG: this for loop seems to create duplicates in some instances
		for length in key_list:
			current = length_dict[length]
			if length == min_length:
				previous = current
				return_list.extend(current)
			else:
				add_to_return_list = list()
				for host in return_list:
					for entry in current:
						if host not in entry and len(entry) > len(host):
							add_to_return_list.append(entry)
				return_list.extend(add_to_return_list)
	return return_list
			
def main():
	setHostsType()
	
	d = dict()
	l = list()
	getWhitelist()
	if getHostsType() == TYPE_STANDARD:
		l.append("https://filters.adtidy.org/extension/chromium/filters/15.txt") # Adguard simplified DNS filter
		l.append("https://raw.githubusercontent.com/piperun/iploggerfilter/master/filterlist") # piperun's iplogger filter
		l.append("https://raw.githubusercontent.com/Yhonay/antipopads/master/hosts") # Yhonay antipopads
		l.append("https://raw.githubusercontent.com/quidsup/notrack/master/trackers.txt") # Quidsup tracker list
	l.append("https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/blacklist.txt") # Personal blacklist
	l.append("https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts") # Steven Black's Hosts
	l.append("https://filters.adtidy.org/extension/chromium/filters/11.txt") # Adguard mobile filters
	l.append("https://raw.githubusercontent.com/anarki999/Adblock-List-Archive/master/Better.fyiTrackersBlocklist.txt") # Better.fyi tracker list

	for url in l:
		downloadHosts(url, d)

	print('Writing hosts to file:\n')
	f = open(file_name, 'w', encoding='utf-8')
	if getHostsType() == TYPE_STANDARD:
		f.write(hosts_header)
	count = 0
	for key in d.keys():
		host_list = d[key]
		host_list = list(dict.fromkeys(host_list)) # Hacky fix to remove duplicates since getUniqueHosts() method seems to introduce duplicates in some cases
		for host in host_list:
			if host == '' or host == '\n':
				continue
			if getHostsType() == TYPE_STANDARD:
				host = '127.0.0.1 ' + host.strip()
			else:
				host = host.strip()
			f.write(host + '\n')
			count += 1
			print(count)
			print(host)
		print('------------------------------------')
	f.close()

if __name__ == '__main__':
	main()
