# Court-Data-Fetcher-Mini-Dashboard


A simple Flask-based web application to look up Indian district court case details (e.g., Faridabad District Court) by Case Type, Number, and Year. It fetches and displays:

- Petitioner and Respondent names  
- Filing Date and Next Hearing Date  
- Linked PDF(s) for latest Order/Judgment  

---

## ⚙️ Tech Stack

- **Frontend:** HTML5 + Tailwind Css
- **Backend:** Python (Flask)
- **Browser Automation:** Playwright
- **Database:** SQLite
- **Parser:** BeautifulSoup4

---

## 🎯 Court Targeted

We are using the [Faridabad District Court Portal](https://districts.ecourts.gov.in/faridabad) for scraping case data.

---

## ✅ Features

-  Search by Case Type, Case Number, Filing Year
-  Manual CAPTCHA handling
-  Fetch and parse case metadata
-  View/download latest order/judgment PDF links
-  Logs each query + HTML response to SQLite
-  Handles invalid entries / site timeout gracefully

---

## 🚀 Setup & Usage

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/court-case-lookup.git
cd court-case-lookup
````

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Or use venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Install Playwright browser

```bash
playwright install
```

### 4. Run the Flask server

```bash
python app/app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧠 CAPTCHA Handling Strategy

The Faridabad court portal uses a CAPTCHA to prevent bots. Since there's no public API or token system:

* The browser is launched via Playwright in non-headless mode.
* The user manually solves the CAPTCHA on the live site.
* Once done, press **Enter** in the terminal to continue.
* The script then clicks **Submit**, waits for the case data, and parses it.

This ensures legal, ethical, and working data access.

---

## 🧪 Sample Search Inputs

* **Case Type:** CS
* **Case Number:** 123
* **Filing Year:** 2017

---

## 🧾 Sample Query Log Table (SQLite)

Stored in `database.db`:

| ID | Petitioner      | Respondent         | Filing Date | Hearing Date | PDF Links                                                         |
| -- | --------------- | ------------------ | ----------- | ------------ | ----------------------------------------------------------------- |
| 1  | VEENA CHAUDHARY | DHBVNL             | 12/01/2017  | 10/04/2025   | [https://.../order1.pdf](https://.../order1.pdf)                  |
| 2  | SANDEP STEEL... | KCA INFRASTRUCTURE | 15/02/2017  | 20/06/2025   | [https://.../judgment\_final.pdf](https://.../judgment_final.pdf) |

---

## 📦 Folder Structure

```
court-case-lookup/
│
├── app/
│   ├── app.py            # Flask app
│   ├── scraper.py        # Playwright + scraper logic
│   ├── parser.py         # HTML parser (BeautifulSoup)
│   └── templates/
│       └── index.html    # UI form
│
├── database.db           # SQLite database (autocreated)
├── debug_output.html     # Raw saved HTML (optional)
├── requirements.txt
└── README.md
```

---

## ❗ Error Handling

* ❌ Invalid Case Numbers → “No results found” message
* ⏱️ Site Downtime / CAPTCHA Timeout → Friendly error in UI
* 🧾 All errors logged for debugging

---

## 📹 Demo Video

[▶️ Watch Demo on YouTube (Coming Soon)]()

---

## 🐳 Optional Extras

* [ ] Dockerfile for containerized deployment
* [ ] Pagination support for multiple case entries
* [ ] GitHub Actions for CI/CD
* [ ] Unit tests with pytest

---

## 📜 License

MIT License

---




