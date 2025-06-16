## Data Collection for Baby Food / Weaning Recipe Dataset

### Overview

This repository documents the data collection process for compiling a comprehensive dataset of baby food and weaning recipes from various regions around the world. The aim is to provide a diverse and culturally representative dataset suitable for research and analysis in nutrition science, early childhood development, and food innovation.

### Methodology

#### Source Identification

The researcher conducted extensive online searches to gather recipes from various formats and platforms, including:

* **Books** (digital or scanned): Referenced for traditional and evidence-based recipes.
* **Academic and Popular Articles:** Utilized for insights into nutritional value and regional practices.
* **Websites:** Scraped to extract structured recipe content with metadata (e.g., ingredients, steps, nutrition).
* **Image-Based Content:** Where recipe data appeared in image formats (e.g., scanned book pages, infographics), AI tools such as GPT were used to transcribe and extract the information accurately.

> *Note: Only data obtained via web scraping will be stored as raw individual files in the repository. Other sources (e.g., book scans, AI-extracted images) will be consolidated and made available only in the final dataset.*

#### Data Collection Techniques

* **Manual Review and Curation:** Recipes were verified and categorized based on origin and content.
* **Web Scraping:** Automated scripts were developed and used to extract data from publicly accessible websites.
* **AI-assisted Extraction:** External support (e.g., GPT models) was used to interpret and convert image-based text into structured data.

All collected data has been documented with source attribution for transparency and potential reproducibility.

### Sample Source Table

Below is a sample of some of the sources used, categorized by country of origin:

| Country        | Sample Sources                                                       |
| -------------- | -------------------------------------------------------------------- |
| Indonesia      | [Link 1](https://example.com/id1), [Link 2](https://example.com/id2) |
| France         | [Link 1](https://example.com/fr1), [Link 2](https://example.com/fr2) |
| United Kingdom | [Link 1](https://example.com/uk1), [Link 2](https://example.com/uk2) |

> *Note: A complete list of sources and citations is maintained in the `/data` directory.*

### Repository Structure

```
.
├── website name /                # Final dataset (CSV, JSON, etc.)
├──── scripts/              # Web scraping and preprocessing scripts
├──── images/               # Extracted images or references (if applicable)
├──── xlsx file
└── README.md             # Documentation file (this file)
```

### Ethical Considerations

All data has been collected from publicly available sources. Any use of copyrighted material has been limited to metadata and for academic purposes only. Proper attribution has been ensured wherever required.

### Contribution

Researchers and collaborators are welcome to contribute to this dataset by submitting new recipes, source links, or helping with data cleaning and validation. Please submit a pull request or contact the maintainer for more information.
