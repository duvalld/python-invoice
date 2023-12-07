import sqlite3

class DatabaseManager:
    """ A class for managing SQLITE database operations """
    def __init__(self):
        self._database_name = "sm_department_store_db.db"

    def open_db(self):
        """Open a connection to the database."""
        self._conn = sqlite3.connect(self._database_name)
        self._cursor = self._conn.cursor()

    def close_db(self):
        """Close the database connection."""
        self._cursor.close()
        self._conn.close()

    def create_table(self, query):
        """Create a table in the database."""
        self.open_db()
        self._cursor.execute(query)
        self._conn.commit()
        self.close_db()

    def insert_record(self, query, col_values, table):
        """Insert a record into the specified table."""
        self.open_db()
        self._cursor.execute(query, col_values)
        self._conn.commit()
        print(f"{table} successfuly added!")

    def entry_checker(self, table, column, id):
        """
        Check if an entry with the given ID exists in the specified table.

        Returns:
            bool: True if the entry exists, False otherwise.
        """
        query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {
            column} = ? LIMIT 1)"
        try:
            self.open_db()
            self._cursor.execute(query, (id))
            result = self._cursor.fetchone()[0]
            return bool(result)
        except sqlite3.Error as e:
            print(f"Error checking entry: {e}")
            return False
        finally:
            self.close_db()
            
db_manager = DatabaseManager()
sales_rep_table_query = """
    CREATE TABLE IF NOT EXISTS sales_representatives(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
    )
"""
customers_table_query = """
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
    )
"""
vendors_table_query = """
    CREATE TABLE IF NOT EXISTS vendors(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
    )
"""
products_table_query = """
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY
        ,name TEXT NOT NULL
        ,vendor_id INTEGER NOT NULL
    )
"""
invoice_table_query = """
    CREATE TABLE IF NOT EXISTS invoice(
        id INTEGER PRIMARY KEY
        ,sales_rep_id TEXT NOT NULL
        ,customer_id INTEGER NOT NULL
    )
"""
invoice_item_table_query = """
    CREATE TABLE IF NOT EXISTS invoice_items(
        id INTEGER PRIMARY KEY
        ,invoice_id TEXT NOT NULL
        ,product_id INTEGER NOT NULL
    )
"""
db_manager.create_table(sales_rep_table_query)
db_manager.create_table(customers_table_query)
db_manager.create_table(vendors_table_query)
db_manager.create_table(products_table_query)
db_manager.create_table(invoice_table_query)
db_manager.create_table(invoice_item_table_query)

def show_sales_rep():
    db_manager.open_db()
    sql_query = """
        SELECT
            id
            ,name
        FROM sales_representatives
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Sales Representative':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_sales_rep) = row
        print(f"{row_id:>4} | {row_sales_rep:<20}")
    db_manager.close_db()
    
def show_customers():
    db_manager.open_db()
    sql_query = """
        SELECT
            id
            ,name
        FROM customers
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Customer':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_customer) = row
        print(f"{row_id:>4} | {row_customer:<20}")
    db_manager.close_db()

def show_vendors():
    db_manager.open_db()
    sql_query = """
        SELECT
            id
            ,name
        FROM vendors
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Vendor':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_vendor) = row
        print(f"{row_id:>4} | {row_vendor:<20}")
    db_manager.close_db()

def show_products():
    db_manager.open_db()
    sql_query = """
        SELECT
            products.id
            ,products.name
            ,vendors.name
        FROM products
        LEFT JOIN vendors ON products.vendor_id = vendors.id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Product':<20} | {'Vendor':<20}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_product, row_vendor) = row
        print(f"{row_id:>4} | {row_product:<20} | {row_vendor:<20}")
    db_manager.close_db()

def show_invoice():
    db_manager.open_db()
    sql_query = """
        SELECT
            i.id
            ,sr.name
            ,c.name
            ,(SELECT GROUP_CONCAT(p.name || '') FROM invoice_items as ii LEFT JOIN products as p WHERE ii.invoice_id = i.id)
        FROM invoice as i
        LEFT JOIN sales_representatives as sr ON sr.id = i.sales_rep_id
        LEFT JOIN customers as c ON c.id = i.customer_id
    """
    db_manager._cursor.execute(sql_query)
    rows = db_manager._cursor.fetchall()
    row_headers = f"{'ID':>4} | {'Sales Rep':<20} | {'Customer':<20} | {'Items':<40}"
    print(row_headers)
    print(len(row_headers) * "-")
    for row in rows:
        (row_id, row_sr, row_cust, row_inv_items) = row
        print(f"{row_id:>4} | {row_sr:<20} | {row_cust:<20} | {row_inv_items:<40}")
    db_manager.close_db()

program_running = True
while program_running:
    main_menu_input = int(input("Enter 1: Sales Representative, 2: Customers, 3: Vendors, 4: Products, 5:Invoice : "))
    if main_menu_input == 1:
        print("Sale Representative")
        sales_rep_input = int(input("Enter 1: View, 2: Add New : "))
        if sales_rep_input == 1:
            show_sales_rep()
        elif sales_rep_input == 2:
            try:
                sale_rep_name_input = input("Sales Rep Name: ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO sales_representatives (name) VALUES (?)", (sale_rep_name_input,), "Sales Representative")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 2:
        print("Customers")
        sales_rep_input = int(input("Enter 1: View, 2: Add New : "))
        if sales_rep_input == 1:
            show_customers()
        elif sales_rep_input == 2:
            try:
                customer_input = input("Customer: ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO customers (name) VALUES (?)", (customer_input,), "Customer")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 3:
        print("Vendors")
        sales_rep_input = int(input("Enter 1: View, 2: Add New : "))
        if sales_rep_input == 1:
            show_vendors()
        elif sales_rep_input == 2:
            try:
                vendor_input = input("Vendor: ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO vendors (name) VALUES (?)", (vendor_input,), "Vendor")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 4:
        print("Products")
        sales_rep_input = int(input("Enter 1: View, 2: Add New : "))
        if sales_rep_input == 1:
            show_products()
        elif sales_rep_input == 2:
            try:
                product_input = input("Product: ")
                show_vendors()
                vendor_input = input("Vendor (ID): ")
                db_manager.open_db()
                db_manager.insert_record("INSERT INTO products (name, vendor_id) VALUES (?, ?)", (product_input, vendor_input), "Product")
                db_manager.close_db()
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 5:
        print("Invoice")
        sales_rep_input = int(input("Enter 1: View, 2: Add New : "))
        if sales_rep_input == 1:
            show_invoice()
        elif sales_rep_input == 2:
            try:
                show_sales_rep()
                product_input = input("Sales Rep (ID): ")
                show_customers()
                vendor_input = input("Customer (ID): ")
                db_manager.open_db()
                db_manager._cursor.execute("INSERT INTO invoice (sales_rep_id, customer_id) VALUES (?, ?)", (product_input, vendor_input))
                last_row_id = db_manager._cursor.lastrowid
                db_manager._conn.commit()
                db_manager.close_db()
                
                add_invoice_items_loop = True
                while add_invoice_items_loop:
                    show_products()
                    product_id = input("Product (ID):")
                    db_manager.open_db()
                    db_manager._cursor.execute("INSERT INTO invoice_items (invoice_id, product_id) VALUES (?, ?)", (last_row_id, product_id))
                    db_manager._conn.commit()
                    db_manager.close_db()
                    confirm_adding = input("Add Another Item to invoice: (Y/N)")
                    if confirm_adding in ["y", "Y"]:
                        add_invoice_items_loop = True
                    elif confirm_adding in ["n", "N"]:
                        add_invoice_items_loop = False
            except sqlite3.Error as e:
                print(f"Error: {e}")
    elif main_menu_input == 6:
        program_running = False
    else:
        program_running = False
