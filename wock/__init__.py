import os
import click
from .utils import ContextObj


@click.group()
@click.option('--pkgname',
              help='Desired package name.\t[current directory name]')
@click.option('--release', envvar='WOCK',
              help='Desired release.\t[{}]'.format(os.environ.get('WOCK')))
@click.option('--architecture', default='x86_64',
              help='Desired architecture.\t[x86_64]')
@click.pass_context
def cli(context, pkgname, release, architecture):
    ''' A wrapper for mock. '''
    context.obj = ContextObj(pkgname, release, architecture)


@click.command()
@click.pass_obj
def init(cobj):
    ''' Initialize a chroot. '''
    cobj.init()


@click.command()
@click.pass_obj
def clean(cobj):
    ''' Purge the chroot. '''
    cobj.clean()


@click.group()
@click.pass_obj
def build(cobj):
    ''' Build a (s)rpm. '''
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
    ''' Install rpm inside chroot. '''
    cobj.install(packages)


@click.command()
@click.argument('command', default='bash')
@click.pass_obj
def shell(cobj, command):
    ''' Run command interactively inside chroot. '''
    cobj.shell(command)


build.add_command(rpm)
build.add_command(srpm)
cli.add_command(init)
cli.add_command(clean)
cli.add_command(build)
cli.add_command(install)
cli.add_command(shell)
