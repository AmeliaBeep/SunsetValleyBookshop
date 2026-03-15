import csv
import os
import sys
import argparse
import django
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export order data with order items and books to CSV."
    )
    parser.add_argument(
        "--output",
        default=str(Path.home() / "Downloads" / "transformed_order_data.csv"),
        help="Output CSV path.",
    )
    return parser.parse_args()


def setup_django() -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()


def fetch_orders():
    from bookshop.models import Order

    return (
        Order.objects.filter(customer__status="ACTIVE")
        .select_related("customer")
        .prefetch_related("items__book")
        .order_by("pk")
    )


def write_csv(orders, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "order_id", "customer_id", "customer_name", "customer_email", "customer_status",
            "book_id", "book_title", "book_author", "quantity", "unit_price", "line_total", 
            "order_total",
        ])

        for order in orders:
            customer = order.customer
            customer_name = f"{customer.first_name} {customer.last_name}"
            items = list(order.items.all())
            order_total = sum(
                item.quantity * item.book.price for item in items)

            for item in items:
                writer.writerow([
                    order.pk,
                    customer.pk,
                    customer_name,
                    customer.email,
                    customer.status,
                    item.book.id,
                    item.book.title,
                    item.book.author,
                    item.quantity,
                    item.book.price,
                    item.quantity * item.book.price,
                    order_total,
                ])


def main() -> None:
    args = parse_args()
    output_file = Path(args.output)

    setup_django()
    orders = fetch_orders()
    write_csv(orders, output_file)
    print(f"CSV saved to {output_file}")


if __name__ == "__main__":
    main()
