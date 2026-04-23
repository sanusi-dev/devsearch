# DevSearch 🔍

**A Developer Talent Marketplace — built with Django, HTMX, and Tailwind CSS**

DevSearch is a full-stack web platform where developers can showcase their portfolios and clients can discover and connect with technical talent. It features dynamic, SPA-like navigation without a JavaScript framework, a real-time email notification pipeline, GitHub OAuth, and a polished dark-mode UI.

> **Origin:** This project started as a follow-along of Dennis Ivy's Django course on Udemy. After completing the tutorial I significantly extended the codebase — adding HTMX-powered partial rendering, GitHub social login, a queued email system with background workers, SweetAlert2 confirmation modals, dark mode, a custom messaging middleware, and more. The tutorial provided the data model foundation; everything beyond CRUD is original work.

---

## 📸 Screenshots

### Developer Profiles
![Devsearch Home](https://github.com/user-attachments/assets/f6a75330-a46b-4f00-8ad4-65a127d7e466)

### Project Showcase
![DevSearch Projects](https://github.com/user-attachments/assets/3a2c6a72-daaf-4f45-a416-24a4add82829)

### Developer Portfolio Page
![Devsearch Profile](https://github.com/user-attachments/assets/1b198682-b422-4d11-9fcf-3f8554315d23)

### Inbox
<img width="1273" height="518" alt="Devsearch Inbox" src="https://github.com/user-attachments/assets/bfc74987-22ed-4c8d-876c-c41c7c57401d" />

---

## 🎥 Demo

> *A walkthrough video will be added here. In the meantime, see the screenshots above.*

---

## ✨ Features

### Core (Tutorial Foundation)
- **Developer Profiles** — Showcase name, bio, location, skills, and social links
- **Project Portfolio** — Upload projects with images, descriptions, tags, and external links
- **Peer Reviews** — Community up/downvote system with written feedback
- **Search & Discovery** — Search developers by name, skill, or intro; search projects by title, tag, or description
- **Direct Messaging** — Contact any developer via a built-in message form
- **Inbox** — Manage received messages with read/unread tracking

### Original Additions (Beyond the Tutorial)

| Feature | Details |
|---|---|
| **HTMX Partial Rendering** | All navigation, search, and form submissions update the page without a full reload, using Django's `{% partialdef %}` template blocks. Zero React, zero Vue. |
| **GitHub OAuth** | Full social authentication via `django-allauth`. Users can sign up and log in with their GitHub account. |
| **Queued Email System** | `django-mailer` queues all outgoing emails in the database. A separate background worker process dispatches them asynchronously, making the app resilient to SMTP failures. |
| **Unread Message Notifications** | A custom management command (`notify_unread_messages`) emails users a daily digest of unread messages. Includes a cryptographically-signed one-click unsubscribe link. |
| **Welcome Emails** | HTML + plaintext transactional welcome emails sent on signup, with personalised content based on whether the user signed up via email or GitHub. |
| **SweetAlert2 Modals** | All destructive actions (delete project, delete message, delete skill) trigger a confirmation modal instead of a separate confirmation page — no extra views or templates required. |
| **Toast Notifications** | Django's messages framework is serialised to JSON and surfaced as SweetAlert2 toasts — works seamlessly for both standard page loads and HTMX partial swaps via a custom `HtmxMessageMiddleware`. |
| **Dark Mode** | Full dark mode implementation with persistent preference stored in `localStorage`. Smooth transitions throughout. |
| **Database-Level Constraints** | A `CheckConstraint` on the `Message` model prevents a user from messaging themselves at the database level, not just the application level. |
| **Auto-complete URL Normalisation** | The project form automatically prepends `https://` to bare URLs entered by users, preventing broken links. |
| **Improved Admin** | All models use the `@admin.register` decorator pattern with `list_display`, `search_fields`, and `list_filter` configurations for immediate usability. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 6.0, Python 3.x |
| **Authentication** | django-allauth 65 (email + GitHub OAuth) |
| **Database** | SQLite (dev) — easily swapped for PostgreSQL in production |
| **Frontend** | HTMX 1.9, Tailwind CSS 3, Vanilla JS |
| **Email** | django-mailer (queue) → SMTP (delivery) |
| **UI Libraries** | SweetAlert2, iconmonstr |
| **Templating** | Django Templates with `django-widget-tweaks` |
| **Environment** | python-decouple |

---

## ⚡ Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

### 1 · Clone the repository

```bash
git clone https://github.com/sanusi-dev/devsearch.git
cd devsearch
```

### 2 · Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values. At minimum, you need:

- `SECRET_KEY` — generate one with: `python -c "import secrets; print(secrets.token_hex(50))"`
- `DEV_EMAIL_USER` and `DEV_EMAIL_PASSWORD` — a free [Mailtrap](https://mailtrap.io) sandbox inbox works perfectly for local development

> **GitHub OAuth (optional):** If you want GitHub login to work locally, create an OAuth App at [github.com/settings/developers](https://github.com/settings/developers). Set the callback URL to `http://127.0.0.1:8000/accounts/github/login/callback/` and add the credentials to `.env`.

### 3 · Install dependencies

```bash
# Python dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Node dependencies (for Tailwind CSS build)
npm install
```

Or, if you have `make`:

```bash
make install
```

### 4 · Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
```

### 5 · Build the CSS

```bash
npm run build:css
# Or to watch for changes during development:
npm run watch:css
```

### 6 · Start the development server

You need **two terminal windows** for the full experience:

**Terminal 1 — Django:**
```bash
python manage.py runserver
```

**Terminal 2 — Email worker (optional, for email features):**
```bash
./run_mailer.sh
```

Visit `http://127.0.0.1:8000/` — you'll land on the developer profiles page.

---

## 🏗️ Architecture & Design Decisions

### HTMX Partial Rendering Strategy

Instead of a separate API + SPA approach, DevSearch uses Django's [`django-template-partials`](https://github.com/carltongibson/django-template-partials) pattern — `{% partialdef %}` blocks within standard templates. When HTMX makes a request, Django detects the `Hx-Request` header and returns only the named block fragment. This keeps the logic entirely server-side with no duplication of routes or serialisers.

```
Full page load  →  return render(request, "template.html")
HTMX request    →  return render(request, "template.html#partial-name")
```

### Toast Notification Architecture

The `HtmxMessageMiddleware` intercepts outgoing HTMX responses and serialises any Django messages into the `HX-Trigger` response header as JSON. The frontend listens for the `messages` event and fires SweetAlert2 toasts. This means the same `messages.success(...)` call in a view works identically whether the request was a full page load or an HTMX swap.

### Email Queue

All email sending goes through `django-mailer`, which writes to a database queue table instead of calling SMTP directly. This means:
- A slow or unresponsive SMTP server never blocks a web request
- Failed sends are retried automatically
- A separate worker process (`run_mailer.sh`) is the only thing that touches SMTP

### Database Constraints

The `Message.prevent_self_message` `CheckConstraint` enforces the "can't message yourself" rule at the database level. This is more robust than application-level validation, which can be bypassed by direct API calls or data imports.

---

## 🗓️ Scheduled Tasks (Production)

The `notify_unread_messages` management command should be run on a schedule in production:

**PaaS (Render, Heroku, Railway):** Use the platform's built-in Cron Job / Scheduler feature.
```
Command: python manage.py notify_unread_messages
Schedule: 0 8 * * *   (daily at 8 AM)
```

**VPS (DigitalOcean, AWS EC2):** Add a crontab entry:
```bash
0 8 * * * cd /path/to/devsearch && .venv/bin/python manage.py notify_unread_messages >> /var/log/devsearch-notify.log 2>&1
```

---

## 📂 Project Structure

```
devsearch/
├── devsearch/              # Django project package
│   ├── settings.py         # Environment-driven settings
│   ├── middleware.py        # Custom HtmxMessageMiddleware
│   └── urls.py
├── projects/               # Project portfolio app
│   ├── models.py           # Project, Review, Tag
│   ├── signals.py          # Auto-recalculate vote_ratio on review save/delete
│   └── views.py
├── users/                  # User & profile app
│   ├── models.py           # Profile, Skill, Message
│   ├── signals.py          # Profile creation, welcome email on signup
│   ├── views.py
│   └── management/
│       └── commands/
│           └── notify_unread_messages.py   # Scheduled email digest
├── templates/              # Global templates (base, navbar, pagination)
│   └── account/            # django-allauth overrides
├── static/
│   ├── js/
│   │   ├── htmx.min.js
│   │   └── main.js         # Toast system, active nav, SweetAlert2 confirm
│   └── styles/
│       └── input.css       # Tailwind source (output.css is git-ignored)
├── .env.example            # All required environment variables with docs
├── Makefile                # Developer shortcuts
├── run_mailer.sh           # Background email worker
├── requirements.txt
└── package.json            # Tailwind CSS build tooling
```

---

## 🔮 Future Enhancements

- [ ] Real-time notifications with Django Channels / WebSockets
- [ ] PostgreSQL support (swap SQLite for production)
- [ ] REST API endpoints for third-party integrations
- [ ] Advanced developer search (filter by location, availability, tech stack)
- [ ] Payment integration for premium profiles

---

## 🙏 Acknowledgments

- **Dennis Ivy** — whose Udemy Django course provided the project concept and initial data model
- The **Django**, **HTMX**, and **django-allauth** communities for outstanding documentation

---

⭐ If you found this project helpful or interesting, a star on GitHub goes a long way!
