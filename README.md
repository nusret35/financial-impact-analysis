---
license: mit
base_model: roberta-base
language:
- en
---

# Financial News Impact Analysis Using RoBERTa

This is a RoBERTa-base model trained on 15k financial news title from January 1, 2021 to April 22, 2024 and finetuned for market impact analysis. The data is taken from forexfactory.com. This model is suitable for English.

**Labels**: 0 -> Low, 1 -> Medium, 2 -> High

### Example

```python
from transformers import AutoModelForSequenceClassification
from transformers import RobertaTokenizerFast
import torch

label_mapping = {
    0: "Low",
    1: "Medium",
    2: "High"
}

MODEL = "nusretkizilaslan/roberta-financial-news-impact-analysis"
tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base')
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

input_text = "German Buba President Nagel Speaks"
encoding = tokenizer(input_text, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
input_ids =  encoding['input_ids'].flatten()
attention_mask = encoding['attention_mask'].flatten()
input_ids = input_ids.unsqueeze(0)
attention_mask = attention_mask.unsqueeze(0)

output = model(input_ids,attention_mask)
predicted_class_index = torch.argmax(output.logits)
predicted_label = label_mapping[predicted_class_index.item()]
print("Predicted Impact:", predicted_label)

```

Output:

```bash
Predicted Impact: Low
```

## Data generation

Data is scraped from forexfactory.com. In `generate_data` folder, there are two `.py`files. `url_generator.py` is to generate the URLs of the pages that are going to be scraped. You can give the desired date range as an input and generate the URLs. `scrape_forex_factory.py` is to scrape those pages. This file will generate `forex_factory_dataset.csv` file. 

## Training

Training steps of the model can be easily followed in the notebook file. You can access the model through HuggingFace. Here is the link for it: https://huggingface.co/nusret35/roberta-financial-news-impact-analysis

