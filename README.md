# Métodos Numéricos: TP1

## Grupo

* Gianfranco Bogetti
  - LU: 693/15
  - e-mail: gianbogetti7@hotmail.com
* Matias Nicolas Strobl Leimeter
  - LU: 645/18
  - e-mail: matias.strobl@gmail.com
* Florencia Fabian
  - LU: 230/19
  - e-mail: flor.fabian@hotmail.com
* Ignacio Losiggio
  - LU: 751/17
  - e-mail: iglosiggio@dc.uba.ar

## Informe

El `.tex` está disponible en la carpeta informe. El `.pdf` tiene el nombre
`informe.pdf` y está en la carpeta raíz del proyecto entregado.

El informe requiere del software `graphviz` para la construcción de algunas
ilustraciones.

Finalmente, el informe provee un `Makefile` que utiliza `latexmk` y se encarga
de generar los gráficos de ser necesario. Para esto requiere las dependencias
propias de la carpeta de experimentación que se detallan más adelante.

## Implementación

La implementación fué realizada en C++, los tests de la cátedra se pueden
correr moviéndose a la carpeta `src` y ejecutando `python3 metnum.py test`.

La implementación tiene la parametrización original dada por la cátedra con la
pequeña adición de que el tipo 2 es el método *Justice* y el tipo 3 *Elo*.

## Experimentación

La experimentación requiere de alrededor de 3GB de espacio de disco. El
`Makefile` disponible en `experimentacion` documenta todas las relaciones entre
los archivos en cuestión y tiene cómo _target_ por defecto la replicación de
los gráficos usados en el informe.

La carpeta de experimentación posee los siguientes scripts y programas que
pueden ser de utilidad:

* `compare_rankings.py`: Dados dos rankings los compara usando el coeficiente
  de correlación para rankings de Spearman. También puede usarse con el
  parámetro `--compare-all` para comparar todos los rankings generados contra
  los _"reales"_ usados durante la creación de los torneos.
* `concat_inputs.py`: Dada una lista de torneos construye uno que suma los
  partidos de todos estos.
* `optimize_wins`: Dado un id de equipo y la ruta a un archivo de torneo
  intenta maximizar el ranking para cada cantidad de victorias fijas posibles
  de ese equipo. Ésto lo hace por medio de random sampling.

La ejecución del target por defecto (**all**) requiere de seaborn y pandas, dos
bibliotecas de python que no forman parte de la distribución estándar. Éstas
están documentadas en `experimentacion/requirements.txt`.

El programa `optimize_wins` es muy lento, por lo que se proveen los resultados
de una corrida realizada por nosotros (el `Makefile` utiliza estos por
defecto).
