# DNS Blocklist Compiler
Compiles a list of DNS hostnames from multiple sources, strips unnecessary data and removes duplicates including
subdomains sharing a similar upper level domains (e.g. sub1.domain.com and subsub2.sub1.domain.com will result in
only sub1.domain.com). Manages to strip back all the listed sources (which often each contain close to 300k including
many unique strings, but still likely duplicates) to well under 400k domains. This was made after searching some
other's host files and finding many duplicate domains

# Current sources:

Check sources.txt
