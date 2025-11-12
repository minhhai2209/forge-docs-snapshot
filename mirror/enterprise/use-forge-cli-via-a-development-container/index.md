# Use Forge CLI via development container

You can run the Forge CLI in a development container, which provides a consistent and isolated environment pre-configured with the dependencies you need to build Forge apps. This guide explains how to run the Forge CLI in the development container using Visual Studio Code or IntelliJ IDEA.

## What is a Development Container?

A [development container](https://containers.dev/) (or dev container) is a Docker container configured to provide a full-featured development environment. Development containers are used to separate tools, libraries, or runtimes needed for development from your local machine.

The development container includes:

* Node.js (LTS version)
* Forge CLI
* Atlassian CLI
* Git
* Essential development tools (curl, wget, jq)
* VS Code extensions for JavaScript/TypeScript development

## Prerequisites

## Setup with Docker Desktop

### Installation

1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop) for your operating system.
2. Install Docker Desktop following the installation wizard instructions.
3. Start Docker Desktop after installation.

## Setup Instructions

To use development containers, create a `.devcontainer.json` configuration file. Here is an example configuration file which pulls the latest version of the provided Docker for the Forge CLI container:

```
```
1
2
```



```
{
  "name": "Atlassian Forge Development Container Sample Config",
  "image": "atlassian/forge-devcontainer:latest",
  "features":{},
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
      }
    }
  },
  "remoteUser": "node"
}
```
```

To pull the Docker image directly, run:

```
```
1
2
```



```
docker pull atlassian/forge-devcontainer:latest
```
```

### Open your project in Visual Studio Code

1. Create a `.devcontainer.json` file with the above configuration.
2. Open the repository containing the `.devcontainer.json` file in VS Code. VS Code will detect the dev container configuration and prompt you to reopen the folder in a container.
3. Select **Reopen in Container**. VS Code will build the devcontainer and open the project inside it. This may take a few minutes the first time.

### Open your project in IntelliJ IDEA

#### Using Dev Containers Plugin

1. Create a `.devcontainer.json` file with the above configuration.
2. Open IntelliJ IDEA.
3. Install the Dev Containers plugin if you haven't already.
4. Go to **File > Open** and select the repository containing the `.devcontainer.json` file. IntelliJ IDEA will detect the dev container configuration and prompt you to open the project in a container.
5. Select **Open in Container**. IntelliJ IDEA will build the container and opens your project inside it.

## Using the Forge CLI in a devcontainer

You must use the terminal in your IDE to run Forge CLI commands.

Do not use forge login in a development container. Instead, set the `FORGE_EMAIL` and `FORGE_API_TOKEN` environment variables in your shell configuration. For more details, see [Using environment variables to log in](https://developer.atlassian.com/platform/forge/getting-started/#using-environment-variables-to-login).

### Creating Your Own Forge App

To create your own Forge app from scratch:

1. Open a terminal in your editor.
2. Create a new Forge app:
3. Follow the prompts to set up your app.
4. Navigate to your app directory:
5. Deploy your app:
6. Install your app:

For more information on developing with Forge, see the [Forge documentation](https://developer.atlassian.com/platform/forge/getting-started/).

## Setup Behind Corporate Proxy

If you're working in a corporate environment with a proxy, you'll need to configure both Docker and the dev container to work with your proxy. Follow these instructions for Linux and Windows Subsystem for Linux (WSL). For more details, see [Use the Forge CLI on a corporate network](https://hello.atlassian.net/platform/forge/enterprise/use-forge-cli-on-corporate-network/).

Replace `http://proxy.example.com:8080` with your actual corporate proxy URL in the examples below.

### Linux Setup

1. Create or edit the Docker daemon configuration file:

   ```
   ```
   1
   2
   ```



   ```
   sudo mkdir -p /etc/systemd/system/docker.service.d
   sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
   ```
   ```
2. Add the following content, replacing the proxy URLs with your corporate proxy details:

   ```
   ```
   1
   2
   ```



   ```
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:8080"
   Environment="HTTPS_PROXY=http://proxy.example.com:8080"
   Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
   ```
   ```
3. Restart the Docker daemon:

   ```
   ```
   1
   2
   ```



   ```
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```
   ```
4. Verify the configuration:

   ```
   ```
   1
   2
   ```



   ```
   sudo systemctl show --property=Environment docker
   ```
   ```

### WSL Setup

1. Create or edit the `.wslconfig` file in your Windows user directory:

   ```
   ```
   1
   2
   ```



   ```
   [wsl2]
   kernelCommandLine = "sysctl.net.ipv4.tcp_keepalive_time=60 net.ipv4.tcp_keepalive_intvl=60 net.ipv4.tcp_keepalive_probes=6"
   ```
   ```
2. In your WSL distribution, create or edit the Docker daemon configuration:

   ```
   ```
   1
   2
   ```



   ```
   sudo mkdir -p /etc/docker
   sudo nano /etc/docker/daemon.json
   ```
   ```
3. Add the following content, replacing the proxy URLs with your corporate proxy details:

   ```
   ```
   1
   2
   ```



   ```
   {
     "proxies": {
       "default": {
         "httpProxy": "http://proxy.example.com:8080",
         "httpsProxy": "http://proxy.example.com:8080",
         "noProxy": "localhost,127.0.0.1,.example.com"
       }
     }
   }
   ```
   ```
4. Restart Docker:

   ```
   ```
   1
   2
   ```



   ```
   sudo service docker restart
   ```
   ```

## Additional Resources
