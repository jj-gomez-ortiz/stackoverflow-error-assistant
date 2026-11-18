"""Stack Overflow error assistant.

Run a Python command; if it fails, search Stack Overflow for the error through the
official Stack Exchange API, print the first related question and its top-voted
answer, and open the question in the browser.
"""

import re
import webbrowser

import requests
from bs4 import BeautifulSoup

API = "https://api.stackexchange.com/2.3"
TIMEOUT = 15


def search_stack_overflow(error_msg):
    """Link to the most relevant Stack Overflow question (with at least one answer)."""
    params = {"order": "desc", "sort": "relevance", "q": error_msg,
              "site": "stackoverflow", "answers": 1}
    r = requests.get(f"{API}/search/advanced", params=params, timeout=TIMEOUT)
    items = r.json().get("items", [])
    return items[0]["link"] if items else None


def most_voted_help(link):
    """Plain text of the highest-voted answer to a question."""
    question_id = link.split("/questions/")[1].split("/")[0]
    params = {"order": "desc", "sort": "votes", "site": "stackoverflow", "filter": "withbody"}
    r = requests.get(f"{API}/questions/{question_id}/answers", params=params, timeout=TIMEOUT)
    items = r.json().get("items", [])
    if not items:
        return "No answers found."
    best = items[0]
    body = BeautifulSoup(best["body"], "html.parser").get_text().strip()
    return f"[{best['score']} votes]\n{body}"


def prompt_web(link):
    """Open the question in a new browser tab, answers sorted by score."""
    if not webbrowser.open_new_tab(link + "?answertab=scoredesc"):
        print("Could not open the browser.")


def get_SOS_help(command, namespace=None, open_browser=True, max_chars=800):
    """Execute `command`. Print "works as intended" or Stack Overflow help for the error.

    Warning: the command is run with `exec`; use it only with your own, trusted code.
    Returns the Stack Overflow link (or None if the command worked / nothing was found).
    """
    namespace = globals() if namespace is None else namespace
    try:
        exec(command, namespace)
        print("works as intended")
        return None
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        print(error_msg)

    # Full message first; if nothing is found, retry without the quoted names
    # ('siz', 'nn'...), which are usually the user's own typos
    link = (search_stack_overflow(error_msg)
            or search_stack_overflow(re.sub(r"'[^']*'", "", error_msg).strip()))
    if link is None:
        print("No Stack Overflow results found.")
        return None

    print(link)
    answer = most_voted_help(link)
    print(answer if len(answer) <= max_chars else answer[:max_chars] + " [...]")
    if open_browser:
        prompt_web(link)
    return link
