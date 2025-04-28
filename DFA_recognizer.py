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
    
    # Text used for demo
    result_str += '''
        <div class="my-3">
            <h4 class="text-primary">Text used for demo:</h4>
        </div>
        <div class="p-3 bg-light border rounded mb-4">
            ''' + text.replace("\n", "<br>") + '''
        </div>
    '''

    # Results section
    result_str += '<div class="my-3"><h4 class="text-primary">Results:</h4></div>'
    
    total_occurrences = sum(len(v) for v in matches.values())

    if total_occurrences > 0:
        # Start of the table
        result_str += '''
        <table class="table table-bordered">
            <thead class="table-light">
                <tr>
                    <th style="text-align: center;">Pattern</th>
                    <th style="text-align: center;">Status</th>
                    <th style="text-align: center;">Found</th>
                    <th style="text-align: center;">Positions</th>
                </tr>
            </thead>
            <tbody style="text-align: center;">
        '''  # Added text-align center to tbody

        for pattern, positions in matches.items():
            display_pattern = pattern.capitalize() if pattern.islower() else pattern
            num_positions = len(positions)

            if num_positions > 0:
                # First row for this pattern
                result_str += "<tr>"

                # Merge Pattern, Status, and Found cells for the first position
                result_str += f'<td rowspan="{num_positions}">{display_pattern}</td>'
                result_str += f'<td class="text-success" rowspan="{num_positions}">Accept</td>'
                result_str += f'<td rowspan="{num_positions}">{num_positions}</td>'

                # Positions column (for the first position)
                result_str += f'<td>({positions[0][0]}, {positions[0][1]})</td>'
                result_str += "</tr>"

                # Additional rows for other positions
                for start, end in positions[1:]:
                    result_str += "<tr>"
                    result_str += f'<td>({start}, {end})</td>'  # Positions column
                    result_str += "</tr>"

            else:
                # No positions for this pattern, just show reject
                result_str += "<tr>"
                result_str += f'<td>{display_pattern}</td>'  # Single cell for Pattern
                result_str += '<td class="text-danger">Reject</td>'
                result_str += '<td class="text-muted">0</td>'
                result_str += '<td>-</td>'
                result_str += "</tr>"

        # Closing the table
        result_str += '''
            </tbody>
        </table>
        '''


        # Total occurrences section
        result_str += f'<div class="fw-bold">Total occurrences: <span class="text-info">{total_occurrences}</span></div>'
        result_str += "<br><br>"

        # Visualization of patterns
        result_str += '''
            <div class="my-3">
                <h4 class="text-primary">Visualization of patterns in the text:</h4>
            </div>
            <div class="p-3 bg-light border rounded mb-4">
                ''' + dfa.visualize_matches(text, matches, patterns_dict) + '''
            </div>
        '''
    else:
        result_str += '<div class="text-warning">All patterns are not found in the given text.</div>'

    return result_str

def process_text(text, patterns):
    base_patterns = set(p.lower() for p in patterns)
    patterns_dict = {pattern: i for i, pattern in enumerate(base_patterns)}
    patterns = list(base_patterns) + [p.capitalize() for p in base_patterns]
    dfa = DFA(patterns)
    matches = dfa.search(text, patterns)
    results  = show_DFA_output(text, dfa, matches, patterns_dict)
    return results