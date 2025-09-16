rime_dep = dependency('rime')
deps = [rime_dep]
# ubuntu jammy
if meson.version().version_compare('<=0.61.2')
  py = import('python').find_installation()
  python_dep = dependency('python3')
  deps += [python_dep]
else
  py = import('python').find_installation(pure: false)
endif

conf_data = configuration_data()
conf_data.set(
  'PROJECT_VERSION',
  meson.project_version(),
  description: 'project version',
)
header_path = run_command('pkg-config', '--variable=includedir', 'rime', check: true).stdout().strip() + '/rime_api.h'
configure_file(command: ['autopxd', header_path, 'rime_api.pxd'], output: 'rime_api.pxd')

py.extension_module(
  'api',
  [
    # https://github.com/mesonbuild/meson/issues/8693#issuecomment-2511060673
    configure_file(input: 'api.pyi', output: 'api.pyx', copy: true),
  ],
  dependencies: deps,
  subdir: 'pyrime',
  install: true,
  cython_args: ['-3I' + meson.current_build_dir()],
)
py.install_sources(
  [
    configure_file(input: '__init__.py', output: '__init__.py', configuration: conf_data),
    '__main__.py',
    'py.typed',
    'api.pyi',
    'dirs.py',
    'key.py',
    'rime.py',
    'session.py',
    'ui.py',
  ],
  subdir: 'pyrime',
)
py.install_sources(
  [
    'ptpython/__init__.py',
    'ptpython/rime.py',
    'ptpython/gdb.py',
  ],
  subdir: 'pyrime/ptpython',
)
py.install_sources(
  [
    'ptpython/utils/ansi.py',
    'ptpython/utils/insert.py',
    'ptpython/utils/prompt_style.py',
  ],
  subdir: 'pyrime/ptpython/utils',
)
py.install_sources(
  [
    'ptpython/plugins/__init__.py',
    'ptpython/plugins/autopair.py',
    'ptpython/plugins/autosuggestion.py',
    'ptpython/plugins/smartinput.py',
    'ptpython/plugins/viemacs.py',
  ],
  subdir: 'pyrime/ptpython/plugins',
)
py.install_sources(
  ['assets/json/keys.json', 'assets/json/modifiers.json'],
  subdir: 'pyrime/assets/json',
)
