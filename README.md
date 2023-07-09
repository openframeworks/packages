# openFrameworks packages

This repository is the continuation of [apothecary](https://github.com/openframeworks/apothecary). It is the central place where all [openFrameworks](https://github.com/openframeworks/openframeworks) dependencies are built and managed, so they can be downloaded and linked into openFrameworks projects.

## Building manually locally

You can build the dependencies locally by running the following command:

```bash
cd packages/<PACKAGE_NAME>
docker-compose up --build
```

This should build the package and place all archive files into a `packages/<PACKAGE_NAME>/out` folder. [Docker](https://www.docker.com) and [Docker-Compose](https://docs.docker.com/compose/) are required to run this command. Most CI environments and Linux servers have Docker pre-installed.