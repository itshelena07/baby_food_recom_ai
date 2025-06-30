import pandas as pd
from collections import Counter

# Extract all ingredients from the ner_ingredient_string column
all_ingredients = []

for ingredient_string in df_ingredients['ner_ingredient_string']:
    if isinstance(ingredient_string, str) and ingredient_string.strip():
        # Split by comma and clean each ingredient
        ingredients = [ing.strip().lower() for ing in ingredient_string.split(',') if ing.strip()]
        all_ingredients.extend(ingredients)

# Get unique ingredients and create DataFrame
unique_ingredients_list = sorted(list(set(all_ingredients)))

# Create DataFrame with ingredient IDs
unique_ingredients_df = pd.DataFrame({
    'ingredient_id': range(1, len(unique_ingredients_list) + 1),
    'ingredient_name': unique_ingredients_list
})

# Count ingredient frequencies for additional analysis
ingredient_counter = Counter(all_ingredients)

# Create frequency DataFrame
ingredient_frequency_df = pd.DataFrame([
    {'ingredient_id': idx + 1, 'ingredient_name': ingredient, 'frequency': ingredient_counter[ingredient]}
    for idx, ingredient in enumerate(unique_ingredients_list)
])

# Save to Excel
unique_ingredients_df.to_excel("unique_ingredients.xlsx", index=False)
ingredient_frequency_df.to_excel("ingredient_frequency_analysis.xlsx", index=False)

print(f"✅ Successfully saved {len(unique_ingredients_df)} unique ingredients to Excel files")
print(f"Total unique ingredients: {len(unique_ingredients_list)}")
print(f"Total ingredient instances: {len(all_ingredients)}")

# Display sample
print("\nFirst 10 unique ingredients:")
print(unique_ingredients_df.head(10))