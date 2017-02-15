# Sistercities

A parser + web frontend to create graph data about the topic sister cities 
from Wikipedia and Wikidata and compare them.


## Installation

Requirements
```
Python34
easyinstall
virtualvenv
de.wikipedia.org account
```

```
~ git clone git@github.com:displayn/sistercities.git
~ cd sistercities/sistercities
~ virtalvenv venv
~ . venv/bin/active
~ pip install requirements.txt

```

## Usage


### Running the Parser
Before starting, change the user-config.py-sample to your Wikipedia account and save it under user-config.py.
Run the parser with:
```
python34 sistercities/parser/de_parser.py
```

### Running the Frontend
Place the generated JSON files from the parser under: 
```
sistercities/web/sistercities/
```
Start the service with:
```
python34 sistercities/web/sistercities/app.py
```
The service is running on http://127.0.0.1:5000/  
## License
MIT. See [LICENSE](LICENSE).