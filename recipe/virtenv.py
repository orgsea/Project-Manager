import sys
import os
import logging
import imp
import virtualenv
import subprocess

class Virtenv(object):
    """
    Recipe to setup a vitualenv and install needed packages listed in the buildout.cfg file.

    Options available for buildout recipe config file:
      location - the location where the virtualenv gets created
      
      site-packages - a boolean value True if including site-packages found in the system wide python env.  If not present will default to False.
      
      use-distribute - boolean value whether it uses distribute to install packages with.  If false will use setuptools.  Defaults to False if not present.

      requirements-file - the location of the requirements file which pip reads and installs any packages listed in it.  See pip docs for more info

      install - a line delimited list of packages to install.  Similar to the format of requirements file.

      
    """
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger(self.name)

    ###
    #recipe required methods
    ###
        
    def install(self):
        """
        The required install method for buildout recipes which will set up the virtualenv and install any packages wanted into it.
        """
        self.logger.info('install: ' + str(self.name))
        bin_dir = self.buildout['buildout']['bin-directory']
        self.pip_cmd = self._location() + '/bin/pip'
        self.python_cmd = self._location() + '/bin/python'
        self.buildout_path = bin_dir+'/buildout'
        self.buildout_args = sys.argv[1:]
        
        
        if not os.path.exists(self.pip_cmd) and not os.path.exists(self.python_cmd):
            self.logger.info('creating virtualenv')
            self._setup()
            self._create_virtual()
            #self._teardown()
            
            with open(self.buildout_path) as f:
                if not self.python_cmd in f.readline():
                    self._reboot_buildout()
        else:
            self.logger.info('installing python packages')
            #self._activate_virtualenv()
            
            
            with open(self.buildout_path) as f:
                if not self.python_cmd in f.readline():
                    self._reboot_buildout()
                else:
                    if self._requirements_file():
                        self._install_from_requirements_file()
                    if self._install_list():
                        self._install_modules_list()
            

        #Return an empty tuple. If we returned path to virtualenv
        #everytime a change happened the directory will be deleted.
        #By this stage buildout is running under that environment,
        #and this absence will cause untold errors as files are not
        #found.
        return ()


    def update(self):
        """
        update method required for buildout recipes.  Currently does nothing.
        """
        self.logger.info('Virtenv update')


    ###
    #Environment setup and teardown for installing virtualenv
    ###
    
    def _setup(self):
        """
        Sets up the environment to allow virtualenv to work properly
        
        Removes the environment variable PYTHONPATH
        Sets sys.path to have the system libraries directory as the first item
        """
        #import buildouts custom site module to reload later
        import site

        #Put the system wide path back at the start of the sys.path.
        #This should be the path which holds the system wide modules
        #which includes site.py.
        path = sys.prefix
        for npath in sys.path:
            if npath.startswith(sys.prefix) and \
                   os.path.exists(npath):
                path = npath
                break

        #setting the path to include the above path as the first item
        #in the list. This will ensure that next time site.py is loaded
        #it is the system wide one, not buildouts version.
        sys.path[0:0] = [
            path,
            ]

        #remove the shell environment PYTHONPATH if it exists
        if 'PYTHONPATH' in os.environ:
            self.oldpythonpath = os.environ['PYTHONPATH']
            del os.environ['PYTHONPATH']

        #reload the site module so that the it is set to the system wide
        #one now.  If we don't do this then the buildout version will be
        #continued to be used.  It seems to use this one even in modules
        #loaded after the python path has been reset.
        imp.reload(site)
        
        #prove that the site module is the system wide one.
        site_location_path = str(site.__file__)
        if site_location_path.endswith('py'):
            site_location_path = site_location_path[:-8]
        else:
            site_location_path = site_location_path[:-9]

        assert site_location_path == path, 'site is not in ' + path + \
               ' it is ' + site_location_path


    def _teardown(self):
        """
        Restore python and system environment to the original state
        
        resets original buildout PYTHONPATH as it was before
        resets to the buildout sys.path
        """
        import site

        #remove first entry in path serach for modules by python
        #del sys.path[0]

        #self.logger.info(sys.path)

        #restore old environment PYTHONPATH if it existed
        if getattr(self, 'oldpythonpath'):
            os.environ['PYTHONPATH'] = self.oldpythonpath

        imp.reload(site)
        self.logger.info(str(site.__file__))

    ###
    #virtualenv creation and setup methods
    ###


    def _create_virtual(self):
        """
        Creates the virtualenv
        """
        
        location = self._location()
        site_packages = self._site_packages()
        use_distribute = self._use_distribute()
        self.logger.info('location = ' + str(location))
        self.logger.info('site-packages = ' + str(site_packages))
        self.logger.info('use-distribute = ' + str(use_distribute))

        sys.prefix = location
        sys.real_prefix = os.sep.join(sys.path[0].split(os.sep)[:-2])
        virtualenv.create_environment(location,
                                      site_packages=site_packages,
                                      use_distribute=use_distribute)


        return location


    def _activate_virtualenv(self):
        """
        Does the equivalent of source location/bin/activate using location/bin/activate_this.py by calling execfile(this_file, dict(__file__=this_file)) where this_file is location/bin/activate_this.py
        """
        import site
        activate_location = self._location() + '/bin/activate_this.py'
        location = self._location()
        del sys.path[:]
        exec(compile(open(activate_location).read(), activate_location, 'exec'), dict(__file__=activate_location))
        #pathback = sys.path
        path = [path for path in sys.path
                if path.startswith(location) or
                not path.endswith('site-packages')]
        del sys.path[:]
        sys.path.extend(path)
        tmp = [os.sep.join(path.split(os.sep)[:-1])
               for path in sys.path if path.endswith('site-packages')]
        
        sys.path.extend(tmp)

        
        self.logger.info('sys.path is now ' + str(sys.path))
        path = self._location() + '/bin'
        old_path = os.environ['PATH']
        os.environ['PATH'] = path + ':' + old_path
        imp.reload(os)
        imp.reload(site)
        


    def _reboot_buildout(self):
        #rerun bootstrap to recreate bin/buildout with
        #the virtualenf python as the interpreter
        buildout_dir = self.buildout['buildout']['directory']
        bootstrap_path = buildout_dir + '/bootstrap.py'
        cmd_list = [self.python_cmd,]
        if os.path.exists(bootstrap_path):
            cmd_list.append(bootstrap_path)
            #cmd_list.extend(self.buildout_args)
        else:
            cmd_list.append(self.buildout_path)
            cmd_list.extend(self.buildout_args)
            cmd_list.append('bootstrap')
        subprocess.call(cmd_list)

        #rerun buildout if it isn't running under the
        #virtualenv interpreter
        self.logger.info(sys.executable)
        if sys.executable != self.python_cmd:
            cmd_list = [self.buildout_path]
            cmd_list.extend(self.buildout_args)
            self.logger.info('Rebooting buildout')
            subprocess.call(cmd_list)
            
            sys.exit()

        
        
        pass


    ###
    #module install methods defined here
    ###

    def _install_from_requirements_file(self):
        """
        Install modules into this virtualenv from a requirements file found through an entry through the buildout.cfg
        """
        requirements_file = self._requirements_file()
        self.logger.info(str(requirements_file))
        self.logger.info(os.environ['PATH'])
        import pip
        initial_args = ['install',
                        '--requirement='+requirements_file,
                        ]
        downloads_dir = self._downloads_dir()
        if downloads_dir:
            initial_args.append('--download-cache='+downloads_dir)
        with open(requirements_file) as f:
            self.logger.info('installing\n\n' + f.read())
        pip.main(initial_args=initial_args)



    def _install_modules_list(self):
        """
        Install modules from a line delimited list found through buildout.cfg
        """
        installs = self._install_list()
        initial_args=[]
        
        downloads_dir = self._downloads_dir()
        if downloads_dir:
            initial_args.append('--download-cache='+downloads_dir)
        import pip
        for install in installs:
            self.logger.info('installing ' + install)
            args = ['install', install]
            args.extend(initial_args)
            pip.main(initial_args=args)
            

        self.logger.info('sys.path is ' + str(sys.path))

    ###
    #Getter methods for recipe variables
    ###


    def _target_site_packages_directory(self):
        """
        Returns the location of the site-packages directory for this virtualenv.
        """
        for location in sys.path:
            if location.startswith(sys.prefix) and \
               location.endswith('site-packages') and \
               os.path.exists(location):
                return location


    def _location(self):
        """
        Retrieves and the location where the virtualenv will be installed
        """
        if 'location' in self.options:
            return self.options['location']
        else:
            return self.buildout['buildout']['directory'] + '/parts/venv'



    def _site_packages(self):
        """
        Finds and returns if site-packages will be used or not.  Defaults to False id not set in buildout.cfg
        """
        return 'site-packages' in self.options and \
               self.options['site-packages'].lower() == 'true'


    def _use_distribute(self):
        """
        Finds and returns if distribute will be used or not.  Defaults to False if not set.
        """
        return 'use-distribute' in self.options and \
               self.options['use-distribute'].lower() == 'true'


    def _requirements_file(self):
        """
        returns the requirements file location as a string if requirements option exists, False otherwise
        """
        return 'requirements-file' in self.options and \
               self.options['requirements-file']


    def _install_list(self):
        """
        returns a list of modules to install if install option exists, False otherwise
        """
        return 'install' in self.options and \
               (str(x).strip() for x in self.options['install'].split(os.linesep))
    

    
        
    def _downloads_dir(self):
        """
        returns a directory to download packages to.  False if option not present
        """
        return 'downloads-dir' in self.options and \
               self.options['downloads-dir']
    
