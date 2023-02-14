import csv
import re
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib3

def scrape_emails(url):
    # Make a request to the website
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }
        
        page = requests.get(url, headers=headers, verify=False)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all email addresses on the page
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.text)

    # Find all the links on the page
    links = [link.get("href") for link in soup.find_all("a")]

    return emails, links

def export_to_csv(emails):
    # Write the emails to a CSV file
    with open("emails.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Email"])
        for email in emails:
            writer.writerow([email])

if __name__ == "__main__":
    urllib3.disable_warnings()

    # Prompt for the URL to start crawling from
    url = input("Enter the URL to scrape: ")

    parsed_url = urlparse(url)
    print(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    print(base_url)
    
    visited = set()
    emails = set()
    queue = [url]

    while queue:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        # print("\033[34mVisiting\033[0m", current_url)
        try:
            page_emails, links = scrape_emails(current_url)
        except:
            continue
        print("\033[35mPages in queue:", len(queue), str(datetime.timedelta(seconds=len(queue))));

        if page_emails:
            print(f"\033[32mFound {len(page_emails)} email(s) on {current_url}:\033[0m")
            for email in page_emails:
               print(f"\033[32m- {email}\033[0m")

        emails.update(page_emails)

        for link in links:
            try:
              if (
                link.startswith(base_url)
                and not link.endswith(".pdf")
                and not link.endswith(".doc")
                and not link.endswith(".docx")
                and not link.endswith(".xls")
                and not link.endswith(".xlsx")
                and not link.endswith(".jpg")
                and not link.endswith(".jpeg")
                and not link.endswith(".png")
                and not link.endswith(".gif")
              ):
                queue.append(link)
            except:
                continue

    export_to_csv(emails)
