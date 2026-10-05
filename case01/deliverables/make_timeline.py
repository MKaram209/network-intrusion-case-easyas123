##Script Made By Claude!!

import csv
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# short labels for the chart, matched to the frame numbers in timeline.csv
short = {
    "1": "Capture starts",
    "135": "Host name announced\nDESKTOP-TEYQ2NR",
    "243": "User brolf logs in",
    "339": "Full name found\nBecka Rolf",
    "2569": "First contact\nwith C2 server",
    "2638": "First POST\nNetSupport Manager",
    "3807": "Beaconing:\none POST per minute",
    "15499": "Last beacon",
    "15512": "Capture ends",
}

# read the csv
events = []
with open("notes/timeline.csv") as f:
    for row in csv.DictReader(f):
        t = datetime.strptime(row["time_utc"], "%Y-%m-%d %H:%M:%S")
        events.append((t, short[row["frame"]]))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

# top panel: the first 7 events, staggered up and down so labels don't overlap
early = events[:7]
levels = [1, -1, 2, -2, 1, -1, 2]
for (t, label), y in zip(early, levels):
    ax1.vlines(t, 0, y, color="gray")
    ax1.plot(t, 0, "o", color="tab:red")
    ax1.text(t, y, label, ha="center", va="bottom" if y > 0 else "top", fontsize=9)
ax1.axhline(0, color="black")
ax1.set_ylim(-3.5, 3.5)
ax1.yaxis.set_visible(False)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax1.set_title("First two minutes of the capture (UTC, 2026-02-28)")
for side in ("left", "right", "top"):
    ax1.spines[side].set_visible(False)

# bottom panel: the whole capture, infection active from first C2 contact to the end
start = early[4][0]
end = events[-1][0]
ax2.axvspan(start, end, color="tab:red", alpha=0.4)
ax2.set_xlim(events[0][0], end)
ax2.text(start + (end - start) / 2, 0.5,
         "C2 beaconing, one POST per minute\n19:55:51 to 00:16:28 UTC (about 4h 20m)",
         ha="center", va="center")
ax2.set_yticks([])
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
ax2.set_title("Whole capture (UTC): infection still active when the recording ended")

plt.tight_layout()
plt.savefig("deliverables/timeline.png", dpi=150)
print("saved deliverables/timeline.png")
