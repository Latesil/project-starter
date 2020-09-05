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
  'templates/python_template.py',
  'templates/rust_template.py',
  'templates/c_template.py',
  'templates/js_template.py',
  'templates/gnome_extension_template.py',
  'keyboard_shortcuts.py',
  'about_window.py',
  'licenses/gpl.py',
  'licenses/mit-x11.py',
  'licenses/apache.py',
  'licenses/lgpl.py',
  'licenses/agpl.py',
  'project_starter_constants.py',
  'common_files.py',
  'templates/template.py',
  'helpers.py',
  'file.py',
]

install_data(project_starter_sources, install_dir: moduledir)
