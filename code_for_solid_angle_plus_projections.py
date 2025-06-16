
import re, math, pathlib
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILES = [
    "hoek_0_c1.csv",  "hoek_0_c2.csv",
    "hoek_20_E_c1.csv","hoek_20_E_c2.csv","hoek_20_W_c1.csv","hoek_20_W_c2.csv",
    "hoek_40_E_c1.csv","hoek_40_E_c2.csv","hoek_40_W_c1.csv","hoek_40_W_c2.csv",
    "hoek_60_E_c1.csv","hoek_60_E_c2.csv","hoek_60_W_c1.csv","hoek_60_W_c2.csv",
]

##############################################################
####################################################################
    #ALL MEASUREMENTES ARE IN METERS
### initial area of the scintillator and table constants
# x_0 is half of the base width of the scintillator
x_0 = 4.5e-2
#y_0 is half of the base length. this does not change with the projections
y_0 = 20.0e-2
#h_0 is the height of the table
h_0 = 86.0e-2

# theta is the angle that the vertical makes with the line that connects both 
# scintillators. Initializing the variable

####CHANGE THIS ANGLE FOR THE DIFFERENT SITUATIONS!!
theta = 0

#FORMULAS FOR THE PROJECTION OF X (THE HALF WIDTH) AND THE DISTANCE BETWEEN BOTH
# SCINTILLATORS H (where h_0 is the height of the table and x_0 is half width of the scintillator)

x_projection = x_0 * math.cos(theta)
h_projection = h_0 * math.cos(theta)



#FUNCTION TO CALCULATE THE SOLID ANGLE
# function to calculate the solid angle
# w is the half width and l is the half length, 
# h is the distance between the centres of both scintillators
# hoek is the angle that the vertical makes with the line that connects both 
# scintillators 
def solid_angle(w, l, h,  hoek):
    return 4*math.atan((w*l)/((h/2) * math.sqrt(w**2 + l ** 2 + (h/2)**2)))


#################################
## call this function with solid_angle( x_projection, y_0, h_projection, theta)


# the effective area can be calculated as:

area = x_projection * y_0






#####################################################################
SURFACE = 0.030551
FILENAME_PATTERN = re.compile(r"hoek_(\d+)(?:_([EW]))?_c\d+\.csv")

tot_N, tot_t, runs = defaultdict(int), defaultdict(float), defaultdict(list)

for fn in CSV_FILES:
    path = pathlib.Path(fn)
    m = FILENAME_PATTERN.fullmatch(path.name)
    if not (m and path.exists()):
        print("⨯", fn, "overgeslagen")
        continue

    theta   = int(m.group(1))
    dir_= m.group(2) or "E"
    key = (theta, dir_)
    hdr = pd.read_csv(path, nrows=1)
    N   = int(hdr["Total coincidences"][0])
    t   = float(hdr["Total runtime (s)"][0])
    flux_run = N / (t * SURFACE)

    tot_N[key] += N
    tot_t[key] += t
    runs[key].append(flux_run)

    if theta == 0 and dir_ == "E":
        key_W = (0, "W")
        tot_N[key_W] += N
        tot_t[key_W] += t
        runs[key_W].append(flux_run)

def flux(N, t):  return N / (t * SURFACE) if t else math.nan
def sigma(N, t): return math.sqrt(N) / (t * SURFACE) if t else math.nan

records = []
for (theta, dir_), N in tot_N.items():
    t  = tot_t[(theta, dir_)]
    f  = flux(N, t)
    sigma  = sigma(N, t)
    rec = {
        "Angle (°)": theta,
        "Direction": "East" if dir_ == "E" else "West",
        "N total": N,
        "t total (s)": round(t, 1),
        "Gem. flux": round(f, 3),
        "Poisson sigma": round(sigma, 3),
        "Min flux": round(min(runs[(theta, dir_)]), 3),
        "Max flux": round(max(runs[(theta, dir_)]), 3),
    }
    records.append(rec)

df = pd.DataFrame(records).sort_values(["Direction", "Angle (°)"])
print("\n=== Samenvatting per hoek & richting ===")
print(df.to_string(index=False))

# ───────── data voor plot ─────────
signed_angles = sorted({a if d=="E" else -a for (a,d) in tot_N})
mean_flux     = [flux(tot_N[(abs(a),"E" if a>=0 else "W")],
                      tot_t[(abs(a),"E" if a>=0 else "W")]) for a in signed_angles]
sig_flux      = [sigma(tot_N[(abs(a),"E" if a>=0 else "W")],
                       tot_t[(abs(a),"E" if a>=0 else "W")]) for a in signed_angles]
rng_lo        = [mean_flux[i] - min(runs[(abs(a),"E" if a>=0 else "W")])
                 for i,a in enumerate(signed_angles)]
rng_hi        = [max(runs[(abs(a),"E" if a>=0 else "W")]) - mean_flux[i]
                 for i,a in enumerate(signed_angles)]
xtick_labels  = [f"{abs(a)}°" for a in signed_angles]

# ───────── plot ─────────
plt.figure(figsize=(8,4))
# range-balk (breed)
plt.errorbar(signed_angles, mean_flux,
             yerr=[rng_lo, rng_hi], fmt="_", lw=0,
             elinewidth=2, capsize=6, label="Bereik (min–max)")
# 1 sigma-balk (smal)
plt.errorbar(signed_angles, mean_flux,
             yerr=sig_flux, fmt="_", lw=0,
             elinewidth=1, capsize=3, label="1 sigma Poisson")

plt.axvline(0, color="k", ls="--", lw=0.7)
plt.xticks(signed_angles, xtick_labels)
plt.xlabel("Hoek theta (°)    West | East")
plt.ylabel("Flux (s$^{-1}$ m$^{-2}$ sr$^{-1}$)")
plt.title("Muon-flux per hoek  (streep-marker, sigma & range)")
plt.grid(True, ls="--", lw=0.4)
plt.legend(loc="upper right")   # legenda verplaatst
plt.tight_layout()
plt.show()
