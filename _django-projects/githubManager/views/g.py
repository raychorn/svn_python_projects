import logging

import settings

from vyperlogix.misc import _utils

from vyperlogix.github.GithubMagicObject import GitHubMagicProxy

__github_client_id__ = 'd89bfe797d057ded5bcd'
__github_client_secret__ = 'dd0e228521ee0e09d666d5102c7cf5d16954b234'

def github(request):
    from views.models import GitHubUser
    from users.views import get_user
    __user__ = get_user(request)
    if (not __user__.is_anonymous()):
	try:
	    githubuser = GitHubUser.objects.get(user=__user__)
	except:
	    githubuser = None
	if (githubuser):
	    from vyperlogix.crypto import blowfish
	    from vyperlogix.misc import hex
	    from github import Github
	    
	    e = hex.hexToStr(githubuser.password)
	    p = blowfish.noramlize(blowfish.decryptData(e, __user__.email))
	    return (githubuser,GitHubMagicProxy(githubuser.username, p, 'http://%s'%(settings.GITHUB_PROXY), client_id=__github_client_id__, client_secret=__github_client_secret__))
    return None,None

def get_githubuser_and_available_repos(request,documents=None):
    try:
	repos = []
	commits = []
	matches = []
	newrepos = []
	githubuser, __g__ = github(request)
	if (githubuser):
	    try:
		repos = [r for r in __g__.github.get.user.repos().repos]
	    except Exception, ex:
		info_string = _utils.formattedException(details=ex)
		logging.exception('#1')
	    if (documents):
		from vyperlogix.classes.SmartObject import SmartObject
		__r__ = dict([(r._name,r) for r in repos])
		for doc in documents:
		    d = SmartObject(doc)
		    if (__r__.has_key(d.docfile_repo_name)):
			__d__ = dict([(d.docfile_repo_name,__r__[d.docfile_repo_name]),(d.docfile_fname,__r__[d.docfile_repo_name])])
			matches.append(__d__)
	    for r in repos:
		try:
		    commits.append(([commit for commit in r.get_commits()],r))
		except:
		    pass
		pass
	    newrepos = [c for c in commits if (len(c[0]) == 0)]
	    for m in matches:
		try:
		    r = m[m.keys()[0]]
		    c = [commit for commit in r.get_commits()]
		except:
		    c = None
		if (not c) or (len(c) == 0):
		    newrepos.append((c,r))
	    pass
    except Exception, ex:
	info_string = _utils.formattedException(details=ex)
	logging.exception('#2')
	githubuser, __g__, newrepos, repos, matches = (githubuser,__g__,[],[],{})
    return githubuser, __g__, newrepos, repos, matches

if (__name__ == '__main__'):
    pass
    