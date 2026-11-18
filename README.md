# Stack Overflow Error Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-Stack%20Exchange-F48024?logo=stackoverflow&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20parsing-4B8BBE)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

# 🎓 About this Project

This project was developed for the **Data Collection Techniques** course in the **MSc in Big Data Science at the University of Navarra (Spain)**.

The brief: write a function that runs a Python command and, if it fails, automatically fetches help from Stack Overflow. It is a small tool, but it covers the full data-collection loop: querying a public API, parsing HTML content and handling the practical obstacles of automated access to a website.

---

# 📌 Highlights

- ✅ One call, `get_SOS_help(command)`, from error to solution
- ✅ Uses the **official Stack Exchange API** instead of scraping (no key required)
- ✅ Retrieves the most relevant question **and its top-voted answer**, cleaned from HTML
- ✅ Fallback search that removes user-specific names from the error to improve recall
- ✅ Opens the question in the browser with answers sorted by score

---

# 📖 Project Overview

```
command ──► exec() ──► OK? ──► "works as intended"
                        │
                        └─ error ──► "TypeError: uniform() got an unexpected keyword argument 'siz'"
                                        │
                                        ▼
                              Stack Exchange API /search/advanced
                                        │  (fallback: retry without 'quoted' names)
                                        ▼
                              first question ──► /questions/{id}/answers (sorted by votes)
                                        │
                                        ▼
                              print link + top answer  ──►  open in browser
```

---

# 🎯 Business Problem

Developers spend a significant part of their time searching for error messages. Copying the error, searching, opening results and finding the best answer is repetitive. This tool automates that loop and brings the community's best answer directly into the working session.

---

# 🛠 Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Data source | Stack Exchange API v2.3 (`/search/advanced`, `/questions/{id}/answers`) |
| HTTP | `requests` |
| Parsing | BeautifulSoup |
| Other | `webbrowser`, `re` |

---

# 🔬 Methodology

## 1. Run and capture

The command is executed with `exec` inside `try/except`. On failure, the error is formatted as `ErrorType: message`.

## 2. Search

The message is sent to the `/search/advanced` endpoint, sorted by relevance and restricted to questions with at least one answer. If the search returns nothing, it is repeated **without the quoted names** (`'siz'`, `'nn'`): they come from the user's own code and make the query too specific.

## 3. Best answer

The answers to the first question are requested sorted by votes with the `withbody` filter. The HTML body is converted to plain text with BeautifulSoup.

## 4. Open

The question is opened in a new browser tab with `?answertab=scoredesc`, so the top-voted answer appears first.

---

# 📈 Results

```python
>>> from sos_help import get_SOS_help
>>> get_SOS_help("np.random.uniform(-1, 1, siz=100)")
TypeError: uniform() got an unexpected keyword argument 'siz'
https://stackoverflow.com/questions/72537485/typeerror-uniform-got-an-unexpected-keyword-argument-low-size
[1 votes]
We must use random.uniform while importing the related class with an alias (using 'as') ...

>>> get_SOS_help("nn.random.uniform(-1, 1, size=100)")
NameError: name 'nn' is not defined
https://stackoverflow.com/questions/56633138/nameerror-name-nn-is-not-defined
[21 votes]
If you got this error you can fix it with the following code: ...

>>> get_SOS_help("np.random.uniform(-1, 1, size=100)")
works as intended
```

The first case returns exactly the reference link given in the assignment.

---

# 📂 Repository Structure

```
stackoverflow-error-assistant/
├── README.md
├── LICENSE
├── requirements.txt
├── sos_help/
│   ├── __init__.py
│   └── core.py          # search_stack_overflow, most_voted_help, prompt_web, get_SOS_help
└── notebooks/
    └── demo.ipynb       # the three test cases, executed
```

### How to use

```bash
pip install -r requirements.txt
```

```python
import numpy as np
from sos_help import get_SOS_help

get_SOS_help("np.random.uniform(-1, 1, siz=100)", namespace=globals())
```

`namespace=globals()` lets the command see your imports (`np`). Use `open_browser=False` to skip opening the tab.

---

# 💼 Potential Applications

- **Developer productivity:** instant help inside notebooks and teaching environments.
- **Education:** students get pointed to relevant explanations of their errors.
- **Internal tooling:** the same pattern works with a company's own knowledge base or ticketing API.

---

# 🔎 Methodological Considerations

- **Why an API and not scraping:** the first version used Selenium to read the answers from the page, but Cloudflare's "Verify you are human" check blocked the automated browser repeatedly. The official API is faster, more stable and the allowed way to access the data.
- `exec` runs arbitrary code: use the tool only with **your own, trusted** commands.
- Without an API key, the Stack Exchange API allows up to 300 requests per day per IP.
- "Most relevant" is decided by Stack Overflow's search; the first result is not always the best match for every error.

---

# 🔮 Future Improvements

- [ ] Hook into errors automatically (IPython exception handler or a `%sos` magic) instead of passing the command as text
- [ ] Rank several candidate questions by similarity to the full traceback
- [ ] Summarise the top answers with an LLM
- [ ] Package it for `pip install`

---

# 👤 Author

**Juan Jesús Gómez Ortiz**
Mechanical Engineer | MSc in Big Data Science

[LinkedIn](https://www.linkedin.com/in/jj-gomez-ortiz/) · [GitHub](https://github.com/jj-gomez-ortiz)

---

# 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE). Stack Overflow content is licensed under [CC BY-SA](https://stackoverflow.com/help/licensing) by its authors.
