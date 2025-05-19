import json
import os
from datetime import datetime

# کلاس پایگاه داده
class Database:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {"users": [], "products": [], "orders": []}
    
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

# کلاس محصول
class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.id}: {self.name} - {self.price} تومان ({self.quantity} عدد)"

# کلاس سبد خرید
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, product, quantity):
        if product.quantity >= quantity:
            if product.id in self.items:
                self.items[product.id] += quantity
            else:
                self.items[product.id] = quantity
            return True
        return False
    
    def calculate_total(self, products):
        total = 0
        for product_id, quantity in self.items.items():
            product = next(p for p in products if p.id == product_id)
            total += product.price * quantity
        return total

# کلاس اصلی فروشگاه
class OnlineStore:
    def __init__(self):
        self.db = Database("store_data.json")
        self.current_user = None
        self.cart = ShoppingCart()
        
        # اگر محصولی وجود ندارد، نمونه‌های اولیه را ایجاد کن
        if not self.db.data["products"]:
            self._init_sample_products()
    
    def _init_sample_products(self):
        sample_products = [
            {"id": 1, "name": "لپ تاپ", "price": 25000000, "quantity": 10},
            {"id": 2, "name": "موبایل", "price": 15000000, "quantity": 15},
            {"id": 3, "name": "هدفون", "price": 3000000, "quantity": 20}
        ]
        self.db.data["products"] = sample_products
        self.db.save()
    
    def show_products(self):
        print("\nمحصولات موجود:")
        for product_data in self.db.data["products"]:
            product = Product(**product_data)
            print(product)
    
    def add_to_cart(self):
        self.show_products()
        try:
            product_id = int(input("شناسه محصول: "))
            quantity = int(input("تعداد: "))
            
            product_data = next(
                (p for p in self.db.data["products"] if p["id"] == product_id), 
                None
            )
            
            if product_data:
                product = Product(**product_data)
                if self.cart.add_item(product, quantity):
                    print(f"{quantity} عدد {product.name} به سبد خرید اضافه شد.")
                else:
                    print("موجودی کافی نیست!")
            else:
                print("محصول یافت نشد!")
        except ValueError:
            print("ورودی نامعتبر!")
    
    def view_cart(self):
        if not self.cart.items:
            print("سبد خرید خالی است.")
            return
        
        print("\nسبد خرید شما:")
        for product_id, quantity in self.cart.items.items():
            product_data = next(p for p in self.db.data["products"] if p["id"] == product_id)
            product = Product(**product_data)
            print(f"{product.name} - {quantity} عدد - {product.price * quantity} تومان")
        
        total = self.cart.calculate_total(
            [Product(**p) for p in self.db.data["products"]]
        )
        print(f"جمع کل: {total} تومان")
    
    def checkout(self):
        if not self.cart.items:
            print("سبد خرید خالی است.")
            return
        
        self.view_cart()
        confirm = input("آیا می‌خواهید پرداخت کنید؟ (y/n): ").lower()
        
        if confirm == 'y':
            # کاهش موجودی محصولات
            for product_id, quantity in self.cart.items.items():
                for product in self.db.data["products"]:
                    if product["id"] == product_id:
                        product["quantity"] -= quantity
            
            # ثبت سفارش
            new_order = {
                "id": len(self.db.data["orders"]) + 1,
                "items": self.cart.items,
                "total": self.cart.calculate_total(
                    [Product(**p) for p in self.db.data["products"]]
                ),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.db.data["orders"].append(new_order)
            self.db.save()
            
            print("پرداخت با موفقیت انجام شد! سفارش شما ثبت گردید.")
            self.cart.items = {}
        else:
            print("پرداخت لغو شد.")

    def run(self):
        while True:
            print("\nفروشگاه آنلاین")
            print("1. مشاهده محصولات")
            print("2. افزودن به سبد خرید")
            print("3. مشاهده سبد خرید")
            print("4. پرداخت")
            print("5. خروج")
            
            choice = input("لطفا گزینه مورد نظر را انتخاب کنید: ")
            
            if choice == "1":
                self.show_products()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.checkout()
            elif choice == "5":
                print("با تشکر از شما!")
                break
            else:
                print("گزینه نامعتبر!")

# اجرای برنامه
if __name__ == "__main__":
    store = OnlineStore()
    store.run()