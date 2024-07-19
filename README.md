# Requmancer

Requmancer is a powerful Python library and command-line tool that analyzes your Python project and generates a comprehensive requirements file. It automatically detects imported packages, determines their versions, and creates either a pip-compatible `requirements.txt` or a Poetry-style `pyproject.toml` section.

With Requmancer, managing your project's dependencies becomes a breeze, ensuring reproducibility and easier setup for other developers.

## Features

- Automatically detects third-party imports in your Python project.
- Determines the installed versions of the imported packages.
- Generates a `requirements.txt` file for pip or a `pyproject.toml` section for Poetry.
- Handles both absolute and relative imports.
- Excludes standard library modules from the requirements file.

## Installation

You can install Requmancer using pip:

```bash
pip install requmancer
```

## Usage

Requmancer can be used both as a command-line tool and as a Python library.

### Command-Line Usage

To generate a `requirements.txt` file for your project, navigate to the root directory of your project and run:

```bash
requmancer .
```

You can specify the output file name and format using the `-o` and `-f` options:

```bash
requmancer . -o requirements.txt -f pip
requmancer . -o pyproject.toml -f poetry
```

### Python Library Usage

You can also use Requmancer as a Python library in your own scripts:

```python
from requmancer.main import RequirementsGenerator

generator = RequirementsGenerator(directory='path/to/your/project', output_file='requirements.txt', format='pip')
generator.generate()
```

## Example

Suppose you have a Python project with the following structure:

```
my_project/
├── main.py
├── module/
│   └── submodule.py
└── requirements.txt
```

And the `main.py` file contains:

```python
import requests
import numpy as np
```

Running `requmancer .` in the `my_project` directory will generate a `requirements.txt` file with the following content:

```
requests==2.25.1
numpy==1.19.5
```

## Development

To contribute to Requmancer, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/ParisNeo/requmancer.git
cd requmancer
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the development dependencies:

```bash
pip install -r requirements_dev.txt
```

4. Run the tests:

```bash
pytest
```

## License

Requmancer is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Author

Requmancer is developed and maintained by [ParisNeo](https://github.com/ParisNeo).

## Acknowledgements

Special thanks to the open-source community for providing the tools and libraries that made this project possible.
