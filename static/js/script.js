let grafPresnosti, grafRychlosti;   //Proměnné pro grafy přesnosti a rychlosti
let vybraneMetody = [];
const barvyGrafu = ['teal','green','orange','red','purple','gray'];

//Maximální hodnoty limitů
const max_iteraci = 2000;
const max_sekund = 10;

//KaTeX kódy pro matematické vzorce jednotlibých metod
const matematickeVzorce = {
    //Eulerovo číslo
    'Limita': 'e = \\lim_{n \\to \\infty} \\left(1 + \\frac{1}{n}\\right)^n',
    'Faktorialova_rada': 'e = \\sum_{n=0}^{\\infty} \\frac{1}{n!}',
    'Retezovy_zlomek_e': 'e = 2 + \\cfrac{1}{1 + \\cfrac{1}{2 + \\cfrac{1}{1 + \\cfrac{1}{1 + \\cfrac{1}{4 + \\ddots}}}}}',

    //Číslo pí
    'Leibniz': '\\pi = 4 \\sum_{n=0}^{\\infty} \\frac{(-1)^n}{2n+1}',
    'Chudnovsky': '\\frac{1}{\\pi} = 12 \\sum_{n=0}^{\\infty} \\frac{(-1)^n (6n)! (545140134n + 13591409)}{(3n)! (n!)^3 (640320)^{3n+3/2}}',
    'Viete': '\\frac{2}{\\pi} = \\frac{\\sqrt{2}}{2} \\cdot \\frac{\\sqrt{2+\\sqrt{2}}}{2} \\cdot \\frac{\\sqrt{2+\\sqrt{2+\\sqrt{2}}}}{2} \\dots',
    'Wallis': '\\frac{\\pi}{2} = \\prod_{n=1}^{\\infty} \\left( \\frac{4n^2}{4n^2 - 1} \\right)',
    'Machin': '\\frac{\\pi}{4} = 4\\arctan\\left(\\frac{1}{5}\\right) - \\arctan\\left(\\frac{1}{239}\\right)',
    'Ramanujan': '\\frac{1}{\\pi} = \\frac{2\\sqrt{2}}{9801} \\sum_{n=0}^{\\infty} \\frac{(4n)!(1103+26390n)}{(n!)^4 396^{4n}}',
    'Montecarlo': '\\pi \\approx 4 \\cdot \\frac{\\text{počet bodů v kruhu}}{\\text{celkový počet bodů}}',

    //Číslo fí
    'Fibonacciho_podily': '\\varphi = \\lim_{n \\to \\infty} \\frac{F_{n+1}}{F_n}, \\quad F_n = \\begin{cases} 0 & n=0 \\\\ 1 & n=1 \\\\ F_{n-1} + F_{n-2} & n \\ge 2 \\end{cases}',
    'Retezovy_zlomek_fi': '\\varphi = 1 + \\cfrac{1}{1 + \\cfrac{1}{1 + \\cfrac{1}{1 + \\cfrac{1}{1 + \\ddots}}}}',
    'Pevny_bod': '\\varphi = x_{n+1} = 1 + \\frac{1}{x_n}, \\quad \\begin{cases} x_0 = 1 \\\\ x_{n+1} = 1 + \\frac{1}{x_n} \\end{cases}',
};

//Grafy se inicializují po načtení stránky
window.onload = function() { inicializujGrafy(); };

//Funkce pro inicializaci grafů
function inicializujGrafy() {
    //Nastavení grafů
    const nastaveniGrafu = {
        responsive: true, maintainAspectRatio: false,
        scales: {
            y: { 
                grid: { color: '#cccccc15' }, 
                ticks: { color: '#cccccc70', font: { size: 10 } } 
            },
            x: { 
                grid: { color: '#cccccc15' }, 
                ticks: { color: '#cccccc70', font: { size: 10 } } }
            },
        plugins: { legend: { display: true, labels: { color: '#ffffff', font: { size: 10 }, boxWidth: 10 } } }
    };
    // Vytvoření grafů pro přesnost a rychlost s výchozím nastavením
    grafPresnosti = new Chart(document.getElementById('grafPresnosti'), { type: 'line', data: { labels: [], datasets: [] }, options: nastaveniGrafu });
    grafRychlosti = new Chart(document.getElementById('grafRychlosti'), { type: 'line', data: { labels: [], datasets: [] }, options: nastaveniGrafu });
}

//Funkce pro změnu limitu
function updateLimitu() {
    //Uložení typu a hodnoty limitu při jeho změně
    const typLimitu = document.getElementById('typLimitu').value;
    const hodnotaLimitu = document.getElementById('hodnotaLimitu');
    const napovedaLimitu = document.getElementById('napovedaLimitu');
    const metrika = typLimitu === 'iterace' ? 'DPI' : 'DPT';

    //Přepsání jednotek a max limitu
    if (typLimitu === 'iterace') { hodnotaLimitu.value = 1000; napovedaLimitu.innerText = "Max. 2000"; }
    else { hodnotaLimitu.value = 5; napovedaLimitu.innerText = "Max. 10s"; }

    //Přejmenování grafu rychlosti růstu podle typu metriky a výpis do terminálu
    document.getElementById('nazev-rychlosti').innerText = `Graf rychlosti růstu (${metrika})`;
    document.getElementById('typ-metriky').innerText = metrika;
    vypisDoTerminalu(`Režim změněn na ${typLimitu === 'iterace' ? 'Iterace' : 'Čas'}. Metrika: ${metrika}`);
}

//Funkce pro výpis zpráv do terminálu
function vypisDoTerminalu(zprava, typ = "info") {
    const terminal = document.getElementById('log-simulace');
    const cas = new Date().toLocaleTimeString('cs-CZ', { hour12: false });

    //Barva zprávy podle jejího typu
    const barva =
        typ === 'uspech' ? 'green' :
        typ === 'error'   ? 'red' :
                            'white';

    //Výpis barevné zprávy do terminálu
    terminal.innerHTML += `<div><span>[${cas}]</span> <span style="color:${barva}">> ${zprava}</span></div>`;
    terminal.scrollTop = terminal.scrollHeight;
}

//Funkce pro změnu metod
function prepinacMetody(konstanta, metoda, tlacitko) {
    const identifikator = `${konstanta}-${metoda}`;
    //Ověření, jestli je metoda už ve vybraných metodách
    const index = vybraneMetody.findIndex(m => m.id === identifikator);
    if (index > -1) {
        //Pokud je metoda už vybraná, odstraní se z pole vybraných metod a dojde k odšednutí jejího tlačítka
        vybraneMetody.splice(index, 1);
        tlacitko.style.backgroundColor = '';
        tlacitko.style.color = '';
    } else {
        //Pokud není vybraná, přidá se do seznamu vybraných metod a dojde ke změně barvy jejího tlačítka na šedou
        vybraneMetody.push({ id: identifikator, konstanta, metoda, stitek: `${konstanta.toUpperCase()}: ${metoda}` });
        tlacitko.style.backgroundColor = '#777777';
        tlacitko.style.color = '#000';
        if (matematickeVzorce[metoda]) katex.render(matematickeVzorce[metoda], document.getElementById('matematicky-vzorec'));  //Vykreslení KaTeX vzorce metody
    }
}

//Funkce pro spuštění výpočtu
async function spustSimulaci() {
    //Kontrola jestli je vybraná alespoň jedna metoda
    if (vybraneMetody.length === 0) return vypisDoTerminalu("Chyba: Vyberte metodu.", "error");

    //Uložení zadaných hodnot
    const typLimitu = document.getElementById('typLimitu').value;
    const hodnotaLimitu = parseFloat(document.getElementById('hodnotaLimitu').value);
    const teloTabulky = document.getElementById('telo-vysledku');
    const metrika = typLimitu === 'iterace' ? 'DPI' : 'DPT';

    //Pojistka pro překročení limitu
    if ((typLimitu === 'iterace' && hodnotaLimitu > max_iteraci) ||
        (typLimitu === 'sekundy' && hodnotaLimitu > max_sekund)) {
        return vypisDoTerminalu(`Chyba: Překročen limit.`, "error");
    }

    //Vyprázdnění polí s hodnotami pro grafy a tabulky výsledků
    document.getElementById('typ-metriky').innerText = metrika;
    teloTabulky.innerHTML = '';
    grafPresnosti.data.labels = [];
    grafPresnosti.data.datasets = [];
    grafRychlosti.data.labels = [];
    grafRychlosti.data.datasets = [];

    vypisDoTerminalu(`Výpočet zahájen. Metrika: ${metrika}`);

    //Cyklus pro postupný výpočet metod, volání Python endpointu a naplňování grafů hodnotami
    for (let i = 0; i < vybraneMetody.length; i++) {
        const met = vybraneMetody[i];
        const barva = barvyGrafu[i % barvyGrafu.length];

        try {
            //Zavolání Python API a čekání na odpověď
            const odpoved = await fetch(`/vypocet/${met.konstanta}/${met.metoda}?typLimitu=${typLimitu}&hodnotaLimitu=${hodnotaLimitu}`);
            const data = await odpoved.json();
            if (data.error) throw new Error(data.error);

            //Označení osy x podle zvoleného limitu (iterace/sekundy)
            if (grafPresnosti.data.labels.length === 0) {
                grafPresnosti.data.labels = data['osa-x'];
                grafRychlosti.data.labels = data['osa-x'];
            }

            //Přidání průběžných hodnot výpočtu do grafů            
            grafPresnosti.data.datasets.push({ label: met.stitek, data: data.presnost, borderColor: barva, borderWidth: 2, pointRadius: 1.5, tension: 0.1 });
            grafRychlosti.data.datasets.push({ label: `${met.stitek} (${metrika})`, data: data['rychlost-konvergence'], borderColor: barva, borderWidth: 2, pointRadius: 1.5, tension: 0.1 });

            //Výpis průběžných výsledků do tabulky výsledků
            data['osa-x'].forEach((zaznam, index) => {
                teloTabulky.innerHTML += `<tr>
                    <td>${zaznam}</td>
                    <td>${met.metoda}</td>
                    <td>${Math.floor(data.presnost[index])}</td>
                    <td>${data['rychlost-konvergence'][index].toFixed(4)}</td>
                </tr>`;
            });
            vypisDoTerminalu(`${met.stitek} hotovo.`, "uspech");
        //Výpis případné chyby do terminálu
        } catch (chyba) { vypisDoTerminalu(`Chyba u ${met.stitek}: ${chyba.message}`, "error"); }
    }

    //Aktualizace grafů po přidání nových dat
    grafPresnosti.update();
    grafRychlosti.update();
}

//Funkce pro tlačítko reset
function resetSystemu() {
    //Vynulování vybraných metod
    vybraneMetody = [];
    document.querySelectorAll('#pi-metody button, #e-metody button, #fi-metody button').forEach(btn => {
        btn.style.backgroundColor = '';
        btn.style.borderColor = '';
        btn.style.color = '';
    });

    //Vyprázdnění všech polí s hodnotami
    grafPresnosti.data.labels = [];
    grafPresnosti.data.datasets = [];
    grafRychlosti.data.labels = [];
    grafRychlosti.data.datasets = [];
    grafPresnosti.update();
    grafRychlosti.update();

    //Resetování tabulky výsledků, matematického vzorce metody a výpis resetu do terminálu
    document.getElementById('telo-vysledku').innerHTML = '';
    document.getElementById('log-simulace').innerHTML = `[${new Date().toLocaleTimeString()}] > Systém resetován.`;
    document.getElementById('matematicky-vzorec').innerHTML = 'Matematický vzorec metody';
}
