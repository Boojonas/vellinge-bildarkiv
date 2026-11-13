#!/usr/bin/env python3
"""
Jämför en eller flera bilder mot Vellinge bildarkiv (Sofie) med perceptuell
hash (dHash, 64 bitar), för att upptäcka bilder som redan finns i arkivet.

Hasharna i vellinge_bildhashar.csv är beräknade på tumnaglar ur Sofies
objektlista (november 2026). Bilder som beslutats tas bort är inte med.

Användning:
    python jamfor_vellinge.py bild.jpg [fler_bilder.jpg ...] [--topp 5]

Kräver: Pillow  (pip install pillow)
"""
import argparse, csv, os, sys, warnings
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

MAPP = os.path.dirname(os.path.abspath(__file__))


def dhash(img, hash_size=8):
    """Samma funktion som i jamfor_bild.py."""
    img = img.convert("L").resize((hash_size + 1, hash_size))
    px = list(img.getdata())
    val = 0
    for row in range(hash_size):
        rp = px[row * (hash_size + 1):(row + 1) * (hash_size + 1)]
        for col in range(hash_size):
            val = (val << 1) | (1 if rp[col] > rp[col + 1] else 0)
    return val


def bedomning(a):
    if a <= 5:
        return "mycket sannolikt samma bild"
    if a <= 10:
        return "möjlig träff - kontrollera visuellt"
    return "sannolikt inte i arkivet"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("bilder", nargs="+")
    p.add_argument("--csv", default=os.path.join(MAPP, "vellinge_bildhashar.csv"))
    p.add_argument("--topp", type=int, default=5)
    a = p.parse_args()
    with open(a.csv, encoding="utf-8") as f:
        arkiv = [(int(r["dhash"], 16), r["bildnr"]) for r in csv.DictReader(f)]
    for bild in a.bilder:
        try:
            with Image.open(bild) as im:
                h = dhash(im)
        except Exception as e:
            print(f"\n{bild}: kunde inte läsas ({e})", file=sys.stderr)
            continue
        traffar = sorted((bin(h ^ x).count("1"), nr) for x, nr in arkiv)[:a.topp]
        print(f"\n=== {bild} ===")
        print(f"Slutsats: {bedomning(traffar[0][0])} (bästa avstånd {traffar[0][0]})")
        for avst, nr in traffar:
            print(f"{avst:>5}  {nr:<20} {bedomning(avst)}")
    print("\nObs: algoritmisk jämförelse. Kontrollera träffar visuellt i Sofie.")


if __name__ == "__main__":
    main()
