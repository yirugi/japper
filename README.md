# Japper: A framework for building Jupyter-based web applications

Japper is a framework for building Jupyter-based web applications. It is designed to be a lightweight, flexible, and
extensible framework that can be used to build a wide range of web applications.

**Note: This project is still in the early stages of development, and the documentation is a work in progress. Please
check back later for updates.**

## Why Japper?

### Problems with Jupyter-based web applications development

Jupyter is a popular open-source web application that provides a rich set of tools for building interactive web
applications. However, building Jupyter-based web applications can be challenging for several reasons:

- Time-consuming setup and configuration
    - Setting up a development environment for Jupyter-based web applications can be time-consuming and error-prone.
    - Managing dependencies and environment can be difficult, especially when working with multiple projects.
    - Test and deployment can be complex.
- Limited frontend capabilities and extensibility of ipywidgets
    - Jupyter provides a rich set of tools for building interactive web applications, but it has limited frontend
      capabilities and extensibility.
    - Building custom components and plugins can be challenging.
- Lack of debugging and error handling
    - Jupyter provides limited support for debugging and error handling, making it difficult to diagnose and fix issues.
- Lack of architectural guidance
    - There is no architectural guidance, making it difficult to build scalable and maintainable web applications.

### Solutions provided by Japper

Japper is a framework for building Jupyter-based web applications easily and quickly. Here are some of the key features:

- Command-line interface for creating and managing Japper projects
- Create a new Japper project with pre-configured templates to get started quickly
- Manage dependencies and environment with a simple configuration file
- Build and run development and production versions using Docker
- Deploy to Docker registry or Kubernetes with a single command
- Automatically generate documentation for your Japper project
- Vue.js-based frontend for building interactive web applications utilizing ipyvuetify
    - Provide a rich set of components and utilities for building web applications
    - Support for custom components and plugins
- Improved debugging and error handling
    - Support for logging and error handling
- Guided Model-View-Presenter (MVP) architectural pattern
    - Support for building scalable and maintainable web applications
    - Support for building reusable components and plugins

## Getting started

To get started with Japper, you can install it using pip:

```bash
pip install japper
```

Note that Japper currently support Linux and MacOS only.

Once installed, you can run japper commands from the command line.

```bash
japper
```

### Japper Forge

Japper Forge is a web-based tool that allows you to create and manage Japper projects. You can access Japper Forge by
running the following command:

```bash
japper forge
```

This will start a web server, and Japper Forge will automatically open in your web browser.

### Japper CLI

You can create a new Japper project using the `japper` command-line interface:

```bash
japper init
```

This will create a new Japper project with pre-configured templates to get you started quickly.

Enter the project directory after creating the project:

```bash
cd <project_name>
```

To run the development version of your Japper project, you can use the `japper run dev` command:

```bash
japper run dev
```

This will start a development server, and you can open your Japper project in a web browser. By default, the development
server will run on port 8888. (You can visit `http://localhost:8888` in your web browser to see your Japper project.)

To build and run the production version of your Japper project, you can use the `japper run prod` command:

```bash
japper run prod
```

This will build a production version of your Japper project and run it using Docker.

To deploy your Japper project to a Docker registry, you can use the `japper deploy registry` command:

```bash
japper deploy registry
```

This will build a production version of your Japper project and deploy it to a Docker registry. Japper will ask you for
the Docker registry URL and other configurations.

To generate documentation for your Japper project, you can use the `japper doc` command:

```bash
japper doc
```

This will generate documentation for your Japper project using pydoc3. You can find the documentation in the `docs`
folder

## Documentation

To be added

