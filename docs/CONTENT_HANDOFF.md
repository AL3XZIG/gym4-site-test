# Content handoff guide

## Purpose

This document explains how school staff can review the demo and what information is still required before the site can become an official resource.

The GitHub Pages version is a static prototype. It has no editorial account, database, upload interface or real message delivery. Editing it requires changing source files and rebuilding the site. The production architecture for browser-based editing is described in [ARCHITECTURE.md](ARCHITECTURE.md).

## What is ready

- Shared header, footer and navigation across the site.
- Responsive page layout and common visual components.
- Dedicated sections for organization information, parents, students, news, admissions and contacts.
- Explicit placeholder cards and table rows where verified school information must be inserted.
- Accessibility controls and a non-submitting demonstration form.
- Automated build and link checks.

## Content checklist

| Page | Information to provide |
|---|---|
| Main page | Approved description, priority announcements, approved photos and links |
| Organization information | Full/short legal name, address, founding date, contacts, management structure, educational programs, staff, material resources and required documents |
| Parents | Catering, safety, medical/psychological support, meetings, rules, notices and downloadable materials |
| Students | Timetable link, calendar, electronic diary link, library, clubs, competitions and project activities |
| News | Approved title, publication date, category, summary, full text, image/alt text and expiry date for notices |
| Admissions | Current admission procedure, dates, documents, official application links and vacancy data with update date |
| Contacts | Verified postal address, phone numbers, email, office hours, reception hours, route and accessibility information |

## Rules for filling placeholders

1. Confirm every factual statement with the school employee responsible for that information.
2. Record the source and verification date for documents, schedules, contacts and vacancy counts.
3. Do not publish personal phone numbers, private email addresses, student personal data or internal documents.
4. Use only images approved for publication; obtain permission where required.
5. Give every downloadable file a descriptive title, date/version and accessible format.
6. Remove expired announcements and update vacancy tables on a defined schedule.
7. Do not add a working contact form until the school approves the processing purpose, legal basis, notice, retention period, responsible staff and secure server-side workflow.

## Where source changes belong

- Page structure and placeholder text: `demo/build_demo.py`.
- Global design and responsive layout: `demo/assets/css/style.css`.
- Navigation, accessibility and UI behavior: `demo/assets/js/app.js`.
- Generated output: `demo/site/` — never edit this folder manually; rerun the generator instead.

The next maintainability step is moving page content into a structured data file so an editor can update approved text without editing Python or HTML templates.

## Before public demonstration

Run the generator and tests, inspect every page on desktop and mobile, check all local links, and make sure every unverified value remains visibly marked as a placeholder. The demo must continue to be labelled as unofficial.
