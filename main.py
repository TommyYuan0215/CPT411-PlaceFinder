from flask import Flask, render_template, request
import DFA_recognizer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Form submitted") # Debug log
        # Check if text comes from file upload or direct input
        if 'file' in request.files and request.files['file'].filename != '':
            # Get text from uploaded file
            file = request.files['file']
            try:
                text = file.read().decode('utf-8')
                print(f"File text: {text[:100]}") # Debug log
            except UnicodeDecodeError:
                print("Encoding error") # Debug log
                return render_template('index.html', error="File encoding not supported. Please use UTF-8 encoded text files.")
        else:
            # Get text from form input
            text = request.form['demotext']
            print(f"Form text: {text[:100]}") # Debug log
        
        # Get patterns from form
        pattern_input = request.form['pattern']
        print(f"Patterns: {pattern_input}") # Debug log
        
        if pattern_input:
            base_patterns = [p.strip() for p in pattern_input.split(',')]
            base_patterns = base_patterns[:15]
        else:
            base_patterns = ["Malaysia", "Penang", "Australia", "Intel", "Pizza Hut", "New York", "Singapore", "Google", "London", "Johor", "KLCC", "Starbucks", "Cyberjaya", "Amazon", "Sunway"]

        # Process the text using the DFA_recognizer
        results = DFA_recognizer.process_text(text, base_patterns)
        print(f"Results generated: {results[:100]}") # Debug log

        return render_template('result.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
