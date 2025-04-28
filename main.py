from flask import Flask, render_template, request
import DFA_recognizer
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if text comes from file upload or direct input
        if 'text_file' in request.files and request.files['text_file'].filename != '':
            # Get text from uploaded file
            file = request.files['text_file']
            try:
                text = file.read().decode('utf-8')
            except UnicodeDecodeError:
                # Handle encoding errors
                return render_template('index.html', error="File encoding not supported. Please use UTF-8 encoded text files.")
        else:
            # Get text from form input
            text = request.form['patterns']
        
        # Get patterns from form
        pattern_input = request.form['pattern']
        if pattern_input:
            # Split the input by commas, strip spaces
            base_patterns = [p.strip() for p in pattern_input.split(',')]
            # Limit to 15 patterns as mentioned in HTML form
            base_patterns = base_patterns[:15]
        else:
            # If no patterns provided, use empty list
            base_patterns = []

        # Create dictionary for pattern tracking
        patterns_dict = {pattern.lower(): i for i, pattern in enumerate(base_patterns)}
        
        # Process the text using the DFA_recognizer
        results = DFA_recognizer.process_text(text, base_patterns)

        return render_template('result.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)