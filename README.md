# Shop Project

A comprehensive E-commerce platform built with Django, featuring advanced authentication, real-time support chat, and a full order management system.

## 🚀 Key Features

### 🔐 Advanced Authentication
*   **Hybrid Login:** Users can log in using either their **Email** or **Phone Number** via a custom authentication backend.
    *   *Implementation:* `EmailPhoneAuthBackend`
*   **OTP Verification:** Secure registration process using SMS One-Time Passwords (via Kavenegar).
*   **Custom User Model:** Extended user profile including National Code, City, and Address fields.

### 🛒 Shopping & Products
*   **Product Catalog:** Categorized products with subcategories, images, and detailed descriptions.
*   **Smart Search:** Postgres-based search functionality for finding products efficiently.
*   **Data Population:** Includes a custom management command to populate the database with fake products for testing.
    *   *Command:* `populate_products`
*   **AJAX Pagination:** Infinite scroll/load more functionality for product listings.

### 📦 Orders & Payments
*   **Shopping Cart:** Session-based cart management with custom template filters for price calculations.
    *   *Helper:* `multiply` filter
*   **Checkout System:** Full checkout flow with address management.
*   **Payment Gateway:** Integration with **Zarinpal** for secure payment processing.
*   **Order History:** Users can track order status (Pending, Paid, Delivered) in their profile.

### 💬 Real-Time Support Chat
*   **Live Chat:** WebSocket-based support system using **Django Channels**.
*   **Role-Based Access:**
    *   **Users:** Can initiate chat sessions with support staff.
    *   **Admins/Staff:** Have a dedicated dashboard to view and reply to active user sessions.
*   **Persistence:** Chat history is saved to the database.
    *   *Logic:* `support_chat` Consumer

### 🔌 API
*   **REST API:** Fully functional API built with Django Rest Framework (DRF).
*   **Documentation:** Auto-generated API documentation using `drf-spectacular` (Swagger UI).

---

## 🛠️ Tech Stack

*   **Backend:** Python, Django 5.2
*   **API:** Django Rest Framework
*   **Real-time:** Django Channels, Redis
*   **Async Tasks:** Celery
*   **Database:** PostgreSQL (Production), SQLite (Dev)
*   **Frontend:** Django Templates, Bootstrap 5, jQuery
*   **Utilities:** Faker (Data generation), Kavenegar (SMS)

---

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Shop
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv env
    # Windows
    .\env\Scripts\activate
    # Linux/Mac
    source env/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    *   Ensure Redis is running (required for Channels/Chat).
    *   Update database settings in `settings.py` if using PostgreSQL.

5.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Populate Dummy Data (Optional)**
    Generate 250 fake products for testing:
    ```bash
    python manage.py populate_products --count=250 --threads=15
    ```

7.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

---

## 📂 Project Structure

*   **`accounts/`**: User authentication, OTP, and profile management.
*   **`home/`**: Main product catalog, search, and homepage views.
*   **`order/`**: Cart logic, checkout process, and payment verification.
*   **`chat/`**: WebSocket consumers and routing for customer support.
*   **`Shop/`**: Project settings, URL configuration, and ASGI/WSGI entry points.
