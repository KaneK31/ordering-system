# 🛒 Ordering System (Django + PayPal)

A simple Django-based food ordering platform with integrated PayPal Checkout and IPN support.

Users can browse products, add them to a cart, and securely complete payment. Order status is automatically updated via PayPal IPN.

---


## ✨ Features

- 🧾 User registration and login
- 🍔 Product catalog with stock tracking
- 🛒 Shopping cart (session-based)
- 💰 PayPal payment integration (sandbox mode)
- 🔄 Instant Payment Notification (IPN) to verify payment server-side
- 📦 Order history for logged-in users
- ⚙️ Admin dashboard for product management

---

## 🚀 Tech Stack

- **Backend**: Python 3.11, Django 5.2.1
- **Database**: SQLite (dev), ready for PostgreSQL
- **Payments**: PayPal Standard + IPN (`paypal.standard.ipn`)
- **Frontend**: Django Templates + Bootstrap 5

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/KaneK31/ordering-system.git
cd ordering-system

pip install -r requirements.txt

4. Environment Variables
DJANGO_SECRET_KEY=your-django-secret-key
BASE_URL=http://127.0.0.1:8000 
PAYPAL_RECEIVER_EMAIL=your-business-sandbox@email.com
