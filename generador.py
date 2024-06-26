import os
import subprocess
from sys import platform

def create_project(name_project):
  # Obtener la ruta del directorio actual
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # Cambiar al directorio actual
  os.chdir(current_dir)

  # Si en el nombre del proyecto hay espacios, reemplazarlos por guiones
  name_project = name_project.replace(" ", "-")

  # Si el nombre del proyecto es solo un punto (.), un guion (-) o una barra (/), asignarle el nombre del directorio actual
  if name_project == "." or name_project == "-" or name_project == "/":
    name_project = os.path.basename(current_dir) 

  #revisar si el nombre del proyecto es igual al de la carpeta actual
  # Si no es igual, crear una carpeta con el nombre del proyecto y moverse a ella
  # Si es igual, no hacer nada
  if name_project != os.path.basename(current_dir):
    # Crear carpeta con el nombre del proyecto
    try:
      os.mkdir(name_project)
    except FileExistsError:
      print(f"La carpeta {name_project} ya existe")
    # Moverse a la carpeta creada
    os.chdir(name_project)  

  # Crear el proyecto
  comando_creacion = f"dotnet new sln -n {name_project}"
  # Creacion webapi
  comando_webapi = f"dotnet new webapi -n {name_project}.WebApi"
  comando_webapi_sln = f"dotnet sln {name_project}.sln add {name_project}.WebApi/{name_project}.WebApi.csproj"
  # Creacion de la capa domain
  comando_domain = f"dotnet new classlib -n {name_project}.Domain"
  comando_domain_sln = f"dotnet sln {name_project}.sln add {name_project}.Domain/{name_project}.Domain.csproj"
  # Creacion de la capa application
  comando_application = f"dotnet new classlib -n {name_project}.Application"
  comando_application_sln = f"dotnet sln {name_project}.sln add {name_project}.Application/{name_project}.Application.csproj"
  # Creacion de la capa Persistence
  comando_persistence = f"dotnet new classlib -n {name_project}.Persistence"
  comando_persistence_sln = f"dotnet sln {name_project}.sln add {name_project}.Persistence/{name_project}.Persistence.csproj"
  # Referencias entre proyectos
  comando_reference_domain_to_application = f"dotnet add {name_project}.Application/{name_project}.Application.csproj reference {name_project}.Domain/{name_project}.Domain.csproj"
  comando_reference_persistence_to_application = f"dotnet add {name_project}.Application/{name_project}.Application.csproj reference {name_project}.Persistence/{name_project}.Persistence.csproj"
  comando_reference_domain_to_persistence = f"dotnet add {name_project}.Persistence/{name_project}.Persistence.csproj reference {name_project}.Domain/{name_project}.Domain.csproj"
  comando_reference_application_to_webapi = f"dotnet add {name_project}.WebApi/{name_project}.WebApi.csproj reference {name_project}.Application/{name_project}.Application.csproj"
  comando_reference_persistence_to_webapi = f"dotnet add {name_project}.WebApi/{name_project}.WebApi.csproj reference {name_project}.Persistence/{name_project}.Persistence.csproj"
  # Instalar paquetes
  # EntityFrameworkCore
  comando_efcore_persistence = f"dotnet add {name_project}.Persistence/{name_project}.Persistence.csproj package Microsoft.EntityFrameworkCore"
  comando_efcore_webapi = f"dotnet add {name_project}.WebApi/{name_project}.WebApi.csproj package Microsoft.EntityFrameworkCore"
  comando_efcoretools_persistence = f"dotnet add {name_project}.Persistence/{name_project}.Persistence.csproj package Microsoft.EntityFrameworkCore.Tools"
  comando_efcoretools_webapi = f"dotnet add {name_project}.WebApi/{name_project}.WebApi.csproj package Microsoft.EntityFrameworkCore.Tools"

  try:
    #Ejecutar comandos
    # - Crear proyecto
    subprocess.run(comando_creacion, shell=True, check=True)
    # - Crear webapi
    subprocess.run(comando_webapi, shell=True, check=True)
    subprocess.run(comando_webapi_sln, shell=True, check=True)
    # - Crear domain
    subprocess.run(comando_domain, shell=True, check=True)
    subprocess.run(comando_domain_sln, shell=True, check=True)
    # - Crear application
    subprocess.run(comando_application, shell=True, check=True)
    subprocess.run(comando_application_sln, shell=True, check=True)
    # - Crear persistence
    subprocess.run(comando_persistence, shell=True, check=True)
    subprocess.run(comando_persistence_sln, shell=True, check=True)
    # - Referencias
    subprocess.run(comando_reference_domain_to_application, shell=True, check=True)
    subprocess.run(comando_reference_persistence_to_application, shell=True, check=True)
    subprocess.run(comando_reference_domain_to_persistence, shell=True, check=True)
    subprocess.run(comando_reference_application_to_webapi, shell=True, check=True)
    subprocess.run(comando_reference_persistence_to_webapi, shell=True, check=True)
    # - Instalar paquetes
    subprocess.run(comando_efcore_persistence, shell=True, check=True)
    subprocess.run(comando_efcore_webapi, shell=True, check=True)
    subprocess.run(comando_efcoretools_persistence, shell=True, check=True)
    subprocess.run(comando_efcoretools_webapi, shell=True, check=True)

    print(f"Proyecto {name_project} creado correctamente")

  except subprocess.CalledProcessError as e:
    print(f"Error al crear el proyecto: {e}")

if __name__ == "__main__":
  name_project = input("Nombre del proyecto: ")
  # Si el nombre del proyecto es vacío, mandar mensaje de error
  if name_project == "":
    print("El nombre del proyecto no puede estar vacío")
  else:
    create_project(name_project)
