import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName

from vyperlogix.decorators.TailRecursive import tail_recursion

from vyperlogix.decorators.memoized import memoized

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

from vyperlogix.sf.abstract import SalesForceAbstract

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

from vyperlogix.trees.tinytree import tinytree
from vyperlogix.trees.tinytree.mixins import TinyTreeMixIn

class AccountTreeNode(tinytree.Tree,TinyTreeMixIn):
    def __init__(self, Id=None, Name=None, ParentId=None, children=None):
        tinytree.Tree.__init__(self, children)
        self.__Id__ = Id
        self.__Name__ = Name
        self.__ParentId__ = ParentId
        self.parent = None

    def __repr__(self):
        return "<%s> <%s> <%s>" % (self.Id,self.Name,self.ParentId)

    def _addChild(self, node):
        try:
            n = self.findForwards(Id=node.Id)
            if (n is None):
                n = self.findForwards(Id=node.ParentId)
                if (n is None):
                    root = self.getRoot()
                    root.addChild(node)
                else:
                    n.addChild(node)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string

    def Id():
        doc = "Id"
        def fget(self):
            return self.__Id__
        def fset(self, Id):
            self.__Id__ = Id
        return locals()
    Id = property(**Id())

    def Name():
        doc = "Name"
        def fget(self):
            return self.__Name__
        def fset(self, Name):
            self.__Name__ = Name
        return locals()
    Name = property(**Name())

    def ParentId():
        doc = "ParentId"
        def fget(self):
            return self.__ParentId__
        def fset(self, ParentId):
            self.__ParentId__ = ParentId
        return locals()
    ParentId = property(**ParentId())

######################################################################
from maglib.molten import roles

from vyperlogix.misc import _utils

from vyperlogix.classes.CooperativeClass import Cooperative
class MagmaAccountTree(Cooperative):
    def __init__(self,sfQuery,account,role=roles.MoltenPrivileges.Member,tree=AccountTreeNode(-1,"root",None)):
        '''
	account is the name of the account of the Id of the account.
	To-Do: Feed this object a COntact Id and let it figure-out the account for the contact.
	'''
        expected_class_name = ObjectTypeName._typeName(AccountTreeNode).split('.')[-1]
        got_class_name = ObjectTypeName.typeClassName(tree).split('.')[-1]
        self.__tree__ = tree if (expected_class_name == got_class_name) else None
        self.__role__ = role if (roles.isValidMoltenUserRole(role)) else None
        self.__sfQuery__ = sfQuery
        self.__accountId__ = None
        self.__account__ = None
        if (self.__tree__ is None):
            raise ValueError('Invalid value for tree attribute.')
        if (self.__role__ is None):
            raise ValueError('Invalid value for role attribute.')
        try:
            n = tree.findForwards(Id=account)
            if (n is not None):
                self.__accountId__ = n.Id
            else:
                n = tree.findForwards(Name=account)
                if (n is not None):
                    self.__accountId__ = n.Id
            if (self.__account__ is None) and (self.__accountId__ is not None):
                sf_accounts = SalesForceAccounts(self.sfQuery)
                accounts = sf_accounts.getAccountById(self.accountId)
                if (sf_accounts.contains_sf_objects(accounts)):
                    self.__account__ = accounts[0]
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        if (self.__account__ is None):
            raise ValueError('Invalid value for account attribute, account must be the Id or the Name of the account.')

    def role():
        doc = "role"
        def fget(self):
            return self.__role__
        def fset(self, role):
            if (roles.isValidMoltenUserRole(role)):
                self.__role__ = role
            else:
                raise ValueError('Invalid Molten User Role, cannot accept %s as a Valid Molten User Role.' % (str(role)))
        return locals()
    role = property(**role())

    def sfQuery():
        doc = "sfQuery"
        def fget(self):
            return self.__sfQuery__
        return locals()
    sfQuery = property(**sfQuery())

    def accountId():
        doc = "accountId"
        def fget(self):
            return self.__accountId__
        return locals()
    accountId = property(**accountId())

    def is_role_Partners():
        doc = "is_role_Partners"
        def fget(self):
            return roles.isPartnersMoltenUserRole(self.role)
        return locals()
    is_role_Partners = property(**is_role_Partners())

    def is_role_Member():
        doc = "is_role_Member"
        def fget(self):
            return roles.isMemberMoltenUserRole(self.role)
        return locals()
    is_role_Member = property(**is_role_Member())

    def is_role_SuperUser():
        doc = "is_role_SuperUser"
        def fget(self):
            return roles.isSuperUserMoltenUserRole(self.role)
        return locals()
    is_role_SuperUser = property(**is_role_SuperUser())

    def is_role_UserManager():
        doc = "is_role_UserManager"
        def fget(self):
            return roles.isUserManagerMoltenUserRole(self.role)
        return locals()
    is_role_UserManager = property(**is_role_UserManager())

    def tree():
        doc = "tree"
        def fget(self):
            return self.__tree__
        return locals()
    tree = property(**tree())

    def accounts():
        doc = "accounts based on the role"
        def fget(self):
            if (self.is_role_Partners or self.is_role_Member):
                return self.tree.findForwards(Id=self.accountId)
            elif (self.is_role_SuperUser):
                return self.tree.findForwards(Id=self.accountId)
            elif (self.is_role_UserManager):
                return self.tree.findForwards(Id=-1)
            return None
        return locals()
    accounts = property(**accounts())
######################################################################

class SalesForceAccounts(SalesForceAbstract):
    def __init__(self, sfQuery):
        self.__account_tree_cache__ = lists.HashedLists2()
        super(SalesForceAccounts, self).__init__(sfQuery,object_name='Account')

    def getAccountsByParentId(self,id): 
        soql="Select a.Id, a.ParentId, a.Name from Account a where a.ParentId='%s'" % id
        return self.sf_query(soql)

    def getAccountAncestors(self,account,ancestors=[]):
        '''Walk-up the tree collecting up all the parents until there are no more parents'''
        try:
            while (account['ParentId'] is not None):
                parents = self.getAccountById(account['ParentId'])
                for parent in parents:
                    ancestors.append(parent)
                    account = parent
        except:
            pass
        return ancestors

    @tail_recursion
    def _getAccountTree_(self,account,tree=[],skip_ancestors=False):
        '''Walk-up the tree look for the account that has no parent then locate all children.'''
        try:
            if (account['ParentId'] is None):
                tree.append(account)
                ancestors = [] # There cannot be any ancestors because this account has no parent and this makes the account the progenitor by default.
            else:
                ancestors = self.getAccountAncestors(account,ancestors=[])
            if (not skip_ancestors) and (len(ancestors) > 0):
                d_ancestors = lists.HashedLists2()
                for ancestor in ancestors:
                    d_ancestors[ancestor['ParentId']] = ancestor
                progenitor = d_ancestors[None]
                if (lists.isDict(progenitor)) and (len([node for node in tree if (node['Id'] == progenitor['Id'])]) == 0):
                    tree.append(progenitor)
                return self._getAccountTree_(progenitor,tree=tree,skip_ancestors=skip_ancestors)
            else:
                if (not lists.isDict(account)):
                    return tree
                children = self.getAccountsByParentId(account['Id'])
                for child in children:
                    if (lists.isDict(child)) and (len([node for node in tree if (node['Id'] == child['Id'])]) == 0):
                        tree.append(child)
                        self._getAccountTree_(child,tree=tree,skip_ancestors=True)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        return tree

    def getAccountTree(self,account,tree=[],skip_ancestors=False):
        '''Account tree in a list sorted by ParentId.'''
        _tree = self._getAccountTree_(account,tree=tree,skip_ancestors=skip_ancestors)
        d_tree = lists.HashedLists()
        for item in _tree:
            pid = item['ParentId']
            d_tree[pid if (pid is not None) else ''] = item
        for k,v in d_tree.iteritems():
            if (not isinstance(v,list)):
                v = [v]
            for _v in v:
                tree.append(_v)
        return tree

    def _getAccountTree(self,account,isDebug=False):
        '''Returns the Tree as a real "tree".'''
        root = AccountTreeNode(-1,"root",None)
        try:
            tree = self.getAccountTree(account)
            if (isDebug):
                from vyperlogix.misc.ReportTheList import reportTheList
                reportTheList(tree,'Account Tree')
            for node in tree:
                root._addChild(AccountTreeNode(node['Id'],node['Name'],node['ParentId']))
            root._addChild(AccountTreeNode(account['Id'],account['Name'],account['ParentId']))
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        return root

    def m_getAccountTree(self,account):
        '''Returns the Tree as a real "tree".'''
        if (self.__account_tree_cache__.has_key(account['Id'])):
            return self.__account_tree_cache__[account['Id']]
        tree = self._getAccountTree(account,isDebug=False)
        for t in tree.preOrder():
            self.__account_tree_cache__[t.Id] = tree
        return tree

    def getAccountSiblings(self,account,siblings=[]):
        '''Collect up all Accounts that have the same parent as the Account.'''
        try:
            parents = self.getAccountsByParentId(account['ParentId'])
            for parent in parents:
                if (parent['ParentId'] is not None):
                    siblings.append(parent)
        except:
            pass
        return siblings

    def getAccountById(self,id):
	_names = self.names
        soql = "Select %s from Account a where a.Id = '%s'" % (', '.join(_names),id)
        return self.sf_query(soql)

    def getAccountsByIds(self,ids):
	_names = self.names
	_ids = ["'%s'" % (id) for id in ids]
	s_ids = ','.join(_ids)
        soql = "Select %s from Account a where a.Id in %s" % (', '.join(_names),s_ids)
        return self.sf_query(soql)

    def getAccountByName(self,name):
	_names = self.names
        soql = "Select %s from Account a where a.Name = '%s'" % (', '.join(_names),name)
        return self.sf_query(soql)

    def getAccountsLikeName(self,name):
	_names = self.names
        soql = "Select %s from Account a where a.Name LIKE '%%%s%%'" % (', '.join(_names),name)
        return self.sf_query(soql)

if (__name__ == "__main__"):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    #n2 = AccountTreeNode(-1,"root",None)
    #n2._addChild(AccountTreeNode("123456","One",None))
    #n2._addChild(AccountTreeNode("234567","Two",None))

    #n2._addChild(AccountTreeNode("123","one","123456"))
    #n2._addChild(AccountTreeNode("234","two","123456"))
    #n2._addChild(AccountTreeNode("123a","one","234567"))
    #n2._addChild(AccountTreeNode("234a","two","234567"))
    #n2.dump()

    from maglib.salesforce.cred import credentials
    from maglib.salesforce.auth import magma_molten_passphrase

    _use_staging = False

    __sf_account__ = credentials(magma_molten_passphrase,0 if (not _use_staging) else 1)

    from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
    sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

    sf_login_model.isStaging = _use_staging
    sf_login_model.perform_login_appropriately()

    if (sf_login_model.isLoggedIn):
        print 'Logged-in Successfully.'

        from vyperlogix.sf.sf import SalesForceQuery
        sfQuery = SalesForceQuery(sf_login_model)

        sf_accounts = SalesForceAccounts(sfQuery)
        accounts = sf_accounts.getAccountsLikeName('Toshiba')
        if (isinstance(accounts,list)):
            for account in accounts:
                tree = sf_accounts._getAccountTree(account)
                print 'BEGIN: (%s) %s (%s)' % (account['Id'],account['Name'],account['ParentId'])
                tree.dump()
                print 'END!'
                print '-'*40
                n = tree.findForwards(Id=account['Id'])
                if (n is not None):
                    n.dump()
                else:
                    print '()'
                print '='*40
                print 'BEGIN: MoltenPrivileges.Member'
                mat = MagmaAccountTree(sfQuery,account['Id'],role=roles.MoltenPrivileges.Member,tree=tree)
                accounts = mat.accounts
                if (accounts is not None):
                    accounts.dump()
                print 'END!  MoltenPrivileges.Member'
                print '\n'
                print 'BEGIN: MoltenPrivileges.Super_User'
                mat.role = roles.MoltenPrivileges.Super_User
                accounts = mat.accounts
                if (accounts is not None):
                    accounts.dump()
                print 'END!  MoltenPrivileges.Super_User'
                print '\n'
                print 'BEGIN: MoltenPrivileges.User_Manager'
                mat.role = roles.MoltenPrivileges.User_Manager
                accounts = mat.accounts
                if (accounts is not None):
                    accounts.dump()
                print 'END!  MoltenPrivileges.User_Manager'
                print '\n'
        pass
    else:
        print >>sys.stderr, sf_login_model.lastError
        print str(sf_login_model)

