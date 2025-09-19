import csv
import json
from product import Product
from customer import Customer
from order import Order

class ECommerceSystem:
    def __init__(self):
        self.products = []
        self.customers = {}
        self.orders = []
        
    def load_products(self):
        """Load products from CSV file"""
        try:
            with open('products.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product = Product(
                        int(row['id']),
                        row['name'],
                        row['category'],
                        float(row['price']),
                        int(row['stock'])
                    )
                    self.products.append(product)
            print("Products loaded successfully!")
        except FileNotFoundError:
            print("Products file not found.")
        except Exception as e:
            print(f"Error loading products: {e}")
    
    def load_orders(self):
        """Load orders from JSON file"""
        try:
            with open('orders.json', 'r') as file:
                orders_data = json.load(file)
                for order_data in orders_data:
                    customer_name = order_data['customer']
                    
                    # Create customer if not exists
                    if customer_name not in self.customers:
                        self.customers[customer_name] = Customer(customer_name)
                    
                    # Create order
                    order = Order(order_data['order_id'], self.customers[customer_name])
                    
                    # Add items to order
                    for item in order_data['items']:
                        product_id = item['product_id']
                        quantity = item['qty']
                        
                        # Find product
                        product = next((p for p in self.products if p.id == product_id), None)
                        if product:
                            order.add_item(product, quantity)
                    
                    self.orders.append(order)
                    self.customers[customer_name].add_order(order)
            print("Orders loaded successfully!")
        except FileNotFoundError:
            print("Orders file not found.")
        except Exception as e:
            print(f"Error loading orders: {e}")
    
    def save_products(self):
        """Save products to CSV file"""
        try:
            with open('products.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'category', 'price', 'stock'])
                for product in self.products:
                    writer.writerow([product.id, product.name, product.category, product.price, product.stock])
            print("Products saved successfully!")
        except Exception as e:
            print(f"Error saving products: {e}")
    
    def save_orders(self):
        """Save orders to JSON file"""
        try:
            orders_data = []
            for order in self.orders:
                order_data = {
                    'order_id': order.order_id,
                    'customer': order.customer.name,
                    'items': [{'product_id': item['product'].id, 'qty': item['quantity']} 
                             for item in order.items]
                }
                orders_data.append(order_data)
            
            with open('orders.json', 'w') as file:
                json.dump(orders_data, file, indent=2)
            print("Orders saved successfully!")
        except Exception as e:
            print(f"Error saving orders: {e}")
    
    def print_all_products(self):
        """Print all available products"""
        print("\n=== ALL PRODUCTS ===")
        for product in self.products:
            print(f"ID: {product.id}, Name: {product.name}, Category: {product.category}, "
                  f"Price: ₹{product.price}, Stock: {product.stock}")
    
    def find_most_expensive_product(self):
        """Find and return the most expensive product"""
        if not self.products:
            return None
        return max(self.products, key=lambda p: p.price)
    
    def process_order(self, order):
        """Process an order and update stock"""
        for item in order.items:
            product = item['product']
            quantity = item['quantity']
            product.update_stock(quantity)
        self.orders.append(order)
        order.customer.add_order(order)
        self.save_products()
        self.save_orders()
    
    def get_customer_orders(self, customer_name):
        """Get all orders for a customer"""
        if customer_name in self.customers:
            return self.customers[customer_name].orders
        return []
    
    def print_order_totals(self):
        """Print customer names and total bills for all orders"""
        print("\n=== ORDER TOTALS ===")
        for order in self.orders:
            print(f"Customer: {order.customer.name}, Total: ₹{order.get_total()}")
    
    def find_most_ordered_product(self):
        """Find the product with the highest total quantity ordered"""
        product_quantities = {}
        for order in self.orders:
            for item in order.items:
                product_id = item['product'].id
                quantity = item['quantity']
                if product_id in product_quantities:
                    product_quantities[product_id] += quantity
                else:
                    product_quantities[product_id] = quantity
        
        if not product_quantities:
            return None, 0
        
        max_product_id = max(product_quantities, key=product_quantities.get)
        max_product = next((p for p in self.products if p.id == max_product_id), None)
        return max_product, product_quantities[max_product_id]
    
    def generate_sales_report(self):
        """Generate sales report with total revenue, revenue by category, and top customer"""
        print("\n=== SALES REPORT ===")
        
        # Total revenue
        total_revenue = sum(order.get_total() for order in self.orders)
        print(f"Total Revenue: ₹{total_revenue}")
        
        # Revenue by category
        category_revenue = {}
        for order in self.orders:
            for item in order.items:
                category = item['product'].category
                revenue = item['product'].price * item['quantity']
                if category in category_revenue:
                    category_revenue[category] += revenue
                else:
                    category_revenue[category] = revenue
        
        print("\nRevenue by Category:")
        for category, revenue in category_revenue.items():
            print(f"{category}: ₹{revenue}")
        
        # Customer with highest spending
        if self.customers:
            top_customer = max(self.customers.values(), key=lambda c: c.get_total_spent())
            print(f"\nTop Customer: {top_customer.name} - ₹{top_customer.get_total_spent()}")
    
    def generate_inventory_report(self):
        """Generate inventory report with low stock alerts and average prices by category"""
        print("\n=== INVENTORY REPORT ===")
        
        # Low stock alert
        low_stock_products = [p for p in self.products if p.stock < 5]
        if low_stock_products:
            print("Low Stock Alert (stock < 5):")
            for product in low_stock_products:
                print(f"{product.name}: {product.stock} remaining")
        else:
            print("No products with low stock.")
        
        # Average price by category
        category_prices = {}
        category_counts = {}
        for product in self.products:
            if product.category in category_prices:
                category_prices[product.category] += product.price
                category_counts[product.category] += 1
            else:
                category_prices[product.category] = product.price
                category_counts[product.category] = 1
        
        print("\nAverage Price by Category:")
        for category, total_price in category_prices.items():
            avg_price = total_price / category_counts[category]
            print(f"{category}: ₹{avg_price:.2f}")
    
    def place_new_order(self):
        """Allow user to place a new order"""
        print("\n=== PLACE NEW ORDER ===")
        
        # Get customer name
        customer_name = input("Enter customer name: ")
        if customer_name not in self.customers:
            self.customers[customer_name] = Customer(customer_name)
        
        # Create new order
        new_order_id = max([order.order_id for order in self.orders], default=100) + 1
        order = Order(new_order_id, self.customers[customer_name])
        
        # Add items to order
        while True:
            self.print_all_products()
            try:
                product_id = int(input("Enter product ID to add to order (0 to finish): "))
                if product_id == 0:
                    break
                
                product = next((p for p in self.products if p.id == product_id), None)
                if not product:
                    print("Invalid product ID.")
                    continue
                
                quantity = int(input(f"Enter quantity for {product.name}: "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    continue
                
                if product.stock < quantity:
                    print(f"Only {product.stock} available. Cannot add {quantity}.")
                    continue
                
                order.add_item(product, quantity)
                print(f"Added {quantity} x {product.name} to order.")
                
            except ValueError:
                print("Please enter a valid number.")
        
        if not order.items:
            print("Order cancelled. No items added.")
            return
        
        # Confirm and process order
        print(f"\nOrder Summary: Total: ₹{order.get_total()}")
        confirm = input("Confirm order? (y/n): ").lower()
        if confirm == 'y':
            self.process_order(order)
            print("Order placed successfully!")
        else:
            print("Order cancelled.")
    
    def view_all_orders(self):
        """Display all orders"""
        print("\n=== ALL ORDERS ===")
        if not self.orders:
            print("No orders found.")
            return
        
        for order in self.orders:
            print(f"\nOrder ID: {order.order_id}, Customer: {order.customer.name}")
            print("Items:")
            for item in order.items:
                print(f"  - {item['product'].name} (Qty: {item['quantity']}, Price: ₹{item['product'].price})")
            print(f"Total: ₹{order.get_total()}")
    
    def run_menu(self):
        """Run the main menu interface"""
        # Load data
        self.load_products()
        self.load_orders()
        
        while True:
            print("\n=== E-COMMERCE ORDER MANAGEMENT SYSTEM ===")
            print("1. View Products")
            print("2. Place New Order")
            print("3. View All Orders")
            print("4. Generate Sales Report")
            print("5. Generate Inventory Report")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.print_all_products()
                most_expensive = self.find_most_expensive_product()
                if most_expensive:
                    print(f"\nMost Expensive Product: {most_expensive.name} - ₹{most_expensive.price}")
                
                most_ordered, qty = self.find_most_ordered_product()
                if most_ordered:
                    print(f"Most Ordered Product: {most_ordered.name} - {qty} units")
            
            elif choice == '2':
                self.place_new_order()
            
            elif choice == '3':
                self.view_all_orders()
            
            elif choice == '4':
                self.generate_sales_report()
            
            elif choice == '5':
                self.generate_inventory_report()
            
            elif choice == '6':
                print("Thank you for using the E-Commerce Order Management System!")
                break
            
            else:
                print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    system = ECommerceSystem()
    system.run_menu()