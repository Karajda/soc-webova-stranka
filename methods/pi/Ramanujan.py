import time
from mpmath import mp, mpf, sqrt
from methods.pomocne_funkce import spravne_desetinne, REAL_PI

def vypocet(typ_limitu, hodnota_limitu):    #Výpočet čísla pí pomocí Ramanujanovy řady
    #Určení přesnosti výpočtu podle typu limitu
    if typ_limitu == 'iterace':
        mp.dps = 15000
    else:
        mp.dps = 25000
    
    #Definování polí pro hodnoty do grafů
    osa_x, presnost_data, rychlost_konvergence = [], [], []

    krok = 0    #Vyznačuje iterace
    pi_obracene = mpf(0)    #Průběžná hodnota obrácené hodnoty pí (1/pi)
    nasobitel = 2 * sqrt(mpf(2)) / 9801 #Konstantní násobitel v každé iteraci

    fac_4k = mpf(1)         #Průběžná hodnota 4k!
    fac_k4 = mpf(1)         #Průběžná hodnota k^4
    mocnina_396_4 = mpf(1)  #Průběžná hodnota 396^4

    konst_a = mpf(1103)     #Konstantní hodnota 1103
    konst_b = mpf(26390)    #Konstantní hodnota 26390
    konst_396_4 = mpf(396) ** 4 #Konstantní hodnota 396^4

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
        citatel = fac_4k * (konst_a + konst_b * krok)   
        jmenovatel = fac_k4 * mocnina_396_4             
        pi_obracene += citatel / jmenovatel             
        pi = 1 / (nasobitel * pi_obracene)              
        
        #Posun hodnot pro další iteraci
        krok += 1
        fac_k4 *= krok ** 4
        fac_4k *= (4*krok - 3) * (4*krok - 2) * (4*krok - 1) * (4*krok)
        mocnina_396_4 *= konst_396_4

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