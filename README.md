# ****📘 NLP for Accessibility – Text Simplification for Dyslexic Readers****
This project focuses on improving text accessibility for individuals with dyslexia by applying advanced Natural Language Processing (NLP) techniques to simplify complex English sentences. The system transforms input text into simpler, easier-to-read versions while preserving the original meaning and structure.

## ****🎯 Objective****
To develop an AI-driven tool that automatically simplifies complex text using transformer-based language models, enhancing readability and comprehension for dyslexic readers.

## ****🔍 Key Features****
****🔡 Lexical Simplification****: Replaces difficult words with simpler synonyms.

****📏 Syntactic Simplification****: Breaks down long, complex sentences into shorter, clearer ones.

****🧠 Phonetic and Visual Adjustments****: Applies formatting to reduce cognitive load (e.g., increased spacing, dyslexia-friendly font suggestions).

****🤖 Transformer-Based Models****: Utilizes pretrained models like T5, BART, and Mistral for text generation and simplification tasks.

****📊 Evaluation Metrics****: Assesses output using BLEU, SARI, and FKGL scores.

****🖥️ Frontend (React.js + Node.js)****
A user-friendly web interface is developed to make the simplification tool easily accessible:

Built using React.js for responsive and interactive UI.

Uses Node.js and Express.js on the backend to handle API requests to the NLP model.

Supports input via text box or file upload.

Displays original and simplified sentences side-by-side.

Designed with accessibility in mind – supports larger fonts, color contrast, and clean layout for dyslexic users.

## ****🧪 Experiment Setup****
****Models Evaluated:****

T5-base, BART, Mistral-7B-Instruct-v0.1

****Prompting Techniques:****

Zero-shot, One-shot, and Few-shot prompting.

****Metrics Used:****

BLEU (Fluency)

SARI (Simplicity and preservation)

FKGL (Readability)

## ****📁 Dataset****
Input: A set of complex English sentences.

Output: Simplified versions suitable for dyslexic readers.

Additional: Custom test cases were created to evaluate model performance across varying levels of complexity.

## ****🛠️ Tech Stack****
****Frontend****: React.js, Tailwind CSS, Axios

****Backend****: Node.js, Express.js

****Model Inference****: Python (Hugging Face Transformers, PyTorch)

****Evaluation Tools****: NLTK, EASSE

Deployment (optional): Docker, Vercel/Render (for frontend), Hugging Face Spaces/API for model inference

## ****🌍 Real-World Impact****
This system can be integrated into:

Educational platforms for students with learning difficulties

E-readers and browsers with built-in text simplification

Assistive reading apps focused on inclusivity

📌 Future Enhancements
Add speech synthesis for read-aloud support

Build a browser extension for live web content simplification

Personalize simplification levels based on individual user needs
