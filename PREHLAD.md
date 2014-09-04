# Rychly prehlad gaminator interface-u

Prevazne na prikladoch.

## Farba

  - `Farba(r, g, b)` - konstruktor
  - `Farba.CIERNA`
  - `Farba.BIELA`
  - `Farba.MODRA`
  - `Farba.ZELENA`
  - `Farba.CERVENA`
  - `Farba.ZLTA`
  - `Farba.ZLTA*0.3 + Farba.MODRA*0.7`
  - `Farba.BIELA.zmixuj(Farba.MODRA)`
  
## okno
Zmeny sa prejavia v dalsom cykle.

  - `okno.vyska`
  - `okno.sirka`
  - `okno.nazov`
  - `okno.celaObrazovka()` - fullscreen
  - `okno.pevne()` - not resizable window 
  - `okno.dynamicke()` - resizable window
  
## Kreslic

  - `x` - relativna suradnicova sustava oproti zaciatku obrazovky
  - `y` - relativna suradnicova sustava oproti zaciatku obrazovky
  - `farba`
  - `obdlznik((x, y), sirka, vyska, okraj)` - ak okraj nepoviete
    tak je vyplneny
  - `elipsa((x, y), sirka, vyska, okraj)` - ak okraj nepoviete
    tak je vyplnena
  - `mhohouholnik([(x, y), ...], okraj)` - ak okraj nepoviete
    tak je vyplneny
  - `ciara((x, y), (x, y), hrubka)`
  
## Svet
Svet je definuje prostredie v hre. Svet je napriklad menu alebo mod hry.
`hra` poskytuje stack svetov.

  - `krok()` - MOZNO PRETAZIT. Spusti sa v kazdom cykle
  - `nastav()` - MOZNO PRETAZIT. Spusti sa pri inicializacii
  - `cas` - pocet milisekund bezania TOHTO sveta
  - `stlacene` - napr. `stlacene[pygame.K_UP]` je `true` ak *K* bolo
    stlacene na zaciatku 
  - `nastalaUdalost("udalost", ...)` - Vytvori novu udalost.
    Spracuje sa v dalsom cykle
  - `nacasujUdalost(milisekundy, "udalost", ...)` - Vytvori novu udalost.
    Spracuje sa v prvom cykle po uplynuti casu.
  
## Vec
Vec je akykolvek objekt vo Svete. Existuje iba v jednom svete,
ktory dostane v konstruktore.

  - `x` - stred
  - `y` - stred
  - `z` - poradie vykreslenia
  - `miestoHore` - pouzivaju kolizie
  - `miestoDole` - pouzivaju kolizie
  - `miestoVpravo` - pouzivaju kolizie
  - `miestoVlavo` - pouzivaju kolizie
  - `krok()` - MOZNO PRETAZIT. Spusti sa v kazdom cykle
  - `nastav()` - MOZNO PRETAZIT. Spusti sa pri inicializacii
  - `nakresli(kreslic)` - MOZNO PRETAZIT. Spusti sa v kazdom cykle,
    kreslic je nastaveny na stred objektu.
  - `svet`
  - `znic()` - zrusi Vec zo sveta - dalej je nepouzitelna
  - `prekryva(vec)` - zisti ci je tato vec s druhou v kolizii
  
## Udalosti
Udalosti pouzivaju dekoratory - moze ich byt lubovolne vela pred funkciou,
ktora sa ma pri danej udalosti zavolat. Funguje na clenske metody Veci a Svetu.

  - `@priUdalosti("udalost")` - nasledujuca funkcia sa zavola,
    ak nastane `"udalost"`.
  - `@priZrazke(Trieda1, Trieda2, ...)` - nasledujuca funkcia sa zavola,
    ak sa tento objekt zrazi s objektom, ktory dedi od danych Tried.
    Funguje iba na veci.
    

## hra
Obsahuje stack Svetov

  - `zacni(svet)` - spusti hlavny cyklus s danym svetom
  - `koniec()` - ukonci aplikaciu
  - `otvorSvet(svet)` - stack push
  - `zavorSvet(svet)` - stack pop
  - `nahradSvet(svet)` - stack pop + stack push
    



  
  
  
  
  

  
  
