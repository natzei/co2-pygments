# -*- coding: utf-8 -*-
"""
    pygments.lexers.jvm
    ~~~~~~~~~~~~~~~~~~~

    Pygments lexers for JVM languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
from pygments.util import shebang_matches
from pygments import unistring as uni

__all__ = ['CO2Lexer']


class CO2Lexer(RegexLexer):
    """
    For `Java <http://www.sun.com/java/>`_ source code.
    """

    name = 'CO2'
    aliases = ['co2']
    filenames = ['*.co2']

    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    tokens = {
        'root': [
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            # keywords: go before method names to avoid lexing "throw new XYZ"
            # as a method signature
            (r'(if|then|else|switch|case|default|tell|do|receive|send|tellAndReturn|tellAndWait|tellRetract|t|retract|ask|from|to|after)\b', Keyword),            
            (r'(single)\b', Keyword.Declaration),
            (r'(int|string|unit|session|boolean)\b', Keyword.Type),
            (r'\w*\s*[!?]', Name.Constant),  # internal/external actions
            
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text), 'system'),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(specification|contract|process|honesty)(\s+)', bygroups(Keyword.Declaration, Text), 'entity'),
            
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"'\\.'|'[^\\]'|'\\u[0-9a-fA-F]{4}'", String.Char),
            # (r'(\.)(\s*(?:[^\W\d]|\$)[\w$]*)', bygroups(Operator, Name.Attribute)),
            (r'^\s*([^\W\d]|\$)[\w$]*:', Name.Label),
            (r'([^\W\d]|\$)[\w$]*', Name),
            (r'@([^\W\d]|\$)[\w$]*', Name),
            (r'([0-9](_*[0-9]+)*\.([0-9](_*[0-9]+)*)?|'
             r'([0-9](_*[0-9]+)*)?\.[0-9](_*[0-9]+)*)'
             r'([eE][+\-]?[0-9](_*[0-9]+)*)?[fFdD]?|'
             r'[0-9][eE][+\-]?[0-9](_*[0-9]+)*[fFdD]?|'
             r'[0-9]([eE][+\-]?[0-9](_*[0-9]+)*)?[fFdD]|'
             r'0[xX]([0-9a-fA-F](_*[0-9a-fA-F]+)*\.?|'
             r'([0-9a-fA-F](_*[0-9a-fA-F]+)*)?\.[0-9a-fA-F](_*[0-9a-fA-F]+)*)'
             r'[pP][+\-]?[0-9](_*[0-9]+)*[fFdD]?', Number.Float),
            (r'0[xX][0-9a-fA-F](_*[0-9a-fA-F]+)*[lL]?', Number.Hex),
            (r'0[bB][01](_*[01]+)*[lL]?', Number.Bin),
            (r'0(_*[0-7]+)+[lL]?', Number.Oct),
            (r'0|[1-9](_*[0-9]+)*[lL]?', Number.Integer),
            (r'[~^*!%&\[\](){}<>|+=:;,./?-]', Operator),
            (r'\(+\)', Operator), # (+) operator
            (r'\n', Text)
        ],
        'entity': [
            (r'([^\W\d]|\$)[\w$]*', Name.Entity, '#pop')
        ],
        'system': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
    }

