# Guía para crear una aplicación Web API en .NET con capas Application, Domain, Persistence

## Paso 1: Instalar .NET SDK

Asegúrate de tener instalada la última versión del SDK de .NET. Puedes descargarlo e instalarlo desde [aquí](https://dotnet.microsoft.com/download).

## Paso 2: Crear la solución y los proyectos

1. **Crea una nueva solución**:

    ```bash
    dotnet new sln -n MyProject
    cd MyProject
    ```

2. **Crea el proyecto de la Web API**:

    ```bash
    dotnet new webapi -n MyProject.Api
    dotnet sln add MyProject.Api/MyProject.Api.csproj
    ```

3. **Crea la capa Domain**:

    ```bash
    dotnet new classlib -n MyProject.Domain
    dotnet sln add MyProject.Domain/MyProject.Domain.csproj
    ```

4. **Crea la capa Application**:

    ```bash
    dotnet new classlib -n MyProject.Application
    dotnet sln add MyProject.Application/MyProject.Application.csproj
    ```

5. **Crea la capa Persistence**:

    ```bash
    dotnet new classlib -n MyProject.Persistence
    dotnet sln add MyProject.Persistence/MyProject.Persistence.csproj
    ```

## Paso 3: Configurar las referencias entre los proyectos

1. **Agregar referencia de Domain a Application**:

    ```bash
    dotnet add MyProject.Application/MyProject.Application.csproj reference MyProject.Domain/MyProject.Domain.csproj
    ```

2. **Agregar referencia de Application a Persistence**:

    ```bash
    dotnet add MyProject.Persistence/MyProject.Persistence.csproj reference MyProject.Application/MyProject.Application.csproj
    ```

3. **Agregar referencia de Application y Persistence a la Web API**:

    ```bash
    dotnet add MyProject.Api/MyProject.Api.csproj reference MyProject.Application/MyProject.Application.csproj
    dotnet add MyProject.Api/MyProject.Api.csproj reference MyProject.Persistence/MyProject.Persistence.csproj
    ```
## Paso 4: Instalar EntityFramework Core
Dependiendo la base de datos que vayas a utilizar, instala los paquetes correspondientes.

### SQL Server
```bash
dotnet add MyProject.Persistence/MyProject.Persistence.csproj package Microsoft.EntityFrameworkCore.SqlServer
dotnet add MyProject.Api/MyProject.Api.csproj package Microsoft.EntityFrameworkCore.SqlServer
```
### MySQL
```bash
dotnet add MyProject.Persistence/MyProject.Persistence.csproj package Pomelo.EntityFrameworkCore.MySql
dotnet add MyProject.Api/MyProject.Api.csproj package Pomelo.EntityFrameworkCore.MySql
```
### SQLite
```bash
dotnet add MyProject.Persistence/MyProject.Persistence.csproj package Microsoft.EntityFrameworkCore.Sqlite
dotnet add MyProject.Api/MyProject.Api.csproj package Microsoft.EntityFrameworkCore.Sqlite
```
### PostgreSQL
```bash
dotnet add MyProject.Persistence/MyProject.Persistence.csproj package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add MyProject.Api/MyProject.Api.csproj package Npgsql.EntityFrameworkCore.PostgreSQL
```
### MongoDB
```bash
dotnet add MyProject.Persistence/MyProject.Persistence.csproj package MongoDB.Driver
dotnet add MyProject.Api/MyProject.Api.csproj package MongoDB.Driver

```

## Paso 5: Configurar las capas

1. **Domain Layer**: Aquí defines tus entidades y objetos de valor.

    - `MyProject.Domain/Entities/User.cs`:

      ```csharp
      namespace MyProject.Domain.Entities
      {
          public class User
          {
              public int Id { get; set; }
              public string Name { get; set; }
          }
      }
      ```

2. **Application Layer**: Aquí defines los contratos (interfaces) y los servicios que manejan la lógica de negocio.

    - `MyProject.Application/Interfaces/IUserService.cs`:

      ```csharp
      namespace MyProject.Application.Interfaces
      {
          public interface IUserService
          {
              User GetUser(int id);
          }
      }
      ```

    - `MyProject.Application/Services/UserService.cs`:

      ```csharp
      namespace MyProject.Application.Services
      {
          public class UserService : IUserService
          {
              public User GetUser(int id)
              {
                  // Implementación de ejemplo
                  return new User { Id = id, Name = "John Doe" };
              }
          }
      }
      ```

3. **Persistence Layer**: Aquí defines el contexto de la base de datos y los repositorios.

    - `MyProject.Persistence/Context/MyDbContext.cs`:

      ```csharp
      using Microsoft.EntityFrameworkCore;
      using MyProject.Domain.Entities;

      namespace MyProject.Persistence.Context
      {
          public class MyDbContext : DbContext
          {
              public DbSet<User> Users { get; set; }

              public MyDbContext(DbContextOptions<MyDbContext> options) : base(options)
              {
              }

              protected override void OnModelCreating(ModelBuilder modelBuilder)
              {
                  base.OnModelCreating(modelBuilder);
              }
          }
      }
      ```

## Paso 6: Configurar la Web API para usar los servicios

1. **Configurar Dependency Injection**:

    - `MyProject.Api/Program.cs`:

      ```csharp
      using Microsoft.EntityFrameworkCore;
      using MyProject.Application.Interfaces;
      using MyProject.Application.Services;
      using MyProject.Persistence.Context;

      var builder = WebApplication.CreateBuilder(args);

      // Add services to the container.
      builder.Services.AddControllers();
      builder.Services.AddEndpointsApiExplorer();
      builder.Services.AddSwaggerGen();

      // Add DbContext
      builder.Services.AddDbContext<MyDbContext>(options =>
          options.UseInMemoryDatabase("MyInMemoryDb"));

      // Add Application Services
      builder.Services.AddScoped<IUserService, UserService>();

      var app = builder.Build();

      // Configure the HTTP request pipeline.
      if (app.Environment.IsDevelopment())
      {
          app.UseSwagger();
          app.UseSwaggerUI();
      }

      app.UseHttpsRedirection();
      app.UseAuthorization();
      app.MapControllers();
      app.Run();
      ```

2. **Crear un controlador**:

    - `MyProject.Api/Controllers/UsersController.cs`:

      ```csharp
      using Microsoft.AspNetCore.Mvc;
      using MyProject.Application.Interfaces;

      [ApiController]
      [Route("[controller]")]
      public class UsersController : ControllerBase
      {
          private readonly IUserService _userService;

          public UsersController(IUserService userService)
          {
              _userService = userService;
          }

          [HttpGet("{id}")]
          public IActionResult GetUser(int id)
          {
              var user = _userService.GetUser(id);
              if (user == null)
              {
                  return NotFound();
              }

              return Ok(user);
          }
      }
      ```

## Paso 7: Ejecutar la aplicación

Finalmente, ejecuta la aplicación:
```bash
dotnet run --project MyProject.Api/MyProject.Api.csproj
```

```bash
dotnet run --project MyProject.Api/MyProject.Api.csproj
