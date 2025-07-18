import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        return "Flask backend is running."

    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # -------- TEXT EXTRACTION -------- #
    if file.filename.lower().endswith('.txt') or file.mimetype == 'text/plain':
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                original_text = f.read()
            print("✅ Extracted text from TXT or typed input file:\n", original_text)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Text file reading error: {str(e)}'})
            
    else:
        try:
            from PIL import Image
            from pytesseract import pytesseract
            pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            img = Image.open(filename)
            original_text = pytesseract.image_to_string(img)
            print("✅ OCR Extracted Text:\n", original_text)

            if not original_text.strip():
                return jsonify({'success': False, 'error': 'OCR produced empty text'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'OCR failed: {str(e)}'})

    
    # -------- SUMMARIZATION USING MISTRAL (OpenRouter) -------- #
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()

        openai.api_key = os.getenv("OPENROUTER_API_KEY")
        openai.api_base = "https://openrouter.ai/api/v1"

        prompt_template = f"""Simplify the following text for someone with dyslexia.

                           Use:
                           - Short and simple sentences
                           - Easy and common words
                           - Simple vocabulary that a child can understand
                           - No difficult or complex words
                           - Clear and direct phrasing
                           - Avoid long or compound sentences\n\nText:\n{original_text}\n\nSimplified:"""

        print("🤖 Sending to Mistral 7B via OpenRouter...")
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that simplifies English text."},
                {"role": "user", "content": prompt_template}
            ],
            temperature=0.7
        )

        summarized_text = response['choices'][0]['message']['content'].strip()
        print("✅ Summarized Text:\n", summarized_text)

        if not summarized_text:
            return jsonify({'success': False, 'error': 'Empty output from Mistral API'})

    except Exception as e:
        return jsonify({'success': False, 'error': f'Mistral API summarization error: {str(e)}'})

    
    # -------- READABILITY EVALUATION -------- #
    try:
        import textstat

        fkgl_original = textstat.flesch_kincaid_grade(original_text)
        fkgl_simplified = textstat.flesch_kincaid_grade(summarized_text)

        dale_original = textstat.dale_chall_readability_score(original_text)
        dale_simplified = textstat.dale_chall_readability_score(summarized_text)

        print("📊 Readability Evaluation:")
        print(f"   Original FKGL: {fkgl_original:.2f} → Simplified FKGL: {fkgl_simplified:.2f}")
        print(f"   Original Dale-Chall: {dale_original:.2f} → Simplified Dale-Chall: {dale_simplified:.2f}")
    except Exception as e:
        print(f"⚠️ Readability evaluation failed: {str(e)}")




    # -------- TEXT TO SPEECH -------- #
    try:
        from gtts import gTTS
        summarized_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], '1.wav')
        original_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], '2.wav')
        gTTS(summarized_text, lang='en').save(summarized_audio_path)
        gTTS(original_text, lang='en').save(original_audio_path)
        print("🔊 Audio files generated successfully.")
    except Exception as e:
        print("❌ TTS failed:", str(e))
        return jsonify({'success': False, 'error': f'TTS failed: {str(e)}'})
    return jsonify({
        'success': True,
        'original_text': original_text,
        'summarized_text': summarized_text,
        'summary_sound': '/uploads/1.wav',
        'original_sound': '/uploads/2.wav'
    })


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    print("🚀 Starting Flask backend on http://localhost:5000")
    app.run("localhost", 5000)
