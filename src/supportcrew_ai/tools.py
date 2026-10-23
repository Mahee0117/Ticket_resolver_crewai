
from crewai.tools import tool


# Mock customer database
CUSTOMERS = {
    "C101": {
        "name": "Arun",
        "email": "arun@example.com",
        "account_status": "Active"
    },
    "C102": {
        "name": "Priya",
        "email": "priya@example.com",
        "account_status": "Suspended"
    }
}


# Mock order database
ORDERS = {
    "ORD101": {
        "customer_id": "C101",
        "status": "Shipped",
        "expected_delivery": "2026-10-27"
    },
    "ORD102": {
        "customer_id": "C102",
        "status": "Processing",
        "expected_delivery": "2026-10-30"
    }
}


@tool("get_customer")
def get_customer(customer_id: str) -> dict:
    """Look up a customer by ID. Returns their name, email,
    and account status. Use when a ticket needs customer details.
    """

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "found": False,
            "message": f"No customer found with ID {customer_id}"
        }

    return {
        "found": True,
        "customer": customer
    }


@tool("get_order_status")
def get_order_status(order_id: str) -> dict:
    """Look up an order by order ID. Returns order status,
    associated customer ID, and expected delivery date.
    Use when a customer asks about an existing order.
    """

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "found": False,
            "message": f"No order found with ID {order_id}"
        }

    return {
        "found": True,
        "order_id": order_id,
        "order": order
    }
