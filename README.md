# 📈 Análisis del Sistema COMPAS en Justicia Penal

Este repositorio presenta un estudio de caso basado en COMPAS, un sistema automatizado de evaluación de riesgo de reincidencia utilizado en el sistema judicial de los Estados Unidos. El análisis explora la validez, exactitud y equidad del sistema utilizando un conjunto de datos reales de más de 11,000 casos entre 2013 y 2014.

## 🚀 Objetivo del Proyecto

Evaluar el rendimiento y la imparcialidad del sistema COMPAS desde una perspectiva de ciencia de datos, considerando:
- Precisión predictiva de reincidencia y crímenes violentos.
- Disparidades por raza y género.
- Problemas éticos y legales relacionados con su uso.

## 📁 Dataset

El dataset proviene de una investigación independiente llevada a cabo por ProPublica e incluye variables como:
- `decile_score`: nivel de riesgo general asignado (1-10)
- `v_decile_score`: nivel de riesgo de crimen violento
- `is_recid`: indicador de reincidencia general
- `is_violent_recid`: reincidencia en delitos violentos

## ⚙️ Metodología

### 1. Exploración de Datos
- Evaluación de la completitud, validez y puntualidad de los datos.
- Limpieza y transformaciones necesarias para el análisis posterior.

### 2. Evaluación de Exactitud
- Se propone una métrica de validación para `is_recid` e `is_violent_recid`.
- Se construye una matriz de confusión considerando como positivo `decile_score >= 7`.

### 3. Análisis de Equidad
- Comparación gráfica de scores por raza y por género.
- Discusión sobre posibles sesgos algorítmicos en la asignación de puntuaciones.

### 4. Rendimiento Comparativo
- Comparación de la capacidad predictiva del sistema para crímenes generales vs. crímenes violentos.

## 🌐 Herramientas Utilizadas

- Python 3.x
- `pandas`, `matplotlib`, `seaborn`, `sklearn`

```bash
pip install pandas matplotlib seaborn scikit-learn
```

## 📊 Resultados Clave

- El sistema presenta diferencias en las puntuaciones asignadas según el género y la raza.
- Se detectan posibles sesgos, especialmente hacia personas afroamericanas.
- La predicción de crímenes violentos es menos precisa que la de reincidencia general.

## 📚 Conclusiones

COMPAS puede ser una herramienta útil para apoyar decisiones judiciales, pero debe usarse con cautela debido a:
- Potencial de generar decisiones sesgadas.
- Falta de transparencia del algoritmo propietario.
- Necesidad de una supervisión humana y ética constante.

## 📅 Dataset original
- [ProPublica COMPAS dataset](https://github.com/propublica/compas-analysis)

## 🔗 Referencias
- ProPublica (2016). Machine Bias.
- Northpointe, Inc. COMPAS Technical Manual.
- "Statistical Modeling: The Two Cultures" - Leo Breiman

---
✉️ Para dudas o colaboraciones, contactar a **Julián Vázquez Sampedro**.

