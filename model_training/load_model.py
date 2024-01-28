import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

# Load the saved model
loaded_model = tf.keras.models.load_model('my_model.h5')

# Tokenize and preprocess the input text
def preprocess_input_text(text, tokenizer, max_sequence_length):
    # Tokenize the input text
    sequences = tokenizer.texts_to_sequences([text])
    # Pad sequences to ensure consistent length
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post', truncating='post')
    return padded_sequences

# Example command line input
input_text = input("Enter your untokenized text: ")

# Preprocess the input text
max_sequence_length = 1000  # Adjust based on your model's architecture
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts([input_text])


input_sequence = preprocess_input_text(input_text, tokenizer, max_sequence_length)

# Make predictions using the loaded model
prediction = loaded_model.predict(input_sequence)

# Convert the prediction to a boolean output (assuming binary classification)
is_phishing = prediction[0][0] > 0.8

# Print the result
print(f'The input text is {"phishing" if is_phishing else "safe"} ({prediction[0][0]}).')
