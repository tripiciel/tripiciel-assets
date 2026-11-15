# Reel 1 · Día 4 — Antes y después: subtítulos y ritmo (Chicho Cars, Chevrolet Onix)

Duración: 25,8 s · 1080x1920 · 60 fps · voz es-MX-JorgeNeural +27 %.
Proyecto del motor: `video-editor/reels-explicativos/proyectos/tripiciel-d4-reel1`.

| t (s) | Voz | Pantalla |
|---|---|---|
| 0,0–4,1 | La mayoría miraba este video sin sonido. Y no tenía subtítulos. | Celular con el video CRUDO del Onix (sin sonido), píldora «ANTES»; insignia de mudo en «sonido», CC tachado en «subtítulos». |
| 4,1–9,8 | *(sin voz: suena el audio real del video editado)* «…así arranca, tenemos 106 mil kilómetros, el odómetro…» | El mismo celular con el video EDITADO (subtítulos dinámicos y audio), píldora «DESPUÉS», insignias de sonido y CC con visto. Corte de entrada y salida en pausas del habla. |
| 9,8–12,0 | Uno: subtítulos que se leen. | ① Subtítulos legibles — «TENEMOS / 106 MIL / KILÓMETROS» entran palabra a palabra. |
| 12,0–14,9 | Dos: cortes al ritmo, sin pausas. | ② Cortes al ritmo — línea de tiempo con tajos; los huecos salen. Cifra: **110 s → 94 s**. |
| 14,9–17,3 | Tres: el gancho, al inicio. | ③ Gancho al inicio — anzuelo sobre el 0:00. Cifra: **2,3 s → 0,2 s**. |
| 17,3–20,4 | Resultados a la vista, hechos por nosotros dos. | Miniaturas ANTES / DESPUÉS; entran M y T con un visto. |
| 20,4–25,8 | Escribe TRIPI por mensaje y en 24 horas te enviamos una propuesta para tu marca, sin costo. | Chat: se teclea TRIPI; respuestas «Propuesta en 24 h», «Para tu marca», «Sin costo». |

## Fuentes de las cifras (medidas)
- **110 s → 94 s:** duración de `projects/chicho-onix/raw/p1.MOV` (110,3 s) y de `outputs/chicho-onix.final.mp4` (94,0 s), por ffprobe.
- **2,3 s → 0,2 s:** primera palabra en el crudo a 2,25 s (`transcript/words.json`) y en el editado a 0,15 s (`hf/words.js`).
- «La mayoría» es estimación redactada como tal; no se usa ningún porcentaje.

## Material
- ANTES: `raw/p1.MOV` 40,2–44,3 s (sin audio). DESPUÉS: `outputs/chicho-onix.final.mp4` 34,55–40,0 s (audio hasta 39,78 s, tras «odómetro»).
- Sin patentes en los tramos usados (solo interior y tablero); revisado cuadro a cuadro.

## Filtro
1. Tesis en < 10 s: sin sonido y sin subtítulos se pierde → se ve el antes y el después. ✔
2. El gancho filtra a dueños de negocio con videos sin subtítulos. ✔
3. Caso con nombre y cifra real: Chicho Cars, 110 s → 94 s y 2,3 s → 0,2 s. ✔
