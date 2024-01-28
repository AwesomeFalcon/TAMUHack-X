# get labels from Phishing_Email.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense

import json

# import tensorflowjs as tfjs


# read csv file
df2 = pd.read_csv('Phishing_Email.csv')

# remove first unnamed column
df2 = df2.drop(df2.columns[0], axis=1)
lendf2 = len(df2)

texts = []
labels = []

# iterate through each row of the first dataframe
for index, row in df2.iterrows():
    # create a new row in the second dataframe
    # df2.loc[index] = [row['text'], row['label']]
    text = row['Email Text']
    label = row['Email Type']

    if not isinstance(text, str):
        continue

    # if text is greater than 5000 words, split into 5000-word chunks
    if len(text) > 5000:
        # split text into 5000-word chunks
        chunks = [text[i:i + 5000] for i in range(0, len(text), 5000)]

        # add each chunk to the dataframe
        for chunk in chunks:
            texts.append(chunk)
            labels.append(label)
    else:
        texts.append(text)
        labels.append(label)

    print("Progress: " + str(index) + "/" + str(lendf2), end="\r")

print()
print(df2.head())


# Split the dataset into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# Convert labels to numerical values
label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_labels)
test_labels_encoded = label_encoder.transform(test_labels)

# Tokenize the text data
max_words = 5000  # Adjust as needed
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(train_data)


with open('vocabulary.json', 'w') as json_file:
    json.dump(tokenizer.word_index, json_file)

# Convert text data to sequences
train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

# Pad sequences to ensure consistent length
max_sequence_length = 1000  # Adjust as needed
train_padded = pad_sequences(train_sequences, maxlen=max_sequence_length, padding='post', truncating='post')
test_padded = pad_sequences(test_sequences, maxlen=max_sequence_length, padding='post', truncating='post')

# Build a simple neural network model
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=32, input_length=max_sequence_length))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_padded, train_labels_encoded, epochs=3, batch_size=32, validation_split=0.2)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_padded, test_labels_encoded)
print(f'Test Accuracy: {test_accuracy}')

model.save('my_model.h5')
# tfjs.converters.save_keras_model(model, 'tfjs_model')