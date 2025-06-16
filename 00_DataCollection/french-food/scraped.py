from urllib.parse import urljoin
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
    title = tree.xpath('/html/body/div[1]/div[4]/div[1]/div/article/div[1]/h1/text()')
    title = title[0].strip() if title else "Unknown_Recipe"
    # Remove any text in parentheses (including the parentheses)
    title = re.sub(r'\s*\(.*?\)', '', title).strip()
    # breakpoint()

    # description = tree.xpath('/html/body/main/section[1]/div/div/div/div[1]/div[1]/div[1]/p/text()')
    # description = description[0].strip() if description else ""

    # Ingredients
    ul_elements = tree.xpath('/html/body/div[1]/div[4]/div[1]/div/article/div[4]/div/ul')

    # 4. Prepare list-style output
    if ul_elements:
        ingredient_step = []
        counter = 1
        for ul in ul_elements:
            list_items = ul.xpath('./li')
            for li in list_items:
                text = li.text_content().strip()
                ingredient_step.append(f"- {text}")

        # 5. Join into a single string if needed
        ingredient_text = "\n".join(ingredient_step)
        print(ingredient_text)
    else:
        print("No <ul> found at the specified XPath.")  

    # breakpoint()  
    # Instructions
    target = tree.xpath('/html/body/div[1]/div[4]/div[1]/div/article/div[4]/div')

    # 4. If the target element is found
    if target:
        ol_elements = target[0].xpath('.//ol')
        
        # 5. Initialize storage for instructions
        instruction_steps = []
        counter = 1

        # 6. Loop through all <ol> and <li> items
        for ol in ol_elements:
            list_items = ol.xpath('./li')
            for li in list_items:
                text = li.text_content().strip()
                instruction_steps.append(f"{counter}. {text}")
                counter += 1

        # 7. Join the steps into a final instruction string
        instruction_text = "\n".join(instruction_steps)
        print(instruction_text)

    else:
        print("Target element not found.")

    # breakpoint()
    # Download image

    # Assuming title and url are defined

    print("\n")
        # Step 1: Try to get src or data-src
    # Try getting the actual image from the <a href="...">
    image_url = tree.xpath('/html/body/div[1]/div[4]/div[1]/div/article/div[2]/a/@href')

    if image_url:
        full_img_url = urljoin(url, image_url[0])
        if full_img_url.startswith("data:"):
            print(f"Skipping invalid image for {title} (inline data URI)")
            img_path = ""
        else:
            headers = {'User-Agent': 'Mozilla/5.0'}
            try:
                img_data = requests.get(full_img_url, headers=headers).content
                filename = (title) + '.jpg'
                os.makedirs('french-food/images', exist_ok=True)
                img_path = os.path.join('french-food/images', filename)
                with open(img_path, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Failed to save image for {title}: {e}")
                img_path = ""
    else:
        print(f"No image link found for: {title}")
        img_path = ""

    # Build row as a dict aligned with the custom column order
    row = {
        "Food Name": title,
        "Ingredients": ingredient_text,
        "Instructions": instruction_text,
        "Age Group": "7",
        "Texture": "",
        "Prep Time": "prep_time",
        "Cook Time": "cook_time",
        "Serving": "serving",
        "Origin": "",
        "Food_Category": "",
        "Difficulty": "",
        "Meal Type": "",
        "Description": "",
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
# Scrape all and collect into rows
data_rows = []
failed_urls = []  # List to track failed URLs

for url in urls:
    print(f"Scraping: {url}")
    try:
        row = scrape_recipe(url)
        data_rows.append(row)
    except Exception as e:
        error_message = str(e)
        print(f"⚠️ Failed to scrape {url}: {error_message}")
        failed_urls.append({"url": url})

if data_rows:
    df = pd.DataFrame(data_rows, columns=columns)
    output_path = 'french-food/scrape_pdf.xlsx'
    df.to_excel(output_path, sheet_name='Recipe', index=False)
    print(f"\n✅ Scraped data saved to: {output_path}")
else:
    print("❌ No valid data to save.")

# Display summary of failed URLs
if failed_urls:
    print("\n===== FAILED SCRAPING ATTEMPTS =====")
    for i, failed in enumerate(failed_urls, 1):
        print(f"{i}. {failed['url']}")
    
    # Optionally save failed URLs to a file
    with open('french-food/failed_urls.txt', 'w') as f:
        for failed in failed_urls:
            f.write(f"{failed['url']}\n")
    
    print(f"\nList of failed URLs saved to: french-food/failed_urls.txt")
    print(f"Total: {len(failed_urls)} failed, {len(data_rows)} successful")