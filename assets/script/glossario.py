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
            next(reader) 
            rows = list(reader)
    else:
        print("\nno glossary found!\n")
        return

    html_content = ""
    last_initial = None 

    rows.sort(key=lambda x: x[0])

    for row in rows:
        termine = row[0].strip()
        descrizione = row[1].strip()
        
        descrizione = descrizione.replace(r"``", '"')
        descrizione = descrizione.replace(r"\`a", 'à')
        descrizione = descrizione.replace(r"\`e", 'è')
        descrizione = descrizione.replace(r"\`i", 'ì')
        descrizione = descrizione.replace(r"\`o", 'ò')
        descrizione = descrizione.replace(r"\`u", 'ù')

        if termine[0] != last_initial:
            html_content += f"<h2 id='{termine[0]}'>{termine[0]}</h2>\n"
            last_initial = termine[0]

        html_content += f"<h3>{termine}</h3>\n<p>{descrizione}</p>\n"

    with open('../../glossario.html', 'r', encoding="utf-8") as file:
        html_template = file.read()

    span_start_index = html_template.find('<span id="glossario" class="section">')
    span_end_index = html_template.find('</span>', span_start_index)

    if span_start_index != -1 and span_end_index != -1:
        html_output = html_template[:span_start_index] + f'<span id="glossario" class="section">{html_content}</span>' + html_template[span_end_index + len('</span>'):]
    else:
        html_output = html_template.replace('<span id="glossario" class="section">', f'<span id="glossario" class="section">{html_content}')

    with open('../../glossario.html', 'w', encoding="utf-8") as file:
        file.write(html_output)
        
    print("\nsuccess!\n")

if __name__ == "__main__":
    main()

