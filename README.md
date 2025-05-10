# CPT411-PlaceFinder
### Short Description:
PlaceFinder DFA is a web-based Python application that implements a Deterministic Finite Automaton (DFA) to identify and extract place names from input text. Users can provide their own list of locations or use a default set of 15 predefined place names (e.g., Malaysia, Penang, Pizza Hut, New York).

## 🔍 Features
- Accepts both uploaded text files and direct user input.
- Dynamically builds a DFA from place name patterns, including handling:
- Case sensitivity (e.g., "Penang", not "PENANG")
- Multi-word entities (e.g., "Pizza Hut", "New York")
- Detects and highlights matched place names in the input text.
- Generates a summary table of matched patterns with position indexes and frequency.

## 🛠 Built With
- Python (Flask for the web app)
- Custom DFA implementation using classes for State and DFA
- Basic HTML for input/output rendering

## 📂 Default Place List
- ["Malaysia", "Penang", "Australia", "Intel", "Pizza Hut", 
 "New York", "Singapore", "Google", "London", "Johor", 
 "KLCC", "Starbucks", "Cyberjaya", "Amazon", "Sunway"]

## 📌 Use Case 
This tool is ideal for geotext analysis, named entity recognition, or text preprocessing tasks where identifying location-based keywords is needed.
