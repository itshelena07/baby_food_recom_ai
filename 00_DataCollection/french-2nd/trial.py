# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("token-classification", model="edwardjross/xlm-roberta-base-finetuned-recipe-all")

# Load model directly
from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("edwardjross/xlm-roberta-base-finetuned-recipe-all")
model = AutoModelForTokenClassification.from_pretrained("edwardjross/xlm-roberta-base-finetuned-recipe-all")

# Your input text (could be one or more ingredients/instructions)
text = "Mix 2 cups of flour and 3 eggs."

# Run the pipeline
results = pipe(text)

# Print results nicely
for result in results:
    print(f"Entity: {result['word']}, Label: {result['entity_group']}, Confidence: {result['score']:.2f}")