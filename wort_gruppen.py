positive=[]
negative=[]
neutral=[]

from transformers import pipeline,AutoTokenizer
from datasets import load_dataset
sentiment_pipeline=pipeline("sentiment-analysis",model="bhadresh-savani/distilbert-base-uncased-emotion",return_all_scores=True)

data=["I am not afraid of you"]

#test=sentiment_pipeline(data)
#print(test)

tokenizer=AutoTokenizer.from_pretrained("distilbert-base-uncased")

def preprocess_function(examples):
   return tokenizer(examples["text"], truncation=True)
 
imdb=load_dataset("imdb")
print(type(imdb))

small_train_dataset = imdb["train"].shuffle(seed=42).select([i for i in list(range(3000))])
small_test_dataset = imdb["test"].shuffle(seed=42).select([i for i in list(range(300))])

print(small_train_dataset)
print(small_train_dataset[0])
dataset=["""Dear Ukrainians!

A summary of this day.

First of all, I thank the Armed Forces of Ukraine, the warriors of the Defence Intelligence of Ukraine – Group 13 of the 9th Department. Today we have increased security in the Black Sea and added motivation to our people. This is important. Step by step we will clear the Black Sea of Russian terrorist objects.

Second. Today, I held a special, lengthy meeting on one of the key issues of this war, namely, our Ukrainian capabilities to counter Russian drones. The meeting was attended by Syrskyi, Umerov, Sukharevskyi, Shmyhal, Kamyshin, Fedorov, Yermak, Korosteliov, representatives of manufacturers, and intelligence officials. I listened to the report on current developments. We are working on both electronic warfare systems and air defense systems. Already about half of the existing systems are Ukrainian-made, developed by our people. Of course, there are also joint projects with partners. And, in fact, there are quite a few productions launched and developments slated for production. The key thing now is to integrate all of them into the practice of applying at the front. Proper adjustment and reconfiguration based on real combat needs, proper deployment, proper and systemic integration into combat tactics. Proper interaction between the demands of the front and the capabilities of our industry. Maximizing our production capacity. Ultimately, this means protecting the lives of our warriors and expanding our operational capabilities at the front. From countering Russian "Orlan" drones to destroying Russian electronic warfare. This year must yield more results for Ukraine – exactly the ones that will restore security for Ukrainian operations. I am grateful to all our developers and manufacturers, to everyone who develops a modern technological component in the Defense Forces. The state will take all the financial, organizational and regulatory steps required. And we must realize that everything that our state and our people will now learn to produce for the sake of our Ukrainian goals in the war will definitely become part of Ukrainian exports after the war, after we achieve our goals. Absolutely fair ones. Ukraine's global role is to be a security donor, a security exporter. Ukrainians know how to be strong and will always be strong and help others.

Third. Another expansion of our international coalitions, including the drone coalition. The Netherlands, Germany, and Estonia have joined the UK, Latvia, and Sweden. The foundation of the coalition is strong, and the coalition is already working. And today, by the way, is a new meeting of Ramstein. Increasing joint production and speeding up deliveries of drones and air defense are the top priorities of this Ramstein.

And one more thing.

Last night, Russian terrorists brutally shelled the city of Selydove in Donetsk region, hitting apartment buildings, ordinary civilian neighborhoods and a hospital. A targeted Russian strike on the city. At the time of this strike, there were almost 150 patients in the hospital, three people were killed – a mother with a little son and a woman who was preparing to become a mother. My condolences to the families and friends! The Russian state will definitely face retaliation for this strike.

We must win, we must fulfill our Ukrainian objectives. Security can only be gained through strength and by the strong.

Glory to all who fight for our country and people! Glory to all who work for Ukraine!""",]

tokenized_train = small_train_dataset.map(preprocess_function, batched=True)
tokenized_test = small_test_dataset.map(preprocess_function, batched=True)

print(tokenized_test)

from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

import numpy as np
from datasets import load_metric
 
def compute_metrics(eval_pred):
   load_accuracy = load_metric("accuracy")
   load_f1 = load_metric("f1")
  
   logits, labels = eval_pred
   predictions = np.argmax(logits, axis=-1)
   accuracy = load_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
   f1 = load_f1.compute(predictions=predictions, references=labels)["f1"]
   return {"accuracy": accuracy, "f1": f1}



from transformers import TrainingArguments, Trainer
 
repo_name = "finetuning-sentiment-model-3000-samples"
 
training_args = TrainingArguments(
   output_dir=repo_name,
   learning_rate=2e-5,
   per_device_train_batch_size=16,
   per_device_eval_batch_size=16,
   num_train_epochs=2,
   weight_decay=0.01,
   save_strategy="epoch",
   push_to_hub=True,
)
 
trainer = Trainer(
   model=model,
   args=training_args,
   train_dataset=tokenized_train,
   eval_dataset=tokenized_test,
   tokenizer=tokenizer,
   data_collator=data_collator,
   compute_metrics=compute_metrics,
)

trainer.train()

trainer.evaluate()