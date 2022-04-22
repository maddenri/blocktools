# Python Bitcoin Reader
## Overview

This application connects to a preconfigured node on the Bitcoin network and parses
incoming messages outputting them to the console as well as a log file 'bitcoin_reader.log'. 
Parsers have been set up to handle payloads of 'block', 'inv', 'tx' and 'version' messages whereas 
any other message types will only output their parsed message structure and payload in 'bytes' format.

Run: `python bitcoin_reader.py` from the cmd line. 

If the preconfigured node is offline:

Run: `python bitcoin_reader.py --peer_ip_address <IP_ADDRESS_OF_ONLINE_NODE>`

###Note: 
Since 'block' messages are only sent from the node roughly every 10 minutes it's difficult to 
see these displayed in the console window so please open the 'bitcoin_reader.log' file once the program has
been running for around 10 minutes and `ctrl+f Block Header`
