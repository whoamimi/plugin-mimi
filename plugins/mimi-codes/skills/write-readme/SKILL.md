---
name: write-readme
description: Write project's README.md file aligning with the template layout and rules defined in this skill file. this skill. 
---

Prior to performing task, check that the github repository is attached to this chat, otherwise, prompt the user to attach repository. 

Update the attached github repository's README.md file. Your README.md file must align with the following template example below.

# README.md Template

```markdown
# Project Title

[ensure to include shields.io badges alike examples below]

[![License](https://shields.io)](LICENSE)
[![Python 3.10+](https://shields.io)](https://python.org)

A concise, **one-to-two sentence description** of what this project does, the problem it solves relative to what my project's main objective and methodology.

## Highlights

- **Objective**: [main objective of the entire project]
- **Key Feature** [input the feature/method/intent/agenda of this project. If multiple features then please list in summary points]
- **Tech stack** [input how the key feature/s was/were implemented in this project e.g. depended open source library, dataset used if any,.etc]
* **Evaluation** [input how the idea/feature/model/algorithm was tested, any GPU acceleration, parallelization, or speed benchmarks]
* **Results & Conclusion** [list maximum of 2-3 summary points of the conclusion and decision made based on the idea implementation. Also, list extension to this project in moving forward]

## Project Directory Overview

[use CLI `tree` e.g. `tree -L 4 -d -I '__pycache__|.venv|node_modules' >` to return the subdirectory structure in the following example format]

Example project structure
```text
├── data/               # Raw and processed scientific data
├── src/                # Core source code and algorithms
├── tests/              # Unit tests
├── config.yaml         # Hyperparameters and file paths
└── main.py             # Main execution script
```

## System Architecture


## Dev Notes

- **Requirements**
  - [list the requirements if its currently mentioned in existing README, otherwise, you may skip this part]

- **Installation**: [input bash code of CLI steps installing the Git repo alike example below]

    ```bash
    # Clone the repository
    git clone https://github.com
    cd project-name
    
    # Create and activate environment
    conda create -n sci-env python=3.10 -y
    conda activate sci-env
    
    # Install dependencies
    pip install -r requirements.txt
    ```

 - **To start**: [input bash code of CLI steps starting/executing the project]
    ```bash
    python main.py --config config/demo.yaml
    ```

  - **Test**: [input bash code of CLI steps to run checks and tests on project]

  - [You may skip this part if there was no research paper mentioned throughout the source code. Otherwise, refer to examples below]
    - **Reproducing Results**: To reproduce the primary findings or figures stated in the paper/documentation:
      1. Update paths in `config.yaml`.
      2. Run the training/analysis pipeline:
           ```bash
           python src/pipeline.py --mode train
           ```

## Citation

If you use this software or method in your research, please cite it as follows:

```bibtex
@article{author2026title,
  author    = {Lastname, Firstname and Collaborator, Second},
  title     = {Scientific Project Title},
  journal   = {Journal Name},
  year      = {2026},
  doi       = {10.1000/xyz123}
}
```
