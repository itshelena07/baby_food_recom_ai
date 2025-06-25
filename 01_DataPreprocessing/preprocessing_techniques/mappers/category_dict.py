dietary_tags = {
    # 🥗 General Dietary Preferences
    "vegan": {
        "allowed_categories": ["plant_based"],
        "excluded_allergen_groups": ["milk", "egg", "fish", "shellfish"],
        "excluded_ingredients": [
            # Animal products
            "meat", "chicken", "beef", "pork", "lamb", "bacon", "gelatin",
            "eggs", "cheese", "butter", "yogurt", "whey", "casein", "lard", "milk", "honey"
        ],
        "notes": "No animal products. Safe only if choking hazard-free."
    },
    
    "vegetarian": {
        "allowed_categories": ["plant_based", "dairy", "egg"],
        "excluded_allergen_groups": ["fish", "shellfish"],
        "excluded_ingredients": [
            "meat", "chicken", "beef", "pork", "lamb", "gelatin", "pork", "bacon", "ham",
            "cod", "salmon", "tuna", "shellfish", "shrimp", "lobster", "crab", "prawn",	
        ],
        "notes": "May contain dairy or eggs, but no meat."
    },
    
    "pescetarian": {
        "allowed_categories": ["plant_based", "dairy", "egg", "seafood"],
        "excluded_allergen_groups": [],
        "excluded_ingredients": [
            "meat", "bacon", "gelatin", "pork", "lamb", "chicken", "beef"
        ],
        "notes": "Contains fish but no other meats."
    },

    # 🚫 Allergen-Friendly Tags
    "dairy_free": {
        "excluded_allergen_groups": ["milk"],
        "excluded_ingredients": [
            # Dairy-based foods
            "cheese", "butter", "yogurt", "milk", "whey", "casein", "cream", "ice cream"
        ]
    },
    
    "egg_free": {
        "excluded_allergen_groups": ["egg"],
        "excluded_ingredients": [
            # Egg-related items
            "eggs", "egg white", "egg yolk", "lecithin", "omelette"
        ]
    },
    
    "soy_free": {
        "excluded_allergen_groups": ["soy"],
        "excluded_ingredients": [
            # Soy-based items
            "soy", "tofu", "edamame", "soy sauce", "soy milk", "tempeh", "miso"
        ]
    },
    
    "nut_free": {
        "excluded_allergen_groups": ["nuts"],
        "excluded_ingredients": [
            # Nut-based items
            "almonds", "cashews", "walnuts", "peanuts", "hazelnuts", "pecans",
            "nut butter", "nut milk", "trail mix"
        ]
    },
    
    "gluten_free": {
        "excluded_allergen_groups": ["gluten"],
        "excluded_ingredients": [
            # Gluten-containing items
            "wheat", "barley", "rye", "bread", "pasta", "semolina", 
            "crackers", "cookies", "cereals", "panko", "flour (wheat)", "beer"
        ]
    },

    # 🍖 Halal / Non-Halal Classification
    "halal": {
        "excluded_allergen_groups": [],  # ✅ Remove pork from here
        "excluded_ingredients": [
            "pork", "bacon", "ham", "gelatin", "alcohol", "non_halal_meat"
        ],
        "notes": "Follows halal food laws — no pork, alcohol, or non-halal meat"
    },
}