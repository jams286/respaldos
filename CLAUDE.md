# respaldos (infra)

Respaldo diario de las BD SQLite de las tools de la casa.

- `respaldar.py`: toma todo `~/.local/share/casa/*.db` (cualquier tool nueva que guarde su BD ahí entra sola) y lo copia con `sqlite3.Connection.backup` (consistente aunque el servicio esté escribiendo) a `/media/datos/Backups/casa/AAAA-MM-DD/`, vía un `.tmp` que luego se renombra. Conserva las últimas 30 carpetas con nombre de fecha y nunca borra otra cosa.
- Si `/media/datos/Backups` no existe (disco no montado), termina con error en vez de escribir en otro lado.
- `servicio/respaldo-casa.service` (oneshot) + `respaldo-casa.timer` (3:30 a. m., `Persistent=true`), instalados como unidades de usuario.
- Jams autorizó escribir **solo** en `/media/datos/Backups/casa/`; el resto de `/media/datos` sigue sin tocarse.
