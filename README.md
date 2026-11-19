# Vellinge bildarkiv – bildhashar

Perceptuella hashar för bilderna i Vellinge bildarkiv (Sofie). Används för att
kontrollera om en bild redan finns inlagd innan den katalogiseras.

## Innehåll

- `vellinge_bildhashar.csv` – en rad per bild: `bildnr`, `dhash`, `phash`, `width`, `height`.
- `jamfor_vellinge.py` – jämför en eller flera bilder mot hashfilen.
- `kyrkbyar_bildhashar.csv` – hashar för de 1 678 fotografierna i boken *Kyrkbyar och städer i förvandling* (Vellinge kommun 1981): bild-id (KB-sida-löpnummer), sida, by, registrets löpnummer, fastighetsbeteckning (1981) och bildtext, `dhash`, `phash`. Kartor och ritningar är inte med.
- `jamfor_kyrkbyar.py` – jämför en eller flera bilder mot bokens fotografier. Provar även centrerade utsnitt och inverterad bild.

`vellinge_bildhashar.csv` innehåller bara bildnummer och hashar, inga titlar, beskrivningar eller bilder. Bokens hashfil innehåller uppgifter som står tryckta i boken, men inga namn ur registret.

## Användning

```
git clone https://github.com/Boojonas/vellinge-bildarkiv
python3 vellinge-bildarkiv/jamfor_vellinge.py ny_bild.jpg [fler_bilder.jpg ...]
python3 vellinge-bildarkiv/jamfor_kyrkbyar.py ny_bild.jpg [fler_bilder.jpg ...]
```

Kräver Pillow (`pip install pillow`).

Avstånd 0–5: mycket sannolikt samma bild. 6–10: möjlig träff, kontrollera visuellt.
Över 10: sannolikt inte i arkivet.

## Om hasharna

- dHash, 64 bitar, samma funktion som `jamfor_bild.py` i repot pljungen-bildarkiv.
- Beräknade på tumnaglar (ca 200 px) ur Sofies objektlista, november 2026.
- Bilder som beslutats tas bort vid dubblettgallringen är inte med.
- Bilder som läggs in i Sofie efter november 2026 finns inte med förrän filen uppdateras.

Jämförelsen är algoritmisk. Kontrollera alltid träffar visuellt i Sofie.
