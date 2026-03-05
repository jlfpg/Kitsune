# Kitsune

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Version](https://img.shields.io/badge/version-1.0-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Security](https://img.shields.io/badge/purpose-security%20labs-orange)
![Status](https://img.shields.io/badge/status-active-success)

Kitsune is a Python-based web form discovery and interaction tool designed for security audits and phishing audits. It crawls a website, discovers forms across multiple pages, extracts their fields, and optionally interacts with them by sending randomized data.

---

# Features

* Recursive website crawling
* Automatic form detection
* Extraction of form metadata
* Detection of hidden forms
* Detection of forms without `method`
* Detection of forms without `action`
* Automatic link discovery
* Multi-threaded crawling
* HTTPS security analysis
* Custom User-Agent support
* Progress bar visualization
* Structured logging system
* Interactive form testing mode
* Automatic random payload generation for form fields

---

# Form Interaction Mode

When enabled, Kitsune allows the user to interact with a discovered form automatically.

The tool generates realistic randomized input depending on the field type.

## Email Fields

Detected when:

* `type="email"`
* the field `name` or `id` contains the word `email`

The user provides a domain (FQDN), and the tool generates addresses like:

```
jhon@domain.com
mike@domain.com
sarah@domain.com
```

---

## Password Fields

Detected when:

* `type="password"`
* the field `name` or `id` contains the word `password`

Random passwords are generated with:

* Length between **8 and 12 characters**
* Special characters allowed:

```
._!$&%
```

Example:

```
k3!fP$8a
Zp$1._aD9
```

---

## Other Fields

All other form inputs receive randomized text strings.

---

## Request Timing

Requests are sent with **random delays between 1 and 10 seconds** to simulate human interaction.

The process continues until the user manually stops the script.

---

# Installation

Clone the repository:

```
git clone https://github.com/jlfpg/kitsune.git
cd kitsune
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Usage

Basic usage:

```
python kitsune.py -u https://example.com
```

---

# Command Line Arguments

| Flag             | Description                                    |
| ---------------- | ---------------------------------------------- |
| `-u`             | Target URL                                     |
| `-t`             | Number of threads (default: 5)                 |
| `--timeout`      | HTTP request timeout                           |
| `--insecure`     | Allow insecure HTTPS connections               |
| `--stealth`      | Use a mobile-style User-Agent                  |
| `--user-agent`   | Custom User-Agent string                       |
| `-v`             | Verbose output                                 |
| `--form-test`    | Enable form interaction mode                   |
| `--max-requests` | Maximum number of requests during form testing |

---

# Examples

## Basic Crawl

```
python kitsune.py -u https://example.com
```

---

## Crawl with Multiple Threads

```
python kitsune.py -u https://example.com -t 10
```

---

## Verbose Mode

Shows detailed information about forms and fields.

```
python kitsune.py -u https://example.com -v
```

---

## Custom User-Agent

```
python kitsune.py -u https://example.com --user-agent "Mozilla/5.0 CustomAgent"
```

---

## Allow Insecure HTTPS

```
python kitsune.py -u https://example.com --insecure
```

---

## Interactive Form Testing

```
python kitsune.py -u https://example.com --form-test
```

After crawling, the tool will prompt:

```
Select the form number to interact with:
```

Once selected, Kitsune will begin sending randomized payloads to the form.

---

# Example Output

```
Forms discovered: 3

Form #1
URL: https://example.com/login
Method: POST
Fields:
- email
- password
- submit

Form #2
URL: https://example.com/contact
Method: POST
Fields:
- name
- email
- message
```

---

# Disclaimer

This tool is intended **for authorized testing only**.

Do **not** use it against systems without permission.

---