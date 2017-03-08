#!/usr/bin/env python

import os
import json
from textwrap import wrap
import itertools

import yaml


def read_data():
    with open('content.yaml') as f:
        return yaml.load(f.read())


def load_esv():
    with open('esv.json') as f:
        return json.loads(f.read())


def log(m):
    print m


def get_in(obj, *keys):
    for k in keys:
        v = obj.get(k, None)

        if not v:
            return None

        obj = v

    return obj


def parse_verse(verse):
    """
    Turn this "John 1:3-4" into [("John", "1", "3",), ("John", "1", "4",)]
    """
    parts = verse.split(' ')

    try:
        int(parts[0])
        book = parts[0] + ' ' + parts[1]
        rest = parts[2:]
    except ValueError:
        if parts[0] == 'Song':
            book = 'Song of Solomon'
            rest = parts[3:]
        else:
            book = parts[0]
            rest = parts[1:]

    numbers = ''.join(rest).split(':')

    if len(numbers) == 1:
        if book in ['Jude']:
            return [(book, "1", numbers[0])]
        else:
            return [(book, numbers[0])]

    chapter = numbers[0]

    verses = numbers[1:][0]

    def verse_range(book, chapter, verses):
        verses = verses.replace(' ', '')
        start, end = verses.split('-')
        start, end = int(start), int(end)
        verses = []

        for x in range(0, 1 + end - start):
            verses.append((book, chapter, str(start + x)))

        return verses

    if ',' in verses:
        verse_parts = verses.split(',')
        result = []

        for v in verse_parts:
            if '-' in v:
                result.append(verse_range(book, chapter, v))
            else:
                result.append([(book, chapter, v)])

        return list(itertools.chain(*result))

    if '-' in verses:
        return verse_range(book, chapter, verses)

    return [
        (book, chapter, verses)
    ]


def print_latex_preamble(out):
    with open('latex-preamble.tex') as f:
        out.write(f.read() + '\n')


def render_latex(data, args):
    """
    * letter paper
    * letter paper landscape two sided
    * footnotes
    * verses inline
    * a4
    * a4 landscape
    * toc
    """
    return render_latex_base(data, args)


def render_latex_base(data, args):
    footnotes = True

    filename = os.path.join(args.build_dir, '1689.tex')

    if not args.clear:
        log('Skipping latex')
        return

    log('Writing latex')

    with open(filename, 'w') as f:

        print_latex_preamble(f)

        for chapter in data['chapters']:
            f.write('\chapter{Chapter ' + str(chapter['number']) + ' - ' + chapter['name'] + '}\n')

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
            f.write('## Chapter ' + str(chapter['number']) + ' -  ' +
                    chapter['name'] + '\n\n')

            for article in chapter['articles']:
                f.write('### Article ' + str(article['number']) + '\n\n')

                text = article['text'].replace('\n', '\n\n')

                for line in wrap(text, width=79):
                    f.write(line + '\n')

                f.write('\n')

                if not args.esv:
                    continue

                for verse_ref, verse_text in article['esv']:
                    if isinstance(verse_text, list):
                        verse_text = '\n'.join(verse_text)

                    for line in wrap(verse_text, width=77):
                        f.write('> ' + line + '\n')

                    f.write('> (' + verse_ref + ')\n')
                    f.write('\n')

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


def render_json(data, args):
    filename = os.path.join(args.build_dir, '1689.json')

    if not args.clear:
        log('Skipping json')
        return

    log('Writing json')

    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=4))


def render_index(args):
    filename = os.path.join(args.build_dir, 'index.html')

    if not args.clear:
        log('Skipping index')
        return

    log('Writing index')

    html = """
    """

    with open(filename, 'w') as f:
        f.write(html)


def populate_with_verses(esv, data):
    for chapter_index, chapter in enumerate(data['chapters']):
        for article_index, article in enumerate(chapter['articles']):
            for verse_index, verse in enumerate(article['verses']):
                verses = parse_verse(verse)

                for v in verses:
                    esv_verse = get_in(esv, *v)

                    if not esv_verse:
                        raise Exception('Cant find verse')

                    if not isinstance(esv_verse, basestring):
                        keys = list(map(int, esv_verse.keys()))
                        keys.sort()
                        nice = []

                        for k in keys:
                            vv = esv_verse[str(k)]
                            nice.append(vv)

                        esv_verse = nice

                    esv_verse = (verse, esv_verse)

                    # LOL, do you even lens?

                    if 'esv' not in data['chapters'][chapter_index]['articles'][article_index]:
                        data['chapters'][chapter_index]['articles'][article_index]['esv'] = []

                    data['chapters'][chapter_index]['articles'][article_index]['esv'].append(esv_verse)

    return data


def main(args):
    data = read_data()
    esv = load_esv()

    if args.esv:
        data = populate_with_verses(esv, data)

    if not os.path.exists(args.build_dir):
        os.mkdir(args.build_dir)

    render_latex(data, args)
    render_markdown(data, args)
    render_org(data, args)
    render_json(data, args)

    render_index(args)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build 1689 documents')
    parser.add_argument('-d', '--dir', type=str, metavar='DIR',
                        default='_build', dest='build_dir',
                        help='Build directory')
    parser.add_argument('-c', '--clear', action='store_true', dest='clear',
                        help='Clear build files')
    parser.add_argument('-e', '--esv', action='store_true', dest='esv',
                        help='Add ESV verses')
    args = parser.parse_args()
    main(args)
