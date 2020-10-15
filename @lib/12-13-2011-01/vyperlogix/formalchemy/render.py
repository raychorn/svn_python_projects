from formalchemy import templates
from formalchemy import FieldSet

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

class HTMLTableEngine(templates.TemplateEngine):
    def get_filename(self, name):
        pass
    
    def get_template(self, name, **kw):
        pass
    
    def render(self, template_name, **kw):
        return 'It works !'
    
class MyFieldSet(FieldSet):
    @staticmethod
    def _render(self,fieldset=None,**kwargs):
        pass

    @staticmethod
    def prettify(self,name):
        pass
    
from formalchemy import fields
from formalchemy import helpers as h
from vyperlogix.classes.CooperativeClass import Cooperative

class TextFieldRenderer(Cooperative,fields.TextFieldRenderer):
    """render a field as a text field"""
    def __init__(self, field):
        super(TextFieldRenderer, self).__init__(field)
    
    def render(self, **kwargs):
        kwargs['size'] = 40
        return h.text_field(self.name, value=self._value, maxlength=self.length, **kwargs)
    
class NameFieldRenderer(Cooperative,fields.TextFieldRenderer):
    """render a field as a text field"""
    def __init__(self, field):
        super(NameFieldRenderer, self).__init__(field)
    
    def render(self, **kwargs):
        kwargs['size'] = 60
        return h.text_field(self.name, value=self._value, maxlength=self.length, **kwargs)
    
class EmailAddressFieldRenderer(Cooperative,fields.TextFieldRenderer):
    """render a field as a text field"""
    def __init__(self, field):
        super(EmailAddressFieldRenderer, self).__init__(field)
    
    def render(self, **kwargs):
        kwargs['size'] = 60
        return h.text_field(self.name, value=self._value, maxlength=self.length, **kwargs)
