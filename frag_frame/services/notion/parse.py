import re
import random
import json
import os

DB_TYPE = os.getenv("NOTION_DATABASE_TYPE")


def get_random_page(database):
    if database["has_more"]:
        raise NotImplementedError("Database has more pages. Must implement pagination.")

    idx = random.choice(list(range(len(database["results"]))))
    page = database["results"][idx]
    return page


def get_page_id(database_page):
    return database_page["id"]


def get_page_url(database_page):
    return database_page["url"]


def get_page_topic(database_page):
    return database_page["properties"]["Tags"]["multi_select"][0]["name"]


def get_page_name(database_page):
    return database_page["properties"].get("Name", {})["title"][0]["text"]["content"]


def parse_page_text_content(page_content):
    try:
        text = ""
        for r in page_content["results"]:
            result_type = r["type"]
            result_text_blocks = r[result_type]["text"]
            if not result_text_blocks:
                text += "<br>"
            else:
                for t in result_text_blocks:
                    content = t["text"]["content"]
                    content_is_bold = t.get("annotations", {}).get("bold")
                    if result_type.startswith("heading"):
                        styled_content = f"<h3>{content}</h3><br>"
                    elif content_is_bold:
                        styled_content = f"<b>{content}</b><br>"
                    else:
                        styled_content = f"{content}<br>"
                    text += styled_content

    except Exception as e:
        print(f"Error parsing text from page {json.dumps(page_content, indent=2)}")
        raise
    return dict(text=text)


def parse_page_quote_content(page_content, **kwargs):
    try:
        quote = page_content["results"][0]["paragraph"]["text"][0]["text"]["content"]
        attrib = page_content["results"][1]["paragraph"]["text"][0]["text"]["content"]
    except Exception as e:
        print(f"Error parsing quote from page {json.dumps(page_content, indent=2)}")
        raise
    return dict(
        quote=quote,
        attrib=attrib,
    )


def parse_page_recipe_content(page_content, **kwargs):
    recipe = parse_page_text_content(page_content)["text"]
    return dict(recipe=recipe)


def parse_page_book_fragment(page_content, page):
    text = parse_page_text_content(page_content)["text"]
    book = page["properties"]["Book"]["rich_text"][0]["plain_text"]
    author = page["properties"]["Author"]["rich_text"][0]["plain_text"]
    return dict(text=text, book=book, author=author)


content_parser = {
    "quote": parse_page_quote_content,
    "recipe": parse_page_recipe_content,
    "book fragment": parse_page_book_fragment,
}


def parse_page_content(page_content, page=None):
    return content_parser[DB_TYPE](page_content, page)
