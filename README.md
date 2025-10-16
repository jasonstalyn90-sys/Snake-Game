# Culebrita
📋 Datos del grupo

Integrante: Jason Stalyn Oña Ayala
Carrera: Ingeniería en Sistemas
Asignatura: Logica de Programación
Docente: LILIAN MARLENE AMAN RAMOS
Fecha: 02 Octubre 2025

Objetivo del programa

Desarrollar un videojuego clásico de “Culebrita” utilizando la biblioteca Pygame en Python, con el fin de aplicar los conocimientos de estructuras de control, listas, manejo de eventos, funciones y animaciones.

El objetivo del juego es guiar a la serpiente para que coma la comida y crezca sin chocar contra las paredes ni consigo misma.
Cada vez que la serpiente come, el jugador obtiene puntos y la velocidad del juego aumenta progresivamente, incrementando la dificultad.

Principales funcionalidades del código

Movimiento de la serpiente
La serpiente se desplaza en una cuadrícula controlada por las flechas del teclado.
El jugador puede moverse hacia arriba, abajo, izquierda o derecha, pero no puede girar 180° directamente.

Generación aleatoria de comida
La comida aparece en una celda aleatoria que no esté ocupada por la serpiente.
Al comer, la serpiente crece y se aumenta el puntaje.

Sistema de puntaje y récord
Cada manzana otorga 10 puntos.
Se muestra el puntaje actual y el mejor puntaje alcanzado durante la sesión.

Aumento progresivo de velocidad
Cada 50 puntos, la velocidad del juego incrementa ligeramente, haciendo que el reto sea mayor.

Detección de colisiones
Si la serpiente choca con los bordes o con su propio cuerpo, el juego termina y aparece el mensaje “¡Game Over!”.

Reinicio del juego
Al presionar la tecla R, se reinicia la partida sin necesidad de cerrar el programa.
Con Esc, el jugador puede salir del juego.

Interfaz visual sencilla
Se utiliza Pygame para graficar la cuadrícula, la serpiente y la comida.
Colores definidos para mejorar la visibilidad (verde para la serpiente, rojo para la comida, gris para la cuadrícula).

Mensajes en pantalla y fuente personalizada

