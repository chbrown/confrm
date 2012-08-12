from paste.deploy import loadapp
application = loadapp('config:development.ini', relative_to='.')
