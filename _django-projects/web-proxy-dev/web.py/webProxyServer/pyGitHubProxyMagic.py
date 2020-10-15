from vyperlogix.github.GithubMagicObject import GitHubMagicProxy

if (__name__ == '__main__'):
    from vyperlogix import github
    
    __github_client_id__ = 'd89bfe797d057ded5bcd'
    __github_client_secret__ = 'dd0e228521ee0e09d666d5102c7cf5d16954b234'
    g = GitHubMagicProxy('raychorn', 'peekab00', 'http://127.0.0.1:9909', client_id=__github_client_id__, client_secret=__github_client_secret__)
    print 'g.github_userid=%s' % (g.github_userid)
    uri = g.uri
    print 'uri=%s' % (uri)
    username = g.username
    print 'username=%s' % (username)
    password = g.password
    print 'password=%s' % (password)
    client_id = g.client_id
    print 'client_id=%s' % (client_id)
    client_secret = g.client_secret
    print 'client_secret=%s' % (client_secret)
    user = g.github.get.user()
    print 'user=%s' % (user)
    print 'user_id=%s' % (user.user__id)
    print 'user_email=%s' % (user.user__email)

    keys = g.github.get.user.keys().keys
    print 'keys=%s' % (keys)

    repos = g.github.get.user.repos().repos
    print 'repos=%s' % (repos)
    repos_available = g.github.get.user.repos.available().available
    print 'repos_available=%s' % (repos_available)
    new_name = 'My Repo Name'
    new_repo_name = github.normalize_repo_name(new_name)
    if (not any([r._name == new_repo_name for r in repos])):
        repos = g.github.user.repos.create('My Repo Name')
        print 'repos=%s' % (repos)
