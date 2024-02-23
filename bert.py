
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from transformers import BertTokenizer
import torch
from transformers import pipeline

sentences = [
  "Here We Go Then, You And I is a 1999 album by Norwegian pop artist Morten Abel. It was Abel's second CD as a solo artist.",
  "The album went straight to number one on the Norwegian album chart, and sold to double platinum.",
  "Among the singles released from the album were the songs \"Be My Lover\" and \"Hard To Stay Awake\".",
  "Riccardo Zegna is an Italian jazz musician.",
  "Rajko Maksimović is a composer, writer, and music pedagogue.",
  "One of the most significant Serbian composers of our time, Maksimović has been and remains active in creating works for different ensembles.",
  "Ceylon spinach is a common name for several plants and may refer to: Basella alba Talinum fruticosum",
  "A solar eclipse occurs when the Moon passes between Earth and the Sun, thereby totally or partly obscuring the image of the Sun for a viewer on Earth.",
  "A partial solar eclipse occurs in the polar regions of the Earth when the center of the Moon's shadow misses the Earth.",
]



#wie sieht die struktur im dataset aus wichtig für tokenize

from datasets import load_dataset
imdb = load_dataset("imdb")


small_test_dataset = imdb["test"].shuffle(seed=42).select([i for i in list(range(10))])

#model = pipeline(model="bert-base-uncased")

from transformers import BertForSequenceClassification

# Load pretrained BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Optionally, you can customize the model configuration
# model.config.hidden_dropout_prob = 0.1
# model.config.num_labels = 2
# etc.


print(small_test_dataset)


train_dict = {
    'text': ["Disgusting","Beautiful","Ugly","Nice"],
    'labels': [0, 1, 0, 1]
}


test_dict = {
    'text': ["Failure","Fear","Negative","Positive"],
    'labels': [0, 0, 0, 1]
}

def create_dataset_from_list(data_dict):
    tensor_dict = {key: tf.constant(value) for key, value in data_dict.items()}
    dataset = tf.data.Dataset.from_tensor_slices(tensor_dict)
    print(dataset)
    return dataset

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


def preprocess_function(data_dict):
    dict={"input_ids":[],"attention_mask":[],"labels":[]}
    for text in data_dict["text"]:
        token=tokenizer(text, truncation=True)
        dict["input_ids"].append(token["input_ids"])
        dict["attention_mask"].append(token["attention_mask"])
    dict["labels"]=data_dict["labels"]
    return dict

from datasets import Dataset

train_tokens=preprocess_function(train_dict)
print(train_tokens)
train_dataset = Dataset.from_dict(train_tokens)
test_tokens=preprocess_function(test_dict)
print(test_tokens)
eval_dataset = Dataset.from_dict(test_tokens)


from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


from transformers import TrainingArguments, Trainer
 
repo_name = "finetuning-sentiment-model-3000-samples"
 
import numpy as np
from datasets import load_metric
import evaluate
 
def compute_metrics(eval_pred):
   accuracy = evaluate.load("accuracy")
   print()
   f1 = evaluate.load("accuracy")
  
   logits, labels = eval_pred
   predictions = np.argmax(logits, axis=-1)
   accuracy = accuracy.compute(predictions=predictions, references=labels)
   f1 = f1.compute(predictions=predictions, references=labels)
   return {"accuracy": accuracy, "f1": f1}



training_args = TrainingArguments(
   output_dir=repo_name,
   learning_rate=2e-5,
   per_device_train_batch_size=16,
   per_device_eval_batch_size=16,
   num_train_epochs=2,
   weight_decay=0.01,
   save_strategy="epoch",
   push_to_hub=False,
)
 
trainer = Trainer(
   model=model,
   args=training_args,
   train_dataset=train_dataset,
   eval_dataset=eval_dataset,
   tokenizer=tokenizer,
   data_collator=data_collator,
   compute_metrics=compute_metrics,
)

trainer.train()


results=trainer.evaluate()
print(results)

#mutliple labels und long text
