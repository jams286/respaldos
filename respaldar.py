#!/usr/bin/env python3
"""Respaldo diario de las bases de datos de las tools de la casa y las personales de Jams.

Copia cada ~/.local/share/casa/*.db a /media/datos/Backups/casa/AAAA-MM-DD/ y cada
~/.local/share/personal/*.db a .../AAAA-MM-DD/personal/, con la API de respaldo de SQLite
(copia consistente aunque el servicio esté escribiendo), más los íconos subidos a mano en
inicio. Deja solo los últimos DIAS_A_GUARDAR días.

    python3 respaldar.py
"""

import re
import shutil
import sqlite3
import sys
from datetime import date
from pathlib import Path

ORIGENES = (  # (carpeta con las BD, subcarpeta dentro del respaldo del día)
    (Path.home() / '.local/share/casa', ''),
    (Path.home() / '.local/share/personal', 'personal'),
)
# Íconos que Jams subió a mano en personal/inicio (los automáticos se vuelven a bajar solos)
ICONOS_INICIO = Path.home() / '.local/share/personal/inicio-iconos/propios'
DESTINO = Path('/media/datos/Backups/casa')
DIAS_A_GUARDAR = 30


def main():
    if not DESTINO.parent.is_dir():
        # El disco JamsData no está montado: mejor fallar (queda en el journal) que escribir en otro lado
        sys.exit(f'No existe {DESTINO.parent}; ¿está montado el disco de datos?')

    carpeta = DESTINO / date.today().isoformat()
    carpeta.mkdir(parents=True, exist_ok=True)

    bases = 0
    for origen_dir, sub in ORIGENES:
        destino_dir = carpeta / sub
        destino_dir.mkdir(exist_ok=True)
        for bd in sorted(origen_dir.glob('*.db')):
            salida = destino_dir / bd.name
            temporal = salida.with_suffix('.tmp')
            with sqlite3.connect(bd) as origen, sqlite3.connect(temporal) as copia:
                origen.backup(copia)
            origen.close()
            copia.close()
            temporal.replace(salida)
            bases += 1
            print(f'{bd.name} -> {salida} ({salida.stat().st_size // 1024} KB)')

    if ICONOS_INICIO.is_dir():
        iconos = carpeta / 'personal' / 'inicio-iconos-propios'
        shutil.copytree(ICONOS_INICIO, iconos, dirs_exist_ok=True)
        print(f'{sum(1 for _ in iconos.iterdir())} íconos propios de inicio -> {iconos}')

    # Solo se borran carpetas con nombre de fecha, nunca otra cosa
    fechas = sorted(p for p in DESTINO.iterdir() if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.name))
    for vieja in fechas[:-DIAS_A_GUARDAR]:
        shutil.rmtree(vieja)
        print(f'Borrado respaldo viejo {vieja.name}')

    print(f'{bases} bases respaldadas en {carpeta}')


if __name__ == '__main__':
    main()
