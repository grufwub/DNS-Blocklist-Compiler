# DNS Blocklist Compiler
Compiles a list of DNS hostnames from multiple sources and strips unnecessary data.

Can either compile a complete list of hosts to a standard hosts file, or compile a list for a blacklist style DNS blocker.

Please note the hosts_blacklist file is compiled from only 3 of the sources, as Adguard iOS Pro doesn't seem to work if your blacklist size is much over 40,000.

# Current sources:

Better.fyi Trackerlist: https://raw.githubusercontent.com/anarki999/Adblock-List-Archive/master/Better.fyiTrackersBlocklist.txt

Steven Black's Hosts: https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts

Adguard's Simplified DNS Hosts: https://filters.adtidy.org/extension/chromium/filters/15.txt

Personal Hosts (to catch stragglers): https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/blacklist.txt

Personal Whitelist (to prevent blocking safe domains): https://raw.githubusercontent.com/grufwub/DNS-Blocklist-Compiler/master/whitelist.txt

anudeepND Whitelist (again, to prevent blocking safe domains): https://github.com/anudeepND/whitelist (https://raw.githubusercontent.com/anudeepND/whitelist/master/whitelist.txt, https://raw.githubusercontent.com/anudeepND/whitelist/master/Google_domains.txt)

Yhonay's Antipopads: https://raw.githubusercontent.com/Yhonay/antipopads/master/hosts

Piperun's IPLogger filter: https://raw.githubusercontent.com/piperun/iploggerfilter/master/filterlist

Quidsup's NoTrack blocklist: https://raw.githubusercontent.com/quidsup/notrack/master/trackers.txt

Adguard's Mobile Ads filter: https://filters.adtidy.org/extension/chromium/filters/11.txt
