import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pipeline import medical_pipeline

def test_pipeline_exists():
    assert medical_pipeline is not None
