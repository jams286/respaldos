#!/usr/bin/env python3
"""Respaldo diario de las bases de datos de las tools de la casa.

Copia cada ~/.local/share/casa/*.db a /media/datos/Backups/casa/AAAA-MM-DD/ con la API
de respaldo de SQLite (copia consistente aunque el servicio esté escribiendo) y deja
solo los últimos DIAS_A_GUARDAR días.

    python3 respaldar.py
"""

import re
import shutil
import sqlite3
import sys
from datetime import date
from pathlib import Path

ORIGEN = Path.home() / '.local/share/casa'
DESTINO = Path('/media/datos/Backups/casa')
DIAS_A_GUARDAR = 30


def main():
    if not DESTINO.parent.is_dir():
        # El disco JamsData no está montado: mejor fallar (queda en el journal) que escribir en otro lado
        sys.exit(f'No existe {DESTINO.parent}; ¿está montado el disco de datos?')

    carpeta = DESTINO / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)

    bases = sorted(ORIGEN.glob('*.db'))
    for bd in bases:
        salida = carpeta / bd.name
        temporal = salida.with_suffix('.tmp')
        with sqlite3.connect(bd) as origen, sqlite3.connect(temporal) as copia:
            origen.backup(copia)
        origen.close()
        copia.close()
        temporal.replace(salida)
        print(f'{bd.name} -> {salida} ({salida.stat().st_size // 1024} KB)')

    # Solo se borran carpetas con nombre de fecha, nunca otra cosa
    fechas = sorted(p for p in DESTINO.iterdir() if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.name))
    for vieja in fechas[:-DIAS_A_GUARDAR]:
        shutil.rmtree(vieja)
        print(f'Borrado respaldo viejo {vieja.name}')

    print(f'{len(bases)} bases respaldadas en {carpeta}')


if __name__ == '__main__':
    main()
