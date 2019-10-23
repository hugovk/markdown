"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).

Legacy Attributes Extension
===========================

An extension to Python Markdown which implements legacy attributes.

Prior to Python-Markdown version 3.0, the Markdown class had an `enable_attributes`
keyword which was on by default and provided for attributes to be defined for elements
using the format `{@key=value}`. This extension is provided as a replacement for
backward compatability. New documents should be authored using attr_lists. However,
numerious documents exist which have been using the old attribute format for many
years. This extension can be used to continue to render those documents correctly.
"""

import re
from markdown.treeprocessors import Treeprocessor, isString
from markdown.extensions import Extension


ATTR_RE = re.compile(r'\{@([^\}]*)=([^\}]*)}')  # {@id=123}


class LegacyAttrs(Treeprocessor):
    def run(self, doc):
        """Find and set values of attributes ({@key=value}). """
        for el in doc.iter():
            alt = el.get('alt', None)
            if alt is not None:
                el.set('alt', self.handleAttributes(el, alt))
            if el.text and isString(el.text):
                el.text = self.handleAttributes(el, el.text)
            if el.tail and isString(el.tail):
                el.tail = self.handleAttributes(el, el.tail)

    def handleAttributes(self, el, txt):
        """ Set attributes and return text without definitions. """
        def attributeCallback(match):
            el.set(match.group(1), match.group(2).replace('\n', ' '))
        return ATTR_RE.sub(attributeCallback, txt)


class LegacyAttrExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(LegacyAttrs(md), 'legacyattrs', 15)


def makeExtension(**kwargs):  # pragma: no cover
    return LegacyAttrExtension(**kwargs)
