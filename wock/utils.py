import pathlib
import subprocess
import click


class ContextObj():
    def __init__(self, pkgname, release, architecture):
        self._base = pathlib.Path.cwd()
        self.pkgname = pkgname or self._base.name

        if release:
            self.release = release
        else:
            err = ('Undefined release.\n\nSet the release either with the '
                   '"--release" flag or by setting the environment variable '
                   'WOCK.\n\nExample:\nexport WOCK=el6\n')
            raise click.ClickException(err)
        self.architecture = architecture

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

        self._sources = self._base / 'SOURCES'
        self.sources = self._sources.as_posix()

        self._results = self._base / 'MOCK' / self.root
        self.results = self._results.as_posix()

        self._spec = self._base / 'SPECS' / (self.pkgname + '.spec')
        self.spec = self._spec.as_posix()

    def do_checks(self):
        if not self._sources.is_dir():
            self._sources.mkdir()
        if not self._results.is_dir():
            self._results.mkdir(parents=True)
        if not self._spec.exists():
            err = 'spec file {} does not exist'.format(self.spec)
            raise click.ClickException(err)
        command = ['spectool',
                   '--directory', self.sources,
                   '--get-files', self.spec]
        self._run(command)

    def get_srpm_name(self):
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
        self.srpm = self._srpm.as_posix()
        if self._srpm.exists():
            return self.srpm
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
        command = ['mock', '--root', self.root, '--init']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def clean(self):
        command = ['mock', '--root', self.root, '--clean']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def install(self, packages):
        command = ['mock', '--root', self.root, '--install']
        command.extend(packages)
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def shell(self, task):
        command = ['mock', '--root', self.root, '--shell', task]
        click.secho(' '.join(command), fg='cyan')
        self._run(command)

    def build_srpm(self):
        # rpmbuild-md5 -D "dist ${DIST}" --define='_topdir %(pwd)' --nodeps
        # -bs ${SPEC}
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

    def build_rpm(self):
        # mock "${MACROS[@]}" --root ${MOCKCFG} --resultdir=MOCK
        # --no-cleanup-after --rebuild MOCK/${SRPM}
        command = ['mock',
                   '--root', self.root,
                   '--define', 'dist .{}'.format(self.release),
                   '--rebuild', self.get_srpm_name(),
                   '--spec', self.spec,
                   '--sources', self.sources,
                   '--resultdir', self.results,
                   '--no-clean',
                   '--no-cleanup-after']
        click.secho(' '.join(command), fg='cyan')
        self._run(command)
