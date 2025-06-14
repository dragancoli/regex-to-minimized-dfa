# Konverter Regularnih Izraza u Minimizovani DKA

Ovaj projekat je implementacija kompletnog alata za transformaciju regularnog izraza u ekvivalentni, minimizovani i potpuno definisani deterministički konačni automat (DKA). Alat je realizovan u programskom jeziku **[Python]** i koristi isključivo standardnu biblioteku.


---

## ✨ Ključne funkcionalnosti

* **Potpuna transformacija**: Konvertuje regularni izraz kroz faze: Neka-ε → Neka → DKA → Minimizovani DKA.
* **Korisnički definisan alfabet**: Podržava alfabete sa višekarakternim simbolima (npr. `START`, `AB`, `10`).
* **Napredna sintaksa**: Pored standardnih operacija (unija, konkatenacija, Kleeneova zvezda), podržava i operatore ponavljanja (`{N}`, `{N,}`, `{N,M}`).
* **Parser sa rekurzivnim spustom**: Implementiran je robustan parser za leksičku, sintaksičku i semantičku analizu izraza.
* **Precizno prijavljivanje grešaka**: U slučaju nevalidnog izraza, ispisuje se jasna poruka o grešci sa tačnom pozicijom problema.
* **Jedinični testovi**: Algoritmi su detaljno testirani pomoću skupa jediničnih testova.
* **Čist kod**: Projekat se pridržava principa čistog koda i sadrži adekvatnu dokumentaciju.

---

## ⚙️ Podržana sintaksa

| Operacija | Simbol/Sintaksa | Primer | Opis |
| :--- | :--- | :--- | :--- |
| Grupisanje | `( )` | `(a+b)` | Menja prioritet izvršavanja operacija. |
| Konkatenacija | _(nema simbola)_ | `ab` | Nizanje simbola. |
| Unija (ILI) | `+` | `a+b` | Prihvata `a` ili `b`. |
| Kleeneova zvezda | `*` | `a*` | Nula ili više ponavljanja `a`. |
| Ponavljanje N puta | `{N}` | `a{3}` | Tačno `N` ponavljanja `a`. |
| Bar N puta | `{N,}` | `a{2,}` | Najmanje `N` ponavljanja `a`. |
| N do M puta | `{N,M}` | `a{2,4}` | Između `N` i `M` ponavljanja `a`. |
| Prazan string | `ε` | `a+ε` | Specijalni simbol za prazan string. |

---

## 🧪 Testiranje

Projekat sadrži skup jediničnih testova koji pokrivaju sve ključne funkcionalnosti, uključujući parsiranje, sve operatore i sve faze transformacije automata. Testovi osiguravaju korektnost i robusnost implementacije.
