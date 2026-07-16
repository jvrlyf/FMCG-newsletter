#!/usr/bin/env python3
"""Validate static files for the CI pipeline."""
import html.parser
import sys

def validate_html():
    with open('static/index.html') as f:
        try:
            html.parser.HTMLParser().feed(f.read())
            print('HTML: valid')
        except Exception as e:
            print(f'HTML ERROR: {e}')
            sys.exit(1)

def validate_js():
    with open('static/app.js') as f:
        content = f.read()
        if content.count('{') != content.count('}'):
            print('JS ERROR: unbalanced braces')
            sys.exit(1)
        print('JS: braces balanced OK')

if __name__ == '__main__':
    validate_html()
    validate_js()
    print('All static file checks passed')