## Урок 15. Deployment на Google Cloud Run

### 15.1. Чому Cloud Run

Cloud Run — керована платформа для запуску контейнеризованих застосунків.

Вона підходить для FastAPI та webhook-based сервісів, коли потрібно масштабувати HTTP workloads без керування власними серверами.

Для AI Knowledge Assistant Cloud Run може виконувати роль API та orchestration layer, тоді як Qdrant і stateful storage розміщуються окремо.

### 15.2. Production Architecture

### 15.3. Основні параметри Cloud Run

Concurrency: кількість одночасних запитів на інстанс.

Memory: доступна пам'ять.

CPU: обчислювальні ресурси.

Request timeout: максимальна тривалість HTTP-запиту.

Minimum instances: кількість інстансів, які залишаються доступними.

Maximum instances: обмеження масштабування.

Для AI API потрібно обирати ці параметри на основі навантажувального тестування, а не випадкових значень.

### 15.4. Deployment

Приклад:

```

gcloud run deploy ai-knowledge-assistant \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/IMAGE:TAG \
  --region REGION \
  --service-account SERVICE_ACCOUNT_EMAIL \
  --memory 2Gi \
  --cpu 2 \
  --concurrency 10 \
  --timeout 300

```

Заміни placeholders на свої значення.

Ця команда припускає, що контейнерний образ уже створено й завантажено до Artifact Registry, а сервісний акаунт має необхідні дозволи.

Доступ до сервісу налаштовуй відповідно до сценарію. Не роби адміністративні endpoint-и публічними.

### 15.5. Secrets та IAM

Не передавай API keys через Docker image або GitHub repository.

Використовуй Secret Manager та service account із мінімально необхідними правами.

Для CI/CD краще використовувати короткоживучу федеративну автентифікацію, а не довгоживучі JSON service account keys.

