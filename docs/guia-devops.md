# Avance DevOps — Motor Contable Transaccional

**Responsable:** Christopher Brad Del Castillo Montoya (DevOps).  
**Estado:** infraestructura inicial propuesta; la ejecución de CI debe comprobarse en GitHub Actions.

## 1. Base del proyecto y límites

Se respeta el stack aprobado en `docs/stack-tecnologico.md`: Django REST Framework, React + Vite + TypeScript, PostgreSQL y Tailwind CSS. Las versiones de Python/Node/Django y los comandos de arranque siguen **pendientes de acuerdo** con Backend y Frontend. Las carpetas `backend/`, `frontend/` y `tests/` estaban vacías en la rama base. Por ello **no se simula una aplicación funcional**, ni se crean Dockerfiles que aparenten ejecutar servicios inexistentes.

Se sigue `docs/flujo-de-trabajo.md`: rama `chore/devops-infraestructura` derivada de `develop`, PR a `develop`, revisión por otra persona y aprobación antes de integrar. El fork es un entorno de preparación; la integración al repositorio oficial requiere aprobación del equipo.

## 2. Entregables realizados

- `compose.yaml`: servicio PostgreSQL 16 para desarrollo con volumen persistente, puerto ligado a localhost y healthcheck.
- `.env.example`: variables documentadas con credenciales **solo de demostración local**.
- `.gitignore` y `.dockerignore`: exclusión de secretos, dependencias y archivos temporales.
- `.github/workflows/ci.yml`: validación de Compose, pruebas de infraestructura y prueba real de arranque/consulta PostgreSQL en GitHub Actions.
- `tests/test_devops_config.py`: pruebas de estructura, configuración y protección básica de secretos.
- Esta guía y el guion de demostración.

## 3. Ejecución local (Linux / Docker Desktop)

Requisitos: Git y Docker con Compose v2. En la raíz del proyecto:

```bash
cp .env.example .env
# Cambiar POSTGRES_PASSWORD en .env para uso local.
docker compose --env-file .env config --quiet
docker compose --env-file .env up -d --wait db
docker compose --env-file .env ps
docker compose --env-file .env exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;"'
python3 -m unittest discover -s tests -p 'test_devops_*.py' -v
docker compose --env-file .env down
```

Para eliminar también datos locales de la base, usar `docker compose down -v` **solo cuando se desee borrar el volumen**.

## 4. Validación remota

En GitHub, abrir **Actions → DevOps CI - infraestructura** y seleccionar la ejecución del push o **Run workflow** en la rama de trabajo. Comprobar los jobs:

1. **Validar configuracion y estructura**: Compose válido, pruebas Python aprobadas, `.env` no versionado.
2. **PostgreSQL - prueba de arranque**: contenedor saludable y `SELECT 1` correcto.

**No declarar CI aprobado sin ver una ejecución verde**. Un fallo de GitHub Actions requiere inspeccionar sus logs. En forks, los workflows pueden requerir habilitación manual en la pestaña Actions.

## 5. Integración futura y responsables

| Dependencia | Responsable | Acción pendiente |
|---|---|---|
| Backend DRF | Backend | Publicar `requirements.txt` o `pyproject.toml`, comando de inicio, variables y migraciones. |
| Frontend React/Vite | Frontend | Publicar `package.json`, scripts, puerto y URL de API. |
| Contratos y BD | Arquitectura + Backend | Confirmar modelo, migraciones y convenciones de conexión. |
| QA | QA | Publicar pruebas de negocio y comando de ejecución para incorporarlo al CI. |
| Jobs recurrentes (HU-07) | Backend + DevOps | Definir mecanismo (scheduler/worker), idempotencia, monitoreo y reintentos antes de automatizar. |
| Equipo | Scrum Master / revisores | Revisar PR y decidir integración al repositorio oficial. |

**Pendiente de esta fase:** contenedores de aplicación, migraciones reales, cobertura QA, CD/despliegue, secrets de producción, backups y monitorización. No se afirma que estén terminados.

## 6. Evidencias para el Meet

1. Mostrar el árbol de archivos de la rama `chore/devops-infraestructura`.
2. Abrir `compose.yaml` y explicar persistencia, healthcheck y acceso localhost.
3. Abrir el workflow CI y describir sus dos jobs.
4. Mostrar **Actions** con el resultado real (verde o fallo con diagnóstico).
5. Mostrar el PR hacia `develop` y explicar los acuerdos pendientes.

**Guion (45–60 s):** “Mi avance DevOps se centra en preparar una infraestructura reproducible para el Motor Contable Transaccional, respetando el stack aprobado. Configuré PostgreSQL con Docker Compose, persistencia y comprobación de salud. Además, preparé un pipeline en GitHub Actions que valida la configuración y ejecuta una consulta real a la base de datos, junto con pruebas de infraestructura. La integración de Backend, Frontend y pruebas contables se incorporará cuando sus responsables publiquen código y definan sus comandos. El trabajo se mantiene en una rama independiente para revisión antes de fusionarse.”
