class Customer:
    def __init__(self, name):
        self.name = name
        self.orders = []
    
    def add_order(self, order):
        """Add an order to customer's order history"""
        self.orders.append(order)
    
    def get_total_spent(self):
        """Calculate total amount spent by customer"""
        return sum(order.get_total() for order in self.orders)
    
    def __str__(self):
        return f"Customer: {self.name}, Orders: {len(self.orders)}, Total Spent: ₹{self.get_total_spent()}"