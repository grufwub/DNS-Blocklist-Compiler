# DNS Blocklist Compiler
Compiles a list of DNS hostnames from multiple sources and strips unnecessary data.

Can either compile a complete list of hosts to a standard hosts file, or compile a list for a blacklist style DNS blocker, like Adguard Pro for iOS, which allows for wildcard entries (blocking whole domains e.g. facebook.com instead of having to specify all subdomains like stats.facebook.com). Both will remove any duplicates.

# Current sources:

Better.fyi Trackerlist: https://raw.githubusercontent.com/anarki999/Adblock-List-Archive/master/Better.fyiTrackersBlocklist.txt

Steven Black's Hosts: https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts

Adguard's Simplified Hosts: https://filters.adtidy.org/extension/chromium/filters/15.txt

Personal Hosts (to catch stragglers): https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/blacklist.txt

Personal Whitelist (to prevent blocking safe domains): https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/whitelist.txt

anudeepND Whitelist (again, to prevent blocking safe domains): https://github.com/anudeepND/whitelist (https://raw.githubusercontent.com/anudeepND/whitelist/master/whitelist.txt, https://raw.githubusercontent.com/anudeepND/whitelist/master/Google_domains.txt)
