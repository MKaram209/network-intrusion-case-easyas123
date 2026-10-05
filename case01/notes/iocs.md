# Indicators of compromise - Case 01

| Type | Value | What it is | Evidence |
|---|---|---|---|
| IP address | 45.131.214[.]85 | C2 server (NetSupport Manager RAT) | output/04_c2_ip_mac.txt |
| Port | 443/tcp | port the C2 traffic uses (plain HTTP, not real TLS) | output/04, output/09 |
| URL | http://45.131.214[.]85/fakeurl.htm | path every beacon POSTs to | output/09_c2_http.txt |
| User agent | NetSupport Manager/1.3 | tool name sent in every request | output/09_c2_http.txt |
| Behavior | one POST per 60 seconds | beaconing, from 19:55:51 UTC until the end of the capture | output/09, output/10 |

## Affected host (not IOCs, but needed to find it)
- IP 10.2.28.88
- MAC 00:19:d1:b2:4d:ad
- Host name DESKTOP-TEYQ2NR
- User brolf (Becka Rolf)

Note: addresses are written with [.] so nobody clicks or connects to them by accident.
