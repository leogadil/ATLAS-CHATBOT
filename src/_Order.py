
class Order:

    Name = ""
    Orders = {}
    confirmCheckout = False

    def __init___(self, Name=""):
        self.Name = Name

    def add_order(self, orders):
        for x in orders:
            if x['database_approximate'] is not None:
                item = self.Orders.get(x['database_approximate']['Order_id'])

                x['database_approximate']['Order_count'] = x['count']
                if item is None:
                    self.Orders[x['database_approximate']['Order_id']] = x['database_approximate']
                else:
                    self.Orders[x['database_approximate']['Order_id']]['Order_count'] += x['database_approximate']['Order_count']
        # print(self.Orders)

    def calculate(self):
        TotalPrice = 0
        TotalItem = 0
        TotalDuration = 0
        for x in self.Orders.values():
            TotalPrice += x['Order_price'] * x['Order_count']
            TotalItem += x['Order_count']
            TotalDuration += x['Order_duration']
        manifest = {
            "Price": TotalPrice,
            "Items": TotalItem,
            "Duration": TotalDuration
        }
        return manifest

    def delete_Item(self, orders):
        for x in orders:
            if x['database_approximate'] is not None:
                item = self.Orders.get(x['database_approximate']['Order_id'])

                x['database_approximate']['Order_count'] = x['count']
                if item is not None:
                    deducted = item['Order_count'] - x['database_approximate']['Order_count']
                    if deducted <= 0:
                        del self.Orders[x['database_approximate']['Order_id']]
                    else:
                        self.Orders[x['database_approximate']['Order_id']]['Order_count'] = x['database_approximate']['Order_count']
        return True

    def set_Name(self, _name):
        if self.Name == "":
            self.Name = _name
            return True
        else:
            return False

    def Delete_Orders(self):
        self.Orders = {}

    def checkout(self):
        if self.Name == "":
            self.confirmCheckout = False
            return "NAMEEMPTY"
        elif len(self.Orders) > 0:
            self.confirmCheckout = False
            return "CONFIRMED"
        else:
            return None

    def ResetAll(self):
        self.Orders = {}
        self.Name = ""

