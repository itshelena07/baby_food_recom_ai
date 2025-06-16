from urllib.parse import urljoin
import requests
from lxml import html
import os
import re
import pandas as pd

# Sanitize filenames
# Modified sanitize_filename function to preserve spaces
def sanitize_filename(name):
    # Remove illegal characters but keep spaces
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()
# Main scraping function
def scrape_recipe(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    # Extract values
    title = tree.xpath('/html/body/main/article/header/div/div/div/h1/text()')
    title = title[0].strip() if title else "Unknown_Recipe"
    # Remove any text in parentheses (including the parentheses)
    title = re.sub(r'\s*\(.*?\)', '', title).strip()
    # breakpoint()
        # Initialize variables
    prep_time = None
    cook_time = None
    portion = None

    # Step 1: Check if ul[2] exists
    ul2 = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]')
    if ul2:
        # Step 2: Check first li and div/div[1] text
        item1_text = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]/li[1]/div/div[1]/text()')
        item1_text = item1_text[0].strip().lower() if item1_text else ""
        print(item1_text)
        item2_text = tree.xpath ('/html/body/main/article/header/div/div/div/ul[2]/li[1]/div/div[2]/text()')
        item2_text = item2_text[0].strip().lower() if item2_text else ""
        # /html/body/main/article/header/div/div/div/ul[2]/li[1]/div/div[2]
        print(item2_text)
        if "preparation" in item1_text:
            prep_time_element = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]/li[1]/div/div[1]/strong')
            if prep_time_element:
                prep_time = prep_time_element[0].text.strip()

        if "baking" in item2_text:
            cook_time_element = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]/li[1]/div/div[2]/strong')
            if cook_time_element:
                cook_time = cook_time_element[0].text.strip()

        # Step 3: Check li[2]/div for "portion"
        li2_div_text = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]/li[2]/div/text()')
        li2_div_text = li2_div_text[0].strip().lower() if li2_div_text else ""

        if "portion" in li2_div_text:
            portion_element = tree.xpath('/html/body/main/article/header/div/div/div/ul[2]/li[2]/div/strong')
            if portion_element:
                portion = portion_element[0].text.strip()
    
    
    age_group = tree.xpath('/html/body/main/article/header/div/div/div/ul/li[1]/text()')
    age_group = age_group[0].strip() if age_group else ""
    type = tree.xpath('/html/body/main/article/header/div/div/div/ul/li[2]/text()')
    type = type[0].strip() if type else ""
    print(age_group)
    print(type)

    # Ingredients
    ul_elements = tree.xpath('/html/body/main/article/div/div/div[1]/div[2]/ul')

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
    # Get the specific <p> element
    paragraph = tree.xpath('/html/body/main/article/div/div/div[2]/div[2]/p')[0]

    # Convert the <p> HTML to string (preserving <br> tags)
    raw_html = html.tostring(paragraph, encoding='unicode', method='html')

    # Replace <br> and <br/> with \n for line breaks
    text_with_breaks = raw_html.replace('<br>', '\n').replace('<br/>', '\n')

    # Strip remaining HTML but preserve line breaks
    clean_text = html.fromstring(text_with_breaks).text_content()

    # Split by lines and format with numbers
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    numbered_lines = [f"{i + 1}. {line}" for i, line in enumerate(lines)]
    for line in numbered_lines:
        print(line)
    # breakpoint()
    # Print the result
    instruction_text = "\n".join(numbered_lines)
    instruction_text = instruction_text.replace('\n', '\r\n')

    # print(formatted_output

    # breakpoint()
    # Download image

    # Assuming title and url are defined

    print("\n")
        # Step 1: Try to get src or data-src
        # Try getting the actual image from the <a href="...">
    image_src = tree.xpath('/html/body/main/article/header/div/div/figure/picture/source/@srcset')
    if not image_src:
        image_src = tree.xpath('/html/body/main/article/header/div/div/figure/picture/img/@src')
    if image_src:
    # Convert to full URL
        full_img_url = urljoin(url, image_src[0])

        if full_img_url.startswith("data:"):
            print(f"Skipping invalid image for {title} (inline data URI)")
            img_path = ""
        else:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_data = requests.get(full_img_url, headers=headers).content

                # Create directory and save
                os.makedirs('french-2nd/images', exist_ok=True)
                
                # Use sanitize_filename but preserve spaces
                cleaned_title = sanitize_filename(title)
                filename = cleaned_title + '.jpg'  # This will now have spaces
                img_path = os.path.join('french-2nd/images', filename)

                with open(img_path, 'wb') as f:
                    f.write(img_data)

                print(f"Image saved to: {img_path}")
            except Exception as e:
                print(f"Failed to download image for {title}: {e}")
                img_path = ""

    # Build row as a dict aligned with the custom column order
    row = {
        "Food Name": title,
        "Ingredients": ingredient_text,
        "Instructions": instruction_text,
        "Age Group": age_group,
        "Texture": "",
        "Prep Time": prep_time,
        "Cook Time": cook_time,
        "Serving": portion,
        "Origin": "french",
        "Food_Category": "",
        "Difficulty": "",
        "Meal Type": type,
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

output_path = 'french-2nd/scrape_pdf.xlsx'
sheet_name = 'full_recipe'

if data_rows:
    df_new = pd.DataFrame(data_rows, columns=columns)

    if os.path.exists(output_path):
        # Load existing data
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Read the existing sheet (if it exists)
            try:
                df_existing = pd.read_excel(output_path, sheet_name=sheet_name)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            except ValueError:
                # Sheet doesn't exist yet
                df_combined = df_new

            # Write the combined DataFrame
            df_combined.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        # File doesn't exist yet
        df_new.to_excel(output_path, sheet_name=sheet_name, index=False)

    print(f"\n✅ Scraped data appended to: {output_path}")
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