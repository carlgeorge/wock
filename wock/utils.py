import pathlib
import subprocess
import click


class ContextObj():
    def __init__(self, pkgname, release, architecture):
        self._base = pathlib.Path.cwd()
        self.pkgname = pkgname or self._base.name
        self.release = release
        self.architecture = architecture

    def setup(self):
        if self.release is None:
            err = ('Undefined release.\n\nSet the release either with the '
                   '"--release" flag or by setting the environment variable '
                   'WOCK.\n\nExample:\nexport WOCK=el6\n')
            raise click.ClickException(err)
        mockdir = pathlib.Path('/etc/mock')
        pattern = '{}?{}.cfg'.format(self.release, self.architecture)
        configs = list(mockdir.glob(pattern))
        if len(configs) == 0:
            raise click.ClickException('no matching mock configs found')
        if len(configs) > 1:
            err = 'multiple matching mock configs found'
            for config in configs:
                err += '\n'
                err += config.as_posix()
            raise click.ClickException(err)
        self._mockcfg = configs[0]
        self.mockcfg = self._mockcfg.as_posix()
        self.root = self._mockcfg.stem

    def build_setup(self):
        self._sources = self._base / 'SOURCES'
        if not self._sources.is_dir():
            self._sources.mkdir()
        self.sources = self._sources.as_posix()

        self._results = self._base / 'MOCK' / self.root
        if not self._results.is_dir():
            self._results.mkdir(parents=True)
        self.results = self._results.as_posix()

        self._spec = self._base / 'SPECS' / (self.pkgname + '.spec')
        if not self._spec.exists():
            err = 'spec file {} does not exist'.format(self.spec)
            raise click.ClickException(err)
        self.spec = self._spec.as_posix()

    def get_sources(self):
        command = ['spectool',
                   '--directory', self.sources,
                   '--get-files', self.spec]
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    @property
    def srpm(self):
        command = ['rpm',
                   '--define', 'dist .{}'.format(self.release),
                   '--query',
                   '--queryformat', '%{name}-%{version}-%{release}\n',
                   '--specfile', self.spec]
        output = subprocess.check_output(command,
                                         universal_newlines=True,
                                         stderr=subprocess.DEVNULL)
        srpm_name = output.split('\n')[0] + '.src.rpm'
        self._srpm = self._results / srpm_name
        if self._srpm.exists():
            return self._srpm.as_posix()
        else:
            err = 'srpm {} does not exist'.format(self._srpm)
            raise click.ClickException(err)

    def _run(self, command):
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              bufsize=1,
                              universal_newlines=True) as process:
            for line in process.stdout:
                print(line, end='')

    def init(self):
        self.setup()
        command = ['mock', '--root', self.root, '--init']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def clean(self):
        self.setup()
        command = ['mock', '--root', self.root, '--clean']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def install(self, packages):
        self.setup()
        command = ['mock', '--root', self.root, '--install']
        command.extend(packages)
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def shell(self, task):
        self.setup()
        command = ['mock', '--root', self.root, '--shell', task]
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def build(self, just_srpm):
        self.setup()
        self.build_setup()
        self.get_sources()

        command = ['mock',
                   '--root', self.root,
                   '--define', 'dist .{}'.format(self.release),
                   '--buildsrpm',
                   '--spec', self.spec,
                   '--sources', self.sources,
                   '--resultdir', self.results,
                   '--no-clean',
                   '--no-cleanup-after']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

        if not just_srpm:
            command = ['mock',
                       '--root', self.root,
                       '--define', 'dist .{}'.format(self.release),
                       '--rebuild', self.srpm,
                       '--spec', self.spec,
                       '--sources', self.sources,
                       '--resultdir', self.results,
                       '--no-clean',
                       '--no-cleanup-after']
            click.secho(' '.join(command), fg='cyan')
            self._run(command)
