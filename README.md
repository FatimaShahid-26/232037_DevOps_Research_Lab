# Pakistan Forest ML — Easy Lab Starter

A simplified, beginner-friendly version of the original lab starter. It uses the **same real Phase 4 CSVs** and still implements Decision Tree, Random Forest, KNN, XGBoost, Flask, Angular and GitHub CI/CD.

## Do these commands in order (Windows PowerShell in project root)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python backend\train_models.py
python backend\make_payload.py
python backend\test_pipeline.py
python -m pytest -q backend\tests
python backend\app.py
```

Leave Flask running in Terminal 1. In Terminal 2, create Angular:

```powershell
npm install -g @angular/cli@22
ng new frontend --routing --style=css --skip-git --defaults
```

Copy `frontend_files/app.ts`, `app.html`, `app.css`, `feature-schema.ts`, and `prediction.service.ts` to `frontend/src/app/`. Copy `frontend_files/proxy.conf.json` to `frontend/`. In `frontend/src/app/app.config.ts`, import `provideHttpClient` from `@angular/common/http` and add `provideHttpClient()` to `providers`.

```powershell
cd frontend
npm run build
ng serve --open --proxy-config proxy.conf.json
```

Open http://localhost:4200 to test predictions. Read `EASY_EXPLANATION.md` for what each file does and GitHub steps. GitHub Pages hosts **only the static Angular interface**; Flask is local.

**Research limitation:** the three target classes are JRC forest-origin/management labels, not Pakistan ecological forest formations. Spatial-test accuracy is materially lower than random validation; do not present the prototype as operationally validated.
