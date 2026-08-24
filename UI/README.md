# UI

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 18.2.0.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

## Docker deployment

This project includes a multi-stage Docker build:
- Build stage: compiles Angular app with Node.
- Runtime stage: serves static files with Nginx.

### 1. Build the Docker image

```bash
docker build -t caseira-ui:latest .
```

### 2. Run the container

```bash
docker run -d --name caseira-ui -p 8080:80 caseira-ui:latest
```

Open the app at:
- `http://localhost:8080`

### 3. Useful Docker commands

View logs:

```bash
docker logs caseira-ui
```

Stop and remove container:

```bash
docker stop caseira-ui
docker rm caseira-ui
```

Remove image:

```bash
docker rmi caseira-ui:latest
```

### 4. Notes

- Angular production output is copied from `dist/ui/browser` into Nginx web root.
- Nginx is configured for SPA routing (`try_files ... /index.html`), so direct route refreshes work.
