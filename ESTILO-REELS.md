# Receta de edición de los reels de Tripiciel

Desde el martes 17/11 todos los reels de Tripiciel se editan con el estilo del reel «4 errores al editar» de
@julianmaciel.edicion. La referencia es el video publicado
`Downloads/reels-vie-sab-dom/sabado/2026-11-14-errores-al-editar.mp4` y su proyecto de edición
`video-editor/reels-explicativos/proyectos/2026-11-12-errores-al-editar/`. La adaptación de muestra está en
`semana-02/muestra/reel-muestra/` (proyecto: `video-editor/reels-explicativos/proyectos/tripiciel-muestra/`).

## Cómo se hace

Con el motor `video-editor/reels-explicativos` (dibujo en código, 1080x1920, 60 fps). El reel nuevo parte de una copia
del proyecto `tripiciel-muestra`, que ya trae la paleta, la firma, los subtítulos en violeta y el cierre TRIPI:
1. `guion.json` con las frases (una palabra clave por frase, `hook: true` en las del gancho).
2. `node motor/voz.mjs <proyecto>` (Jorge es-MX, gratis) y se planean los planos con los tiempos de cada palabra.
3. Un plano por frase en `video/planos/` + `sonidos.js` con un efecto en cada cosa que se mueve.
4. `node motor/sonido.mjs <proyecto>` y `node motor/render.mjs <proyecto>`.
5. Música (`musica.py`) mezclada a −21 dB bajo la voz y master final a −14 LUFS, pico −1,2 dBFS.
6. Portada: un cuadro sin subtítulos (`node motor/ver.mjs <proyecto> <segundo> --sin-subtitulos --ancho 1080`).

## El estilo, medido sobre el original

**Duración y ritmo**
- Total 30–36 s (el original dura 36,3 s; la muestra, 32,3 s). 60 fps.
- Una frase = un plano, de 3 a 5 s cada uno. Dentro de cada plano siempre se mueve algo: entra un elemento nuevo en
  cada palabra importante, así que el cambio visual real ocurre cada 0,5–1,5 s, aunque el plano dure 4 s.
- Corte seco entre planos (sin barridos ni zooms de cámara). El fondo es el mismo en todo el video, así que el corte no
  salta: solo cambia lo que está encima.

**Estructura**
1. **Gancho (0–5 s), dos frases.** La primera dice de qué va con el número: «Tres errores que hacen que la gente
   deslice el video de tu negocio.» Se ve desde el fotograma 0 lo que dice (un celular con el feed deslizándose y
   avisos «!» que saltan, uno por error). La segunda interpela: «¿Cuántos estás cometiendo tú?» (lista de casillas
   vacías y un «?» grande que cae en «tú»).
2. **Desarrollo, un plano por punto.** Cada punto abre con «Uno:», «Dos:», «Tres:», arriba aparece un rótulo-píldora
   con su número en un círculo («① Música alta») y debajo, en una sola tarjeta de interfaz, la cosa haciendo lo que
   dice la voz (los faders de música y voz, la línea de tiempo con tajos, el celular con la lupa). La segunda mitad de
   la frase explica por qué (la consecuencia) y la imagen la muestra (el globo de diálogo tapado por notas, el clip
   que salta en zigzag, la cruz sobre el texto ilegible).
3. **Remate.** Vuelve la lista del gancho, ahora con nombre, y se tilda casilla por casilla; cae un sello «PRO».
4. **Razón para contratarnos** (en Tripiciel): «Nosotros dos lo hacemos por ti» con los dos del equipo (M y T) y un
   visto.
5. **Cierre / CTA.** Un chat: la palabra clave se teclea letra a letra, sale como un mensaje grande y llegan tres
   respuestas-píldora, una por cada cosa que nombra la voz. Debajo, la frase completa palabra por palabra.

**Texto**
- Tipografía única: **Figtree** (ExtraBold/Bold/Medium).
- **Subtítulos arriba** (y ≈ 320–400), 74 px, de a 6 palabras o 30 letras como mucho. Cada palabra aparece al decirse
  con un leve desenfoque que se aclara; la que suena en blanco y negrita, las ya dichas en gris (#7b818a). La palabra
  clave de cada frase va dentro de un recuadro con dos tiradores, como una selección de texto.
- Textos dentro de las tarjetas: 48–56 px, peso 800. Rótulos de cada punto: píldora con número en círculo, 56 px.
- Nada de bloques de texto: la tarjeta muestra, el subtítulo dice.

**Elementos gráficos**
- Fondo: azul noche con dos o tres brillos grandes y difusos que se mueven despacio, una grilla de puntitos que sube y
  una textura de manchas muy suave.
- Una sola tarjeta de interfaz por plano: esquinas de 44–60 px, borde fino de color, sombra larga, reflejo arriba.
- Íconos dibujados: celular, play, clips, faders, lupa, casillas, sellos. Entran con un pequeño rebote o deslizamiento
  (0,3 s) y nunca hay más de 3 o 4 elementos en pantalla.

**Sonido**
- Voz en off: es-MX-JorgeNeural a +27 %, una sola toma, sin cortes ni aceleraciones.
- Música: electro alegre original (128 BPM, Am–F–C–G, bombo, palmas, hi-hat, bajo y pluck), a −21 dB bajo la voz,
  con 2 s de salida. Siempre por debajo: la voz se entiende en todo momento.
- Efectos en cada cosa que se mueve (deslizar, clic, golpe, toque, timbre, tecla), entre −16 y −10 dB, nunca en un
  corte y sin huecos de más de 2 s.
- Master: −14 LUFS integrados, pico ≤ −1 dBFS.

## Lo que cambia para Tripiciel (y nada más)

- **Paleta:** fondo azul noche #070A1C; violeta #5B5BF5 (acento, tarjetas, píldoras, recuadro de la palabra clave);
  lavanda #A99CFF (segundo acento); crema #F6F2EA para textos; lima #C6F432 solo para cifras y los números de los
  puntos. Estrellita violeta de 4 puntas arriba a la derecha como firma, en todos los planos.
- **CTA:** «Escribe TRIPI por mensaje y en 24 horas te enviamos una propuesta para tu marca, sin costo.» Se teclea
  TRIPI en el chat y las respuestas son «Propuesta en 24 h», «Para tu marca», «Sin costo».
- **Antes del CTA, una razón para contratarnos,** mostrando que somos dos personas reales (M y T).
- **Nunca** se menciona inteligencia artificial, IA, voz sintética ni herramientas automáticas, ni en la voz, ni en
  pantalla, ni en el caption.
- Español neutro (sin voseo).
- Portada sin texto: un cuadro del gancho sin subtítulos.
