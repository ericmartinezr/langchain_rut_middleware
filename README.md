# LangChain RUT middleware

Middleware simple para tratar los RUTs Chilenos como PII.

Solo está configurado para detectar los siguientes tipos de RUTs:

1. 12345678-9
2. 12.345.678-9
3. 12.345.67-8

## Forma de uso

```python
create_agent(
    model="gpt-oss:20b",
    middleware=[
        RUTMiddleware(
            strategy="redact",
            apply_to_input=True,
            apply_to_output=True,
            apply_to_tool_results=True
        )
    ]
)
```

---

Preferí extender `PIIMiddleware` a pesar de que esto también se puede hacer como `Composition`, ya que podría sobreescribir los hooks en un futuro de querer hacerlo. En resumen da más flexibilidad.

Ejemplo

```python
def rut_detector(content: str) -> list[PIIMatch]:
    # ...
    return [PIIMatch(type="rut", value=match.group(), start=match.start(), end=match.end())]

PIIMiddleware(
    "rut",
    strategy="redact",
    detector=rut_detector,
    apply_to_input=True,
    apply_to_output=True,
    apply_to_tool_results=True
)
```

## Testing

```bash
pytest tests
```

---

## Nota

Tuve que normalizar el contenido ya que las pruebas las realicé con documentos pasados por `PyPDFLoader` y guardados en `PostgreSQL (PGVector)`. En algún punto de ese proceso los guiones quedaban distintos a los comunes (ver docstring the `_normalize_content`) lo que rompía los regex que uso.
