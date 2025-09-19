class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []  # List of dictionaries: {'product': product, 'quantity': qty}
    
    def add_item(self, product, quantity):
        """Add a product to the order"""
        self.items.append({
            'product': product,
            'quantity': quantity
        })
    
    def get_total(self):
        """Calculate total cost of the order"""
        total = 0
        for item in self.items:
            total += item['product'].price * item['quantity']
        return total
    
    def __str__(self):
        return f"Order #{self.order_id} - Customer: {self.customer.name}, Total: ₹{self.get_total()}"