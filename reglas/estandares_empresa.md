# Estándares de Código y Buenas Prácticas de la Empresa

1. **Nomenclatura (`snake_case`):** Todas las funciones, métodos y variables deben nombrarse en `snake_case` (minúsculas separadas por guiones bajos). Las clases deben usar `PascalCase`.
2. **Prohibición de `print()`:** No se permite dejar sentencias `print()` en el código. Para registrar información o depurar, debe utilizarse siempre la librería estándar `logging`.
3. **Manejo específico de excepciones:** Está prohibido capturar excepciones genéricas (`except:` o `except Exception:`). Debe capturarse el tipo de error específico (por ejemplo, `ValueError`, `KeyError`, `FileNotFoundError`).
4. **Documentación (*Docstrings*):** Toda función o método público debe incluir un *docstring* explicando brevemente qué hace, qué parámetros recibe y qué valor devuelve.
5. **Constantes:** Los valores fijos o configuraciones globales deben definirse en `MAYUSCULAS_CON_GUIONES_BAJOS` al inicio del archivo.