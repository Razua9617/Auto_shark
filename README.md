# Auto Shark
## What Auto Shark Does?
The main objective of AutoShark is to save you hours by automating all the information you need from a pcap file. AutoShark will parse through a pcap file and extract useful information. Furthermore, this would be helpful for a blue team member to investigate malicious activities on the network. You no longer need to stare at a small wireshark window to search for nmap scan or brute force attacks. AutoShark will automatically tell you certain Indicators of Compromise, any files that an attacker might have tried to upload to a victim’s server. You do not need to run AutoShark multiple times. Once you are done using the tool, Autoshark will prompt you to choose if you would like to save the information you need into a file. Now I will show a walkthrough of AutoShark.

Option 1 - Extarct Ips

	Option 1 is to take in a pcap file and extarct all the ips in the pcap and group them with their respective mac,source port. The ips are subdivided into source and destination ips. The ports were subdivided between TCP and UDP ports. Modules we used are scapy to read the pcap file and re expressions to search for patterns. 
Option 2 - Extarct Files 

	Option 2 is to extract any files that were being used from each packet in the pcap file. For this option we used scapy.
Option 3 - Detect Indicator of Compromise

	Option 3 was created to detect indicators of compromises(IOC) such as brute force attacks and nmap scans. We used modules such as Pyshark.
Option 4 - Export to a file 

	Option 4 was used to export and save our findings into a file. 
## How to Download the Code
The code can be downloaded several different ways:

	Using Command Line:
		< wget https://github.com/Razua9617/Auto_shark.git >
		< gh repo clone Razua9617/Auto_shark >
	Download the ZIP directly from the repository
	Open the repository with Github Desktop

## How to run the Code
To run our code you run one of the following command lines, depending on your OS system:

	Linux: python3 Auto_shark <pcap_filename>
	Windows python3 .\Auto_shark <pcap_filename>
