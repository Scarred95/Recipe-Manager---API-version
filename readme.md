
# Recipe Manager API (Assignment 3)

Name: Auren Appelt
Course: 25-06-EON - Agile Softwareentwicklung

## Project Overview

This project implements a RESTful API using FastAPI to manage a cookbook and a pantry inventory. It allows users to manage recipes, check available ingredients, and "cook" meals by automatically deducting ingredients from the pantry.

The project follows a **Service Layer Architecture** to separate concerns:
-   `main_auren_appelt3.py`: The API endpoints (Controller).
-   `logic_auren_appelt3.py`: The business logic and validation.
-   `storage_auren_appelt3.py`: JSON file persistence.
-   `model_auren_appelt3.py`: Pydantic data models.
## ⚠️ IMPORTANT: Setup Instructions ⚠️ 

**Before starting the server, you must perform the following steps:**
1.  Create the Data Directory:
    Ensure a folder named **data** exists in the same directory as the python scripts. The application will look for Recipes.json and Pantry.json inside this folder.
    
    _If the folder does not exist, please create it manually to avoid storage errors._
    
2.  JSON File Placement:
    Place the provided Recipes.json and Pantry.json files inside the data/ folder.


**Your final folder structure should look like this:**

```
/auren_assignment3
│   ├── main_auren_appelt3.py    (The API endpoints)
│   ├── model_auren_appelt3.py   (The Data Classes)
│   ├── logic_auren_appelt3.py   (The business logic and validation)
│   ├── storage_auren_appelt3.py (JSON file persistence)
│   ├── README.md                (Instructions)
│   └── /data                    
│       ├── Recipes.json
│       └── Pantry.json

```

##  Usage Guidelines & Constraints
-   Case Sensitivity:
    The API is Case Sensitive. All ingredient names are expected to be in lowercase (e.g., "potato", not "Potato").
    -   Inputs: When adding ingredients via `PUT /pantry`, ensure names are lowercase. 
    -   Recipes: Ensure ingredient keys in recipes are lowercase to match the pantry.

## How to Start
1.  **Install Dependencies:**
    ```
    pip install "fastapi[standard]"
    
    ```

2.  **Run the Server:**
    ```
    fastapi dev main_auren_appelt3.py
    
    ```

3.  Open Swagger UI:
    Navigate to http://127.0.0.1:8000/docs to test the endpoints.

## Available Endpoints

### Recipes
-   `GET /recipes`: List all stored recipes.
-   `GET /recipes/{r_id}`: Get details of a specific recipe.
-   `GET /recipes/cookable`: **(Smart Feature)** Returns only recipes that you have enough ingredients to cook right now.
-   `POST /recipes`: Add a new recipe to the collection.
-   `POST /recipes/cook/{recipe_id}`: Cooks a meal. Validates ingredients and **removes** them from the pantry inventory.

### Pantry
-   `GET /pantry`: View current ingredient stock.
-   `PUT /pantry`: Add or Update an item.
    -   _Positive amount:_ Adds to stock.
    -   _Negative amount:_ Removes from stock.
    -   _Zero:_ No change.

## Code Structure & Module Explanation
This project is designed with modularity in mind, mimicking professional Cloud Engineering standards. Each file has a specific responsibility:

### `main_auren_appelt3.py` (Controller Layer)
This is the entry point of the application. It initializes the **FastAPI** instance and defines the HTTP routes.
-   **Responsibility:** Handling HTTP Requests and Responses.
-   **Key Functions:** It does not contain business logic. Instead, it routes requests (like `GET /recipes`) to the appropriate function in the `logic` module.
-   **Status Codes:** It ensures the API returns correct HTTP status codes (e.g., 200 OK, 201 Created).

### `logic_auren_appelt3.py` (Service Layer)
This file contains the "Brain" of the application. It bridges the gap between the API (Main) and the Database (Storage).

-   **Responsibility:** Data validation, algorithms, and business rules.
-   **Key Functions:**
    -   `find_cookable_recipes()`: Implements the algorithm to compare pantry stock vs. recipe requirements.
    -   `cook_recipe()`: Orchestrates the transaction of verifying ingredients and removing them from the pantry.
    -   `modify_pantry()`: Handles the logic for adding, updating, or removing items based on positive/negative input values.

### `storage_auren_appelt3.py` (Persistence Layer)
This module handles all low-level file Input/Output (I/O).

-   **Responsibility:** Reading from and writing to the JSON files in the `data/` directory.
-   **Key Functions:**
    -   `_load_json` / `_save_json`: Generic helpers that handle file opening, closing, and error catching (e.g., corrupted files).
    -   `get_recipes_data` / `set_pantry_data`: Specific wrappers to ensure type safety when accessing data.

### `model_auren_appelt3.py` (Data Layer)

This file defines the data structures using **Pydantic**.

-   **Responsibility:** Data validation and schema definition.
-   **Key Classes:**
    -   `Recipe`: Defines the structure of a recipe (ID, Name, Ingredients, Instructions). It enforces that IDs are positive integers.
    -   `PantryItem`: Defines the structure for inventory updates.
    -   `StorageError`: A custom Exception class for handling file I/O errors gracefully.