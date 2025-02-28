import sys
import re
import os
from playwright.sync_api import sync_playwright
from elevate import elevate
from bs4 import BeautifulSoup

def run(playwright, url):
    print("Starting the browser...")
    browser = playwright.chromium.launch()
    page = browser.new_page()
    print(f"Navigating to {url}")
    page.goto(url)

    print("Waiting for table to load...")
    try:
        page.wait_for_selector("table.table_default", timeout=30000)
        print("Table loaded!")
    except Exception as e:
        print(f"Timeout waiting for table: {e}")
        browser.close()
        return

    print("Extracting course info...")
    extract_course_info(playwright, browser, url)

    print("Closing the browser...")
    browser.close()

def extract_course_info(playwright, browser, url):
    print("Selecting course links...")
    page = browser.new_page()
    print(f"Navigating to {url}")
    page.goto(url)
    course_links = page.query_selector_all('table.table_default > tbody > tr > td.width > a[href^="preview_course_nopop.php"]')
    print(f"Found {len(course_links)} course links")

    username = os.environ['USERNAME']
    output_dir = f"C:\\Users\\{username}\\Documents\\GitHub\\Course-Catalog-Information-Aggregator\\Output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "augusta_university_courses.txt")

    print(f"Writing to file: {filename}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Augusta University Course Catalog\n\n")
        for i, link in enumerate(course_links, 1):
            course_name = link.inner_text().strip()
            course_url = link.get_attribute('href')

            try:
                # Navigate to the course page
                course_page = browser.new_page()
                print(f"Navigating to: https://catalog.augusta.edu/{course_url}")  # Debugging
                course_page.goto(f"https://catalog.augusta.edu/{course_url}", timeout=30000)  # Added timeout

                # Extract course details
                course_details = course_page.query_selector('.coursedetail')
                if course_details:
                    course_info = course_details.inner_text()
                    f.write(f"Course: {course_name}\n")
                    f.write(f"Details: {course_info}\n\n")
                else:
                    f.write(f"Course: {course_name}\n")
                    f.write("Details: Not available\n\n")

                course_page.close()

            except Exception as e:
                print(f"Error processing course {i}: {e}")
                if 'course_page' in locals():
                    try:
                        course_page.close()  # Ensure page is closed even on error
                    except:
                        pass  # Ignore close errors in error handling

            if i % 10 == 0:
                print(f"Processed {i} courses...")

    print(f"Course information saved as {filename}")

def extract_course_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    details = {}
    
    # Description
    desc_element = soup.find('span', class_='coursedetail')
    details['description'] = desc_element.
    

if __name__ == "__main__":
    url = "https://catalog.augusta.edu/content.php?catoid=45&navoid=5479"
    
    try:
        elevate()
        with sync_playwright() as playwright:
            run(playwright, url)
    except Exception as e:
        print(f"An error occurred: {e}")

    input("Press Enter to exit...")
