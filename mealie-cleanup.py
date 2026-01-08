#!/usr/bin/env python3
"""
Mealie v3.9.2 - CLEAN FOODS + ALWAYS Check Recipes
ENGLISH OUTPUT - No foods check required
"""

import requests, time

MEALIE_URL = "http://yourmealieinstance/api"
TOKEN = "Bearer yourmealieapitoken"
headers = {"Authorization": TOKEN}
DELAY = 0.05

print("🧹 FOODS CLEANUP + RECIPE CHECK (ALWAYS)")

# 1️⃣ NUKE FOODS (anche se 0)
food_deleted = 0
endpoints = ["/organizers/foods", "/foods"]

for endpoint in endpoints:
    print(f"\n🔍 Foods: {endpoint}")
    resp = requests.get(f"{MEALIE_URL}{endpoint}?perPage=-1", headers=headers)
    
    if resp.status_code == 200:
        foods = resp.json().get("items", [])
        print(f"📦 {len(foods)} foods found")
        
        for food in foods:
            del_resp = requests.delete(f"{MEALIE_URL}{endpoint}/{food['id']}", headers=headers)
            if del_resp.status_code in [200, 204, 404]:
                food_deleted += 1
            time.sleep(DELAY)
        
        print(f"✅ Deleted {food_deleted} from {endpoint}")
        break
    else:
        print(f"⏭️  Skip {endpoint}")

print(f"\n🎉 TOTAL FOODS DELETED: {food_deleted}")

# 2️⃣ SEMPRE CHECK RECIPES (indipendente da foods)
print("\n🔍 ALWAYS checking recipes...")
resp = requests.get(f"{MEALIE_URL}/recipes?perPage=-1", headers=headers)
if resp.status_code == 200:
    recipes = resp.json().get("items", [])
    print(f"📖 Found {len(recipes)} recipes")
    
    if recipes:
        print("❓ Delete ALL recipes? (y/N): ", end="")
        choice = input().lower().strip()
        if choice in ['y', 'yes', 's', 'si']:
            print("🗑️  Mass deleting recipes...")
            recipe_deleted = 0
            for recipe in recipes:
                del_resp = requests.delete(f"{MEALIE_URL}/recipes/{recipe['id']}", headers=headers)
                if del_resp.status_code in [200, 204]:
                    recipe_deleted += 1
                time.sleep(DELAY)
            print(f"✅ {recipe_deleted} recipes deleted")
        else:
            print("👌 Recipes preserved")
    else:
        print("✅ No recipes found")
else:
    print(f"❌ Recipe check failed: {resp.status_code}")

print("\n🎉 CLEANUP FINISHED!")
