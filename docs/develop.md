
# Develop requirements 
 - python : `3.9.4`
 - docker : `0.0.0`
 - torch : `0.0.0`

# Getting Started

Install venv
```bash
python -m venv .venv
.venv/bin/activate
python -V
```

Install requirements
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Set `PYTHONPATH`
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo $PYTHONPATH
```

# Method of Contributing to Open Source

Checklist Before Committing
```bash
pylint .
isort .
black .
pytest .
```