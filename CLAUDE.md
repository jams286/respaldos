# respaldos (infra)

Tracker: respaldos

Respaldo diario de las BD SQLite de las tools de la casa.

- `respaldar.py`: toma todo `~/.local/share/casa/*.db` y `~/.local/share/personal/*.db` (cualquier tool nueva que guarde su BD ahí entra sola; las personales van a la subcarpeta `personal/` del día) y lo copia con `sqlite3.Connection.backup` (consistente aunque el servicio esté escribiendo) a `/media/datos/Backups/casa/AAAA-MM-DD/`, vía un `.tmp` que luego se renombra. Conserva las últimas 30 carpetas con nombre de fecha y nunca borra otra cosa.
- ROMs de casa/gameflix (`~/.local/share/casa/gameflix-roms/`, archivos `<sha1>.<ext>` que no cambian): van a una sola carpeta espejo `/media/datos/Backups/casa/gameflix-roms/`, no a cada día; solo se agregan las nuevas y nunca se borra ahí (si se borra un juego en Gameflix, su ROM queda en el respaldo). La BD `gameflix.db` (perfiles, carátulas, saves y estados) entra como cualquier otra.
- También copia `~/.local/share/personal/inicio-iconos/propios/` (íconos subidos a mano en personal/inicio) a `personal/inicio-iconos-propios/`; los automáticos no hacen falta.
- Ojo: `personal/inicio.db` lleva en su tabla `config` la contraseña de app de Pi-hole y el permiso de Spotify sin cifrar. `/media/datos` está en Samba (`JamsData`) solo para el usuario jams.
- Si `/media/datos/Backups` no existe (disco no montado), termina con error en vez de escribir en otro lado.
- `servicio/respaldo-casa.service` (oneshot) + `respaldo-casa.timer` (3:30 a. m., `Persistent=true`), instalados como unidades de usuario.
- Jams autorizó escribir **solo** en `/media/datos/Backups/casa/`; el resto de `/media/datos` sigue sin tocarse.
