from fastapi import FastAPI, HTTPException, status
import logic_auren_appelt3
from model_auren_appelt3 import Recipe, PantryItem

app = FastAPI()

# --- Endpoints ---

@app.get("/recipes", response_model=list[Recipe], status_code=status.HTTP_200_OK)
def get_recipes():
    """Returns a list of all recipes stored in the Database
    """
    return logic_auren_appelt3.get_recipes()

@app.get("/recipes/cookable", response_model=list[Recipe], status_code=status.HTTP_200_OK)
def get_cookable():
    """Returns a list of all COOKABLE recipes stored in the Database
    """
    return logic_auren_appelt3.find_cookable_recipes()

@app.get("/recipes/{r_id}", response_model=Recipe, status_code=status.HTTP_200_OK)
def get_single_recipe(r_id: int):
    """
    Finds a specific recipe by ID.
    """
    all_recipes = logic_auren_appelt3.get_recipes()
    
    for r in all_recipes:
        if r.recipe_id == r_id:
            return r
    # if loop fnishes without finding any
    raise HTTPException(status_code=404, detail="Recipe not found")

@app.post("/recipes", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def post_recipe(new_recipe: Recipe):
    """
    Adds a new recipe to the collection.
    Validates that the ID is unique.
    """
    return logic_auren_appelt3.add_new_recipe(new_recipe)

@app.put("/recipes/cook/{recipe_id}", status_code=status.HTTP_201_CREATED)
def post_cook(recipe_id: int):
    """
    Cooks a recipe, removing ingredients from the pantry.
    """
    # Logic handles all the validation (404 Not Found, 400 Missing Ingredients)
    dish_name = logic_auren_appelt3.cook_recipe(recipe_id)
    return {"message": f"Successfully cooked {dish_name.name}. Ingredients removed from Pantry."}


@app.get("/pantry", response_model=list[PantryItem], status_code=status.HTTP_200_OK)
def get_Pantry():
    """Returns a list of all Pantry Items
    """
    return logic_auren_appelt3.get_pantry()

@app.put("/pantry", status_code=status.HTTP_200_OK)
def update_pantry_item(item: PantryItem):
    """
    Updates (or adds) an item to the pantry.
    """
    updated_pantry = logic_auren_appelt3.modify_pantry(item)
    old = updated_pantry[0]
    new = updated_pantry[1]
    if item.name in old.keys() and item.name in new.keys():
        return {
            "message": f"Updated {item.name}.",
            "old_stock": old[item.name],
            "new_stock": new[item.name]
        }
    elif item.name in old.keys() and not item.name in new.keys():
        return {
            "message": f"Updated {item.name}. It is no longer in the Pantry."
        }
    elif item.name not in old.keys() and item.name in new.keys():
        return {
            "message": f"Updated {item.name}. It has been added to the Pantry",
            "new_stock": new[item.name]
        }