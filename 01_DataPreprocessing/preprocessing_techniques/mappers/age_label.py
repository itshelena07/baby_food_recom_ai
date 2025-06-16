age_rules = {
    # --------------------------------------------
    # 1. Recipe Name Keywords → Suggested Age/Texture
    # --------------------------------------------
    "age_keywords": {
        "puree": {"min_age": 4, "max_age": 8, "reason": "Smooth texture for early weaning"},
        "mash": {"min_age": 6, "max_age": 10, "reason": "Lumpy texture for advancing skills"},
        "finger food": {"min_age": 8, "max_age": 36, "reason": "Self-feeding for older babies"},
        "chopped": {"min_age": 10, "max_age": 36, "reason": "Small soft pieces for chewing practice"},
        "stew": {"min_age": 6, "max_age": 36, "reason": "Soft, mixed textures"},
        "porridge": {"min_age": 4, "max_age": 12, "reason": "Easy-to-swallow grains"},
        # ... add more keywords
    },

    # --------------------------------------------
    # 2. Ingredient-Based Rules (Safety & Allergens)
    # --------------------------------------------
    "ingredient_rules": {
        "honey": {"min_age": 12, "reason": "Risk of infant botulism"},
        "cow milk (as drink)": {"min_age": 12, "reason": "Not recommended as main drink under 12 months"},
        "salt": {"min_age": 12, "reason": "Avoid added salt for babies"},
        "sugar": {"min_age": 12, "reason": "Avoid added sugars for babies"},
        "whole nuts": {"min_age": 36, "reason": "Choking hazard"},
        "peanut butter": {"min_age": 6, "reason": "Introduce as smooth paste (allergy guidelines)"},
        "shellfish": {"min_age": 12, "reason": "High allergen risk"},
        "grapes (whole)": {"min_age": 24, "reason": "Choking risk; always quarter"},
        # ... add more ingredients
    },

    # --------------------------------------------
    # 3. Instruction-Based Texture Analysis
    # --------------------------------------------
    "instruction_keywords": {
        "blend until smooth": {"min_age": 4, "max_age": 6, "reason": "Stage 1 puree"},
        "mash with a fork": {"min_age": 6, "max_age": 8, "reason": "Lumpy texture"},
        "chop into small pieces": {"min_age": 8, "reason": "Finger food for self-feeding"},
        "grate": {"min_age": 8, "reason": "Soft grated textures"},
        "steam until soft": {"min_age": 6, "reason": "Soft, dissolvable texture"},
        # ... add more cooking methods
    },

    # --------------------------------------------
    # 4. Texture → Age Mapping (Fallback)
    # --------------------------------------------
    "texture_to_age": {
        "smooth": {"min_age": 4, "max_age": 6},
        "lumpy": {"min_age": 6, "max_age": 8},
        "finger_food": {"min_age": 8, "max_age": 36},
        "family_food": {"min_age": 12, "max_age": 36},
    }
}