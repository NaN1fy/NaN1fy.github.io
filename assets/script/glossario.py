import os
from pathlib import Path

def main():
    # Imposta la directory di lavoro nella cartella del file di script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Leggi il contenuto del file glossario.tex
    with open((Path("../data/").glob("glossario*."))[0], 'r', encoding="utf-8") as file:
        lines = file.readlines()
    description = ""
    html_content = ""

    reached_first_section = False

    for line in lines:
        line = line.strip()
        line = line.replace(r"``", '"')  # sostituisci `` con aperte doppie quote
        line = line.replace(r"\`a", "à")  # sostituisci \'a con à
        line = line.replace(r"\`e", "è")  # sostituisci \'e con è
        line = line.replace(r"\`i", "ì")  # sostituisci \'i con ì
        line = line.replace(r"\`o", "ò")  # sostituisci \'o con ò
        line = line.replace(r"\`u", "ù")  # sostituisci \'u con ù

        if reached_first_section:
            if line.startswith(r'\section*{') or line.startswith(r'\subsection*{'):
                term = line.split('{')[-1].split('}')[0]
                if description:
                    html_content += f"<p>{description}</p>\n"
                    description = ""
                if line.startswith(r'\section*{'):
                    html_content += f"<h2>{term}</h2>\n"
                else:
                    html_content += f"<h3>{term}</h3>\n"
            elif line.startswith(r'\newpage') or line.startswith(r'\addcontentsline{toc}{section}{'):
                pass
            else:
                description += line
        elif line.startswith(r'\section*{A}'):
            reached_first_section = True

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

