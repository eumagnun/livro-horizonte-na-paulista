"""Garante que `import exercicio` sempre resolva para o arquivo exercicio.py
DESTA pasta, mesmo rodando `pytest` para o repositório inteiro de uma vez.

Sem isso, o Python cacheia o primeiro módulo chamado "exercicio" que
encontrar e reaproveita esse cache para todos os outros módulos -- já que
vários módulos deste curso têm, de propósito, um arquivo `exercicio.py`
com o mesmo nome."""

import sys
from pathlib import Path

sys.modules.pop("exercicio", None)
sys.path.insert(0, str(Path(__file__).parent))
