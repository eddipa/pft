# 💰 Personal Finance Tracker

A simple and elegant Django-based application for tracking your personal income and expenses. Easily manage your financial data, categorize transactions, and analyze trends through a user-friendly dashboard.

---

## ✨ Features

- 🔐 Email-based user authentication
- 💼 Manage multiple transaction accounts (e.g., bank, cash, digital wallet)
- 🗂️ Create custom categories for income and expenses
- ➕ Add income and expense transactions with details
- 📊 View a monthly dashboard with basic analytics
- 📁 Export filtered transactions to CSV

---

## ⚙️ Requirements

- Python 3.11+
- [Django 5.1](https://www.djangoproject.com/)
- [django-environ](https://github.com/joke2k/django-environ)

---

## 🚀 Getting Started

1. **Clone the repository** and create a virtual environment:
   ```bash
   git clone https://github.com/eddipa/pft.git
   cd pft
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Then edit .env to add your local config (e.g., secret key, debug, db settings)
   ```

4. **Apply migrations and create a superuser**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to start tracking your finances!

---

## 📁 Project Structure

```
personal-finance-tracker/
├── pft/             # Django project configuration
├── accounts/        # User authentication app (custom user model)
├── finance/         # Main finance tracking features
├── templates/       # HTML templates
├── static/          # Static assets (CSS, JS, icons)
└── manage.py
```

---

## 🧪 Running Tests

To run the test suite:

```bash
python manage.py test
```

---

## 📌 Notes

- Designed for local use and experimentation.
- Can be extended with bank API integrations, budgeting tools, or investment tracking.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

© 2024 Masoud Koochak. You are free to use, modify, and distribute this software under the terms of the MIT license.


---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.
