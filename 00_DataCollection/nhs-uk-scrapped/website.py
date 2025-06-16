import requests
from lxml import html
import os
import re
import pandas as pd

# Sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip().replace(" ", "_")

# Main scraping function
def scrape_recipe(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    # Extract values
    title = tree.xpath('/html/body/main/section[1]/div/div/div/div[1]/div[1]/h1/text()')
    title = title[0].strip() if title else "Unknown_Recipe"

    description = tree.xpath('/html/body/main/section[1]/div/div/div/div[1]/div[1]/div[1]/p/text()')
    description = description[0].strip() if description else ""

    meta = tree.xpath('/html/body/main/section[1]/div/div/div/div[1]//p/text()')
    meta = [m.strip() for m in meta]

    # Ingredients
    ingredients = tree.xpath('/html/body/main/section[1]/div/div/div/div[2]/div/div/div[1]/ul//li/text()')
    ingredients_text = "\n- " + "\n- ".join(i.strip() for i in ingredients)

    # Instructions
    instructions = tree.xpath('/html/body/main/section[1]/div/div/div/div[2]/div/div/div[2]/ol/li')
    instruction_steps = []
    for idx, li in enumerate(instructions, 1):
        texts = li.xpath('.//text()')
        full_text = ' '.join(t.strip() for t in texts if t.strip())
        instruction_steps.append(f"{idx}. {full_text}")
    instruction_text = "\n".join(instruction_steps)

    # Download image
    image_url = tree.xpath('/html/body/main/section[1]/div/div/div/div[1]/div[2]/figure/img/@src')
    if image_url:
        img_data = requests.get(image_url[0]).content
        os.makedirs('scraping-code/images', exist_ok=True)
        filename = sanitize_filename(title) + '.jpg'
        img_path = os.path.join('nhs-uk-srapped/images', filename)
        with open(img_path, 'wb') as f:
            f.write(img_data)
    else:
        img_path = ""

    # Extract value after colon
    def get_meta_value(label):
        for m in meta:
            if label.lower() in m.lower() and ':' in m:
                return m.split(':', 1)[1].strip()
        return ""

    age_group = get_meta_value("Age")
    prep_time = get_meta_value("Prep")
    cook_time = get_meta_value("Cook")
    serving = get_meta_value("Portion") or get_meta_value("Serve")

    # Build row as a dict aligned with the custom column order
    row = {
        "Food Name": title,
        "Ingredients": ingredients_text,
        "Instructions": instruction_text,
        "Age Group": age_group,
        "Texture": "",
        "Prep Time": prep_time,
        "Cook Time": cook_time,
        "Serving": serving,
        "Origin": "",
        "Food_Category": "",
        "Difficulty": "",
        "Meal Type": "",
        "Description": description,
        "Flavor_type": "",
        "Dietary Tags": "",
        "choking_hazard": "",
        "tips": "",
        "allergen": "",
        "hypoallergenic": "",
        "Nutrion Value": "",
        "Credibility": "",
        "Link": url
    }

    return row

# ==== MAIN ====

# Custom columns as per your request
columns = [
    "Food Name", "Ingredients", "Instructions", "Age Group", "Texture", "Prep Time", "Cook Time",
    "Serving", "Origin", "Food_Category", "Difficulty", "Meal Type", "Description", "Flavor_type",
    "Dietary Tags", "choking_hazard", "tips", "allergen", "hypoallergenic", "Nutrion Value",
    "Credibility", "Link"
]

# # Ask user for input URLs
# urls_input = input("Enter comma-separated recipe URLs: ").strip()
# urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

# # Scrape all and collect into rows
# data_rows = []
# for url in urls:
#     print(f"Scraping: {url}")
#     try:
#         row = scrape_recipe(url)
#         data_rows.append(row)
#     except Exception as e:
#         print(f"⚠️ Failed to scrape {url}: {e}")

# # Save to Excel
# if data_rows:
#     # df = pd.DataFrame(data_rows, columns=columns)
#     # output_path = 'nhs-uk-scrapped/scrapped_second_Recipe.xlsx'
#     # df.to_excel(output_path, sheet_name='Recipe', index=False)
#     print(f"\n✅ Scraped data saved to: {output_path}")
# else:
#     print("❌ No valid data to save.")

# ...existing code...

# Ask user for input URLs
print("Enter recipe URLs (one per line). Press Enter twice when done:")
urls = []
while True:
    line = input().strip()
    if not line and not urls:  # If first input is empty, continue prompting
        continue
    if not line and urls:  # If empty line after entering at least one URL
        break
    if line:  # Add non-empty lines to the list
        urls.append(line)

# Scrape all and collect into rows
data_rows = []
for url in urls:
    print(f"Scraping: {url}")
    try:
        row = scrape_recipe(url)
        data_rows.append(row)
    except Exception as e:
        print(f"⚠️ Failed to scrape {url}: {e}")

# ...existing code...
