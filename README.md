# respaldos

Respaldo diario de las bases de datos de las tools de la casa (`~/.local/share/casa/*.db`: lista de compras, tareas, cocina, pizarra) y de las personales de Jams (`~/.local/share/personal/*.db`: inicio, con sus íconos subidos a mano) en el disco JamsData.

- Destino: `/media/datos/Backups/casa/AAAA-MM-DD/` (las personales en `AAAA-MM-DD/personal/`; se guardan los últimos 30 días).
- Corre todos los días a las 3:30 a. m. (timer de systemd de usuario). Si el server estaba apagado a esa hora, corre al encender.

## Comandos

```
python3 ~/proyectos/infra/respaldos/respaldar.py           # respaldar ahora
systemctl --user list-timers respaldo-casa.timer           # próxima corrida
journalctl --user -u respaldo-casa -n 20                   # qué hizo
```

Instalar o actualizar:

```
cp ~/proyectos/infra/respaldos/servicio/respaldo-casa.* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now respaldo-casa.timer
```

## Restaurar

Detener el servicio de la tool, copiar el respaldo encima y volver a arrancar. Ejemplo con la lista de compras:

```
systemctl --user stop lista-compras
cp /media/datos/Backups/casa/AAAA-MM-DD/lista-compras.db ~/.local/share/casa/lista-compras.db
rm -f ~/.local/share/casa/lista-compras.db-wal ~/.local/share/casa/lista-compras.db-shm
systemctl --user start lista-compras
```

Mi inicio (personal):

```
systemctl --user stop inicio
cp /media/datos/Backups/casa/AAAA-MM-DD/personal/inicio.db ~/.local/share/personal/inicio.db
rm -f ~/.local/share/personal/inicio.db-wal ~/.local/share/personal/inicio.db-shm
cp -n /media/datos/Backups/casa/AAAA-MM-DD/personal/inicio-iconos-propios/* ~/.local/share/personal/inicio-iconos/propios/
systemctl --user start inicio
```

## Restaurar

Probado el 2026-10-31 con la lista de compras: la copia restaurada estaba íntegra y el servidor la sirvió con el dato de prueba.

Probar un respaldo sin tocar los datos reales (otra base y otro puerto):

```
cp /media/datos/Backups/casa/AAAA-MM-DD/lista-compras.db /tmp/prueba.db
sqlite3 /tmp/prueba.db 'pragma integrity_check'
LISTA_BD=/tmp/prueba.db LISTA_PUERTO=18770 python3 ~/proyectos/casa/lista-compras/servidor.py
curl -s http://127.0.0.1:18770/api/items
```

Restaurar de verdad (ejemplo: lista de compras; igual para tareas, cocina y pizarra con su servicio):

```
systemctl --user stop lista-compras.service
cp ~/.local/share/casa/lista-compras.db ~/.local/share/casa/lista-compras.db.antes   # por si acaso
rm -f ~/.local/share/casa/lista-compras.db-wal ~/.local/share/casa/lista-compras.db-shm
cp /media/datos/Backups/casa/AAAA-MM-DD/lista-compras.db ~/.local/share/casa/
systemctl --user start lista-compras.service
```
