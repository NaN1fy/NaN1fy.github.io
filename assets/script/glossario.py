import csv
import os
from pathlib import Path

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    file_paths = list(Path("../data/").glob("glossario*.csv"))

    if file_paths:
        with open(file_paths[0], 'r', encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Skip header row
            rows = list(reader)
    else:
        print("Nessun file corrispondente al modello 'glossario*.' trovato.")
        return

    html_content = ""

    for row in rows:
        termine = row[0].strip()
        descrizione = row[1].strip()

        # Sostituisci le doppie virgolette con aperte doppie quote
        descrizione = descrizione.replace(r"``", '"')
        descrizione = descrizione.replace(r"\`a", 'à')
        descrizione = descrizione.replace(r"\`e", 'è')
        descrizione = descrizione.replace(r"\`i", 'ì')
        descrizione = descrizione.replace(r"\`o", 'ò')
        descrizione = descrizione.replace(r"\`u", 'ù')

        # Aggiungi termine e descrizione al contenuto HTML
        html_content += f"<h3 id='{termine[0]}'>{termine}</h3>\n<p>{descrizione}</p>\n"

    # Leggi il contenuto del file glossario.html
    with open('../../glossario.html', 'r', encoding="utf-8") as file:
        html_template = file.read()

    span_start_index = html_template.find('<span id="glossario" class="section">')
    span_end_index = html_template.find('</span>', span_start_index)

    # Sostituisci il contenuto esistente con il nuovo contenuto
    html_output = html_template[:span_start_index] + f'<span id="glossario" class="section">{html_content}</span>' + html_template[span_end_index + len('</span>'):]

    # Scrivi il risultato nel file glossario.html
    with open('../../glossario.html', 'w', encoding="utf-8") as file:
        file.write(html_output)

    print("Contenuto del glossario integrato con successo")

if __name__ == "__main__":
    main()

