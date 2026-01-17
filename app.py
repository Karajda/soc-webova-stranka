from flask import Flask, render_template, jsonify, request
import importlib

app = Flask(__name__)  #Inicializace Flask aplikace

#Hlavní stránka
@app.route('/')
def uvodni_stranka():
    return render_template('index.html')    #Vrací HTML šablonu hlavní stránky (index.html)

#Endpoint pro výpočet zvolené metody
@app.route('/vypocet/<konstanta>/<metoda>')
def vypocet(konstanta, metoda):
    #Získání typu a hodnoty limitu z URL
    typ_limitu = request.args.get('typLimitu', 'iterace')
    hodnota_limitu = request.args.get('hodnotaLimitu', '1000')
    
    #Převod hodnoty limitu na číslo, při chybě nastavení na 1000
    try:
        limit = float(hodnota_limitu)
    except ValueError:
        limit = 1000

    try:
        #Načtení správného modulu s metodou
        cesta_k_metode = f"methods.{konstanta}.{metoda}"
        matematicka_metoda = importlib.import_module(cesta_k_metode)
        
        #Spuštění výpočtu a vrácení výsledků jako json
        vysledky = matematicka_metoda.vypocet(typ_limitu, limit)
        return jsonify(vysledky)
        
    except Exception as chyba:
        #Při chybě se zpráva vypíše do terminálu a vrátí prázdná data
        print(f"CHYBA MODULU: {chyba}")
        return jsonify({
            "osa-x": [],                #Popisky osy x pro grafy (iterace / sekundy)
            "presnost": [],             #Hodnoty přesnosti (Správná desetinná místa)
            "rychlost-konvergence": [], #Hodnoty rychlosti růstu (DPI/DPT)
            "error": str(chyba)         #Text chyby pro terminál
        })

#Spuštění aplikace
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
