import time
from mpmath import mp, mpf
from methods.pomocne_funkce import spravne_desetinne, REAL_PI

def vypocet(typ_limitu, hodnota_limitu):    #Výpočet čísla pí pomocí Machinova vzorce
    #Určení přesnosti výpočtu podle typu limitu
    if typ_limitu == 'iterace':
        mp.dps = 3000
    else:
        mp.dps = 25000
    
    #Definování polí pro hodnoty do grafů
    osa_x, presnost_data, rychlost_konvergence = [], [], []

    krok = 1    #Vyznačuje iterace
    x1 = mpf(1) / 5     #Hodnota 1/5 pro Machinův vzorec
    x2 = mpf(1) / 239   #Hodnota 1/239 pro Machinův vzorec
    x1_nadruhou = x1 * x1   #Druhá mocnina x1 (pro opakované násobení)
    x2_nadruhou = x2 * x2   #Druhá mocnina x2 (pro opakované násobení)

    soucet1 = mpf(0)    #Průběžný součet prvních členů
    soucet2 = mpf(0)    #Průběžný součet druhých členů

    clen1 = x1  #Průběžný člen první řady
    clen2 = x2  #Průběžný člen první řady

    delitel = mpf(1)    #Průběžný dělitel v každé iteraci
    ctyri = mpf(4)      #Převedení čísla 4 na přesnost nastavenou výše, aby nedocházelo ke konverzi datových typů každou iteraci

    #Parametry měření
    pocet_mereni = 50                           #Počet bodů zaznamenávaných do grafu
    cas_vypoctu, index_mereni = 0.0, 1          #Celkový čas výpočtu a index aktuálního měření
    predchozi_presnost, predchozi_krok, predchozi_cas = 0, 0, 0.0  #Hodnoty z předchozího měření (pro výpočet rychlosti růstu)
    
    #Intervaly ukládání
    interval_iteraci = max(1, int(hodnota_limitu / pocet_mereni))
    interval_casu = float(hodnota_limitu / pocet_mereni)

    #Přidání nulového bodu na začátek grafů
    osa_x.append(0)
    presnost_data.append(0)
    rychlost_konvergence.append(0)

    #Cyklus pro výpočet metody
    while True:
        start_cas = time.process_time()    #Čas začátku iterace

        #Výpočet jedné iterace
        soucet1 += clen1 / delitel
        soucet2 += clen2 / delitel

        pi = ctyri * (ctyri * soucet1 - soucet2)
        
        #Posun hodnot pro další iteraci
        clen1 *= -x1_nadruhou
        clen2 *= -x2_nadruhou
        delitel += 2

        cas_vypoctu += (time.process_time() - start_cas)    #Postupné přičítání času výpočtu

        #Kontrola ukončení výpočtu
        if (typ_limitu == 'iterace' and krok > hodnota_limitu) or \
           (typ_limitu == 'sekundy' and cas_vypoctu >= hodnota_limitu) or krok > 5000000:
            break

        #Určení, zda se určitá iterace má uložit
        ulozit = False
        if typ_limitu == 'iterace' and krok >= index_mereni * interval_iteraci:
            ulozit = True
        elif typ_limitu == 'sekundy' and cas_vypoctu >= index_mereni * interval_casu:
            ulozit = True

        #Uložení každé iterace odpovídající intervalu ukládání
        if ulozit:
            aktualni_presnost = int(spravne_desetinne(pi, REAL_PI))    #Zjištění počtu správných desetinných míst
            
            #Výpočet rychlosti růstu konvergence podle typu limitu
            if typ_limitu == 'iterace':
                rozdil_kroku = krok - predchozi_krok
                rychlost = float(aktualni_presnost - predchozi_presnost) / rozdil_kroku if rozdil_kroku > 0 else 0
            else:
                rozdil_casu = cas_vypoctu - predchozi_cas
                rychlost = (float(aktualni_presnost - predchozi_presnost) / (rozdil_casu + 1e-12)) * (hodnota_limitu / pocet_mereni)

            #Uložení průběžných hodnot do polí
            osa_x.append(int(krok) if typ_limitu == 'iterace' else round(cas_vypoctu, 3))
            presnost_data.append(aktualni_presnost)
            rychlost_konvergence.append(float(rychlost))
            
            #Aktualizace posledních hodnot (pro výpočet rychlosti růstu)
            predchozi_presnost, predchozi_krok, predchozi_cas = aktualni_presnost, krok, cas_vypoctu
            index_mereni += 1

        krok += 1    #Přidání iterace

    #Uložení posledního bodu na konec grafu (pokud tam ještě není)
    posledni_hodnota = hodnota_limitu
    
    if not osa_x or osa_x[-1] != posledni_hodnota:
        posledni_presnost = int(spravne_desetinne(pi, REAL_PI))
        
        #Výpočet rychlosti růstu pro poslední bod
        if typ_limitu == 'iterace':
            rozdil = hodnota_limitu - predchozi_krok
            rychlost = float(posledni_presnost - predchozi_presnost) / rozdil if rozdil > 0 else 0
        else:
            rozdil = cas_vypoctu - predchozi_cas
            rychlost = (float(posledni_presnost - predchozi_presnost) / (rozdil + 1e-12)) * (hodnota_limitu / pocet_mereni)

        osa_x.append(posledni_hodnota)
        presnost_data.append(posledni_presnost)
        rychlost_konvergence.append(float(rychlost))

    #Vrácení dat pro grafy
    return {
        "osa-x": osa_x,
        "presnost": presnost_data,
        "rychlost-konvergence": rychlost_konvergence
    }