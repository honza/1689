import yaml


def read_data():
    with open('content.yaml') as f:
        return yaml.load(f.read())


def print_latex_preamble():
    with open('latex-preamble.tex') as f:
        print(f.read())


def render_latex(data):
    print_latex_preamble()

    for chapter in data['chapters']:
        print('\chapter{', chapter['name'], '}')

        for article in chapter['articles']:
            print('\section{Article ', article['number'], '}')
            print('')
            print(article['text'].replace('\n', '\n\n'))
            print('')

    print('\end{document}')


def main():
    data = read_data()
    render_latex(data)


if __name__ == '__main__':
    main()