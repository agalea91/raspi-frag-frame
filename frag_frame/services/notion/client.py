import requests
import time
import os

HEADERS = {
    "Authorization": f"Bearer {os.getenv('NOTION_SECRET_TOKEN')}",
    "Notion-version": "2021-05-13",
}

MAX_PAGINATION = 20


def retrieve_database(database_id, query=None) -> dict:
    database = {"has_more": True, "next_cursor": None, "results": []}

    i = 0
    while database["has_more"]:
        i += 1
        if i > MAX_PAGINATION:
            raise NotImplementedError(f"Max pagination reached ({MAX_PAGINATION})")

        next_cursor = database.get("next_cursor")
        if not next_cursor and i > 1:
            break

        next_database = _retrieve_paginated_database(database_id, query, next_cursor)
        for k, v in next_database.items():
            if k == "results":
                database["results"].extend(v)
            else:
                database[k] = v

        time.sleep(1)
    return database


def _retrieve_paginated_database(database_id, query=None, start_cursor=None) -> dict:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = query or {}
    if start_cursor:
        data["start_cursor"] = start_cursor
    print(f"POST {url} with data: {data}")
    response = requests.post(url=url, headers=HEADERS, json=data)
    response.raise_for_status()
    database = response.json()
    return database


def retrieve_page_content(page_id) -> dict:
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    print(f"GET {url}")
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    page = response.json()
    return page
