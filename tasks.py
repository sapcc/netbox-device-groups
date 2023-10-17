from distutils.util import strtobool
from invoke import Collection, task as invoke_task
import os


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_netbox_physical_cluster_xxx
namespace = Collection("netbox_physical_cluster")
namespace.configure(
    {
        "netbox_physical_cluster": {
            "netbox_ver": "3.5.9",
            "python_ver": "3.10",
            "project_name": "netbox_physical_clusters",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": [
                "docker-compose.dev.yml",
                "docker-compose.base.yml",
                "docker-compose.postgres.yml",
                "docker-compose.redis.yml",
            ],
            "compose_http_timeout": "86400",
        }
    }
)


def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker-compose command with all appropriate parameters and environment.

    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker-compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        # Note: 'docker-compose logs' will stop following after 60 seconds by default,
        # so we are overriding that by setting this environment variable.
        "COMPOSE_HTTP_TIMEOUT": context.netbox_physical_cluster.compose_http_timeout,
        "NETBOX_VER": context.netbox_physical_cluster.netbox_ver,
        "PYTHON_VER": context.netbox_physical_cluster.python_ver,
    }
    compose_command = f'docker-compose --project-name {context.netbox_physical_cluster.project_name} \
        --project-directory "{context.netbox_physical_cluster.compose_dir}"'
    for compose_file in context.netbox_physical_cluster.compose_files:
        compose_file_path = os.path.join(context.netbox_physical_cluster.compose_dir, compose_file)
        compose_command += f' -f "{compose_file_path}"'
    compose_command += f" {command}"
    print(f'Running docker-compose command "{command}"')
    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, **kwargs):
    """Wrapper to run a command locally or inside the netbox container."""
    if is_truthy(context.netbox_physical_cluster.local):
        context.run(command, **kwargs)
    else:
        # Check if netbox is running, no need to start another netbox container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if "phy-cluster-ui" in results.stdout:
            compose_command = f"exec phy-cluster-ui {command}"
        else:
            compose_command = f"run --entrypoint '{command}' phy-cluster-ui"

        docker_compose(context, compose_command, pty=True)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    }
)
def build(context, force_rm=False, cache=True):
    """Build Netbox docker image."""
    command = "build"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(
        f"Building Netbox {context.netbox_physical_cluster.netbox_ver} "
        f"with Python {context.netbox_physical_cluster.python_ver}..."
    )
    docker_compose(context, command)


@task
def generate_packages(context):
    """Generate all Python packages inside docker and copy the file locally under dist/."""
    command = "poetry build"
    run_command(context, command)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context):
    """Start Netbox and its dependencies in debug mode."""
    print("Starting Netbox in debug mode...")
    docker_compose(context, "up")


@task
def start(context):
    """Start Netbox and its dependencies in detached mode."""
    print("Starting Netbox in detached mode...")
    docker_compose(context, "up --detach")


@task
def restart(context):
    """Gracefully restart all containers."""
    print("Restarting Netbox...")
    docker_compose(context, "restart")


@task
def stop(context):
    """Stop Netbox and its dependencies."""
    print("Stopping Netbox...")
    docker_compose(context, "down")


@task
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying Netbox...")
    docker_compose(context, "down --volumes")


@task
def vscode(context):
    """Launch Visual Studio Code with the appropriate Environment variables to run in a container."""
    command = "code code.code-workspace"

    context.run(command)


@task(
    help={
        "service": "Docker-compose service name to view (default: netbox)",
        "follow": "Follow logs",
        "tail": "Tail N number of lines or 'all'",
    }
)
def logs(context, service="netbox", follow=False, tail=None):
    """View the logs of a docker-compose service."""
    command = "logs "

    if follow:
        command += "--follow "
    if tail:
        command += f"--tail={tail} "

    command += service
    docker_compose(context, command)


# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
@task(
    help={
        "autoformat": "Apply formatting recommendations, rather than failing if formatting is incorrect.",
    }
)
def black(context, autoformat=False):
    """Check Python code style with Black."""
    if autoformat:
        black_command = "black"
    else:
        black_command = "black --check --diff"

    command = f"{black_command} ."

    run_command(context, command)


@task
def flake8(context):
    """Check for PEP8 compliance and other style issues."""
    command = "flake8 ."
    run_command(context, command)


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting adheres to defined standards."""
    # We exclude the /migrations/ directory since it is autogenerated code
    command = "pydocstyle ."
    run_command(context, command)


@task
def check_migrations(context):
    """Check for missing migrations."""
    command = "python /opt/netbox/netbox/manage.py makemigrations --dry-run --check"

    run_command(context, command)


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task
def cli(context):
    """Launch a bash shell inside the running Development container."""
    run_command(context, "zsh")


@task
def nbshell(context, name=""):
    """Perform python commandsin Django shell with all models loaded."""
    command = "python /opt/netbox/netbox/manage.py nbshell"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task
def dbshell(context, name=""):
    """Perform psql commaned in netbox dbshell."""
    command = "python /opt/netbox/netbox/manage.py dbshell"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task(
    help={
        "user": "name of the superuser to create (default: admin)",
    }
)
def createsuperuser(context, user="admin"):
    """Create a new Development superuser account (default: "admin"), will prompt for password."""
    command = f"python /opt/netbox/netbox/manage.py createsuperuser --username {user}"

    run_command(context, command)


@task(
    help={
        "name": "name of the migration to be created; if unspecified, will autogenerate a name",
    }
)
def makemigrations(context, name=""):
    """Perform makemigrations operation in Django."""
    command = "python /opt/netbox/netbox/manage.py makemigrations"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task
def migrate(context):
    """Perform migrate operation in Django."""
    command = "python /opt/netbox/netbox/manage.py migrate"

    run_command(context, command)


@task
def seed(context):
    """Perform seed operation in Django."""
    command = "python /opt/netbox/netbox/manage.py loaddata development/data/seed.json"

    run_command(context, command)


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------
@task
def unittest(context):
    """Perform migrate operation in Django."""
    command = "python /opt/netbox/netbox/manage.py test"

    run_command(context, command)
