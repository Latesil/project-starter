project('project-starter',  
          version: '0.1.5',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

appname = 'com.github.Latesil.project-starter'

i18n = import('i18n')


subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
