# To run:
#  cd path/to/w3
# python test_import_w2.py

import sys
from pathlib import Path

# Optionally, add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from w1.utils import Stats, DataReader



try:
    import w1.utils # This line is redundant as it's already imported above
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
