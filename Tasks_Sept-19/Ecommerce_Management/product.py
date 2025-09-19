class Product:
    def __init__(self, id, name, category, price, stock):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
    
    def update_stock(self, qty):
        """Decrease stock after purchase"""
        if self.stock >= qty:
            self.stock -= qty
            return True
        else:
            print(f"Insufficient stock for {self.name}. Available: {self.stock}, Requested: {qty}")
            return False
    
    def __str__(self):
        return f"{self.name} (₹{self.price}) - {self.stock} in stock"