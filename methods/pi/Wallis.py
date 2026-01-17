import time
from mpmath import mp, mpf
from methods.pomocne_funkce import spravne_desetinne, REAL_PI

def vypocet(typ_limitu, hodnota_limitu):    #Výpočet čísla pí pomocí Wallisovy metody
    #Určení přesnosti výpočtu podle typu limitu
    if typ_limitu == 'iterace':
        mp.dps = 10
    else:
        mp.dps = 25000
    
    #Definování polí pro hodnoty do grafů
    osa_x, presnost_data, rychlost_konvergence = [], [], []

    krok = 1   #Vyznačuje iterace
    pi = mpf(2)   #Průběžná hodnota čísla pí

    pocet_mereni = 50   #Počet bodů zaznamenávaných do grafu

    #Parametry měření
    cas_vypoctu, index_mereni = 0.0, 1
    predchozi_presnost, predchozi_krok, predchozi_cas = 0, 0, 0.0
    
    #Intervaly ukládání hodnot do grafu
    interval_iteraci = max(1, int(hodnota_limitu / pocet_mereni))
    interval_casu = float(hodnota_limitu / pocet_mereni)

    #Přidání nulového bodu na začátek grafů
    osa_x.append(0)
    presnost_data.append(0)
    rychlost_konvergence.append(0)

    #Cyklus pro výpočet metody
    while True:
        start_cas = time.process_time()   #Čas začátku iterace

        #Výpočet jedné iterace
        dva_k = mpf(2*krok)
        pi *= (dva_k * dva_k) / ((dva_k - 1) * (dva_k + 1))

        cas_vypoctu += (time.process_time() - start_cas)   #Postupné přičítání času výpočtu

        #Kontrola ukončení výpočtu
        if (typ_limitu == 'iterace' and krok > hodnota_limitu) or \
           (typ_limitu == 'sekundy' and cas_vypoctu >= hodnota_limitu) or krok > 5000000:
            break

        #Určení, zda se aktuální iterace má uložit
        ulozit = False
        if typ_limitu == 'iterace' and krok >= index_mereni * interval_iteraci:
            ulozit = True
        elif typ_limitu == 'sekundy' and cas_vypoctu >= index_mereni * interval_casu:
            ulozit = True

        #Uložení průběžných hodnot do polí pro grafy
        if ulozit:
            aktualni_presnost = int(spravne_desetinne(pi, REAL_PI))   #Počet správných desetinných míst
            
            #Výpočet rychlosti růstu konvergence podle typu limitu
            if typ_limitu == 'iterace':
                rozdil_kroku = krok - predchozi_krok
                rychlost = float(aktualni_presnost - predchozi_presnost) / rozdil_kroku if rozdil_kroku > 0 else 0
            else:
                rozdil_casu = cas_vypoctu - predchozi_cas
                rychlost = (float(aktualni_presnost - predchozi_presnost) / (rozdil_casu + 1e-12)) * (hodnota_limitu / pocet_mereni)

            #Uložení hodnot do polí pro grafy
            osa_x.append(int(krok) if typ_limitu == 'iterace' else round(cas_vypoctu, 3))
            presnost_data.append(aktualni_presnost)
            rychlost_konvergence.append(float(rychlost))
            
            #Aktualizace předchozích hodnot pro další výpočet rychlosti růstu
            predchozi_presnost, predchozi_krok, predchozi_cas = aktualni_presnost, krok, cas_vypoctu
            index_mereni += 1
            if index_mereni > pocet_mereni: break

        krok += 1   #Přidání iterace

    #Přidání posledního bodu na konec grafu
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
