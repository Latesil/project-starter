pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'project_starter')
gnome = import('gnome')

gnome.compile_resources('project-starter',
  'project_starter.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'project-starter.in',
  output: 'project-starter',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

project_starter_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'python_template.py',
  'rust_template.py',
  'c_template.py',
  'js_template.py',
  'gnome_extension_template.py',
  'keyboard_shortcuts.py',
  'about_window.py',
  'gpl.py',
  'mit.py',
  'apache.py',
  'lgpl.py',
  'agpl.py',
  'project_starter_constants.py',
  'template.py',
  'helpers.py',
  'file.py',
]

install_data(project_starter_sources, install_dir: moduledir)
