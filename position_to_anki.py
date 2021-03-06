#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
import os
import sys
import subprocess
import tempfile


def get_position(soup):
    position = soup.find_all('table')[0].find_all('td')[0].get_text('\n')
    # remove emply lines at beginning/end
    position = '\n'.join([line for line in position.split('\n') if line.strip() != ''])

    return position

def get_analysis(soup):
    return soup.find_all('table')[2]

def get_best_move(soup):
    return get_analysis(soup).find_all('tr')[0].find_all('td')[2].get_text()

def get_xgid(soup):
    return [t.get_text() for t in soup.find_all('td') if 'XGID' in t.get_text()][0].strip()

def positions_to_tex(positions):
    with open('latex/template.tex') as f:
        positions = map(lambda position: '\\begin{board}\n' + position + '\n\\end{board}', positions)
        positions = '\n\\newpage\n'.join(positions)
        tex = f.read()
        tex = tex.replace('__POSITIONS__', positions)
        return tex

def tex_to_pdf(tex):
    tmp = tempfile.mkstemp()[1] # ignore file handler

    subprocess.run([
        'lualatex',
        f"--output-directory={os.path.dirname(tmp)}",
        f"--jobname={os.path.basename(tmp)}"
        ],
        input=tex.encode('utf-8')
    )

    return tmp

def pdf_to_png(path_to_pdf, output_dir, output_filename):
    if not path_to_pdf.endswith('.pdf'):
        path_to_pdf = f"{path_to_pdf}.pdf"

    # create subfolder 'png'
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print(f"ERROR: {output_dir} exists and is not a directory")
        sys.exit(1)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    subprocess.run([
        'convert',
        '-density', '600',
        '-quality', '100',
        '-trim',
        path_to_pdf,
        '-scene', '1',
        f"{output_dir}/{output_filename}.png"
        ]
    )

def delete_latex_files(filename):
    os.remove(f"{filename}")
    os.remove(f"{filename}.pdf")
    os.remove(f"{filename}.log")
    os.remove(f"{filename}.aux")

def positions_to_anki(positions, output_dir):
    # create subfolder
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print(f"ERROR: {output_dir} exists and is not a directory")
        sys.exit(1)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with open(f"{output_dir}/anki-cards.txt", 'w', newline='') as csvfile:
        # \t is the separator between front and back
        cardwriter = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

        for position in positions:
            cardwriter.writerow([
                f"""<img src="{position['image']}">""",
                f"""<center>{position['title']} - Best move: {position['best']}</center><br>
                    {position['analysis']}
                    <center><small>{position['xgid']}</small></center>"""
            ])
            # TODO: tags? -> chapter name

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print(f"USAGE: {sys.argv[0]} <position1.html> [<position2.html>, ...]")
        sys.exit(1)

    PREFIX = '501-essential-backgammon-problems'
    PNG_OUTPUT_DIR = 'png'
    CARD_OUTPUT_DIR = 'cards'
    positions = []
    problems = []
    
    for f in sys.argv[1:]:
        if not f.endswith('.html'):
            continue

        with open(f) as fh:
            html_doc = fh.read()
            problem_number = int(os.path.basename(f).strip('.html'))
            soup = BeautifulSoup(html_doc, 'html.parser')

            positions.append(get_position(soup))
            problems.append({
                'image': '',
                'analysis': get_analysis(soup),
                'best': get_best_move(soup),
                'xgid': get_xgid(soup),
                'title': f"Problem {problem_number}",
                'tags': 'TODO'
            })

    tex = positions_to_tex(positions)
    tempfile = tex_to_pdf(tex)
    pdf_to_png(tempfile, PNG_OUTPUT_DIR, PREFIX)
    delete_latex_files(tempfile)

    for i, problem in enumerate(problems, start=1):
        problem['image'] = f"{PREFIX}-{i}.png"

    positions_to_anki(problems, CARD_OUTPUT_DIR)
    print('move pngs into collection.media: ~/.local/share/Anki2/<User>/collection.media/')
