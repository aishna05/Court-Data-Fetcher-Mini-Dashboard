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
