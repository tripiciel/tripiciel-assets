# Receta de edición de los reels de Tripiciel (v2.1, desde el domingo 22/11)

Reemplaza la receta anterior (estilo «4 errores al editar», tarjetas planas). Motivo: los reels con ese estilo se
estancaron en menos de 130 vistas y entre el 50 y el 90 % de la gente los salteó en los primeros 3 s. Los reels de
referencia que sí funcionan (deepzerr, just_charlyy, diegocastro.sistemas) comparten lo que sigue.

## 1. Visual: una metáfora 3D cinematográfica por reel

- UNA sola metáfora física por reel, contada de principio a fin: un dado, un tablero, billetes que caen, un medidor tipo
  velocímetro, tubos con luz, partículas, estanterías, un cuaderno viejo.
- Calidad de render de producto premium: luz direccional + luz de relleno, sombras suaves, profundidad de campo,
  reflejos y materiales (papel, metal, vidrio, cartón). El objeto tiene que verse real.
- Prohibido: plantillas planas, cajas de texto, tarjetas de interfaz como protagonistas, íconos clip-art.
- Herramientas: Three.js renderizado cuadro a cuadro en Chrome sin cabeza (con el motor HyperFrames
  `npx -y hyperframes@0.8.105` o con Playwright), Blender sin cabeza, o Remotion con escenas 3D. Si se muestran
  capturas reales (por ejemplo de Fiadito), van como textura dentro de un celular 3D con reflejo en la pantalla.

## 2. Fondo y color

- Fondo oscuro: negro, verde muy oscuro o violeta muy oscuro, con viñeta y bokeh suave.
- La paleta de Tripiciel solo en los acentos: violeta #5B5BF5, lavanda #A99CFF, lima #C6F432 (cifras), crema
  #F6F2EA. Nunca fondos de color plano.

## 3. Subtítulos

- Chicos: 46 a 52 px de alto de letra a 1080 de ancho. Blancos o gris claro.
- Centrados en el tercio medio-superior del cuadro (aprox. y 560 a 760), de a pocas palabras.
- Palabra por palabra, sincronizados con la voz (tiempos medidos de cada palabra).
- UNA palabra clave por frase en negrita y en un color de acento.
- Prohibido el texto gigante que tape la escena. La escena 3D es la protagonista.

## 4. Movimiento constante

- La cámara siempre se mueve: dolly, órbita lenta, push-in. Nunca un cuadro quieto.
- Cambio de plano o de animación cada 1,5 a 2,5 s.
- Easing suave (entradas y salidas), motion blur en lo que se mueve rápido.

## 5. Sonido

- Voz en off masculina neutra (es-MX-JorgeNeural), ritmo ágil, español neutro (tú), una sola toma, sin cortes en
  las palabras y con aire después de la última.
- Música de fondo tensa o cinemática, baja (unos −22 dB bajo la voz).
- Efecto de sonido en cada transición: whoosh, clic, tic de cronómetro, golpe suave. Ninguno encima de una palabra
  clave.
- Master: −14 LUFS integrados, pico ≤ −1 dBFS, sin compresión dinámica que bombee.

## 6. Duración y estructura (45 a 60 s)

1. **Gancho (0 a 2 s):** una afirmación o pregunta que el dueño de un negocio no puede dejar pasar, con la metáfora
   ya en movimiento desde el cuadro 0.
2. **La idea que el espectador no conocía (2 a 15 s).**
3. **Explicación con la metáfora (15 a 45 s):** cada paso de la idea es algo que le pasa al objeto 3D.
4. **Cierre + CTA de comentario (últimos 5 s).**

## 7. CTA: siempre de comentario con palabra clave

- Nunca «escríbenos por mensaje». Siempre: «Comenta PALABRA y te mandamos…». Ejemplos: «Comenta FIADO y te mandamos
  el link para probarlo 3 días gratis», «Comenta GUÍA y te mandamos gratis la guía…».
- Se dice en la voz y va en el caption. En pantalla, la palabra clave puede aparecer chica, como acento.

## 8. Nada de hablar de nosotros como agencia

- Prohibido en los reels: «somos dos personas», «todo en un solo lugar», «cinco proveedores», «equipo y no
  freelancers» o cualquier frase sobre Tripiciel como agencia. Esos reels tuvieron entre 3 y 50 vistas.
- La marca aparece solo en un logo chico al final (isotipo o logo horizontal) y en el caption.

## 9. Honestidad

- Nunca mencionar IA, inteligencia artificial, ChatGPT, Claude ni herramientas automáticas («bot de respuesta
  automática» como servicio sí). Grep antes de entregar:
  `grep -riE "\bIA\b|inteligencia|artificial|chatgpt|claude|automatiz"` sobre guion, caption y textos en pantalla.
- Sin datos inventados: si se usa una cifra que no es real, en pantalla y en la voz va como «ejemplo».

## 10. Control de calidad antes de entregar

- Exportar fotogramas en 0,5 s, 2 s, 10 s, 30 s y en el último segundo, a tamaño completo, y revisarlos.
- Rehacer todo lo que se vea plano, pixelado, con dientes de sierra, con texto superpuesto o con subtítulos encima
  del objeto principal.
- Portada: el fotograma más llamativo del reel, sin texto gigante.
- Entregables por reel: reel-N.mp4 (1080x1920, H.264, AAC), portada.jpg, guion.md, caption.txt (gancho + 2 o 3
  líneas + CTA de comentario + 5 hashtags).

## 11. Mejoras v2.1 (aprendido en el día 8)

- **Ningún plano con el fondo vacío:** siempre hay un objeto 3D en primer plano o en movimiento.
- **Nada tapa cifras ni textos clave:** revisarlo cuadro por cuadro en los planos con números o carteles.
- **Luz neutra o cálida sobre papel y objetos claros:** que nunca se vean rosados ni violetas (la luz violeta va
  solo como borde).
- **Calidad mínima** = la segunda pasada del día 8: vidrio con transmisión, etiquetas impresas, madera con vetas,
  sombras suaves, profundidad de campo, motion blur por submuestras, supermuestreo, peso final < 45 MB.

## 12. Voz y ritmo (v2.1)

- Voz enérgica y dinámica, tono de quien cuenta un secreto con urgencia, velocidad 1,15x a 1,2x, entonación
  variada: sube en las preguntas y remarca la palabra clave.
- **Cero silencios:** recortar toda pausa de más de 0,12 s entre frases y respiraciones (jump cuts de audio, sin
  cortar palabras). La frase siguiente arranca apenas termina la anterior.
- La música no se corta nunca. Un efecto (whoosh, clic, golpe) en cada cambio de plano.
- Cambio de plano o de animación cada 1 a 1,5 s.
- Duración: 35 a 45 s.
- Control: `ffmpeg -i voz.wav -af silencedetect=noise=-35dB:d=0.15 -f null -` sobre la pista de voz debe dar 0
  silencios (fuera del aire final después de la última palabra).

## 13. Contenido de valor (v2.1)

- Cero publicidad en los reels de valor: no se mencionan Fiadito, Tripiciel, apps, servicios, webs ni bots. Solo el
  logo chico de Tripiciel en el último segundo.
- CTA de comentario que no promete nada que haya que enviar: una pregunta que dan ganas de responder («Comenta SÍ si
  te pasó», «Comenta 1, 2 o 3»).
- Hashtags de comercio de barrio, sin marca.
