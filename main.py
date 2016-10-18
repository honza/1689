import os
from textwrap import wrap

import yaml


def read_data():
    with open('content.yaml') as f:
        return yaml.load(f.read())


def log(m):
    print(m)


def print_latex_preamble(out):
    with open('latex-preamble.tex') as f:
        out.write(f.read() + '\n')


def render_latex(data, args):
    footnotes = True

    filename = os.path.join(args.build_dir, '1689.tex')

    if not args.clear:
        log('Skipping latex')
        return

    log('Writing latex')

    with open(filename, 'w') as f:

        print_latex_preamble(f)

        for chapter in data['chapters']:
            f.write('\chapter{' + chapter['name'] + '}\n')

            for article in chapter['articles']:
                f.write('\section{Article ' + str(article['number']) + '}\n\n')
                text = article['text'].replace('\n', '\n\n')

                if footnotes:
                    verses = ' '.join(article['verses'])
                    f.write(text + '\\footnote{' + verses + '}\n')
                else:
                    f.write(text + '\n')

                f.write('\n')

        f.write('\end{document}')


def render_html(data):
    pass


def render_markdown(data, args):
    filename = os.path.join(args.build_dir, '1689.md')

    if not args.clear:
        log('Skipping markdown')
        return

    log('Writing markdown')

    with open(filename, 'w') as f:

        f.write('# 1689 Second London Confession of Faith\n\n')

        for chapter in data['chapters']:
            f.write('## ' + chapter['name'] + '\n\n')

            for article in chapter['articles']:
                f.write('### Article ' + str(article['number']) + '\n\n')

                text = article['text'].replace('\n', '\n\n')

                for line in wrap(text, width=79):
                    f.write(line + '\n')

                f.write('\n')


def render_org(data, args):
    filename = os.path.join(args.build_dir, '1689.org')

    if not args.clear:
        log('Skipping org')
        return

    log('Writing org')
    with open(filename, 'w') as f:

        f.write('* 1689 Second London Confession of Faith\n')

        for chapter in data['chapters']:
            f.write('** ' + chapter['name'] + '\n')

            for article in chapter['articles']:
                f.write('*** Article ' + str(article['number']) + '\n\n')

                text = article['text'].replace('\n', '\n\n')

                for line in wrap(text, width=75):
                    f.write('    ' + line + '\n')

                f.write('\n')


def main(args):
    data = read_data()

    if not os.path.exists(args.build_dir):
        os.mkdir(args.build_dir)

    render_latex(data, args)
    render_markdown(data, args)
    render_org(data, args)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build 1689 documents')
    parser.add_argument('-d, --dir', type=str, metavar='DIR', default='_build',
                        dest='build_dir', help='Build directory')
    parser.add_argument('-c, --clear', action='store_true', dest='clear',
                        help='Clear build files')
    args = parser.parse_args()
    main(args)
