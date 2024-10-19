Eco-Friendly Water Bottles E-Commerce Website
Welcome to the Eco-Friendly Water Bottles e-commerce website! This project is built using Django and aims to provide users with a platform to purchase eco-friendly and reusable water bottles. The website includes features like user registration, authentication, shopping cart functionality, a checkout process with multiple payment options, product search, and more.

Project Overview-
The Eco-Friendly Water Bottles project was created to promote environmentally friendly and sustainable alternatives to single-use plastic bottles. Users can browse and purchase a range of eco-friendly water bottles, with features to enhance the user experience, including:
Account management (registration, login).
Shopping cart and order management.
Payment methods including Cash on Delivery (COD) and mobile payments (UPI).
Search functionality to easily find products.

Technologies Used-
Frontend: HTML, CSS
Backend: Python, Django
Database: SQLite (default Django database) 
Payment Integration: UPI, Cash on Delivery (COD)
Authentication: Django’s built-in user authentication system

Installation-
Follow these steps to get the project running on your local machine.

Clone the repository:
git clone https://github.com/SonuNMGit/CodeAlpha_Ecommerce_Store.git
cd CodeAlpha_Ecommerce_Store

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Access the project: Open your web browser and go to http://127.0.0.1:8000/.

Usage-
Once the website is up and running, you can:
Register for an account.
Browse eco-friendly water bottles.
Add products to the cart.
Proceed to checkout and choose a payment method.
Track your orders.

Admin Access-
If you want to access the Django admin panel:
Create a superuser:
python manage.py createsuperuser
Go to http://127.0.0.1:8000/admin/ and log in with your credentials.
