# Proyecto de titulación

* Andrés Antonio Alcaíno Castro
* Universidad de Santiago de Chile
* Departamento de Ingeniería Informática
* 1-2021

## Título

Búsqueda local iterada para optimizar tiempo en órdenes de construcción en Starcraft 2: experiencia Protoss.

## Descripción

Programa que permite encontrar órdenes de construcción en el juego Starcraft 2 para la raza Protoss, mediante la implementación de grafos y la metaheurística de búsqueda local iterada.

## Requisitos

  * Python 3.9.5.
  * De preferencia utilizar Sistema Operativo basado en linux.
 
## Instalaciones necesarias (Linux)

  * Pip:

```sh
sudo apt install python3-pip
```
 
  * Python Igraph:

```sh
pip install python-igraph
```

  * XlsxWriter:

```sh
pip install XlsxWriter
```

  * R:
```sh
https://cran.r-project.org/
```

## Ejecución

```sh
cd ProyectoTitulacion/main/
```
```sh
python3 main.py
```

## Ejecución de irace

```sh
cd ProyectoTitulacion/irace
```
```sh
R -f irace-run.R
```
## Salida

Al ejecutar el algoritmo de búsqueda local iterada con la opción 7 del menú se generarán
4 archivos .xlsx:

1) BuildOrder_Solution: Orden de construcción.
2) genScores: Puntajes obtenidos por generación en el algoritmo greedy.
3) EntitiesBuilt: Entidades (Unidades/Edificios/Tecnologías) construidas.
4) constructionQueue: Cola de construcción al momento de detener el orden de construcción.