import pathlib
import subprocess
import click
from .utils import ContextObj


@click.group()
@click.option('--pkgname')
@click.option('--release', envvar='WOCK')
@click.option('--architecture', default='x86_64')
@click.pass_context
def cli(context, pkgname, release, architecture):
    context.obj = ContextObj(pkgname, release, architecture)


@click.command()
@click.pass_obj
def init(cobj):
    cobj.init()


@click.command()
@click.pass_obj
def clean(cobj):
    cobj.clean()


@click.group()
@click.pass_obj
def build(cobj):
    cobj.do_checks()


@click.command()
@click.pass_obj
def srpm(cobj):
    cobj.build_srpm()


@click.command()
@click.pass_obj
def rpm(cobj):
    cobj.build_rpm()


@click.command()
@click.argument('packages', nargs=-1, type=click.Path(exists=True))
@click.pass_obj
def install(cobj, packages):
    cobj.install(packages)


@click.command()
@click.argument('command', default='bash')
@click.pass_obj
def shell(cobj, command):
    cobj.shell(command)


build.add_command(rpm)
build.add_command(srpm)
cli.add_command(init)
cli.add_command(clean)
cli.add_command(build)
cli.add_command(install)
cli.add_command(shell)
