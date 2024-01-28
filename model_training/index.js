// Load the TensorFlow.js model and vocabulary
const loadModelAndVocabulary = async () => {
  const model = await tf.loadLayersModel("tfjs_model/model.json");

  // Load the vocabulary (word index)
  const vocabulary = await fetch("vocabulary.json").then((response) =>
    response.json()
  );

  return { model, vocabulary };
};

// Manually perform tokenization and padding
const preprocessInputText = (text, vocabulary, maxSequenceLength) => {
  // Tokenize the input text
  const words = text.split(" ");
  const sequence = words.map((word) => vocabulary[word] || 0);

  // Pad sequences to ensure consistent length
  while (sequence.length < maxSequenceLength) {
    sequence.push(0); // Pad with zeros
  }

  // Truncate sequences if necessary
  const truncatedSequence = sequence.slice(0, maxSequenceLength);

  // Convert to TensorFlow.js tensor
  const inputData = tf.tensor2d([truncatedSequence]);

  return inputData;
};

// Make predictions using the loaded model
const makePredictions = async (
  { model, vocabulary },
  inputText,
  maxSequenceLength
) => {
  // Preprocess the input text
  const inputData = preprocessInputText(
    inputText,
    vocabulary,
    maxSequenceLength
  );

  // Make predictions
  const predictions = model.predict(inputData);

  // Log the predictions
  // predictions.print();

  console.log(`${(predictions.dataSync()[0] * 100).toFixed(4)}% safe`);

  // Clean up
  inputData.dispose();
  predictions.dispose();
};

// Main function to use the model
const runApp = async () => {
  // Load the model and vocabulary
  const { model, vocabulary } = await loadModelAndVocabulary();

  // Example input text
  const inputText = prompt("give me input");
  const maxSequenceLength = 1000; // Adjust based on your model's architecture

  // Make predictions
  await makePredictions({ model, vocabulary }, inputText, maxSequenceLength);
};

// Call the main function when the page is loaded
runApp();
