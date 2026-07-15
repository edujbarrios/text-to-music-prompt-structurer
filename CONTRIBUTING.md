# Contributing to Text-to-Music Prompt Structurer

Thanks for your interest in contributing to the Text-to-Music Prompt Structurer project!

**Developed by [Eduardo J. Barrios](https://edujbarrios.com)**

## Cómo Contribuir

### Reportar Bugs
1. Verifica que el bug no haya sido reportado antes
2. Crea un issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Versión de Python que usas

### Sugerir Nuevas Features
1. Abre un issue describiendo:
   - La funcionalidad que propones
   - Por qué sería útil
   - Ejemplo de uso

### Agregar Vocabulario
La forma más fácil de contribuir es expandir los vocabularios JSON:

1. Fork el repositorio
2. Edita los archivos en `text_to_music_prompt_structurer/vocab/`:
   ```json
   // text_to_music_prompt_structurer/vocab/genres.json
   {
     "tu-nuevo-genero": { "genre": "Tu Nuevo Género", "subgenre": null }
   }
   ```
3. Crea un Pull Request

### Agregar Nuevos Detectores

Si quieres agregar una nueva categoría de detección:

1. Crea el archivo JSON de vocabulario:
   ```json
   // text_to_music_prompt_structurer/vocab/tu_categoria.json
   {
     "keyword1": "Valor 1",
     "keyword2": "Valor 2"
   }
   ```

2. Crea el detector (opcional si usas `KeywordListDetector`):
   ```python
   class TuDetector(Detector):
       def detect(self, text, prompt):
           # Tu lógica aquí
           pass
   ```

3. Regístralo en `text_to_music_prompt_structurer/engine.py` → `MusicPromptEngine.__init__`:
   ```python
   self.registry.register(KeywordListDetector(
       loader.load("tu_categoria"), 
       "tu_atributo"
   ))
   ```

## Estándares de Código

- Python 3.10+
- Sigue PEP 8
- Usa type hints cuando sea posible
- Documenta funciones complejas
- Mantén la separación de concerns

## Estructura de Commits

```
tipo: descripción breve

Descripción más detallada si es necesario.
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `vocab`: Cambios en vocabularios JSON
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests

## Proceso de Pull Request

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nombre-feature`
3. Commit tus cambios: `git commit -m 'feat: agregar nueva categoría'`
4. Push a tu fork: `git push origin feature/nombre-feature`
5. Abre un Pull Request

## Extender Vocabularios

### Géneros Musicales
Agrega a `text_to_music_prompt_structurer/vocab/genres.json`:
```json
{
  "key-name": { 
    "genre": "Nombre del Género", 
    "subgenre": "Subgénero (opcional)" 
  }
}
```

### Moods
Agrega a `text_to_music_prompt_structurer/vocab/moods.json`:
```json
{
  "keyword": "Mood Descriptor"
}
```

### Instrumentos
Agrega a `text_to_music_prompt_structurer/vocab/instruments.json`:
```json
{
  "search-term": "Display Name"
}
```

## Testing

Antes de hacer PR, prueba tu código:

```bash
# Test básico
python structurer.py "tu texto de prueba"

# Test con tu nueva funcionalidad
python structurer.py "texto que active tu nueva feature"
```

## Preguntas

Si tienes dudas, abre un issue con la etiqueta `question`.

## Código de Conducta

- Sé respetuoso y constructivo
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Ayuda a otros contributors

---

¡Gracias por hacer mejor este proyecto! 🚀
