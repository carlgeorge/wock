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


@click.command()
@click.option('--just-srpm', is_flag=True, help='Only build the srpm.')
@click.pass_obj
def build(cobj, just_srpm):
    ''' Build an rpm inside the chroot. '''
    cobj.build(just_srpm)


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


cli.add_command(init)
cli.add_command(clean)
cli.add_command(build)
cli.add_command(install)
cli.add_command(shell)
