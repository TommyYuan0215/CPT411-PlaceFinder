from IPython.display import display, HTML

def bolding_words(word, code, i):
    css_colors = [
        ('teal', '#008080'),
        ('navy', '#000080'),
        ('olive', '#808000'),
        ('blue', '#0000FF'),
        ('green', '#00FF00'),
        ('magenta', '#FF00FF'),
        ('bright_black', '#666666'),
        ('yellow', '#FFFF00'),
        ('red', '#FF0000'),
        ('orange', '#FFA500'),
        ('purple', '#800080'),
        ('pink', '#FFC0CB'),
        ('brown', '#A52A2A'),
        ('gold', '#FFD700'),
        ('maroon', '#800000'),
    ]

    font_size = 0
    font_large = 25
    font_normal = 20
    font_bold = ""

    color_code = ""

    if i == -1:
        if code == "title":
            colour_code = 'black'
            font_size = font_large
            font_bold = "font-weight:bold;"
        elif code == "success":
            color_code = 'green'
            font_size = font_normal
            font_bold = "font-weight:bold;"
        elif code == "error":
            color_code = 'red'
            font_size = font_normal
            font_bold = "font-weight:bold;"
        elif code == "normal_bold":
            color_code = 'black'
            font_size = font_normal
            font_bold = "font-weight:bold;"
        else:
            color_code = 'black'
            font_size = font_normal
    else:
        if code == "result":
            color_code = css_colors[i][1]
            font_size = font_normal
            font_bold = "font-weight:bold;"

    if i != -1:
        color_code = css_colors[i % len(css_colors)][1] 
    html_text = f'<span style="font-size:{font_size}px; {font_bold} color:{color_code};">{word}</span>'
    return html_text


def display_HTML(text):
    return display(HTML(text))

class State:
    def __init__(self, is_final=False):
        self.transitions = {}
        self.is_final = is_final

    def add_transition(self, char, state):
        self.transitions[char] = state

class DFA:
    def __init__(self, patterns):
        self.start_state = State()
        self.build_dfa(patterns)

    def build_dfa(self, patterns):
        for pattern in patterns:
            current_state = self.start_state
            for char in pattern:
                if char not in current_state.transitions:
                    current_state.transitions[char] = State()
                current_state = current_state.transitions[char]
            current_state.transitions['$'] = State()
            current_state = current_state.transitions['$']
            current_state.is_final = True
    
    def search(self, text, patterns):
        matches = {pattern.lower(): [] for pattern in patterns}
        length = len(text)
        for idx in range(length):
            # Check if the pattern can start here
            if idx > 0 and text[idx - 1].isalnum():
                continue  # Skip because we're in the middle of a word
            
            current_state = self.start_state
            for j, char in enumerate(text[idx:]):
                if char in current_state.transitions:
                    current_state = current_state.transitions[char]
                    
                    # We have reached the end of a pattern
                    if '$' in current_state.transitions:
                        check_state = current_state.transitions['$']
                        if check_state.is_final:
                            # We've reached the end of the text or the next char is not a letter or digit
                            if idx + j + 1 == length or not text[idx + j + 1].isalnum():
                                original_pattern = text[idx:idx+j+1]
                                pattern_key = original_pattern.lower()
                                matches[pattern_key].append((idx, idx+j+1))
                            else:
                                # The following character is a letter or digit, hence it's not a word boundary
                                continue
                else:
                    break
        return matches
    
    def visualize_matches(self, text, matches, patterns_dict):
        result = text
        sorted_matches = sorted(
            ((pattern, start, end) for pattern, positions in matches.items() for start, end in positions),
            key = lambda x: x[1],
            reverse=True
        )
        for pattern, start, end in sorted_matches:
            color_index = patterns_dict.get(pattern.lower(), -1)
            formatted_pattern = bolding_words(text[start:end], "result", color_index)
            result = result[:start] + formatted_pattern + result[end:]

        return result
    
def show_DFA_output(text, dfa, matches, patterns_dict):
    result_str = ""
    result_str += bolding_words("Text used for demo:", "title", -1) + "<br>"
    result_str += text.replace("\n", "<br>") + "<br><br>"
    result_str += bolding_words("Results:", "title", -1) + "<br>"

    total_occurrences = sum(len(v) for v in matches.values())

    if total_occurrences > 0:
        for pattern, positions in matches.items():
            display_pattern = pattern.capitalize() if pattern.islower() else pattern
            result_str += bolding_words("Pattern:", "normal_bold", -1) + " " + bolding_words(display_pattern, "", -1) + "<br>"

            if len(positions) == 0:
                result_str += bolding_words("Status:", "", -1) + " " + bolding_words("Reject", "error", -1) + "<br>"
                result_str += bolding_words("Found:", "", -1) + " " + bolding_words(str(len(positions)), "normal_bold", -1) + "<br>"
            else:
                result_str += bolding_words("Status:", "", -1) + " " + bolding_words("Accept", "success", -1) + "<br>"
                result_str += bolding_words("Found:", "", -1) + " " + bolding_words(str(len(positions)), "normal_bold", -1) + "<br>"
                result_str += bolding_words("Positions:", "normal_bold", -1) + "<br>"
                for start, end in positions:
                    result_str += bolding_words(f"({start}, {end})", "", -1) + "<br>"
            result_str += "<br>"

        result_str += bolding_words("Total occurrences:", "", -1) + " " + bolding_words(total_occurrences, "normal_bold", -1) + "<br><br>"
        result_str += bolding_words("Visualization of patterns in the text:", "title", -1) + "<br>"
        result_str += dfa.visualize_matches(text, matches, patterns_dict) + "<br>"

    else:
        result_str += bolding_words("All patterns are not found in the given text.", "", -1)

    return result_str

def process_text(text, patterns):
    base_patterns = set(p.lower() for p in patterns)
    patterns_dict = {pattern: i for i, pattern in enumerate(base_patterns)}
    patterns = list(base_patterns) + [p.capitalize() for p in base_patterns]
    dfa = DFA(patterns)
    matches = dfa.search(text, patterns)
    results  = show_DFA_output(text, dfa, matches, patterns_dict)
    return results