# A full-stack FastAPI application demonstrating integration with PostgreSQL


## Backend setup Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Frontend Requirements

* Node.js (with `npm`).

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* You can now open your browser and access the following URLs:

Frontend (served via Docker, routes handled by path): http://localhost

Backend API (JSON-based, built on OpenAPI): http://localhost/api/

Interactive API docs with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative API docs with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin (PostgreSQL web administration): http://localhost:5050

Flower (Celery task monitoring and administration): http://localhost:5555

Traefik UI (view how routes are handled by the proxy): http://localhost:8090

Note: The first time you start the stack, it may take a minute to become fully ready. The backend waits for the database to initialize and complete its configuration. You can monitor progress via the logs.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```

If your Docker is not running on localhost, please refer to the sections below on Development with Docker Toolbox and Development using a custom IP.

## Additional Notes for Backend Local Development

### General Workflow

Dependencies are managed using Poetry
. Make sure it is installed before proceeding.

From the ./backend/app/ directory, install all required dependencies with:

```bash
$ poetry install
```
Afterwards, you can activate a shell within the virtual environment using:

```bash
$ poetry shell
```
Next, open your editor in `./backend/app/` instead of the project root (`./`). This ensures you can see the `./app/` directory with your code, allowing your editor to correctly resolve imports and dependencies. Make sure your editor is using the Poetry environment you just created.

You can then:

* SQLAlchemy models: modify or add them in `./backend/app/app/models/`

* Pydantic schemas: modify or add them in `./backend/app/app/schemas/`

* API endpoints: add or update them in `./backend/app/app/api/

* CRUD utilities (Create, Read, Update, Delete): edit or add them in `./backend/app/app/worker.py`

Tip: You can copy the existing implementations for Items (models, endpoints, and CRUD utils) as a starting point and adjust them to your needs.

For Celery tasks, add or modify them in `./backend/app/app/worker.py`.
If you need to install additional packages for the worker, add them in `./backend/app/celeryworker.dockerfile`.


### Docker Compose Override

During development, you can customize Docker Compose settings that only affect the local environment by editing the `docker-compose.override.yml`.

Changes in this file do not impact the production environment, so you can safely add temporary adjustments to improve your development workflow.

For example, the backend code directory is mounted as a Docker host volume, which maps your local changes directly into the container. This allows you to test updates immediately without rebuilding the Docker image. This setup is intended only for development—for production, always build the Docker image with the latest backend code. Using volumes during development enables fast iteration.

Additionally, a command override runs `/start-reload.sh`(from the base image) instead of the default `/start.sh` This starts a single server process and automatically reloads whenever your code changes.

⚠️ Note: If a Python file contains a syntax error and you save it, the process will crash and the container will stop. To recover, fix the error and restart the container.


 
 
 There is also a commented-out `command` override. You can uncomment it and comment out the default command. This makes the backend container run a “do-nothing” process, keeping the container alive.

* This is useful for accessing the running container to execute commands, for example:

* Start a Python interpreter to test installed dependencies

* Launch the development server with automatic reload on code changes

* Start a Jupyter Notebook session 

To open a `bash session inside the container, start the stack with:

```console
$ docker-compose up -d
```

and then `exec` inside the running container:

```console
$ docker-compose exec backend bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

This means you are now in a `bash` session inside the container, logged in as the `root` user, with the working directory set to `/app`.

From here, you can run the debug server with live reload using the script `/start-reload.sh`. Execute it inside the container with:


```console
$ bash /start-reload.sh
```

...it will look like:

```console
root@7f2607af31c3:/app# bash /start-reload.sh
```


Then, press Enter to run the live-reloading server. The server will automatically reload whenever it detects changes in the code.

However, if there is a syntax error, the server will stop with an error. Since the container is still running and you are in a Bash session, you can quickly restart the server after fixing the error by pressing the up arrow and Enter.

This workflow is exactly why it’s useful to keep the container running with a “do-nothing” process. From within the Bash session, you can start the live-reload server as needed without restarting the container.

### Backend tests

To test the backend run:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```


The file `./scripts/test.sh` contains commands to generate a testing `docker-stack.yml` file, start the stack, and run the tests.

Tests are executed using Pytest. You can modify existing tests or add new ones in `./backend/app/app/tests/`.

If you are using GitLab CI, the tests will run automatically as part of the CI pipeline.

#### Test running stack

If your stack is already running and you:

```bash
docker-compose exec backend /app/tests-start.sh
```

The script `/app/tests-start.sh` simply runs `pytest` after ensuring that the rest of the stack is up and running.

If you need to pass additional arguments to `pytest`, you can provide them when running this script—they will be forwarded directly to pytest.

For example, to stop on the first error:

```bash
docker-compose exec backend bash /app/tests-start.sh -x
```

#### Test Coverage


Since the test scripts forward arguments to `pytest`, you can generate an HTML test coverage report by passing --cov-report=html.

To run the local tests with coverage reports in HTML format:

```Bash
DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```

To run the tests on a running stack and generate HTML coverage reports:

```bash
docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```

### Live Development Using Python Notebooks


If you are familiar with Python (http://jupyter.org/)
, you can leverage them for local development.

During local development, the `docker-compose.override.yml` file passes an `env`= `dev` variable to the Docker build process. The `Dockerfile` then installs and configures Jupyter inside the container.

This allows you to enter the running Docker container and start using Jupyter Notebooks for interactive development.

```bash
docker-compose exec backend bash
```

You can then use the environment variable `$JUPYTER` to start a Jupyter Notebook, fully configured to listen on the public port so it’s accessible from your browser.

The output will look similar to:

```console
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

You can copy the provided URL and modify the host to `localhost` or the domain you are using for development (e.g.,`local.dockertoolbox.tiangolo.com`).

For example, in the case above, the URL would become:

```
http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```
Then, open the URL in your browser.

You will have a fully functional Jupyter Notebook running inside the container, with direct access to your database by container name (db), and more. This allows you to run sections of your backend code interactively, (https://code.visualstudio.com/docs/python/jupyter-support-py) or [Hydrogen](https://github.com/nteract/hydrogen)
 or Hydrogen

### Migrations

During local development, since your app directory is mounted as a volume inside the container, you can run migrations using `alembic` inside the container, and the migration files will be saved in your app directory. This allows you to track them in your Git repository.

Always make sure to create a revision of your models and upgrade your database with that revision whenever you make changes. This ensures your database tables stay in sync with your models—otherwise, your application may encounter errors.

To start an interactive session in the backend container:

```console
$ docker-compose exec backend bash
```

* If you create a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`. This module, which imports all models, is used by Alembic to detect changes.

* After modifying a model (for example, adding a new column), create a migration revision inside the container, for example:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit the files generated in the Alembic directory to your Git repository.

* After creating a revision, apply the migration to the database to actually update its schema:

```console
$ alembic upgrade head
```

If you prefer not to use migrations, you can uncomment the line in `./backend/app/app/db/init_db.py` that contains:

```python
Base.metadata.create_all(bind=engine)
```

And comment out the line in the `prestart.sh`file that contains:

```console
$ alembic upgrade head
```

If you don’t want to start with the default models and prefer to remove or modify them from the beginning—without keeping any previous revisions—you can delete the existing migration files (`.py` Python files) located in `./backend/app/alembic/versions/`/. After that, create an initial migration as described above.


### Development with Docker Toolbox

If you are using Docker Toolbox on Windows or macOS instead of Docker for Windows or Docker for Mac, Docker will run inside a VirtualBox virtual machine. In this case, it will use a local IP address different from `127.0.0.1`, which is the standard `localhost`  address on your machine.

The Docker Toolbox virtual machine usually has the IP address `192.168.99.100` by default.

Since this is a common scenario, the domain `local.dockertoolbox.tiangolo.com` is configured to point to that private IP address. In fact, `dockertoolbox.tiangolo.com` and all of its subdomains resolve to the same IP. This setup is intended to simplify local development.

Using this domain allows you to start the stack with Docker Toolbox and access it through a browser as if it were running on a remote server. This also enables proper handling of CORS (Cross-Origin Resource Sharing), just like in a cloud environment.

If you selected the default CORS configuration when generating the project, `local.dockertoolbox.tiangolo.com` is already included in the allowed origins. If not, you will need to manually add it to the `BACKEND_CORS_ORIGINS` variable in the`.env` file.

To apply this configuration, follow the section “Change the development domain” below and use `local.dockertoolbox.tiangolo.com` as the development domain.

After completing these steps, you should be able to open
(http://local.dockertoolbox.tiangolo.com )
,
and it will be served directly by your stack running inside the Docker Toolbox virtual machine.

You can find all other available service URLs in the section at the end.


### Development in `localhost` with a custom domain

You may want to use a domain other than localhost. For example, this can be useful if you encounter issues with cookies that require a subdomain and Chrome does not allow them when using `localhost`.

In this case, you have two options. You can either follow the instructions in Development with a custom IP to modify your system’s hosts file, or simply use `localhost.tiangolo.com`. This domain is configured to point to localhost (to the IP `127.0.0.1`), including all of its subdomains. Because it is a real domain, browsers will correctly store cookies and other related data during development.

If you selected the default CORS configuration when generating the project, `localhost.tiangolo.com`  is already included in the allowed origins. Otherwise, you will need to add it manually to the `BACKEND_CORS_ORIGINS` variable in the `.env` file.

To apply this configuration, follow the section “Change the development domain” below and use localhost.tiangolo.com as the development domain.

After completing these steps, you should be able to open
(http://localhost.tiangolo.com )
,
and it will be served by your stack running on`localhost`.

You can find all other available service URLs in the section at the end.

### Development with a custom IP 

If your Docker setup is running on an IP address other than `127.0.0.1` (`localhost`) or `192.168.99.100` (the default for Docker Toolbox), some additional configuration steps are required. This typically applies when using a custom virtual machine, a secondary Docker Toolbox instance, or when Docker is running on a different machine within your network.

In this scenario, you will need to use a custom local domain (`dev.example-full-stack-fastapi-application-with-postgresql.com`)  and configure your system to resolve that domain to your custom IP address (e.g. 192.168.99.150).

If you used the default CORS configuration when generating the project, dev.example-full-stack-fastapi-application-with-postgresql.com is already included in the allowed origins. If you choose a different domain, make sure to add it to the `BACKEND_CORS_ORIGINS` variable in the `.env` file.

To configure your system, follow these steps:

* Open your `hosts`  file with administrative privileges using a text editor.

Windows:
* Open the Start menu, search for Notepad, right-click it, and select Run as administrator.
Then go to File → Open, navigate to
* C:\Windows\System32\Drivers\etc\,
change the file type filter to All files, and open the hosts file.

macOS and Linux:
The `hosts` file is typically located at `/etc/hosts`.

```
192.168.99.100    dev.example-full-stack-fastapi-application-with-postgresql.com
```

* Save the file.

* **Windows note: Make sure to save the file as All files, without adding a `.txt`extension. Windows may try to append the extension automatically, so ensure the file is saved exactly as hosts.

These steps will make your system treat the fake local domain as if it were served by the specified custom IP address. When you open the domain in your browser, it will communicate directly with your locally running server. From the browser’s perspective, it behaves like a remote server, even though it is running on your own machine.

To apply this configuration to your stack, follow the section “Change the development domain” below and use the domain `dev.example-full-stack-fastapi-application-with-postgresql.com`.

After completing these steps, you should be able to open
(http://dev.example-full-stack-fastapi-application-with-postgresql.com )
,
and it will be served by your stack running on `localhost`.

You can find all other available service URLs in the section at the end.


### Change the development "domain"

If you need to run your local stack using a domain other than `localhost`, make sure that the chosen domain resolves to the IP address where your stack is running. Refer to the sections above for different ways to achieve this, such as using Docker Toolbox with `local.dockertoolbox.tiangolo.com`, `localhost.tiangolo.com` , or a custom `dev.example-full-stack-fastapi-application-with-postgresql.com`.

To simplify your Docker Compose configuration—for example, so that the API documentation (Swagger UI) correctly detects the API base URL—you should explicitly define the development domain.

This requires modifying one line in two files.

* Open the file located at `./.env`. You should see a line similar to:

```
DOMAIN=localhost
```

* Change it to the domain you are going to use, e.g.:

```
DOMAIN=localhost.tiangolo.com
```

That variable will be used by the Docker Compose files.

* Now open the file located at `./frontend/.env`. It would have a line like:

```
VUE_APP_DOMAIN_DEV=localhost
```

* Change that line to the domain you are going to use, e.g.:

```
VUE_APP_DOMAIN_DEV=localhost.tiangolo.com
```

This variable ensures that your frontend communicates with the specified domain when interacting with the backend API, provided that the`VUE_APP_ENV`variable is set to `development`.

After updating both lines, restart your stack using:

```bash
docker-compose up -d
```
Then, verify all corresponding available URLs listed in the section at the end.


## Frontend development

* Enter the `frontend` directory, install the NPM packages and start the live server using the `npm` scripts:

```bash
cd frontend
npm install
npm run serve
```

Then open your browser at http://localhost:8080

Note that this live development server does not run inside Docker. It is intended for local development and represents the recommended workflow. Once you are satisfied with your frontend changes, you can build and run the frontend Docker image to test it in a production-like environment. However, rebuilding the Docker image on every change is far less efficient than using a local development server with live reload.

Check the `package.json` file to explore additional available scripts and options.

If you have Vue CLI installed, you can also run `vue ui` to manage, configure, serve, and analyze your application through a convenient local web interface.

If you are working exclusively on the `./frontend/.env`(for example, while other team members are developing the backend) and a staging environment is already deployed, you can configure your local frontend to use the staging API instead of running the full local Docker Compose stack.

To do this, edit the file `./frontend/.env`, where you will find a section similar to:

```
VUE_APP_ENV=development
# VUE_APP_ENV=staging
```

* Switch the comment, to:

```
# VUE_APP_ENV=development
VUE_APP_ENV=staging
```

### Removing the frontend

If you are developing an API-only application and want to remove the frontend, you can do so easily:

* Delete the `./frontend` directory.

* In the `docker-compose.yml` file, remove the entire `frontend` service section.

* In the `docker-compose.override.yml`, remove the entire `frontend` service section.

That’s it—you now have a frontend-less, API-only application.

---

If desired, you can also remove the `FRONTEND` environment variables from:

* `.env`
* `.gitlab-ci.yml`
* `./scripts/*.sh`

However, this is purely for cleanup purposes—leaving the `FRONTEND` environment variables in place will not affect your API-only application.

## Deployment

You can deploy the stack to a Docker Swarm cluster with a main Traefik proxy, using the concepts from DockerSwarm.rocks
 to enable features like automatic HTTPS certificates.

Additionally, you can set up continuous integration (CI) systems to deploy the stack automatically.

However, a few configurations must be completed before doing so.

### Traefik network

This stack expects the public Traefik network to be named `traefik-public`, as shown in the tutorials at <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a>.
.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files under the following section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```
### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.

#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.yml` file.

To make sure that your labels are unique per volume per stack (for example, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your `docker-compose.yml` file for the services that need to be fixed with each volume.

To be able to use different environments, like `prod` and `stag`, you should pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME=stag-example-full-stack-fastapi-application-with-postgresql-com sh ./scripts/deploy.sh
```

To use and expand that environment variable inside the `docker-compose.yml` files you can add the constraints to the services like:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME?Variable not set}.app-db-data == true
```

note the `${STACK_NAME?Variable not set}`. In the script `./scripts/deploy.sh`, the `docker-compose.yml` would be converted, and saved to a file `docker-stack.yml` containing:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.example-full-stack-fastapi-application-with-postgresql-com.app-db-data == true
```

**Note**: The `${STACK_NAME?Variable not set}` means "use the environment variable `STACK_NAME`, but if it is not set, show an error `Variable not set`".

If you add more volumes to your stack, you need to make sure you add the corresponding constraints to the services that use that named volume.

Then you have to create those labels in some nodes in your Docker Swarm mode cluster. You can use `docker-auto-labels` to do it automatically.

#### `docker-auto-labels`

You can use [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) to automatically read the placement constraint labels in your Docker stack (Docker Compose file) and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

To do that, you can install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

And then run it passing your `docker-stack.yml` file as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

#### (Optionally) adding labels manually

If you don't want to use `docker-auto-labels` or for any reason you want to manually assign the constraint labels to specific nodes in your Docker Swarm mode cluster, you can do the following:

* First, connect via SSH to your Docker Swarm mode cluster.

* Then check the available nodes with:

```console
$ docker node ls


// you would see an output like:

ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

then chose a node from the list. For example, `dog.example.com`.

* Add the label to that node. Use as label the name of the stack you are deploying followed by a dot (`.`) followed by the named volume, and as value, just `true`, e.g.:

```bash
docker node update --label-add example-full-stack-fastapi-application-with-postgresql-com.app-db-data=true dog.example.com
```

* Then you need to do the same for each stack version you have. For example, for staging you could do:

```bash
docker node update --label-add stag-example-full-stack-fastapi-application-with-postgresql-com.app-db-data=true cat.example.com
```

### Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

* Set these environment variables, right before the next command:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build.sh
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.

If you are using a registry and pushing your images, you can omit running the previous script and instead using this one, in a single shot.

* Set these environment variables:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build-push.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Set these environment variables:
  * `DOMAIN=example-full-stack-fastapi-application-with-postgresql.com`
  * `TRAEFIK_TAG=example-full-stack-fastapi-application-with-postgresql.com`
  * `STACK_NAME=example-full-stack-fastapi-application-with-postgresql-com`
  * `TAG=prod`
* Use the provided `scripts/deploy.sh` file with those environment variables:

```bash
DOMAIN=example-full-stack-fastapi-application-with-postgresql.com \
TRAEFIK_TAG=example-full-stack-fastapi-application-with-postgresql.com \
STACK_NAME=example-full-stack-fastapi-application-with-postgresql-com \
TAG=prod \
bash ./scripts/deploy.sh
```

---

If you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable in the previous commands. If you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command and update these other environment variables accordingly. And it would all work, that way you could have different environments and deployments of the same app in the same cluster.

#### Deployment Technical Details

Building and pushing is done with the `docker-compose.yml` file, using the `docker-compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. And the scripts set some additional environment variables as well.

The deployment requires using `docker stack` instead of `docker-swarm`, and it can't read environment variables or `.env` files. Because of that, the `deploy.sh` script generates a file `docker-stack.yml` with the configurations from `docker-compose.yml` and injecting the environment variables in it. And then uses it to deploy the stack.

You can do the process by hand based on those same scripts if you wanted. The general structure is like this:

```bash
# Use the environment variables passed to this script, as TAG and FRONTEND_ENV
# And re-create those variables as environment variables for the next command
TAG=${TAG?Variable not set} \
# Set the environment variable FRONTEND_ENV to the same value passed to this script with
# a default value of "production" if nothing else was passed
FRONTEND_ENV=${FRONTEND_ENV-production?Variable not set} \
# The actual comand that does the work: docker-compose
docker-compose \
# Pass the file that should be used, setting explicitly docker-compose.yml avoids the
# default of also using docker-compose.override.yml
-f docker-compose.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.yml
# file passed to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file,
# but didn't do anything with it yet

# docker-auto-labels makes sure the labels used for constraints exist in the cluster
docker-auto-labels docker-stack.yml

# Now this command uses that same file to deploy it
docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
```

### Continuous Integration / Continuous Delivery

If you use GitLab CI, the included `.gitlab-ci.yml` can automatically deploy it. You may need to update it according to your GitLab configurations.

If you use any other CI / CD provider, you can base your deployment from that `.gitlab-ci.yml` file, as all the actual script steps are performed in `bash` scripts that you can easily re-use.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.

If you need to add more environments, for example, you could imagine using a client-approved `preprod` branch, you can just copy the configurations in `.gitlab-ci.yml` for `stag` and rename the corresponding variables. The Docker Compose file and environment variables are configured to support as many environments as you need, so that you only need to modify `.gitlab-ci.yml` (or whichever CI system configuration you are using).

## Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker-compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker-compose` to apply overrides on top of `docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker-compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.

## URLs

These are the URLs that will be used and generated by the project.

### Production URLs

Production URLs, from the branch `production`.

Frontend: https://example-full-stack-fastapi-application-with-postgresql.com

Backend: https://example-full-stack-fastapi-application-with-postgresql.com/api/

Automatic Interactive Docs (Swagger UI): https://example-full-stack-fastapi-application-with-postgresql.com/docs

Automatic Alternative Docs (ReDoc): https://example-full-stack-fastapi-application-with-postgresql.com/redoc

PGAdmin: https://pgadmin.example-full-stack-fastapi-application-with-postgresql.com

Flower: https://flower.example-full-stack-fastapi-application-with-postgresql.com

### Staging URLs

Staging URLs, from the branch `master`.

Frontend: https://stag.example-full-stack-fastapi-application-with-postgresql.com

Backend: https://stag.example-full-stack-fastapi-application-with-postgresql.com/api/

Automatic Interactive Docs (Swagger UI): https://stag.example-full-stack-fastapi-application-with-postgresql.com/docs

Automatic Alternative Docs (ReDoc): https://stag.example-full-stack-fastapi-application-with-postgresql.com/redoc

PGAdmin: https://pgadmin.stag.example-full-stack-fastapi-application-with-postgresql.com

Flower: https://flower.stag.example-full-stack-fastapi-application-with-postgresql.com

### Development URLs

Development URLs, for local development.

Frontend: http://localhost

Backend: http://localhost/api/

Automatic Interactive Docs (Swagger UI): https://localhost/docs

Automatic Alternative Docs (ReDoc): https://localhost/redoc

PGAdmin: http://localhost:5050

Flower: http://localhost:5555

Traefik UI: http://localhost:8090

### Development with Docker Toolbox URLs

Development URLs, for local development.

Frontend: http://local.dockertoolbox.tiangolo.com

Backend: http://local.dockertoolbox.tiangolo.com/api/

Automatic Interactive Docs (Swagger UI): https://local.dockertoolbox.tiangolo.com/docs

Automatic Alternative Docs (ReDoc): https://local.dockertoolbox.tiangolo.com/redoc

PGAdmin: http://local.dockertoolbox.tiangolo.com:5050

Flower: http://local.dockertoolbox.tiangolo.com:5555

Traefik UI: http://local.dockertoolbox.tiangolo.com:8090

### Development with a custom IP URLs

Development URLs, for local development.

Frontend: http://dev.example-full-stack-fastapi-application-with-postgresql.com

Backend: http://dev.example-full-stack-fastapi-application-with-postgresql.com/api/

Automatic Interactive Docs (Swagger UI): https://dev.example-full-stack-fastapi-application-with-postgresql.com/docs

Automatic Alternative Docs (ReDoc): https://dev.example-full-stack-fastapi-application-with-postgresql.com/redoc

PGAdmin: http://dev.example-full-stack-fastapi-application-with-postgresql.com:5050

Flower: http://dev.example-full-stack-fastapi-application-with-postgresql.com:5555

Traefik UI: http://dev.example-full-stack-fastapi-application-with-postgresql.com:8090

### Development in localhost with a custom domain URLs

Development URLs, for local development.

Frontend: http://localhost.tiangolo.com

Backend: http://localhost.tiangolo.com/api/

Automatic Interactive Docs (Swagger UI): https://localhost.tiangolo.com/docs

Automatic Alternative Docs (ReDoc): https://localhost.tiangolo.com/redoc

PGAdmin: http://localhost.tiangolo.com:5050

Flower: http://localhost.tiangolo.com:5555

Traefik UI: http://localhost.tiangolo.com:8090

## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

You can check the variables used during generation in the file `cookiecutter-config-file.yml`.

You can generate the project again with the same configurations used the first time.

That would be useful if, for example, the project generator (`tiangolo/full-stack-fastapi-postgresql`) was updated and you wanted to integrate or review the changes.

You could generate a new project with the same configurations as this one in a parallel directory. And compare the differences between the two, without having to overwrite your current code but being able to use the same variables used for your current project.

To achieve that, the generated project includes the file `cookiecutter-config-file.yml` with the current variables used.

You can use that file while generating a new project to reuse all those variables.

For example, run:

```console
$ cookiecutter --config-file ./cookiecutter-config-file.yml --output-dir ../project-copy https://github.com/tiangolo/full-stack-fastapi-postgresql
```

That will use the file `cookiecutter-config-file.yml` in the current directory (in this project) to generate a new project inside a sibling directory `project-copy`.
