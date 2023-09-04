# -*- cofing: utf-8 -*-

# INDEX_FILE = "/Users/alex/Downloads/index.html"
INDEX_FILE = "/home/alex/raspi-frag-frame/index.html"

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["NOTION_DATABASE_TYPE"] = "book fragment"

import frag_frame.services.notion.client as notion_client
from frag_frame.services.notion.parse import (
    get_random_page,
    get_page_id,
    parse_page_book_fragment,
)
from frag_frame.html import format_as_html


def _check_database_type():
    db_type = os.getenv("NOTION_DATABASE_TYPE")
    if not db_type:
        raise ValueError("Must set NOTION_DATABASE_TYPE env variable")
    if db_type not in ("book fragment"):
        raise NotImplementedError


def run():
    _check_database_type()

    database = notion_client.retrieve_database(
        database_id=os.getenv("NOTION_DATABASE_ID"),
    )

    book_frag_page = get_random_page(database)
    book_frag_page_id = get_page_id(book_frag_page)
    book_frag_page_content = notion_client.retrieve_page_content(book_frag_page_id)
    book_frag = parse_page_book_fragment(book_frag_page_content, book_frag_page)
    book_frag_html = format_as_html(book_frag)

    print(f"Writing to {INDEX_FILE}")
    with open(INDEX_FILE, "w") as f:
        f.write(book_frag_html)


if __name__ == "__main__":
    run()
