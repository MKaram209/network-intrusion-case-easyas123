## [2026-10-05 16:38 UTC] Step 01: Evidence Integrity
- Objective: Compute SHA-256 hash of raw PCAP to preserve evidence chain of custody.
- Command: sha256sum case01/evidence/2026-02-28-traffic-analysis-exercise.pcap
- Output: case01/output/01_pcap_sha256.txt

## [2026-10-05 16:47 UTC] - Capture Metadata Overview
Ran capinfos to get baseline stats on the capture before digging into packets.
- Command: capinfos case01/evidence/2026-02-28-traffic-analysis-exercise.pcap
- Key details: 15,512 packets total, ~4h21m window on 2026-02-28.
- Saved output: case01/output/02_capinfos.txt

## [2026-10-05 16:56 UTC] - Protocol Hierarchy Analysis
Ran tshark protocol hierarchy to map out all active network protocols across the 15k packets.
- Command: tshark -r case01/evidence/2026-02-28-traffic-analysis-exercise.pcap -q -z io,phs
- Output saved: case01/output/03_protocol_hierarchy.txt

## [2026-10-05 17:03 UTC] - IP Conversation Mapping
Generated IP conversation statistics to map out endpoints and identify suspicious external connections.
- Command: tshark -r case01/evidence/2026-02-28-traffic-analysis-exercise.pcap -q -z conv,ip
- Output saved: case01/output/03_ip_conversations.txt

