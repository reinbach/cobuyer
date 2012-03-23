from __future__ import with_statement
from fabric.api import *

env.app = 'cobuyer'
env.hosts = ['web1']
env.sites_dir = '/opt/sites/'
env.app_dir = env.sites_dir + env.app
#TODO change the repo to new github repo
env.repo = "http://hg.ironlabs.com/cobuyer"
env.nginx_conf_dir = "/opt/nginx/conf/sites/"

def install():
    """Installs app on server"""
    with settings(user="root"):
        run("virtualenv --distribute --no-site-packages -p python2 {app_dir}".format(app_dir=env.app_dir))
        with cd(env.app_dir):
            # clone repo
            run("hg clone {repo} master".format(repo=env.repo))
            with cd("master"):
                run("source {app_dir}/bin/activate && pip install -r requirements.txt".format(app_dir=env.app_dir))
                run("cp {app_dir}/master/nginx.conf {nginx_conf_dir}{app}.conf".format(
                    app_dir=env.app_dir,
                    nginx_conf_dir=env.nginx_conf_dir,
                    app=env.app
                ))
                with cd("{app}".format(app=env.app)):
                    with cd("settings"):
                        run("rm -f currentenv.py")
                        run("ln -s prod.py currentenv.py")
                    run("source {app_dir}/bin/activate && python manage.py syncdb".format(app_dir=env.app_dir))
                    run("source {app_dir}/bin/activate && python manage.py migrate".format(app_dir=env.app_dir))
                    run('source {app_dir}/bin/activate && python manage.py collectstatic -v0 --noinput')
        run("/etc/rc.d/uwsgi reload")
        run("/etc/rc.d/nginx reload")

def update():
    """Updates code base on server"""
    with settings(user="root"):
        with cd("{app_dir}/master".format(app_dir=env.app_dir)):
            run("hg pull && hg update")
            run("source {app_dir}/bin/activate && pip install -r requirements.txt".format(app_dir=env.app_dir))
            run("cp {app_dir}/master/nginx.conf {nginx_conf_dir}{app}.conf".format(
                app_dir=env.app_dir,
                nginx_conf_dir=env.nginx_conf_dir,
                app=env.app
            ))
            with cd("{app}".format(app=env.app)):
                run("source {app_dir}/bin/activate && python manage.py syncdb".format(app_dir=env.app_dir))
                run("source {app_dir}/bin/activate && python manage.py migrate".format(app_dir=env.app_dir))
                run('source {app_dir}/bin/activate && python manage.py collectstatic -v0 --noinput'.format(app_dir=env.app_dir))
        run("/etc/rc.d/uwsgi reload")
        run("/etc/rc.d/nginx reload")
