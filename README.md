# Extracción de Datos con Selenium

Esta aplicación permite extraer datos de una página web específica, seleccionando diferentes opciones de un desplegable y guardando los resultados en un archivo de texto. Utiliza Selenium para automatizar la navegación web, BeautifulSoup para analizar el contenido HTML y Tinker para la sencilla interfaz gráfica

## Uso

1. **Clonar el repositorio o descargar el script**:
    ```sh
    git clone <URL_DE_TU_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```

2. **Interfaz de usuario**:
    - Introduce la URL de la página web en el campo de entrada.
    - Haz clic en el botón "Generar" para iniciar el proceso de extracción de datos.

## Estructura del Código

- `extraer_datos_por_marca(url_inicial, clase_objetivo)`: Función principal que realiza la extracción de datos.
- `generar_datos()`: Función que obtiene la URL ingresada en la interfaz y llama a `extraer_datos_por_marca`.
- `Tkinter` GUI: Proporciona una interfaz simple para ingresar la URL y ejecutar la extracción.

## Detalles Técnicos

- **Automatización de Navegación**: Utiliza Selenium WebDriver para navegar a la página web y seleccionar opciones del desplegable.
- **Interacción con la Página**: Si hay un solo elemento en el desplegable, se hace clic adicional en el campo de búsqueda para cargar los datos dinámicamente.
- **Manejo de Cookies**: Intenta aceptar automáticamente las cookies si aparece el botón correspondiente.
- **Extracción de Datos**: Analiza el contenido de la página con BeautifulSoup para encontrar y extraer los datos deseados.
- **Archivo de Salida**: Los datos extraídos se guardan en un archivo de texto cuyo nombre se basa en el contenido del `<h1>` de la página.

## Estructura del Proyecto

- `main.py`: Contiene la lógica principal de la aplicación y la interfaz gráfica de usuario.

## Ejemplo de Uso

Al ejecutar la aplicación y proporcionar la URL, el script seleccionará cada opción del desplegable de marcas, hará clic en el campo de búsqueda si es necesario, y guardará los datos extraídos en un archivo de texto.

```python
# Ejemplo de uso de la función principal
extraer_datos_por_marca("https://ejemplo.com", "clase-objetivo")

