import json
import api as api_
import asyncio
import data as data_
from datetime import datetime, timedelta
from typing import Dict, Any

async def invoke(async_func, *args, **kwargs):
    res = await async_func(*args, **kwargs)
    return res

def to_datetime(input_str: str) -> datetime:
    try:
        dt = datetime.strptime(input_str, "%Y-%m-%d_%H:%M:%S")
        return dt
    except ValueError as err:
        raise ValueError(f"Invalid date/time format: {input_str}") from err

def print_unknown():
    print("Unknown/invalid command. Available commands:")
    print("product: create, get, get-all, update, delete, delete-all, generate")
    print("customer: create, get, get-all, update, delete, delete-all, generate")
    print("purchase: create, get, get-all, update, delete, delete-all, generate")
    print("query: 1 (products by manufacturer), 2 (customer purchases), 3 (update prices), 4 (sales by product)")

format_flag = True

method_dict = {
    "product": {
        "create": api_.create_product,
        "get": api_.get_product,
        "get-all": api_.get_all_products,
        "update": api_.update_product,
        "delete": api_.delete_product,
        "delete-all": api_.delete_all_products,
        "generate": api_.generate_products
    },
    "customer": {
        "create": api_.create_customer,
        "get": api_.get_customer,
        "get-all": api_.get_all_customers,
        "update": api_.update_customer,
        "delete": api_.delete_customer,
        "delete-all": api_.delete_all_customers,
        "generate": api_.generate_customers
    },
    "purchase": {
        "create": api_.create_purchase,
        "get": api_.get_purchase,
        "get-all": api_.get_all_purchases,
        "update": api_.update_purchase,
        "delete": api_.delete_purchase,
        "delete-all": api_.delete_all_purchases,
        "generate": api_.generate_purchases
    },
    "query": {
        "1": api_.get_products_by_manufacturer,
        "2": api_.get_customer_purchases,
        "3": api_.update_product_prices,
        "4": api_.get_sales_by_product
    }
}

def parse_command(command: str) -> Dict[str, Any]:
    try:
        args = command.split()
        if len(args) < 2:
            return {"valid": False}
            
        entity, action = args[0], args[1]
        if entity not in method_dict or action not in method_dict[entity]:
            return {"valid": False}
            
        return {
            "valid": True,
            "entity": entity,
            "action": action,
            "args": args[2:],
            "method": method_dict[entity][action]
        }
    except Exception:
        return {"valid": False}

while (command := input("Enter command: ")) != "exit":
    parsed = parse_command(command)
    
    if not parsed["valid"]:
        print_unknown()
        continue
        
    try:
        if parsed["action"] == "generate":
            if len(parsed["args"]) != 1:
                print("Generate command requires exactly one argument (number of items)")
                continue
            result = asyncio.run(invoke(parsed["method"], int(parsed["args"][0])))
            
        elif parsed["action"] in ["get", "delete"]:
            if len(parsed["args"]) != 1:
                print(f"{parsed['action']} command requires exactly one argument (ID)")
                continue
            result = asyncio.run(invoke(parsed["method"], int(parsed["args"][0])))
            
        elif parsed["action"] == "get-all":
            skip = int(parsed["args"][0]) if len(parsed["args"]) > 0 else 0
            limit = int(parsed["args"][1]) if len(parsed["args"]) > 1 else 100
            result = asyncio.run(invoke(parsed["method"], skip, limit))
            
        elif parsed["action"] == "create":
            if parsed["entity"] == "product":
                if len(parsed["args"]) != 3:
                    print("Product creation requires: name manufacturer unit")
                    continue
                result = asyncio.run(invoke(parsed["method"], *parsed["args"]))
                
            elif parsed["entity"] == "customer":
                if len(parsed["args"]) != 4:
                    print("Customer creation requires: name address phone contact_person")
                    continue
                result = asyncio.run(invoke(parsed["method"], *parsed["args"]))
                
            elif parsed["entity"] == "purchase":
                if len(parsed["args"]) != 5:
                    print("Purchase creation requires: product_id customer_id quantity delivery_date price_per_unit")
                    continue
                args = list(parsed["args"])
                args[2] = float(args[2])  # quantity
                args[3] = to_datetime(args[3])  # delivery_date
                args[4] = float(args[4])  # price_per_unit
                result = asyncio.run(invoke(parsed["method"], *args))
                
        elif parsed["action"].startswith("query"):
            result = asyncio.run(invoke(parsed["method"], *parsed["args"]))
            
        else:
            print_unknown()
            continue
            
        if format_flag and result:
            if isinstance(result, (list, dict)):
                print(json.dumps(result, indent=4, default=str))
            else:
                print(result)
        else:
            print(result)
            
    except Exception as e:
        print(f"Error executing command: {str(e)}")