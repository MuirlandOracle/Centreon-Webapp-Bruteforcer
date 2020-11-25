# Centreon-Webapp-Bruteforcer
## Python script for getting around the Centreon webapp bruteforce protection 
### Tested against Centreon v19.04.0

This tool is very simple at this point in time. It is single threaded, and does the bare minimum required to perform a bruteforce attack against Centreon with the protective measures in place.
See `./bruteforce.py --help` for usage and available switches
Note: Rockyou has some weird non-utf8 characters in it which Python doesn't like importing. If using rockyou, convert it first:
```iconv -f ISO-8859-1 -t UTF-8 /usr/share/wordlists/rockyou.txt > rockyou_utf8.txt```

**Warning:** The code in this repository may be used for academic/ethical purposes only. The author does not condone the use of this exploit for any other purposes -- it may only be used against systems which you own, or have been granted access to test.
