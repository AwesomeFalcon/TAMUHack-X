import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
# Load the saved model
loaded_model = tf.keras.models.load_model('model_training/my_model.h5')

with open('model_training/vocabulary.json', 'r') as json_file:
    vocabulary = json.load(json_file)

def process(text):
    # Tokenize and preprocess the input text
    def preprocess_input_text(text, tokenizer, max_sequence_length):
        # Tokenize the input text
        sequences = tokenizer.texts_to_sequences([text])
        # Pad sequences to ensure consistent length
        padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post', truncating='post')
        return padded_sequences

    # Example command line input
    input_text = text

    # Preprocess the input text
    max_sequence_length = 1000  # Adjust based on your model's architecture
    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.word_index = vocabulary
    tokenizer.fit_on_texts([input_text])

    input_sequence = preprocess_input_text(input_text, tokenizer, max_sequence_length)

    # Make predictions using the loaded model
    prediction = loaded_model.predict(input_sequence)

    # Convert the prediction to a boolean output (assuming binary classification)
    is_phishing = prediction[0][0]

    # Print the result
    return is_phishing

# start Flask server
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['GET'])
def predict():
    text = request.args.get('text')
    print()
    print(text)
    result = process(text)  # Replace with your actual processing logic
    print()
    print(result)
    print()
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)
