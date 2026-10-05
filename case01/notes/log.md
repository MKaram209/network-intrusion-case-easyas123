# Investigation Log - Case 01
Task: Network intrusion detection and incident investigation.
Evidence: 2026-02-28-traffic-analysis-exercise.pcap
Note: Kali shows local time (UTC-5). The report uses UTC.

## Step 1 - Verified the evidence
What I did: Ran sha256sum on the pcap and saved the result (output/01_pcap_sha256.txt).
Why: The hash is a fingerprint of the file. If it ever changes, someone altered the evidence. It proves the file I analyzed is exactly the one I was given.
Result: 3dc470f5...407e61, matches the original.

## Step 2 - Checked the capture's basic facts
What I did: Ran capinfos on the pcap (output/02_capinfos.txt).
Why: To know how big the recording is and what time window I'm investigating before digging in.
Result: 15,512 packets, about 4 hours 21 minutes, starting 19:55 UTC.

## Step 3 - Looked at what kinds of traffic exist
What I did: Ran tshark with the protocol hierarchy report (output/03_protocol_hierarchy.txt).
Why: To get an overview of the traffic (DNS, HTTP, Kerberos, and so on) so I know where to look first, like reading a table of contents.
Result: A Windows domain network (Kerberos, SMB, LDAP) with a lot of TLS and HTTP traffic.

## Step 4 - Started looking for the infected computer
What I did: Filtered for packets sent to the suspicious server 45.131.214.85 (output/04_c2_ip_mac.txt).
Why: The SIEM alert named this IP as a NetSupport Manager RAT server, so whichever internal computer talks to it is the infected one.
Result: Infected computer found. IP 10.2.28.88, MAC 00:19:d1:b2:4d:ad. First packet to the C2 server is frame 2569 at 19:55:51 UTC, port 443.

## Step 5 - Found the computer's name
What I did: Filtered for NBNS packets sent from 10.2.28.88 (output/05_hostname.txt).
Why: NBNS is how Windows computers announce their name on the network, so it tells me the infected computer's host name.
Result: Host name is DESKTOP-TEYQ2NR, in the domain EASYAS123. Seen in frame 135 at 19:55:11 UTC, same MAC as the C2 traffic (00:19:d1:b2:4d:ad).

## Step 6 - Found the user account
What I did: Filtered for Kerberos packets between 10.2.28.88 and the domain controller and read the account name field (output/06_username.txt).
Why: When a user logs into a Windows domain, their account name is sent to the domain controller using Kerberos, so it tells me who was using the infected computer.
Result: User account is brolf. First seen in frame 243 at 19:55:23 UTC, a login request from 10.2.28.88 to the domain controller 10.2.28.2.

## Step 7 - full name of the user
What I did: opened the pcap in Wireshark and searched for "Rolf" (Ctrl+F, string, packet details, case sensitive), since the username brolf looks like first initial + surname. Saved the packet text to output/07_fullname_frame339.txt and a screenshot to screenshots/07_fullname_frame339.png.
Why: the domain controller sends back account details when a computer looks up a user, and that includes the full name. Searching the surname was the quickest way to land on that packet.
Result: the full name is Becka Rolf. It's in frame 339, a SAMR reply from the domain controller (10.2.28.2) to the infected computer (10.2.28.88).

## Step 8 - how long the C2 connection lasted
What I did: ran the conversation table (tshark -z conv,ip) limited to 45.131.214.85 and saved it to output/08_c2_conversation.txt. My first run used -Y and it didn't filter anything, so I put the filter inside the -z part and reran it.
Why: to see how long the infected computer stayed connected to the suspicious server and how much data went each way.
Result: one conversation, 10.2.28.88 <-> 45.131.214.85, 550 frames and 95 kB total. The victim sent 276 frames (78 kB) and received 274 frames (17 kB). It started 44.9 seconds into the capture (19:55:51 UTC) and lasted about 15,637 seconds (4 hours 20 minutes), so it was a long-running session, not a quick check-in.

## Step 9 - what the C2 traffic looks like
What I did: listed the HTTP requests sent to 45.131.214.85 (output/09_c2_http.txt).
Why: the protocol overview showed a lot of HTTP form posts, and I wanted to know what they were and whether they follow a pattern.
Result: every request is a POST to http://45.131.214.85/fakeurl.htm with the user agent NetSupport Manager/1.3. The first four are within one second of each other (19:55:51 to 19:55:52 UTC, frames 2638 to 2645), then one request every 60 seconds (frames 3807, 4093, 4134...). That regular timing is beaconing. The traffic is plain HTTP on port 443, not encrypted TLS.

## Step 10 - did the beaconing last until the end
What I did: listed the last 5 HTTP requests to 45.131.214.85 (output/10_c2_http_last.txt).
Why: to check if the infection was still active when the recording stopped, or if it had ended earlier.
Result: the last request is frame 15499 at 00:16:28 UTC on 2026-03-01, about 7 seconds before the capture ends (00:16:35 UTC). The one-minute beaconing never stopped, so the computer was still infected and talking to the C2 server for the whole capture, about 4 hours 20 minutes.

## Wireshark/tshark analysis closed
What I did: re-ran sha256sum on the pcap and saved it to output/12_final_hash_check.txt.
Why: to prove the evidence is exactly the same as when I started.
Result: hash matches the original (3dc470f5...407e61). Analysis stopped here. I did not check how the infection started (DNS and web activity before the first C2 contact), so the report will say the initial infection vector was not determined from this capture.

## IOC list written
What I did: put the indicators from my evidence into notes/iocs.md.
Why: the task asks for indicators of compromise, and these are what a security team would block or search for.
Result: C2 IP 45.131.214.85, port 443, URL /fakeurl.htm, user agent NetSupport Manager/1.3, and the one-minute beaconing. No file hashes, because I didn't extract any files from the capture.

## Timeline written
What I did: put the key events in order with UTC times and frame numbers into notes/timeline.csv.
Why: the task needs a clear incident timeline, and the chart will be built from this file.
Result: nine events, from the capture start at 19:55:06 UTC to the last beacon at 00:16:28 UTC on 2026-03-01. The whole infection story fits in the first minute: name announced at 19:55:11, user login at 19:55:23, first C2 contact at 19:55:51.

## Timeline chart made
What I did: wrote deliverables/make_timeline.py (Python + matplotlib), which reads notes/timeline.csv and saves deliverables/timeline.png.
Why: the task asks for a timeline visualization. The chart has a zoomed view of the first two minutes (name, login, first C2 contact) and a whole-capture view showing the infection lasting until the recording ended.
Result: deliverables/timeline.png created.
