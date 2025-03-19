import sys
import re
import os
import datetime
from playwright.sync_api import sync_playwright
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

    # selector to target only course links
    course_links = page.query_selector_all('table.table_default > tbody > tr > td.width > a[href^="preview_course_nopop.php"]')
    print(f"Found {len(course_links)} course links")

    output_dir = os.path.join(os.path.dirname(__file__), "Output")
    os.makedirs(output_dir, exist_ok=True)
    date = datetime.datetime.now()
    date_form = date.strftime("%d-%b-%Y_%H-%M")
    file_name = f"augusta_university_courses_{date_form}.txt"
    filename = os.path.join(output_dir, file_name)

    print(f"Writing to file: {filename}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Augusta University Course Catalog\n\n")
        for i, link in enumerate(course_links, 1):
            course_name = link.inner_text().strip()
            course_url = link.get_attribute('href')

            try:
                course_page = browser.new_page()
                print(f"Navigating to: https://catalog.augusta.edu/{course_url}")
                course_page.goto(f"https://catalog.augusta.edu/{course_url}", timeout=30000)
                course_page.wait_for_load_state() # wait for js to render

                course_details = extract_course_details(course_page)

                f.write(f"Course: {course_name}\n")
                f.write(f"Description: {course_details.get('description', 'Not found')}\n")
                f.write(f"Prerequisites: {course_details.get('prerequisites', 'Not found')}\n")
                f.write(f"Lecture Hours: {course_details.get('lecture_hours', 'Not found')}\n")
                f.write(f"Repeat Status: {course_details.get('repeat_status', 'Not found')}\n")
                f.write(f"Grade Mode: {course_details.get('grade_mode', 'Not found')}\n")
                f.write(f"Schedule Type: {course_details.get('schedule_type', 'Not found')}\n\n")

                course_page.close()

            except Exception as e:
                print(f"Error processing course {i}: {e}")
                if 'course_page' in locals():
                    try:
                        course_page.close()
                    except:
                        pass

            if i % 10 == 0:
                print(f"Processed {i} courses...")

    print(f"Course information saved as {filename}")

def extract_course_details(course_page):
   
    html_content = course_page.content() 
    soup = BeautifulSoup(html_content, 'html.parser')
    details = {}

    # Course Description
    try:
        title_element = soup.find(id='course_preview_title')
        if title_element:
            desc_element = title_element.find_next('p')
            details['description'] = desc_element.text.strip() if desc_element else "Description not found"
        else:
            details['description'] = "Description not found"
    except:
        details['description'] = "Description not found"

    # Prerequisites, Lecture Hours, Repeat Status, Grade Mode, Schedule Type:
   
    try:
        # Prerequisites
        prereq_heading = soup.find('strong', string=re.compile(r'Prerequisite(s)?', re.IGNORECASE))
        if prereq_heading:
            #The Prereq text is the next sibling
            prereq_text = prereq_heading.next_sibling.strip()
            details['prerequisites'] = prereq_text if prereq_text else "Prerequisites not found"
        else:
            details['prerequisites'] = "Prerequisites not found"
    except:
        details['prerequisites'] = "Prerequisites not found"

    try:
        # Lecture Hours:
        lecture_hours_strong = soup.find('strong', string=re.compile(r'Lecture Hours', re.IGNORECASE))
        if lecture_hours_strong:
            details['lecture_hours'] = lecture_hours_strong.next_sibling.strip()
        else:
            details['lecture_hours'] = "Lecture Hours not found"
    except:
        details['lecture_hours'] = "Lecture Hours not found"

    try:
        # Repeat Status:
        repeat_status_strong = soup.find('strong', string=re.compile(r'Repeat Status', re.IGNORECASE))
        if repeat_status_strong:
            details['repeat_status'] = repeat_status_strong.next_sibling.strip()
        else:
            details['repeat_status'] = "Repeat Status not found"
    except:
        details['repeat_status'] = "Repeat Status not found"

    try:
        # Grade Mode:
        grade_mode_strong = soup.find('strong', string=re.compile(r'Grade Mode', re.IGNORECASE))
        if grade_mode_strong:
            details['grade_mode'] = grade_mode_strong.next_sibling.strip()
        else:
            details['grade_mode'] = "Grade Mode not found"
    except:
        details['grade_mode'] = "Grade Mode not found"

    try:
        # Schedule Type:
        schedule_type_strong = soup.find('strong', string=re.compile(r'Schedule Type', re.IGNORECASE))
        if schedule_type_strong:
            details['schedule_type'] = schedule_type_strong.next_sibling.strip()
        else:
            details['schedule_type'] = "Schedule Type not found"
    except:
        details['schedule_type'] = "Schedule Type not found"
    return details

if __name__ == "__main__":
    
    url = "https://catalog.augusta.edu/content.php?catoid=45&navoid=5479"
    
    try:
        with sync_playwright() as playwright:
            run(playwright, url)
    except Exception as e:
        print(f"An error occurred: {e}")

    input("Press Enter to exit...")
