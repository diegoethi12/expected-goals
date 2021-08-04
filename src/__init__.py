from pathlib import Path

DATA_PATH = Path(__file__).parent / 'data'
DATA_PATH.mkdir(exist_ok=True)

MODEL_PATH = Path(__file__).parent / 'model'
MODEL_PATH.mkdir(exist_ok=True)

__ALL__ = ['DATA_PATH']
