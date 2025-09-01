import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
while current_dir != current_dir.parent:
    if (current_dir / 'manage.py').exists():
        project_root = current_dir
        break
    current_dir = current_dir.parent
else:
    raise RuntimeError("Could not find project root containing manage.py")

sys.path.insert(0, str(project_root))
print(f"Added to PYTHONPATH: {project_root}")  # Для отладки