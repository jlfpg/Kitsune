#!/usr/bin/env python3

"""
KITSUNE v1.0
Web Form Crawler and Interactive Testing Tool

This tool crawls a website, detects forms, allows user interaction,
and optionally performs automated form testing in controlled environments.
"""

# ==============================
# Imports
# ==============================

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import logging
import random
import string
import time
import threading
import queue
import sys
import os

# ==============================
# Global Configuration
# ==============================

VERSION = "1.0"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ==============================
# Banner
# ==============================

def print_banner():
    """
    Prints the Kitsune ASCII banner with smooth red-to-yellow fade,
    correctly centered without breaking Unicode spacing.
    """

    banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠙⠻⢶⣄⡀⠀⠀⠀⢀⣤⠶⠛⠛⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⣙⣿⣦⣤⣴⣿⣁⠀⠀⣸⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣡⣾⣿⣿⣿⣿⣿⣿⣿⣷⣌⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣷⣄⡈⢻⣿⡟⢁⣠⣾⣿⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⠘⣿⠃⣿⣿⣿⣿⡏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠈⠛⣰⠿⣆⠛⠁⠀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣦⠀⠘⠛⠋⠀⣴⣿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠀⠀⠀⠾⢿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⡿⠟⠋⣁⣠⣤⣤⡶⠶⠶⣤⣄⠈⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⣿⣿⣮⣉⣉⣉⣤⣴⣶⣿⣿⣋⡥⠄⠀⠀⠀⠀⠉⢻⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣋⣁⣤⣀⣀⣤⣤⣤⣤⣄⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⠁⠀⠀⠀⠀⠈⠛⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

    lines = banner.strip("\n").split("\n")

    # Get actual drawing width
    banner_width = max(len(line) for line in lines)
    terminal_width = os.get_terminal_size().columns

    # Calculate manual padding
    left_padding = max((terminal_width - banner_width) // 2, 0)

    total_lines = len(lines)

    for i, line in enumerate(lines):
        ratio = i / (total_lines - 1)
        r = 255
        g = int(255 * ratio)
        b = 0

        color = f"\033[38;2;{r};{g};{b}m"
        reset = "\033[0m"

        print(" " * left_padding + color + line + reset)

    red = "\033[38;2;255;0;0m"
    reset = "\033[0m"

    title = f"DOLOS v{VERSION}"
    title_padding = max((terminal_width - len(title)) // 2, 0)

    print(" " * title_padding + red + title + reset)
    print()

# ==============================
# Logging Configuration
# ==============================

def configure_logging(verbose=False):
    """
    Configures logging level based on verbose flag.
    """

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# ==============================
# Random Data Generators
# ==============================

def random_username(length=8):
    """
    Generates a random lowercase username.
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_password():
    """
    Generates a random password between 8 and 12 characters.
    Includes letters, digits and selected special characters.
    """
    chars = string.ascii_letters + string.digits + "._!$&%"
    length = random.randint(8, 12)
    return ''.join(random.choices(chars, k=length))


def random_text(length=10):
    """
    Generates random alphabetic text for generic form fields.
    """
    return ''.join(random.choices(string.ascii_letters, k=length))

# ==============================
# Field Classification
# ==============================

def classify_field(field):
    """
    Classifies a form field as email, password, or generic text
    based on type, name or id attributes.
    """

    field_type = (field.get("type") or "").lower()
    name = (field.get("name") or "").lower()
    field_id = (field.get("id") or "").lower()

    if field_type == "email" or \
       "email" in name or "mail" in name or \
       "email" in field_id:
        return "email"

    if field_type == "password" or \
       "pass" in name or "pwd" in name or \
       "password" in field_id:
        return "password"

    return "text"

# ==============================
# Payload Builder
# ==============================

def build_payload(form, fqdn=None):
    """
    Builds a dynamic payload for a selected form.
    Email fields receive randomized email addresses.
    Password fields receive randomized passwords.
    Other fields receive generic random text.
    """

    payload = {}

    for field in form["fields"]:
        name = field.get("name")
        if not name:
            continue

        field_type = classify_field(field)

        if field_type == "email":
            if fqdn:
                payload[name] = f"{random_username()}@{fqdn}"
            else:
                payload[name] = f"{random_username()}@example.com"

        elif field_type == "password":
            payload[name] = random_password()

        else:
            payload[name] = random_text()

    return payload

# ==============================
# CLI Arguments
# ==============================

def parse_arguments():
    """
    Parses command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="KITSUNE - Web Form Crawler and Testing Tool"
    )

    parser.add_argument("-u", "--url", required=True,
                        help="Target URL to crawl")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")

    parser.add_argument("--form-test", action="store_true",
                        help="Activate interactive form testing mode")

    parser.add_argument("--max-requests", type=int, default=None,
                        help="Maximum number of automated form submissions")

    parser.add_argument("--timeout", type=int, default=10,
                        help="Request timeout in seconds")

    parser.add_argument("--threads", type=int, default=5,
                        help="Number of crawling threads")

    parser.add_argument("--user-agent", type=str,
                        help="Custom User-Agent string")

    return parser.parse_args()

# ==============================
# Multithreaded Crawler
# ==============================

class Crawler:
    """
    Multithreaded web crawler that:
    - Crawls internal links
    - Extracts forms
    - Stores form metadata
    """

    def __init__(self, base_url, headers, timeout=10, threads=5):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.headers = headers
        self.timeout = timeout
        self.threads = threads

        self.visited = set()
        self.forms = []
        self.queue = queue.Queue()

    def start(self):
        """
        Starts the crawling process using worker threads.
        """
        self.queue.put(self.base_url)

        workers = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            workers.append(t)

        self.queue.join()

        return self.forms

    def worker(self):
        """
        Worker thread that processes URLs from the queue.
        """
        while True:
            try:
                url = self.queue.get(timeout=1)
            except queue.Empty:
                return

            if url not in self.visited:
                self.visited.add(url)
                self.process_url(url)

            self.queue.task_done()

    def process_url(self, url):
        """
        Fetches a URL, extracts forms and internal links.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.text, "html.parser")

            self.extract_forms(soup, url)
            self.extract_links(soup, url)

        except Exception as e:
            logging.debug(f"Error processing {url}: {e}")

    def extract_links(self, soup, current_url):
        """
        Extracts internal links and adds them to the queue.
        """
        for link in soup.find_all("a", href=True):
            href = urljoin(current_url, link["href"])
            parsed = urlparse(href)

            if parsed.netloc == self.domain:
                if href not in self.visited:
                    self.queue.put(href)

    def extract_forms(self, soup, url):
        """
        Extracts forms and stores structured metadata.
        """
        forms = soup.find_all("form")

        for form in forms:
            form_details = {}
            form_details["url"] = url
            form_details["action"] = form.get("action")
            form_details["method"] = (form.get("method") or "get").lower()

            inputs = []
            for input_tag in form.find_all(["input", "textarea"]):
                inputs.append({
                    "type": input_tag.get("type", "text"),
                    "name": input_tag.get("name"),
                    "id": input_tag.get("id")
                })

            form_details["fields"] = inputs
            self.forms.append(form_details)

# ==============================
# Form Display
# ==============================

def display_forms(forms):
    """
    Displays summary of detected forms.
    """

    print("\nCrawl completed")
    print(f"Forms found: {len(forms)}")

    for i, form in enumerate(forms, 1):
        print(f"Form {i}")
        print(f"  URL: {form['url']}")
        print(f"  Method: {form['method'].upper()}")
        print(f"  Action: {form['action']}")
        print("  Fields:")

        for field in form["fields"]:
            print(f"    - type: {field['type']}, name: {field['name']}, id: {field['id']}")

        print()

# ==============================
# Interactive Form Selection
# ==============================

def select_form(forms):
    """
    Prompts user to select a form by index.
    """

    while True:
        try:
            choice = int(input("Select the number of the form to be tested: "))
            if 1 <= choice <= len(forms):
                return forms[choice - 1]
        except ValueError:
            pass

        print("Invalid selection.")

# ==============================
# Automated Form Testing
# ==============================

def test_form(form, headers, timeout, max_requests=None):
    """
    Continuously submits randomized payloads to the selected form.
    - Detects email field
    - Prompts user for FQDN
    - Submits at random intervals
    - Stops on Ctrl+C or max_requests
    """

    email_present = any(
        classify_field(field) == "email"
        for field in form["fields"]
    )

    fqdn = None
    if email_present:
        fqdn = input("Enter the DOMAIN to generate emails: ")

    target_url = urljoin(form["url"], form["action"]) if form["action"] else form["url"]

    count = 0

    print("\nStarting automatic sending. Ctrl+C to stop.\n")

    try:
        while True:
            payload = build_payload(form, fqdn)

            if form["method"] == "post":
                response = requests.post(target_url,
                                         data=payload,
                                         headers=headers,
                                         timeout=timeout)
            else:
                response = requests.get(target_url,
                                        params=payload,
                                        headers=headers,
                                        timeout=timeout)

            count += 1

            print(f"Petition #{count} -> Status: {response.status_code}")

            if response.status_code == 429:
                print("Possible rate limiting detected.")

            if max_requests and count >= max_requests:
                print("The configured maximum number of shipments has been reached.")
                break

            sleep_time = random.randint(1, 10)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStopped by the user.")


# ==============================
# Main
# ==============================

def main():
    """
    Main execution function.
    """

    args = parse_arguments()

    configure_logging(args.verbose)
    print_banner()

    user_agent = args.user_agent if args.user_agent else DEFAULT_USER_AGENT

    headers = {
        "User-Agent": user_agent
    }

    crawler = Crawler(
        base_url=args.url,
        headers=headers,
        timeout=args.timeout,
        threads=args.threads
    )

    forms = crawler.start()

    if not forms:
        print("No forms were found.")
        return

    display_forms(forms)

    if args.form_test:
       selected_form = select_form(forms)
       test_form(
           selected_form,
           headers=headers,
           timeout=args.timeout,
           max_requests=args.max_requests
       )


if __name__ == "__main__":
    main()
