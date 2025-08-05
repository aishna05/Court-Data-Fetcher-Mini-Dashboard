from playwright.sync_api import sync_playwright
from parser import parse_case_html
import sqlite3

def fetch_and_save_case_details(case_type, case_number, year, court_type, court_code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://faridabad.dcourts.gov.in/case-status-search-by-case-number/")

        # 1. Select court type radio
        if court_type == "complex":
            page.check("#chkYes")

            # Wait for the dropdown to be enabled (not for the option itself)
            page.wait_for_selector("select#est_code:enabled", timeout=10000)
            # Optionally, wait for options to be populated
            page.wait_for_function(
            "() => document.querySelectorAll('#est_code option').length > 1",
            timeout=10000
            )
            html = page.inner_html("select#est_code")
            print("Current est_code options:\n", html)
            # Now select the option (do not wait for the option itself)
            # If court_code contains commas, pick the first code
            selected_code = court_code
            # Manually set the correct value (as per actual HTML value)
            page.select_option("select#est_code", "HRFB01,HRFB02,HRFB03")
            print("👉 Selecting court_code: HRFB01,HRFB02,HRFB03")
            
            print("👉 Selecting court_code:", court_code)

            # Removed invalid JavaScript code. Playwright handles option selection in Python.


        else:
            page.check("#chkNo")

            page.wait_for_selector("select#court_establishment:enabled", timeout=10000)
            page.wait_for_function(
            "() => document.querySelectorAll('#court_establishment option').length > 1",
            timeout=10000
            )
            page.select_option("select#court_establishment", court_code)

        # 2. Wait for case_type to be enabled
        page.wait_for_selector("select#case_type:enabled", timeout=10000)

        # 3. Fill rest of the form
        page.select_option("select#case_type", case_type)
        page.fill("input#reg_no", case_number)
        page.fill("input#reg_year", year)

        # 4. Wait for user to solve CAPTCHA manually
        input("🧠 Please solve CAPTCHA in browser, then press Enter here...")

        # 5. Submit
        
        page.click("input[type='submit']")

        # 6. Wait for results
        try:
           page.wait_for_selector(".resultsHolder, .resultsHolder", timeout=30000)
           html = page.inner_html(".resultsHolder")
           print("✅ Page loaded, extracting case details...")

           if page.query_selector(".resultsHolder"):
              html = page.inner_html(".resultsHolder")
           elif page.query_selector(".resultsHolder"):
              html = page.inner_html(".resultsHolder")
           else:
              html = page.content()  # fallback debug
              print("⚠️ Could not find result container.")
        except Exception as e:
            print("❌ Timeout or error while waiting for results.")
            page.screenshot(path="debug_screenshot.png") 
            html = page.content()
            browser.close()
            return {"error": "Timeout or case not found."}

    case_data = parse_case_html(html)
    print("📦 Parsed Case Data:", case_data)

    # Save to SQLite
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    court TEXT,
    serial TEXT,
    case_info TEXT,
    parties TEXT,
    case_cno TEXT
)""")
    for case in case_data:
       c.execute("INSERT INTO cases (court, serial, case_info, parties, case_cno) VALUES (?, ?, ?, ?, ?)",
              (case["court"], case["serial"], case["case_info"], case["parties"], case["case_cno"]))
    conn.commit()
    conn.close()

  
    return case_data

from bs4 import BeautifulSoup

def parse_case_html(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    with open("debug_output.html", "w", encoding="utf-8") as f:
       f.write(html)
    print("🔍 Saved HTML to debug_output.html")


    tables = soup.select(".distTableContent")
    print("✅ Found", len(tables), "tables")

    for table in tables:
        court_name_tag = table.find("caption")
        court_name = court_name_tag.text.strip() if court_name_tag else "Unknown Court"

        for row in table.select("tbody tr"):
            try:
                sn = row.select_one("td[data-th*='Serial Number'] .bt-content").text.strip()
                case_info = row.select_one("td[data-th*='Case Type/Case Number/Case Year'] .bt-content").text.strip()
                parties = row.select_one("td[data-th*='Petitioner versus Respondent'] .bt-content").get_text(" ", strip=True)
                view_button = row.select_one("td[data-th*='View'] a")
                case_cno = view_button['data-cno'] if view_button else "N/A"

                results.append({
                    "court": court_name,
                    "serial": sn,
                    "case_info": case_info,
                    "parties": parties,
                    "case_cno": case_cno
                })
            except Exception as e:
                print("⚠️ Error parsing row:", e)
                print("🧱 Row HTML:", row)

    print("✅ Total parsed cases:", len(results))
    return results
