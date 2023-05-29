# Maquina de Estados para un Wall-E recolector de objetos reciclables que se mueve en un plano de 5x5 

### Integrantes:

- **Samuel Alejandro Chaparro Ortiz** - [7004072]

Se diseñó una maquina de estados de un robot Wall-E que es capaz de recolectar objetos reciclables en un plano de 5x5. El robot se mueve en el plano de manera aleatoria y cuando encuentra un objeto reciclable de una categoria (Lata, Botellas Plásticas) lo recoge y lo lleva a la base de reciclaje. El robot sale del plano cuando se encuentra en la posición (0,0) "home" y comienza a analizar el plano de manera aleatoria con una cámara al lado de su garra hasta que encuentre el objeto de la categoria a su interés. Cuando el robot encuentra el objeto, intenta recogerlo, si lo tropieza, intentará acomodarlo para recogerlo o sino después de un tiempo, perderá el interés e irá a recoger otro objeto de la misma categoria. Si lo recoge, lo llevará a la base de reciclaje, si se encuentra con un obstáculo, lo intentará dejar en la posición anterior en la que se encontraba el robot. El robot puede recoger varios objetos de la misma categoria y los lleva a la base de reciclaje. Cuando se haya verificado que todos los objetos de una categoria hayan sido recogidos, cambiará de categoria y comenzará a recoger los objetos de la misma. Cuando todos los objetos del plano hayan sido recogido, el robot se dirige a la posición (0,0) "home" y termina ejecución, o comienza a analizar otro plano en busca de más objetos o se dirige a un puesto de recarga de bateria y termina la ejecución.

#### Consideraciones.

- El robot se desplaza hacia adelante o hacia atrás.
- El robot puede rotar 0, 90, 180, 270 grados.
- Si existe un fallo mecánico o eléctrico, el robot entra en estado de emergencia y termina la ejecución.
- El robot tiene una cámara al lado de su garra que le permite identificar los objetos reciclables. Si esta cámara falla, los objetos del entorno desaparecerán. 
- El robot tiene una batería que se descarga con el tiempo. Si la batería se descarga, el robot irá a un puesto de recarga, de lo contrario el robot entra en estado de emergencia y termina la ejecución.
- El robot tiene una base de reciclaje en la posición (0,0) "home" donde deja los objetos reciclables que ha recogido.




## Creación de un repositorio en GitHub

Para cargar un proyecto local a su repositorio de GitHub, puede seguir estos pasos:

Cree un nuevo repositorio en GitHub:

Vaya al sitio web de GitHub e inicie sesión en su cuenta.
Haga clic en el botón "+" en la esquina superior derecha de la página y seleccione "Nuevo repositorio".
Asigne un nombre a su repositorio y elija cualquier otra configuración que desee, como hacerlo público o privado.
Haga clic en el botón "Crear repositorio".
Inicializa tu proyecto local como un repositorio de Git:

Abra una terminal o símbolo del sistema.
Navegue al directorio raíz de su proyecto usando el comando `cd`

Ejecute el comando git init para inicializar un nuevo repositorio de Git.
Agregue sus archivos de proyecto al repositorio de Git:

Ejecute el comando `git add.` para preparar todos los archivos en el directorio de su proyecto para la confirmación. Si solo desea agregar archivos específicos, puede especificar sus rutas en lugar de usar el punto (.) .


Ejecute el comando `git commit -m "Initial commit"` para confirmar los cambios. Reemplace "Initial commit" con un mensaje de confirmación apropiado.
Conecta tu repositorio local al repositorio remoto de GitHub:

En la página de su repositorio de GitHub, copie la URL del repositorio. Debería verse como https://github.com/username/repository.git.
En su terminal o símbolo del sistema, ejecute el comando `git remote add origin <repository-url>`, reemplazando `<repository-url>` con la URL que copió.
Sube tu repositorio local a GitHub:

Ejecute el comando git `push -u origin master` para enviar su repositorio local a la rama "master" del repositorio remoto en GitHub. Si está trabajando con una rama diferente, reemplace "master" con el nombre de la rama.
Después de ejecutar estos pasos, su proyecto local se cargará en su repositorio de GitHub. Puede actualizar la página del repositorio de GitHub para ver los archivos y los cambios reflejados allí.

## Requerimientos para el uso de la maquina de estados

- Python 3.8.5

- Crear  el environment en VScode de esta manera:

Enviar el comando para crear el environment


```shell script
python -m venv .env
```
Si no funciona el anterior, pruebe con el siguiente
```shell script
py -m venv .env
```
 Despues de enviado le debe aparecer una ventana preguntando si quiere vincular este environment al workspace actual, selecciones Si.

Al crear el environment se crea una carpeta .env dentro del workspace con algunos Scripts, entre ellos se crea un link al ejecutable de python del sistema operativo: ####\Scripts\python.exe. En esa carpeta tambien se guardarán las bibliotecas (libraries) necesarias para el proyecto.

- Activar el environment para instalar los paquetes

Envie primero este comando para habilitar permisos, toda la linea es el comando

```shell script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Comando para activar el environment:

```shell script
.env\Scripts\activate
```
Luego de activarlo deberá aparecer al lado izquierdo entre parentesis el nombre del environment activo. 

```shell script
(.env) C:\Users\username\
```

Si se cierra este terminal y se abre otro nuevo, es necesario activar el environment otra vez:

```shell script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.env\Scripts\activate
```

- Instalar los paquetes o módulos en el environment 

```shell script
python -m pip install --upgrade pip
```
Si en este punto le aparece el siguiente WARNING o un error, la instalación requiere unas configuraciones adicionales. En caso contrario salte al siguiente comando.

```shell script
WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
```
Probablemente su environment tomó una preinstalación del interpretador de Python de Anaconda o de alguna otra preninstalación, y su environment no encuentra el camino o PATH a algunas "libraries" necesarias.

La solución es agregar el PATH C:\\...\anaconda3\Library\bin a las variables de entorno del sistema operativo. Note que los ... depende de cada computador, normalmente la carpeta que necesitamos se encuentra en este camino o PATH C:\Users\username\anaconda3\Library\bin pero deberá verificarlo en su computador. 

Pasos:

1. Cierre VScode
2. Agregue este PATH a través de "Editar la variables de entorno del sistema" (busqueda de windows). No olvide al final darle aceptar a todas la ventanas. https://parzibyte.me/blog/2017/12/21/agregar-directorio-path-windows/
3. Abra de nuevo VScode
4. Habilite los permisos para activar el environment desde un terminal
5. Active el environment
6. Verifique el cambio, enviando el comando de instalación anterior: python -m pip install --upgrade pip


Instalar:


```shell script
pip install -r requirements.txt
```
