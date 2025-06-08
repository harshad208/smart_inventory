# scripts/seed.py

import argparse
import logging
import random

from faker import Faker
from faker_commerce import Provider as CommerceProvider
from sqlalchemy.orm import Session
from tqdm import tqdm

from app.db.session import SessionLocal
from app.models import InventoryMovement, Order, OrderItem, Product, Supplier
from app.models.inventory_movement import MovementType

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker for generating mock data
fake = Faker()

fake.add_provider(CommerceProvider)


def seed_data(db: Session, num_suppliers: int, num_products: int, num_orders: int):
    """
    Populates the database with a large set of realistic test data.
    """

    # --- 1. SEED SUPPLIERS ---
    logger.info("Seeding suppliers...")
    suppliers = []
    for _ in tqdm(range(num_suppliers), desc="Creating Suppliers"):
        supplier = Supplier(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
        )
        suppliers.append(supplier)
    db.add_all(suppliers)
    db.commit()
    logger.info(f"Successfully created {len(suppliers)} suppliers.")

    # --- 2. SEED PRODUCTS (with initial inventory) ---
    logger.info("Seeding products and initial inventory...")
    products = []
    inventory_movements = []
    # Ensure we have suppliers to link to
    supplier_ids = [s.id for s in db.query(Supplier).all()]
    if not supplier_ids:
        logger.error("No suppliers found. Please seed suppliers first.")
        return

    for _ in tqdm(range(num_products), desc="Creating Products"):
        initial_stock = random.randint(50, 500)
        product = Product(
            sku=fake.unique.ean(length=13),
            name=fake.ecommerce_name(),
            description=fake.sentence(),
            price=round(random.uniform(10.99, 999.99), 2),
            quantity_in_stock=initial_stock,
            supplier_id=random.choice(supplier_ids),
        )
        products.append(product)

        # We need to commit the product to get its ID for the inventory movement
        db.add(product)
        db.commit()

        # Create the initial "restock" inventory movement record
        movement = InventoryMovement(
            product_id=product.id,
            quantity_changed=initial_stock,
            movement_type=MovementType.RESTOCK,
            # Generate a realistic timestamp for partitioning tests
            timestamp=fake.date_time_between(start_date="-2y", end_date="-1y"),
        )
        inventory_movements.append(movement)

    db.add_all(inventory_movements)
    db.commit()
    logger.info(
        f"Successfully created {len(products)} products and their initial inventory movements."
    )

    # --- 3. SEED ORDERS AND SALES INVENTORY ---
    logger.info("Seeding orders and sales inventory movements...")
    # Ensure we have products to link to
    all_products = db.query(Product).all()
    if not all_products:
        logger.error("No products found. Please seed products first.")
        return

    for _ in tqdm(range(num_orders), desc="Creating Orders"):
        order = Order(
            customer_name=fake.name(),
            status=random.choice(["pending", "completed", "cancelled"]),
        )
        db.add(order)
        db.commit()  # Commit to get order.id

        # Each order will have 1 to 5 items
        num_items_in_order = random.randint(1, 5)
        for _ in range(num_items_in_order):
            product_to_order = random.choice(all_products)
            quantity_ordered = random.randint(1, 5)

            # Only create the order item if there is enough stock
            if product_to_order.quantity_in_stock >= quantity_ordered:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product_to_order.id,
                    quantity=quantity_ordered,
                )
                db.add(order_item)

                # Update product stock
                product_to_order.quantity_in_stock -= quantity_ordered

                # Create the "sale" inventory movement
                sale_movement = InventoryMovement(
                    product_id=product_to_order.id,
                    quantity_changed=-quantity_ordered,
                    movement_type=MovementType.SALE,
                    timestamp=fake.date_time_this_year(),
                )
                db.add(sale_movement)

    db.commit()
    logger.info(f"Successfully created {num_orders} orders and updated inventory.")


def clean_data(db: Session):
    """
    Deletes all data from the tables in the correct order to respect foreign keys.
    """
    logger.warning("Cleaning all data from the database...")
    # The order of deletion is critical to avoid foreign key constraint errors
    db.query(InventoryMovement).delete()
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(Product).delete()
    db.query(Supplier).delete()
    db.commit()
    logger.info("All data has been deleted.")


def main():
    parser = argparse.ArgumentParser(description="Seed the database with test data.")
    parser.add_argument(
        "--clean", action="store_true", help="Delete all existing data before seeding."
    )
    parser.add_argument(
        "--suppliers", type=int, default=50, help="Number of suppliers to create."
    )
    parser.add_argument(
        "--products", type=int, default=500, help="Number of products to create."
    )
    parser.add_argument(
        "--orders", type=int, default=2000, help="Number of orders to create."
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.clean:
            clean_data(db)

        seed_data(
            db=db,
            num_suppliers=args.suppliers,
            num_products=args.products,
            num_orders=args.orders,
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
