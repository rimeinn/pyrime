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
    'key.py',
    'rime.py',
    'session.py',
    'utils.py',
  ],
  subdir: 'pyrime',
)
py.install_sources(
  [
    'ime/__init__.py',
    'ime/ime.py',
    'ime/key.py',
    'ime/ui.py',
  ],
  subdir: 'pyrime/ime',
)
py.install_sources(
  [
    'ptpython/gdb.py',
    'ptpython/layout.py',
    'ptpython/formatted_text.py',
    'ptpython/ime.py',
    'ptpython/rime.py',
  ],
  subdir: 'pyrime/ptpython',
)
py.install_sources(
  [
    'nvim/__init__.py',
    'nvim/keymap.py',
    'nvim/rime.py',
    'nvim/win.py',
  ],
  subdir: 'pyrime/nvim',
)
py.install_sources(
  [
    'ptpython/utils/ansi.py',
    'ptpython/utils/prompt_style.py',
  ],
  subdir: 'pyrime/ptpython/utils',
)
py.install_sources(
  [
    'ptpython/bindings/__init__.py',
    'ptpython/bindings/rime.py',
    'ptpython/bindings/autopair.py',
    'ptpython/bindings/autosuggestion.py',
    'ptpython/bindings/smartinput.py',
    'ptpython/bindings/viemacs.py',
    'ptpython/bindings/extra.py',
    'ptpython/bindings/autocorrect.py',
    'ptpython/bindings/autoinsert.py',
  ],
  subdir: 'pyrime/ptpython/bindings',
)
py.install_sources(
  ['assets/json/keys.json', 'assets/json/modifiers.json'],
  subdir: 'pyrime/assets/json',
)
