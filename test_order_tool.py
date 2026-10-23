
from supportcrew_ai.tools import get_order_status

print("Existing order:")
print(get_order_status.run(order_id="ORD101"))

print("\nMissing order:")
print(get_order_status.run(order_id="ORD999"))
