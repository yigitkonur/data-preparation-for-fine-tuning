#### Introduction

Welcome to the `data-preparation-for-fine-tuning` project, a robust and versatile Python toolkit designed for the meticulous preparation and comprehensive analysis of datasets from JSONL files. Our tools, `dataset-chooser.py` and `dataset-evaluator.py`, are not just scripts but powerful instruments in your data science arsenal. They enable users to homogenize datasets based on pre-specified weights for each category, particularly focusing on assistant responses. This feature is especially beneficial for fine-tuning machine learning models, ensuring the dataset aligns perfectly with your specific needs and biases are minimized.

#### JSONL File Format

Our scripts work with datasets in JSONL format. Each line in a JSONL file is a valid JSON object. Here's a glimpse of what our dataset might look like:

```jsonl
{"messages": [{"role": "system", "content": "Classify..."}, {"role": "user", "content": "saas..."}, {"role": "assistant", "content": "History"}]}
{"messages": [{"role": "system", "content": "Classify..."}, {"role": "user", "content": "diskussionsrunden..."}, {"role": "assistant", "content": "Retail"}]}
{"messages": [{"role": "system", "content": "Classify..."}, {"role": "user", "content": "polis..."}, {"role": "assistant", "content": "Consumer Electronics"}]}
```

#### Installation and Setup

1. **Clone the Repository:**
   ```
   git clone https://github.com/yourusername/data-preparation-for-fine-tuning.git
   cd data-preparation-for-fine-tuning
   ```
   
2. **Dependencies:**
   Python 3.6+ is required. Install dependencies using:
   ```
   pip install pandas rich configparser
   ```

#### Configuration

1. **config.ini File:**
   Create this in the root directory. Modify paths and weights to suit your dataset:
   ```ini
   [Paths]
   jsonl_directory = /path/to/jsonl/files
   output_file = /path/to/output/dataset.jsonl

   [Weights]
   category_weights = {
       "Category1": 0.05,
       ...
   }

   [Settings]
   total_examples = 1000000
   ```

#### Usage

1. **Dataset Preparation (`dataset-chooser.py`):**
   Reads, shuffles, and categorizes JSONL files. Tailor your dataset for specific modeling needs.
   ```
   python dataset-chooser.py
   ```

2. **Dataset Analysis (`dataset-evaluator.py`):**
   Analyzes the prepared dataset, providing insightful metrics and distributions.
   ```
   python dataset-evaluator.py
   ```

#### Use Cases

- **Model Training:** Prepare balanced or weighted datasets for training machine learning models, ensuring diverse representation across categories.
- **Data Analysis:** Gain insights into the composition of your datasets, identifying prevalent themes or gaps in data.
- **Custom Dataset Creation:** Generate datasets tailored to specific research or business needs, focusing on relevant categories.

#### Fine-Tuning Models with Homogenized Data

Utilizing `data-preparation-for-fine-tuning`, you can fine-tune machine learning models with data that's been carefully balanced or weighted according to your specifications. This process involves:

1. Defining category weights in `config.ini` to reflect the desired emphasis in your dataset.
2. Running `dataset-chooser.py` to prepare a dataset that adheres to these weights.
3. Using the processed dataset to train models, ensuring the data is representative and aligned with your goals.

This approach is particularly useful in scenarios where certain categories need more representation or when trying to avoid biases inherent in unbalanced datasets.
