# -*- coding: utf-8 -*-

from typing import Dict
from textwrap import dedent


def format_as_html(book_frag: Dict[str, str]):
    """
    Format parsed notion page data for book fragment as HTML.

    Inputs:

    book_frag
        e.g.
        {
            "text": "He squatted in the sand and watched the sun...",
            "book": "Blood Meridian",
            "author": "Cormac McCarthy",
        }
    """

    # Split on <br> tags in book_frag["text"] (these separate paragraphs)
    # And replace newlines with <br> tags for HTML
    paragraphs = []
    for p in book_frag["text"].split("<br>"):
        p_html = p.strip().replace("\n", "<br>")
        if p_html.strip():
            paragraphs.append(f"<p>{p_html}</p>")
    paragraphs = "\n".join(paragraphs)

    book = book_frag["book"]
    author = book_frag["author"]

    html_str = dedent(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="font.css">
            <link rel="stylesheet" href="style.css" />
        </head>
        <body>
            <div class="main">
                <div class="center">
                    <div class="fragment">
                        {paragraphs}
                    </div>
                    <div class="footnote">
                        <p>{book}<br>{author}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    )

    return html_str
