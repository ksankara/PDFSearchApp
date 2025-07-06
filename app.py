from flask import Flask, render_template, request, jsonify
import PyPDF2
import io
import os
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            question = request.form.get('question', '').strip()
            if not question:
                return jsonify({'error': 'No question provided'}), 400
            # Compose the prompt
            prompt = f"PDF Content:\n{text}\n\nQuestion: {question}\nAnswer:"
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                return jsonify({'error': 'OpenAI API key not set in .env file'}), 500
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions about PDF documents."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=128,
                    temperature=0
                )
                answer = response.choices[0].message.content.strip()
                return jsonify({'answer': answer})
            except Exception as e:
                return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=False)
