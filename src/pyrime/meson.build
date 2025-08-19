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
  'rime',
  [
    # https://github.com/mesonbuild/meson/issues/8693#issuecomment-2511060673
    configure_file(input: 'rime.pyi', output: 'rime.pyx', copy: true),
  ],
  dependencies: deps,
  subdir: 'pyrime',
  install: true,
  cython_args: ['-3I' + meson.current_build_dir()],
)
py.install_sources(
  [
    configure_file(input: '__init__.py', output: '__init__.py', configuration: conf_data),
    'rime.pyi',
    'py.typed',
    '__main__.py',
    'draw_ui.py',
  ],
  subdir: 'pyrime',
)
py.install_sources(
  [
    'prompt_toolkit/__init__.py',
    'prompt_toolkit/rime.py',
    'prompt_toolkit/gdb.py',
    'prompt_toolkit/terminfo.py',
  ],
  subdir: 'pyrime/prompt_toolkit',
)
py.install_sources(
  [
    'prompt_toolkit/utils/condition.py',
    'prompt_toolkit/utils/ansi.py',
    'prompt_toolkit/utils/insert.py',
    'prompt_toolkit/utils/prompt_style.py',
  ],
  subdir: 'pyrime/prompt_toolkit/utils',
)
py.install_sources(
  [
    'prompt_toolkit/plugins/__init__.py',
    'prompt_toolkit/plugins/autopair.py',
    'prompt_toolkit/plugins/autosuggestion.py',
    'prompt_toolkit/plugins/smartinput.py',
    'prompt_toolkit/plugins/viemacs.py',
  ],
  subdir: 'pyrime/prompt_toolkit/plugins',
)
py.install_sources(
  ['assets/json/keys.json', 'assets/json/modifiers.json'],
  subdir: 'pyrime/assets/json',
)
