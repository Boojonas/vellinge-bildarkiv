#!/usr/bin/env python3
"""
Jämför en eller flera bilder mot fotografierna i boken Kyrkbyar och städer
i förvandling (Vellinge kommun 1981), med perceptuell hash (dHash och pHash,
64 bitar). Avståndet är det minsta av de två.

Hasharna i kyrkbyar_bildhashar.csv är beräknade på utklipp ur en skanning
av boken (300 dpi gråskala). Kartor och ritningar är inte med.

Användning:
    python jamfor_kyrkbyar.py bild.jpg [fler_bilder.jpg ...] [--topp 5]

Tolkning: 0-5 mycket sannolikt samma bild, 6-10 möjlig träff som bör
kontrolleras visuellt mot boken, över 10 sannolikt inte i boken.
Bild-id KB-sida-löpnummer pekar på sidan i boken. Registeruppgifterna finns
i projektets kyrkbyar_1981_register.md.

Kräver: Pillow. ImageHash (pip install imagehash) ger även pHash och säkrare träffar.
"""
import argparse, csv, os, sys, warnings
from PIL import Image, ImageOps
try:
    import imagehash
except ImportError:  # utan ImageHash används bara dHash
    imagehash = None
warnings.filterwarnings("ignore", category=DeprecationWarning)
MAPP = os.path.dirname(os.path.abspath(__file__))

def dhash(img, hash_size=8):
    """Samma funktion som i jamfor_bild.py och jamfor_vellinge.py."""
    img = img.convert("L").resize((hash_size + 1, hash_size))
    px = list(img.getdata())
    val = 0
    for row in range(hash_size):
        rp = px[row * (hash_size + 1):(row + 1) * (hash_size + 1)]
        for col in range(hash_size):
            val = (val << 1) | (1 if rp[col] > rp[col + 1] else 0)
    return val

def bedomning(a):
    if a <= 5: return "mycket sannolikt samma bild"
    if a <= 10: return "möjlig träff - kontrollera visuellt"
    return "sannolikt inte i boken"

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("bilder", nargs="+")
    p.add_argument("--csv", default=os.path.join(MAPP, "kyrkbyar_bildhashar.csv"))
    p.add_argument("--topp", type=int, default=5)
    a = p.parse_args()
    with open(a.csv, encoding="utf-8") as f:
        bok = list(csv.DictReader(f))
    for r in bok:
        r["_d"] = int(r["dhash"], 16); r["_p"] = int(r["phash"], 16)
    for bild in a.bilder:
        try:
            with Image.open(bild) as im:
                im = ImageOps.exif_transpose(im).convert("L")
                # negativ skannade som negativ: prova även inverterad bild
                # boken visar ofta ett utsnitt av negativet: prova även centrerade utsnitt
                w, h = im.size
                utsnitt = [im] + [im.crop((int(w*(1-f)/2), int(h*(1-f)/2), int(w*(1+f)/2), int(h*(1+f)/2))) for f in (0.92, 0.85, 0.78)]
                varianter = utsnitt + [ImageOps.invert(u) for u in utsnitt]
                hs = [(dhash(v), int(str(imagehash.phash(v)), 16) if imagehash else None) for v in varianter]
        except Exception as e:
            print(f"\n{bild}: kunde inte läsas ({e})", file=sys.stderr); continue
        res = []
        for r in bok:
            avst = min(min(bin(d ^ r["_d"]).count("1"), bin(ph ^ r["_p"]).count("1") if ph is not None else 64) for d, ph in hs)
            res.append((avst, r))
        res.sort(key=lambda t: t[0])
        print(f"\n=== {bild} ===")
        print(f"Slutsats: {bedomning(res[0][0])} (bästa avstånd {res[0][0]})")
        for avst, r in res[:a.topp]:
            plats = f"{r['by']} nr {r['nr']}, {r['fastighet']} (1981)" if r["del"] == "register" else f"{r['by']}: {r['bildtext']}"
            osk = f" [{r['osaker']}]" if r["osaker"] else ""
            print(f"{avst:>5}  {r['id']:<10} s. {r['sida']:<4} {plats[:70]}{osk}  - {bedomning(avst)}")
    print("\nObs: algoritmisk jämförelse. Kontrollera träffar visuellt mot boken.")

if __name__ == "__main__":
    main()
