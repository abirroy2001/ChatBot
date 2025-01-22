import json
import random
import pickle
import numpy as np
import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents file (ensure the correct path to your intents.json)
intents_file_path = r'F:\E\Project\25centai\backend\intents.json'

with open(intents_file_path, 'r') as file:
    intents = json.load(file)

# Prepare words and classes (labels)
words = []
classes = []
documents = []
ignore_words = ['?', ',', '.', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize words and filter out unnecessary ones
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(set(words))  # Remove duplicates and sort
classes = sorted(set(classes))

# Save words and classes to pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Prepare training data
training_sentences = []
training_labels = []
for doc in documents:
    word_list = doc[0]
    word_list = [lemmatizer.lemmatize(w.lower()) for w in word_list]
    
    # Create bag of words
    bag = [1 if w in word_list else 0 for w in words]
    
    training_sentences.append(bag)
    training_labels.append(classes.index(doc[1]))

# Convert training data to numpy arrays
training_sentences = np.array(training_sentences)
training_labels = np.array(training_labels)

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(training_sentences[0]),), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(classes), activation='softmax')
])

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(training_sentences, training_labels, epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save('chatbot_model.h5')

print("Model trained and saved as chatbot_model.h5")
