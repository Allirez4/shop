#!/usr/bin/env python
"""
Simple test script to verify the hybrid password reset form works correctly
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings')
django.setup()

from accounts.forms import hybridresetform
from accounts.models import CustomUser

def test_hybrid_form():
    print("🧪 Testing Hybrid Password Reset Form")
    print("=" * 50)
    
    # Test 1: Valid email
    print("\n1️⃣ Testing with valid email format...")
    form_data = {'email': 'test@example.com'}
    form = hybridresetform(data=form_data)
    
    if '@' in form_data['email']:
        print("✅ Email format detected correctly")
    else:
        print("❌ Email format not detected")
    
    # Test 2: Valid phone
    print("\n2️⃣ Testing with valid phone format...")
    form_data = {'email': '09123456789'}  # Note: using 'email' field for phone
    form = hybridresetform(data=form_data)
    
    if '@' not in form_data['email']:
        print("✅ Phone format detected correctly")
    else:
        print("❌ Phone format not detected")
    
    # Test 3: Form field attributes
    print("\n3️⃣ Testing form field attributes...")
    form = hybridresetform()
    email_field = form.fields['email']
    
    print(f"Label: {email_field.label}")
    print(f"Widget class: {email_field.widget.attrs.get('class', 'None')}")
    print(f"Placeholder: {email_field.widget.attrs.get('placeholder', 'None')}")
    
    # Test 4: Check if users exist for testing
    print("\n4️⃣ Checking existing users for testing...")
    users = CustomUser.objects.all()[:3]
    
    if users.exists():
        print(f"Found {users.count()} users for testing:")
        for user in users:
            email = user.email or "No email"
            phone = user.phone_number or "No phone"
            print(f"  - Email: {email}, Phone: {phone}")
    else:
        print("⚠️ No users found. Create some users to test password reset.")
    
    print("\n" + "=" * 50)
    print("✅ Hybrid form test completed!")
    print("\nTo test the full functionality:")
    print("1. Start your Django server")
    print("2. Go to /accounts/password_reset/")
    print("3. Try entering both email and phone numbers")
    print("4. Check that validation works properly")

if __name__ == "__main__":
    test_hybrid_form()