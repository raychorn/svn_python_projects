import os, sys
import shutil

import re
import compileall

import stat

import random

from datetime import datetime

from functions import delete_recursive, copy_folders_background, background_copytree, __utility_Q__join

from misc import callersName, get_function_name

from misc import formattedException

from __utils import find_postgresql_in, get_process_by_name, get_parent_pid_for, terminate_postgres
from __utils import __postgresexe__, terminate

from myobjects import MDict

__is_building_ce__ = False

__pound_src__ = __pgsql_src__ = "C:/#kbrwyle-development/#source"

if (__is_building_ce__):
    __src__ = __pgsql_src__
else:
    __src__ = "C:/#kbrwyle-development/#source-pcat-karp/trunk"

release_number = '.32'

ce_name = 'CostEstimator'
ce_version = "%s_1-0.7.0%s" % (ce_name, release_number)

pcat_name = 'PCAT'
pcat_version = "%s+3.2.8.0%s" % (pcat_name, release_number)

__url__ = "http://127.0.0.1:8000?a=%d" % (random.randint(9999, 99999))

__const__copy__ = ' - Copy'

import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.FileHandler',
              'formatter': 'f',
              'level': logging.DEBUG,
              'filename': os.path.sep.join([os.path.abspath('.'),os.path.splitext(os.path.basename(__file__))[0]+'_'+datetime.now().strftime("%m-%d-%Y_%H-%M-%S")+'.log']),
              }
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

dictConfig(logging_config)

logger = logging.getLogger()

def onerror(*args):
    f, fpath, err = args
    
    logger.debug('DEBUG: %s --> err = %s' % (get_function_name(), err))
    if (err.find('The directory is not empty') > -1):
        for dirpath, dirnames, filenames in os.walk(fpath):
            for f in filenames:
                pass

def compile_all(fpath):
    fpaths = [fpath]
    for fp in fpaths:
        logger.info('DEBUG: compile_all.1 --> compile_all("%s")' % (fp))
        compileall.compile_dir(fpath, rx=re.compile(r'[/\\][.]svn'), force=True)
    
def configure_product(fpath, alt=None):
    __has_copied_sources__ = False
    files = [f for f in os.listdir(fpath if (__is_building_ce__) else alt) if (f.lower().startswith('start_') and f.lower().endswith('.cmd'))]
    for f in files:
        fname = 'Start_%s.cmd' % ('CostEstimator' if (__is_building_ce__) else 'PCAT')
        if (f != fname):
            oldname = os.sep.join([fpath, f])
            newname = os.sep.join([fpath, fname])
            if (alt) and (not os.path.exists(oldname)):
                shutil.copyfile(os.sep.join([alt, f]), os.sep.join([fpath, f]))
            try:
                os.rename(oldname, newname)
            except:
                logger.warning('Are we maybe trying to rename "%s" --> "%s" more than once?' % (oldname, newname))
            fname = newname
        else:
            fname = os.sep.join([fpath, fname])
        
        if (__is_building_ce__):
            if (fpath.find(pcat_version) > -1):
                oldname = fname
                newname = fname.replace(ce_name, pcat_name)
                try:
                    os.rename(oldname, newname)
                except:
                    logger.warning('Are we maybe trying to rename "%s" --> "%s" more than once?' % (oldname, newname))
                fname = newname
            
        fIn = open(fname, mode='r')
        line = fIn.read()
        fIn.close()
        
        toks = line.split()
        toks2 = [t for t in toks[-1].split('"%~dp0') if (len(t) > 0)]
        pgsql_cmd = toks2[0].split('"')[0]
        pgsql_cmd_fpath = os.sep.join([fpath, pgsql_cmd])
        logger.info('DEBUG: configure_product.1 --> pgsql_cmd_fpath=%s' % (pgsql_cmd_fpath))

        ###########################################
        def __ignore_files__(src, names, criteria = ['.svn', '.7z']):
            filenames = []
            __is__ = any([(str(src).find(c) > -1) for c in criteria])
            if (logger):
                logger.info('__ignore_files__.1 --> "%s" --> %s (%s)' % (src, criteria, __is__))
            if (__is__):
                filenames = [f for f in names if (not any([f.endswith(c) for c in criteria]))]
            if (logger):
                logger.info('__ignore_files__.2 --> %s' % (filenames))
            return filenames
        ###########################################
        
        if (not __has_copied_sources__):
            __deployment_dst__ = fpath
            __svn__ = os.sep.join(['', '.svn']).replace(os.sep,'/')
            __chrome__ = os.sep.join(['', 'chrome']).replace(os.sep,'/')
            __PostgreSQL__ = os.sep.join(['', 'PostgreSQL']).replace(os.sep,'/')
            __Python__ = os.sep.join(['', 'Python']).replace(os.sep,'/')
            logger.info('DEBUG: configure_product.1.1 --> __svn__=%s' % (__svn__))
            logger.info('DEBUG: configure_product.1.2 --> __chrome__=%s' % (__chrome__))
            logger.info('DEBUG: configure_product.1.3 --> __PostgreSQL__=%s' % (__PostgreSQL__))
            logger.info('DEBUG: configure_product.1.4 --> __Python__=%s' % (__Python__))
            for dirpath, dirnames, filenames in os.walk(__pound_src__, topdown=True):
                dst_fpath = os.sep.join([__deployment_dst__, dirpath.replace(__pound_src__, '')]).replace(os.sep+os.sep,os.sep).replace(os.sep,'/')
                logger.info('DEBUG: configure_product.1.4.1 --> dst_fpath=%s' % (dst_fpath))
                if (not os.path.exists(dst_fpath)) and (dst_fpath.find(__svn__) == -1):
                    logger.info('DEBUG: configure_product.1.4.2 --> dst_fpath=%s' % (dst_fpath))
                    if (dst_fpath.find(__chrome__) > -1) or (dst_fpath.find(__PostgreSQL__) > -1) or (dst_fpath.find(__Python__) > -1): 
                        logger.info('DEBUG: configure_product.1.5 --> COPY dirpath=%s to dst_fpath=%s' % (dirpath, dst_fpath))
                        shutil.copytree(dirpath, dst_fpath, ignore=__ignore_files__)
                        continue
                    logger.info('DEBUG: configure_product.1.6 --> dst_fpath=%s' % (dst_fpath))
            ###############################################################################################################
            if (os.path.exists(pgsql_cmd_fpath)):
                logger.info('DEBUG: configure_product.1.1.1 --> pgsql_cmd_fpath=%s' % (pgsql_cmd_fpath))
                parts = list(os.path.splitext(pgsql_cmd_fpath))
                parts[0] = parts[0] + '_new'
                new_pgsql_cmd_fpath = ''.join(parts)
                fIn = open(pgsql_cmd_fpath, mode='r')
                fOut = open(new_pgsql_cmd_fpath, mode='w')
                for line in fIn:
                    ignore_line = False
                    extra_lines = []
                    is_rem_start = (line.find('REM start "KBRWyle SERVER"') > -1)
                    is_start_without_rem = (line.find('start "KBRWyle SERVER"') > -1)
                    is_start_chrome = (line.find('start "Chrome Browser"') > -1)
                    if ( is_rem_start or is_start_without_rem ):
                        if (line.find('python.exe') > -1):
                            if (line.find('runserver') > -1):
                                line = line.replace('REM start ', 'start ')
                                #extra_lines.append('start "Chrome Browser" "%~dp0..\..\..\chrome\App\Chrome-bin\chrome.exe" %s' % (__url__))
                            else:
                                ignore_line = True
                    if (is_start_chrome):
                        line = line.replace(__url__.split('?')[0], __url__)
                    if (not ignore_line):
                        print >> fOut, line.rstrip()
                        for e in extra_lines:
                            print >> fOut, e
                        extra_lines = []
                fIn.close()
                fOut.flush()
                fOut.close()
                
                os.remove(pgsql_cmd_fpath)
                os.rename(new_pgsql_cmd_fpath, pgsql_cmd_fpath)
                
                pgsql_cmd_fpath_dirname = os.path.dirname(pgsql_cmd_fpath)
                pgsql_cmd_copy_fpath = os.sep.join([pgsql_cmd_fpath_dirname, 'pgsql - Copy.cmd'])
                if (os.path.exists(pgsql_cmd_copy_fpath)):
                    os.remove(pgsql_cmd_copy_fpath)
                pgsql_cmd_copy_fpath = os.sep.join([pgsql_cmd_fpath_dirname, '@pgsql.cmd'])
                if (os.path.exists(pgsql_cmd_copy_fpath)):
                    os.remove(pgsql_cmd_copy_fpath)
                    
                logger.info('DEBUG: configure_product.2 --> compile_all("%s")' % (pgsql_cmd_fpath_dirname))
                compile_all(pgsql_cmd_fpath_dirname)
                files = [os.sep.join([pgsql_cmd_fpath_dirname, f]) for f in os.listdir(pgsql_cmd_fpath_dirname) if (f.endswith('.py'))]
                for f in files:
                    os.remove(f)
                ####################################################################################################
                utils_base_fpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pgsql_cmd_fpath))))
                dirs = dict([tuple([f, os.sep.join([utils_base_fpath, f])]) for f in os.listdir(utils_base_fpath) if (f not in ['chrome', 'Launcher']) and (not any([(f.lower().find(t.lower()) > -1) for t in ['postgre', 'python']]))])
                for dirpath, dirnames, filenames in os.walk(utils_base_fpath, topdown=True):
                    valids = [d for d in dirnames if (dirs.has_key(d))]
                    logger.debug('(###) valids=%s' % (valids))
                    logger.debug('(###) dirs=%s' % (dirs))
                    logger.debug('(###) dirnames=%s' % (dirnames))
                    break
                ###
                for aDir in valids:
                    utils_cmd_fpath = os.sep.join([os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pgsql_cmd_fpath)))), aDir])
                    if (os.path.exists(utils_cmd_fpath)):
                        # copy the two source files required for this section...
                        source_files = ['analyze_perdiem.py', 'myobjects.py']
                        ignore_source_files = ['analyze_perdiem.py', 'start_analyze_perdiem.cmd']
                        source_files = [os.sep.join([os.path.abspath('.'), f]) for f in source_files if (f not in ignore_source_files)]
                        logger.info('DEBUG: source_files --> "%s".' % (', '.join(source_files)))
                        source_files_actual = [f for f in source_files if (os.path.exists(f)) and (os.path.isfile(f))]
                        logger.info('DEBUG: source_files_actual --> "%s".' % (', '.join(source_files_actual)))
                        ignore_source_files_actual = [os.sep.join([utils_cmd_fpath, f]) for f in ignore_source_files]
                        if (len(source_files_actual) > 0):
                            for f in source_files_actual:
                                dst = os.sep.join([utils_cmd_fpath, os.path.basename(f)])
                                logger.info('Copying "%s" --> "%s".' % (f, dst))
                                shutil.copyfile(f, dst)
                        else:
                            logger.warning('Cannot find the following: "%s".' % (', '.join(source_files)))
                        logger.info('DEBUG: (***) ignore_source_files_actual --> "%s".' % (', '.join(ignore_source_files_actual)))
                        logger.info('DEBUG: (***) ignore_source_files_actual --> "%s".' % (len(ignore_source_files_actual)))
                        if (len(ignore_source_files_actual) > 0):
                            for f in ignore_source_files_actual:
                                if (f.endswith('.py')):
                                    f.replace('.py', '.pyc')
                                logger.info('DEBUG: delete? --> "%s".' % (f))
                                if (os.path.exists(f)):
                                    logger.info('DEBUG: delete! --> "%s".' % (f))
                                    os.remove(f)
                        logger.info('DEBUG: configure_product.3 --> compile_all("%s")' % (utils_cmd_fpath))
                        compile_all(utils_cmd_fpath)
                        remove_source_files_from(utils_cmd_fpath, logger=logger, bypass=True)
                    else:
                        logger.warning('Cannot find the directory in "%s".' % (utils_cmd_fpath))
                ####################################################################################################
                launcher_cmd_fpath = os.sep.join([os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pgsql_cmd_fpath)))), 'Launcher'])
                if (os.path.exists(launcher_cmd_fpath)):
                    logger.info('DEBUG: configure_product.4 --> compile_all("%s")' % (launcher_cmd_fpath))
                    compile_all(launcher_cmd_fpath)
                    names = [os.sep.join([launcher_cmd_fpath, f]) for f in os.listdir(launcher_cmd_fpath) if (f.endswith('.py') and (not f.endswith('.pyc')))]
                    for fp in names:
                        logger.info('DEBUG: --> compile_all("%s")' % (fp))
                        compileall.compile_file(fp, ddir=launcher_cmd_fpath, force=1)
                    remove_source_files_from(launcher_cmd_fpath, logger=logger)
                else:
                    logger.warning('Cannot find the utils directory in "%s".' % (launcher_cmd_fpath))
                ####################################################################################################
                paths = MDict()
                backend_base_fpath = utils_base_fpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pgsql_cmd_fpath))))
                dirs = dict([tuple([f, os.sep.join([utils_base_fpath, f])]) for f in os.listdir(utils_base_fpath) if (any([(f.lower().find(t.lower()) > -1) for t in ['postgre', 'python']]))])
                for k,fpath in dirs.iteritems():
                    for dirpath, dirnames, filenames in os.walk(fpath, topdown=True):
                        dlls = [f.lower() for f in filenames if (f.lower().endswith('.dll'))]
                        cmds = [f.lower() for f in filenames if (f.lower().endswith('.cmd'))]
                        if (len(dlls) > 0):
                            paths['dlls'] = dirpath.replace(backend_base_fpath+"\\", "%~dp0..\\")
                            logger.debug('DLL path --> "%s".' % (dirpath))
                            for dll in dlls:
                                logger.debug('DLL --> "%s".' % (dll))
                            logger.debug('='*40)
                        if (len(cmds) > 0):
                            paths['cmds'] = dirpath
                            logger.debug('CMD path --> "%s".' % (dirpath))
                            for c in cmds:
                                logger.debug('CMD --> "%s".' % (c))
                            logger.debug('='*40)
                #logger.info('DEBUG: --> DLL paths --> "%s".' % (paths))
                logger.debug('backend_base_fpath --> "%s".' % (backend_base_fpath))
                fname = os.sep.join([backend_base_fpath, 'PATH.TXT'])
                fOut = open(fname, 'w')
                print >> fOut, 'set PATH=%s;' % (';'.join(paths.get('dlls', [])))
                fOut.flush()
                fOut.close()
                logger.debug('PATH.TXT --> "%s".' % (fname))

            __has_copied_sources__ = True

    ####################################################################################################
    logger.info('DEBUG: configure_product.5 --> fpath=%s' % (fpath))
    
    ###########################################
    dirs_to_delete = [os.sep.join([__deployment_dst__, d]) for d in os.listdir(__deployment_dst__) if (d.find('.svn') > -1)]
    for d in dirs_to_delete:
        logger.info('DEBUG: configure_product.9 --> rmtree=%s' % (d))
        shutil.rmtree(d)

def remove_source_files_from(fpath, logger=None, bypass=False):
    fpaths = [fpath]
    
    for fp in fpaths:
        removed = 0
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            if (dirpath.find('.backend') == -1):
                msg = 'BEGIN: %s' % (dirpath)
                if (logger):
                    logger.info(msg)
                else:
                    print msg
                if (dirpath.endswith("\Sinthia\static")):
                    pcat_fpath = os.sep.join([dirpath, pcat_name.lower()])
                    ce_fpath = os.sep.join([dirpath, 'ce'])
                    if (dirpath.find(ce_name) > -1) and (os.path.exists(pcat_fpath)):
                        msg = '\tREMOVE: "%s".' % (pcat_fpath)
                        if (logger):
                            logger.info(msg)
                        else:
                            print msg
                        shutil.rmtree(pcat_fpath)
                    elif (dirpath.find(pcat_name) > -1) and (os.path.exists(ce_fpath)):
                        msg = '\tREMOVE: "%s".' % (ce_fpath)
                        if (logger):
                            logger.info(msg)
                        else:
                            print msg
                        shutil.rmtree(ce_fpath)
    
                if (dirpath.endswith("\.svn")):
                    delete_recursive(dirpath, topdown=False)
    
                files = [f for f in filenames if (os.path.splitext(f)[-1] in ['.py', '.gz'])]
                for f in files:
                    msg = '\tREMOVE: "%s".' % (f)
                    if (logger):
                        logger.info(msg)
                    else:
                        print msg
                    os.remove(os.sep.join([dirpath, f]))
                    removed += 1
                msg = 'END!!! %s' % (dirpath)
                if (logger):
                    logger.info(msg)
                else:
                    print msg
            elif (bypass) or ( (dirpath.find('utils') > -1) or (dirpath.find('Launcher') > -1) ):
                files = [f for f in filenames if (os.path.splitext(f)[-1] in ['.py', '.gz'])]
                for f in files:
                    msg = '\tREMOVE: "%s".' % (f)
                    if (logger):
                        logger.info(msg)
                    else:
                        print msg
                    os.remove(os.sep.join([dirpath, f]))
                    removed += 1
                msg = 'END!!! %s' % (dirpath)
                if (logger):
                    logger.info(msg)
                else:
                    print msg
        
        msg = 'Removed %s files.' % (removed)
        if (logger):
            logger.info(msg)
        else:
            print msg

def rename_fixtures_from(fpath, make_invisible=False):
    fpaths = [fpath]
    
    for fp in fpaths:
        removed = 0
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            if (dirpath.endswith('fixtures') > -1):
                print 'BEGIN: %s' % (dirpath)
    
                files = [f for f in filenames if (os.path.splitext(f)[-1] in ['.py', '.gz'])]
                for f in files:
                    print '\tREMOVE: "%s".' % (f)
                    os.remove(os.sep.join([dirpath, f]))
                    removed += 1
                print 'END!!! %s' % (dirpath)
        
        print 'Removed %s files.' % (removed)

def touch(path):
    import os, time
    now = time.time()
    try:
        os.utime(path, (now, now))
    except os.error:
        pass
        
def touch_files_in(fpath):
    for dirpath, dirnames, filenames in os.walk(fpath, topdown=True):
        files = [f for f in filenames]
        for f in files:
            touch(os.sep.join([dirpath, f]))
    
def touch_files_in_using(fpath, token=None, callback=None):
    logger.debug('touch_files_in_using :: fpath --> %s, token=%s, callback=%s' % (fpath, token, callback))
    for dirpath, dirnames, filenames in os.walk(fpath, topdown=True):
        files = [f for f in filenames if (token) and (f.find(token) > -1)]
        dirs = [f for f in dirnames if (token) and (f.find(token) > -1)]
        if (len(files) > 0):
            logger.debug('touch_files_in_using :: files --> %s' % (files))
        for f in files:
            if (callable(callback)):
                try:
                    callback(os.sep.join([dirpath, f]), token=token)
                except Exception, details:
                    logger.exception(formattedException(details=details))
        if (len(dirs) > 0):
            logger.debug('touch_files_in_using :: dirs --> %s' % (dirs))
        for d in dirs:
            if (callable(callback)):
                try:
                    callback(os.sep.join([dirpath, d]), token=token)
                except Exception, details:
                    logger.exception(formattedException(details=details))
    
def make_archive(dest, src):
    import zipfile
    
    print 'BEGIN ZIP:'
    with zipfile.ZipFile(dest,
                         "w",
                         zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zf:
        for root, _, filenames in os.walk(src, topdown=True):
            for name in filenames:
                name = os.path.join(root, name)
                name = os.path.normpath(name)
                toks = name.split(os.sep)
                while ( (toks[1].find(ce_name) == -1) and (toks[1].find(pcat_name) == -1) ):
                    for i in xrange(1,len(toks)):
                        if (toks[i].find(ce_name) > -1) or (toks[i].find(pcat_name) > -1):
                            break
                        else:
                            del toks[i]
                            break
                arch_name = os.sep.join(toks)
                #print 'ZIP: "%s" --> "%s".' % (name, arch_name)
                zf.write(name, arch_name)
    print 'END ZIP!!!'
    
def kill_process_by_name(procName):
    import psutil
    
    for proc in psutil.process_iter():
        if (proc.name() == procName):
            print 'kill_process_by_name :: Killing process "%s".' % (proc.name())
            proc.kill()
            break

def get_process_by_pid(pid):
    import psutil
    
    for proc in psutil.process_iter():
        if (proc.pid == pid):
            return proc.name(), proc.pid

def kill_postgresql(exename):
    kill_process_by_name(exename)
    
def find_Sinthia_in(fpath):
    fpaths = [fpath]
    
    response = {}
    for fp in fpaths:
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            #logger.info('DEBUG: find_Sinthia_in.1 --> dirpath=%s' % (dirpath))
            if (dirpath.find('Sinthia') > -1):
                #logger.info('DEBUG: find_Sinthia_in.2 --> dirpath=%s' % (dirpath))
                response['Sinthia'] = dirpath
                break
    logger.info('DEBUG: find_Sinthia_in.3 --> response=%s' % (response))
    return response

def find_managepy_in(fpath):
    fpaths = [fpath]
    
    response = {}
    for fp in fpaths:
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            #logger.info('DEBUG: find_managepy_in.1 --> dirpath=%s' % (dirpath))
            for f in filenames:
                #logger.info('DEBUG: find_managepy_in.2 --> f=%s' % (f))
                if ( (f.find('manage.py') > -1) or (f.find('manage.pyc') > -1) ):
                    #logger.info('DEBUG: find_managepy_in.3 --> f=%s' % (f))
                    response['manage.py'] = os.sep.join([dirpath, f])
                    break
    logger.info('DEBUG: find_managepy_in.4 --> response=%s' % (response))
    return response

def find_sitepackages_in(fpath):
    fpaths = [fpath]
    
    response = {}
    for fp in fpaths:
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            #logger.info('DEBUG: find_sitepackages_in.1 --> dirpath=%s' % (dirpath))
            if (dirpath.find('site-packages') > -1):
                #logger.info('DEBUG: find_sitepackages_in.2 --> dirpath=%s' % (dirpath))
                response['site-packages'] = dirpath
                break
    logger.info('DEBUG: find_sitepackages_in.3 --> response=%s' % (response))
    return response

def find_pythonexe_in(fpath):
    fpaths = [fpath]
    
    response = {}
    for fp in fpaths:
        for dirpath, dirnames, filenames in os.walk(fp, topdown=True):
            for f in filenames:
                if (f.find('python.exe') > -1):
                    response['python.exe'] = os.sep.join([dirpath, f])
                    break
    return response

def run_system_cmd(cmd, handler=None, onError=None, onBeforeExit=None):
    from popen import Shell
    import _utils
    
    s = Shell([cmd], shell=None, env=None, isExit=False, isWait=False, isVerbose=False, fOut=handler, onError=onError)
    if (callable(onBeforeExit)):
        try:
            onBeforeExit(s)
        except Exception, ex:
            if (callable(onError)):
                onError(ex)
    s.doSendWithTail('exit')


skip_cleanup = True
skip_copy = False
skip_config = False
skip_compilation = False
skip_archive = True
skip_ce = False if (__is_building_ce__) else True
skip_pcat = False
skip_flush = True

ignore_fixtures = True

if (__name__ == '__main__'):
    if (__is_building_ce__):
        deployment_root = os.sep.join([os.path.dirname(__src__), '##builds'])
    else:
        deployment_root = os.sep.join([os.path.dirname(os.path.dirname(__src__)), '##builds'])
    if (not os.path.exists(deployment_root)):
        os.mkdir(deployment_root)
    deployment_ce_root = os.sep.join([deployment_root, ce_version])
    deployment_pcat_root = os.sep.join([deployment_root, pcat_version])
    
    ce_file_version_number = 1
    pcat_file_version_number = 1
    while (1):
        if (os.path.exists(deployment_ce_root)):
            version_extent = '(%s)' % (ce_file_version_number)
            deployment_ce_root = os.sep.join([deployment_root, ce_version+version_extent])
            ce_file_version_number += 1
        elif (os.path.exists(deployment_pcat_root)):
                version_extent = '(%s)' % (pcat_file_version_number)
                deployment_pcat_root = os.sep.join([deployment_root, pcat_version+version_extent])
                pcat_file_version_number += 1
        else:
            logger.info('INFO: deployment_ce_root --> "%s".' % (deployment_ce_root))
            logger.info('INFO: deployment_pcat_root --> "%s".' % (deployment_pcat_root))
            break
    
    response = find_postgresql_in(os.sep.join([__pgsql_src__, '.backend']))
    
    pg_ctl = response.get('pg_ctl.exe', '')
    pg_data = response.get('PGDATA', '')
    pg_log = response.get('PGLOG', '')
    fpath = os.sep.join([os.path.dirname(__file__), 'start_db.cmd'])
    fpath1 = os.sep.join([os.path.dirname(__file__), 'status_db.cmd'])
    fpath2 = os.sep.join([os.path.dirname(__file__), 'status_db.txt'])
    fpath3 = os.sep.join([os.path.dirname(__file__), 'kill_db.cmd'])
    fpath4 = os.sep.join([os.path.dirname(__file__), 'flush_db.cmd'])
    fpath5 = os.sep.join([os.path.dirname(__file__), 'loadmetadata.cmd'])
    fpath6 = os.sep.join([os.path.dirname(__file__), 'start_db_init.cmd'])

    if (0):
        if (ignore_fixtures):
            rename_fixtures_from(sinthia_fpath, make_invisible=True)
    
        if (ignore_fixtures):
            rename_fixtures_from(sinthia_fpath, make_invisible=False)

    terminate_postgres(fpath3, exename=__postgresexe__, verbose=True, pg_ctl=pg_ctl)

    fOut = open(fpath, 'w')
    print >> fOut, '@echo off\n'
    cmd = '"%s" start -w -t 15 -D "%s" -l "%s"' % (pg_ctl, pg_data, pg_log)
    print >> fOut, cmd
    fOut.flush()
    fOut.close()
    
    start_db_state = 0
    
    def start_db_handler(msg):
        global start_db_state
        
        if ( (start_db_state == 0) and (msg.find('waiting for server to start') > -1) ):
            start_db_state = 1
        elif ( (start_db_state == 1) and (msg.find('done') > -1) ):
            start_db_state = 2
        elif ( (start_db_state == 2) and (msg.find('server started') > -1) ):
            start_db_state = 3
        logger.debug('DEBUG: %s --> %s' % (get_function_name(), msg))
        
    def start_db_error_handler(err):
        global start_db_state

        start_db_state = -1

        logger.debug('DEBUG: %s --> %s' % (get_function_name(), err))
        

    cmd = fpath
    print 'Start postgreSQL...\n\t%s' % (cmd)
    run_system_cmd(cmd, handler=start_db_handler, onError=start_db_error_handler)
    
    if (start_db_state == 3):
        logger.debug('DEBUG: %s --> Database started !!!' % (get_function_name()))
    
    fOut = open(fpath1, 'w')
    print >> fOut, '@echo off\n'
    cmd = '"%s" status -D "%s"' % (pg_ctl, pg_data)
    print >> fOut, cmd
    fOut.flush()
    fOut.close()
    
    status_db_state = None
    
    def status_db_handler(msg):
        global status_db_state
        
        if (status_db_state is None):
            if (msg.find('pg_ctl:') > -1) and (msg.find('server is running') > -1) and (msg.find('PID:') > -1):
                pid = msg.split('(')[-1].split(')')[0].split(':')[-1].strip()
                if (str(pid).isdigit()):
                    pid = int(pid)
                    procname, procpid = get_process_by_pid(pid)
                    if (procname and procpid):
                        procppid, process_tree = get_parent_pid_for(__postgresexe__)
                        if (procppid == procpid):
                            status_db_state = tuple([procname, procpid])
        logger.debug('DEBUG: %s --> %s' % (get_function_name(), msg))
        

    cmd = fpath1
    print 'Status postgreSQL...\n\t%s' % (cmd)
    response = run_system_cmd(cmd, handler=status_db_handler)

    if (not isinstance(status_db_state, tuple)):
        print 'WARNING: database is not running... please correct this and retry.'
        terminate()
        
    #################################

    def status_db_init_handler(msg):
        logger.debug('DEBUG: %s --> %s' % (get_function_name(), msg))

    if (not os.path.exists(fpath6)) or (not os.path.isfile(fpath6)):
        print 'Cannot find "%s". Please correct and retry.' % (fpath6)
        terminate()
        
    cmd = fpath6
    print 'Initialize Db...\n\t%s' % (cmd)
    response = run_system_cmd(cmd, handler=status_db_init_handler)

    #################################

    response = find_pythonexe_in(os.sep.join([__pgsql_src__, '.backend']))

    pythonexe = response.get('python.exe', None)
    if (not pythonexe):
        print 'WARNING: Cannot find python.exe... please correct this and retry.'
        terminate()

    response = find_Sinthia_in(__src__)

    Sinthia = response.get('Sinthia', None)
    if (not Sinthia):
        print 'WARNING: Cannot find Sinthia... please correct this and retry.'
        terminate()

    response = find_managepy_in(Sinthia)

    managepy = response.get('manage.py', None)
    if (not managepy):
        print 'WARNING: Cannot find manage.py... please correct this and retry.'
        terminate()

    response = find_sitepackages_in(os.path.dirname(pythonexe))
    sitepackages = response.get('site-packages', None)
    if (not sitepackages):
        print 'WARNING: Cannot find site-packages... please correct this and retry.'
        terminate()
        
    fOut = open(fpath4, 'w')
    print >> fOut, '@echo off\n'
    cmd = '"%s" "%s" flush --noinput' % (pythonexe, managepy)
    # add unit tests here to ensure the fixtures are in the Db...
    print >> fOut, cmd
    fOut.flush()
    fOut.close()
    
    flush_db_state = None
    
    def flush_db_handler(msg):
        global flush_db_state
        
        if (flush_db_state is None):
            pass
        logger.debug('DEBUG: %s --> %s' % (get_function_name(), msg))
        
    def respond_to_flush(aShell):
        if (0):
            aShell.doSendWithTail('yes')
            import time
            time.sleep(15)
        
    if (not skip_flush):
        cmd = fpath4
        print 'Flush database...\n\t%s' % (cmd)
        response = run_system_cmd(cmd, handler=flush_db_handler, onBeforeExit=respond_to_flush)

    metadata_json = os.sep.join([os.path.dirname(managepy), 'meta', 'fixtures', 'initial_data.json'])
    
    if (os.path.exists(metadata_json) and os.path.isfile(metadata_json)):
        fOut = open(fpath5, 'w')
        print >> fOut, '@echo off\n'
        cmd = '"%s" "%s" loaddata "%s"' % (pythonexe, managepy, metadata_json)
        print >> fOut, cmd
        fOut.flush()
        fOut.close()
    
    load_metadata_state = None
    
    def load_metadata_handler(msg):
        global load_metadata_state
        
        if (load_metadata_state is None):
            pass
        logger.debug('DEBUG: %s --> %s' % (get_function_name(), msg))
        
    def respond_to_load_metadata(aShell):
        if (0):
            aShell.doSendWithTail('yes')
            import time
            time.sleep(15)
        
    if (not skip_flush):
        cmd = fpath5
        print 'Load metadata...\n\t%s' % (cmd)
        response = run_system_cmd(cmd, handler=load_metadata_handler, onBeforeExit=respond_to_load_metadata)

    terminate_postgres(fpath3, exename=__postgresexe__, verbose=True, pg_ctl=pg_ctl)
   
    if (not skip_copy):
        if (not skip_cleanup):
            if (os.path.exists(deployment_ce_root)):
                if (os.path.isdir(deployment_ce_root)):
                    delete_recursive(deployment_ce_root, ignore_errors=True, onerror=onerror, topdown=False)
                else:
                    os.remove(deployment_ce_root)
        
            if (os.path.exists(deployment_pcat_root)):
                if (os.path.isdir(deployment_pcat_root)):
                    delete_recursive(deployment_pcat_root, ignore_errors=True, onerror=onerror)
                else:
                    os.remove(deployment_pcat_root)
        
        criteria = ['.svn', '.7z']

        def is_folder_copyable(fpath, logger=None):
            __is__ = not any([(str(fpath).find(c) > -1) for c in criteria])
            if (logger):
                logger.info('is_folder_copyable.2 --> "%s" --> %s (%s)' % (fpath, criteria, __is__))
            return __is__
        
        def ignore_files(src, names):
            filenames = []
            __is__ = any([(str(src).find(c) > -1) for c in criteria])
            if (logger):
                logger.info('ignore_files.1 --> "%s" --> %s (%s)' % (src, criteria, __is__))
            if (__is__):
                filenames = [f for f in names if (not any([f.endswith(c) for c in criteria]))]
            if (logger):
                logger.info('ignore_files.2 --> %s' % (filenames))
            return filenames

        copy_folders = lambda src, dst : copy_folders_background(src, dst, ignore=ignore_files, logger=logger, topdown=False, callback=is_folder_copyable, simulation=False)
        if (not skip_ce):
            print 'BEGIN: COPY: "%s" --> "%s".' % (__src__, deployment_ce_root)
            background_copytree(__src__, deployment_ce_root, ignore=ignore_files, simulation=False, logger=logger)
            print 'END!!! COPY: "%s" --> "%s".' % (__src__, deployment_ce_root)
    
        if (not skip_pcat):
            print 'BEGIN: COPY: "%s" --> "%s".' % (__src__, deployment_pcat_root)
            background_copytree(__src__, deployment_pcat_root, ignore=ignore_files, simulation=False, logger=logger)
            print 'END!!! COPY: "%s" --> "%s".' % (__src__, deployment_pcat_root)
            
        __utility_Q__join(logger=logger)
            
    if (not skip_config):
        if (not skip_ce):
            configure_product(deployment_ce_root)
        if (not skip_pcat):
            configure_product(deployment_pcat_root, alt=__pgsql_src__)
        
    if (not skip_compilation):
        if (not skip_ce):
            if (__is_building_ce__):
                sinthia_fpath = os.sep.join([deployment_ce_root, Sinthia])
            else:
                sinthia_fpath = deployment_ce_root
            backend_svn_fpath = os.sep.join([deployment_ce_root, '.backend', '.svn'])
            logger.info('DEBUG: --> compile_all("%s")' % (sinthia_fpath))
            compile_all(sinthia_fpath)
            remove_source_files_from(sinthia_fpath)
            delete_recursive(backend_svn_fpath, ignore_errors=True, onerror=onerror, topdown=False)
            backend_svn_fpath_root = os.path.dirname(backend_svn_fpath)
            files = [os.sep.join([backend_svn_fpath_root, f]) for f in os.listdir(backend_svn_fpath_root) if (f.find('.7z') > -1)]
            for f in files:
                logger.info('Deleting "%s".' % (f))
                os.remove(f)
        if (not skip_pcat):
            if (__is_building_ce__):
                sinthia_fpath = os.sep.join([deployment_pcat_root, Sinthia])
            else:
                sinthia_fpath = os.sep.join([deployment_pcat_root, 'Sinthia'])
            backend_svn_fpath = os.sep.join([deployment_pcat_root, '.backend', '.svn'])
            launcher_fpath = os.sep.join([deployment_pcat_root, '.backend', 'Launcher'])
            utils_fpath = os.sep.join([deployment_pcat_root, '.backend', 'utils'])
            pgsql_fpath = os.sep.join([deployment_pcat_root, '.backend', 'PostgreSQLPortable_9.6.1'])
            logger.info('DEBUG: --> compile_all("%s")' % (sinthia_fpath))
            compile_all(sinthia_fpath)
            remove_source_files_from(sinthia_fpath)
            compile_all(launcher_fpath)
            remove_source_files_from(launcher_fpath)
            compile_all(utils_fpath)
            remove_source_files_from(utils_fpath)
            compile_all(pgsql_fpath)
            remove_source_files_from(pgsql_fpath)
            delete_recursive(backend_svn_fpath, ignore_errors=True, onerror=onerror, topdown=False)
            backend_svn_fpath_root = os.path.dirname(backend_svn_fpath)
            files = [os.sep.join([backend_svn_fpath_root, f]) for f in os.listdir(backend_svn_fpath_root) if (f.find('.7z') > -1)]
            for f in files:
                logger.info('Deleting "%s".' % (f))
                os.remove(f)

    def callback_handle_file_or_dir(fpath, token=None):
        if (os.path.exists(fpath)):
            if (os.path.isfile(fpath)):
                logger.info('*** Removing single file via fpath="%s" using token="%s".' % (fpath, token))
                os.remove(fpath)
            elif (os.path.isdir(fpath)):
                logger.info('*** Removing directory via fpath="%s" using token="%s".' % (fpath, token))
                shutil.rmtree(fpath, ignore_errors=True)
    
    logger.info('BEGIN: touch_files_in_using.')
    touch_files_in_using(deployment_pcat_root, token=__const__copy__, callback=callback_handle_file_or_dir)
    logger.info('END!!! touch_files_in_using.')
                
    if (not skip_archive):
        archive_fpath = os.sep.join([deployment_root, ce_version + '.zip'])
        touch_files_in(deployment_ce_root)
        make_archive(archive_fpath, deployment_ce_root)
    print 'DONE !!!'
    terminate()
    