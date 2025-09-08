
### `docs/api.md`:

```markdown
# 🔌 API Документация

## 🌐 Gradio Web API

Gradio автоматически генерирует API-схему.

После запуска открой: `http://localhost:7860/docs` — получишь Swagger UI.

### Пример вызова (Python)

```python
import requests

response = requests.post(
    "http://localhost:7860/api/predict",
    json={
        "data": [
            "Как работает фотосинтез",
            "научный",
            True
        ]
    }
)
print(response.json())
