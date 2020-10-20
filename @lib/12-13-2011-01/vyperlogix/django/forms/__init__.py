import sys

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.misc import ObjectTypeName

from vyperlogix.html import myOOHTML as oohtml

import fields

from vyperlogix.django import captcha

from vyperlogix.django import django_utils

from vyperlogix.classes.CooperativeClass import Cooperative

from django.utils.datastructures import SortedDict as SortedDictFromList

from vyperlogix.mail.validateEmail import validateEmail

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
class DjangoForm(Cooperative):
    '''This class handles all aspects of the life-cycle for a Django Form based on a Django Model.'''
    def __init__(self, request, name, model, action, target='_top'):
        self.__model_choice_fields = lambda self:[field for field in [self.fields[k] for k in self.fields.keyOrder] if self.is_ModelChoiceField(field)]
        self.__model__ = model
        self.__form_name__ = name
        self.__target__ = target
        self.__action__ = action
	self.__request__ = request
        self.__datasources__ = lists.HashedLists2() # datasource specifies the source of data for any given field name.
        self.__fields__ = fields.fields_for_model(model)
        self.__model_choice_fields__ = self.__model_choice_fields(self)
        self.__d_model_choice_fields__ = lists.HashedFuzzyLists2()
        for field in self.__model_choice_fields__:
            self.__d_model_choice_fields__[field.label] = field
        self.__choice_models__ = lists.HashedLists2()
        self.__choice_model_defaults__ = lists.HashedLists2()
        self.__last_error__ = ''
        self.__use_captcha__ = False
	self.__captcha_form_name__ = None
	self.__captcha_font_name__ = None
	self.__captcha_font_size__ = 18
	self.__captcha_choices__ = ''.join(chr(ch) for ch in xrange(ord('A'),ord('Z')+1))
	self.__captcha_fill__ = (255,255,255)
	self.__captcha_bgImage__ = 'bg.jpg'
	self.__get_freehost_by_name__ = None
        self.__datetime_field_content__ = ''
        self.__submit_button_title__ = 'Submit Button Title'
        self.__submit_button_value__ = 'Submit Button Value'
        self.__field_validations__ = [] # list of tuples where first element is a lambda and the second element is a dict that connects context elements to error messages when validation fails.
        self.__hidden_fields__ = lists.HashedLists2()
        self.__field_ordering__ = [] # list of field names to be used to render the fields as HTML.
        self.__extra_fields__ = lists.HashedLists2()
        
    def get_model_choice_field_by_name(self,field_name):
        '''returns a ModelChoiceField for a field by name'''
        return self.__d_model_choice_fields__[field_name]
        
    def get_choice_model_default_for_field_by_name(self,field_name):
        '''returns a string value that represents a choice default for a ModelChoiceField'''
        return self.__choice_model_defaults__[field_name]
        
    def set_choice_model_default_for_field_by_name(self,field_name,choice_model_default):
        '''choice_model_default is a string value that represents a choice default for a ModelChoiceField'''
        self.__choice_model_defaults__[field_name] = choice_model_default
        
    def get_choice_model_for_field_by_name(self,field_name):
        '''returns a choice_model that is a Smart Object that holds a value_id and text_id, each of which refers to field name for an object that populates a <select>'''
        return self.__choice_models__[field_name]
        
    def set_choice_model_for_field_by_name(self,field_name,choice_model):
        '''choice_model is a Smart Object that holds a value_id and text_id, each of which refers to field name for an object that populates a <select>'''
        self.__choice_models__[field_name] = choice_model
        
    def get_datasource_for_field_by_name(self,field_name):
        '''returns a datasource that is a pointer to a function that returns a list of records'''
        return self.__datasources__[field_name]
        
    def set_datasource_for_field_by_name(self,field_name,datasource):
        '''datasource is a pointer to a function that returns a list of records'''
        self.__datasources__[field_name] = datasource
	
    def add_hidden_field(self,field_name,field_value):
        '''add fields that are hidden for record identifcation'''
        self.__hidden_fields__[field_name] = field_value
	
    def add_extra_field(self,field_name,field_value):
        '''add fields that are carried along to the object being saved, works for SITE_ID and other types of data.'''
        self.__extra_fields__[field_name] = field_value
	
    def get_fields_by_name(self,name):
	fields = []
        for field_name in self.fields.keyOrder:
	    if (field_name == name):
		aField = self.fields[field_name]
		fields.append(aField)
	return fields
        
    def is_BooleanField(self,obj):
        return (ObjectTypeName.typeClassName(obj).find('fields.BooleanField') > -1)
        
    def is_ModelChoiceField(self,obj):
        return (ObjectTypeName.typeClassName(obj).find('models.ModelChoiceField') > -1)
        
    def is_CharField(self,obj):
        return (ObjectTypeName.typeClassName(obj).find('fields.CharField') > -1)
        
    def is_EmailField(self,obj):
        return (ObjectTypeName.typeClassName(obj).find('fields.EmailField') > -1)
        
    def is_DateTimeField(self,obj):
        return (ObjectTypeName.typeClassName(obj).find('fields.DateTimeField') > -1)
        
    def as_html(self, request=None, width='100%',max_length=40,context={}):
        h = oohtml.Html()
	_no_show_fields = []
	_action = self.action.split('/')
	for k,v in self.__hidden_fields__.iteritems():
	    if (str(v).isdigit()) and (int(v) > -1):
		_action.insert(len(_action)-(1 if (_action[-1] == '') else 0),'%s' % (v))
	    else:
		_no_show_fields.append(k)
        form = h.tag(oohtml.oohtml.FORM, name=self.form_name, id="%sForm" % (self.form_name), target=self.target, action='/'.join(_action), enctype="application/x-www-form-urlencoded", method="post")
	_remaining_fields = list(set(self.fields.keyOrder) - set(self.__field_ordering__) - set(_no_show_fields))
        for k in self.__field_ordering__ + _remaining_fields:
	    _k = "VALUE_%s" % (k.upper())
            v = self.fields[k]
	    _is_BooleanField = self.is_BooleanField(v)
	    _is_DateTimeField = self.is_DateTimeField(v)
            _tr = form.tag(oohtml.oohtml.TR)
            _th = _tr.tag(oohtml.oohtml.TH, width="*", align="right")
            _nobr = _th.tagNOBR()
            _nobr.tagLABEL('id_%s' % k, '%s:&nbsp;' % (v.label))
            _td = _tr.tag(oohtml.oohtml.TD, align="left")
            ds = self.get_datasource_for_field_by_name(k)
            if (self.is_ModelChoiceField(v)) or (_is_BooleanField):
                _value_id = 'value'
                _text_id = 'text'
                choice_model = self.get_choice_model_for_field_by_name(k)
                if (choice_model is not None):
                    _value_id = choice_model.value_id
                    _text_id = choice_model.text_id
                else:
		    try:
			keys = [kk for kk in v.queryset[0].__dict__.keys() if (kk != 'version')]
			for kk,vv in v.queryset[0].__dict__.iteritems():
			    if (kk in keys):
				if (misc.isString(vv)):
				    _text_id = kk
				else:
				    _value_id = kk
			    if (len(_value_id) > 0) and (len(_text_id) > 0):
				break
		    except: # possibly there is no data to populate so we do nothing here...
			pass
		_selected = self.get_choice_model_default_for_field_by_name(k)
		_selected = _selected if (not context.has_key(_k)) else context[_k]
		_selected = _selected if (_selected is not None) else ''
		if (len(_selected) == 0) and (request is not None):
		    _selected = request.POST[k]
                oohtml.render_select_content(v.queryset if (not _is_BooleanField) else [{'value':'True','text':'True'},{'value':'False','text':'False'}],tag=_td,id='id_%s' % (k),name=k,text_id=_text_id,value_id=_value_id,defaultChoose=True,selected=_selected)
            elif (_is_DateTimeField):
		_td.tagDIV(django_utils.render_from_string(self.datetime_field_content,context=context) + '&nbsp;&nbsp;&nbsp;&nbsp;* Required' if (v.required) else '')
		v.required = False
            elif (callable(ds)):
                oohtml.render_select_content(ds(),tag=_td,id='id_%s' % (k),name=k,text_id=_text_id,value_id=_value_id,defaultChoose=True,selected=self.get_choice_model_default_for_field_by_name(k))
            else:
		_max_length = max_length
		try:
		    _max_length = min(v.max_length,max_length)
		except: # Account for differences between various Django releases in this regard.
		    pass
                _td.tagOp(oohtml.oohtml.INPUT, type=oohtml.oohtml.TEXT, name=k, size=_max_length, maxlength=_max_length, value="{{ %s }}" % (_k))
            l = []
            if (v.required):
                l.append('* Required')
                try:
                    if (v.min_length) and (not self.is_ModelChoiceField(v)):
                        l.append(' minimum %d chars' % (v.min_length))
                except:
                    pass
            _td.tagSPAN('&nbsp;%s%s{{ ERROR_%s }}%s' % ('(' if (len(l) > 0) else '',','.join(l),k.upper(),')' if (len(l) > 0) else ''))
        tr = form.tag(oohtml.oohtml.TR)
        td = tr.tag(oohtml.oohtml.TD, align="left", colspan="2")
	if (misc.isString(self.captcha_form_name)) and (misc.isString(self.captcha_font_name)):
	    td.tagDIV(captcha.render_captcha_form(self.request,form_name=self.captcha_form_name,font_name=self.captcha_font_name,font_size=self.captcha_font_size,choices=self.captcha_choices,fill=self.captcha_fill,bgImage=self.captcha_bgImage))
        tr = form.tag(oohtml.oohtml.TR)
        td = tr.tag(oohtml.oohtml.TD, align="center", colspan="2")
        td.tagSUBMIT(self.submit_button_title, value=self.submit_button_value, onclick="this.disabled=true;")
        return h.toHtml()
    
    def validate_and_save(self,request,d_context,callback=None,callback_beforeSave=None,callback_validation_failed=None,callback_error=None):
	self.__last_error__ = ''
	for field_name in request.POST.keys():
	    if (self.fields.has_key(field_name)):
		aField = self.fields[field_name]
		aField.value = request.POST[field_name]
		if (aField.required):
		    if (self.is_CharField(aField)):
			if (len(aField.value.strip()) < aField.min_length if (aField.min_length) else 1):
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('&nbsp;%s requires at least %d chars.' % (aField.label,aField.min_length if (aField.min_length is not None) else 0), class_='error')
		    elif (self.is_EmailField(aField)):
			valid_email = validateEmail(aField.value)
			valid_email_domain = True # Assume the domain is valid so long as the domain name appears to be valid in case there is no other filter.
			email_domain = aField.value.split('@')[-1]
			if (callable(self.get_freehost_by_name)) and (valid_email):
			    hosts = self.get_freehost_by_name(email_domain)
			    valid_email_domain = (hosts is None) or ((misc.isList(hosts)) and (len(hosts) == 0))
			if (not valid_email) or (not valid_email_domain):
			    extra_msg = ' because "%s" is not an allowed domain' % (email_domain) if (not valid_email_domain) else ''
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('&nbsp;Please enter a valid internet email address%s.' % (extra_msg), class_='error')
		    elif (self.is_ModelChoiceField(aField)):
			can_consisder_validation = True
			for validation_tuple in self.__field_validations__:
			    if (callable(validation_tuple[0])):
				if (validation_tuple[-1].has_key(field_name)):
				    can_consisder_validation = False
			if (can_consisder_validation):
			    if (len(aField.value) == 0):
				d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('&nbsp;Selection for %s is not valid.' % (aField.label), class_='error')
			if (len(aField.value) > 0):
			    kw = {self.get_choice_model_for_field_by_name(field_name).value_id:aField.value}
			    aField._value = aField.queryset.filter(**kw)[0]
		    elif (self.is_BooleanField(aField)):
			isError = False
			try:
			    aField.value = eval(aField.value)
			except Exception, e:
			    isError = True
			    info_string = _utils.formattedException(details=e)
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('<BR/>'.join(info_string.split('\n')), class_='error')
			    aField.value = False
			if (not isError) and (not isinstance(aField.value,bool)):
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('Not a valid Boolean value.', class_='error')
		    elif (self.is_DateTimeField(aField)):
			isError = False
			try:
			    aField.value = _utils.getFromDateTimeStr(aField.value,format=_utils.formatDate_MMDDYYYY_slashes())
			except Exception, e:
			    isError = True
			    info_string = _utils.formattedException(details=e)
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('<BR/>'.join(info_string.split('\n')), class_='error')
			    aField.value = None
			if (not isError) and (ObjectTypeName.typeClassName(aField.value) != 'datetime.datetime'):
			    d_context['ERROR_%s' % (field_name.upper())] = oohtml.render_SPAN('Not a valid DateTime value.', class_='error')
	    else:
		pass
	for validation_tuple in self.__field_validations__:
	    if (callable(validation_tuple[0])):
		if (validation_tuple[0](self)):
		    for k,v in validation_tuple[-1].iteritems():
			d_context['ERROR_%s' % (k.upper())] = oohtml.render_SPAN('&nbsp;%s' % (v), class_='error')

	if (len(d_context) > 0):
	    for field_name in request.POST.keys():
		if (self.fields.has_key(field_name)):
		    aField = self.fields[field_name]
		    aField.value = request.POST[field_name]
		    d_context['VALUE_%s' % (field_name.upper())] = aField.value
	    if (callable(callback_validation_failed)):
		return callback_validation_failed(self,d_context)
	else:
	    lable_from_field = lambda foo:f.label if (not misc.isString(f)) else f
	    try:
		pk = self.model._meta.pk
		try:
		    kw = {lable_from_field(pk.formfield()):[f for f in self.fields if (lable_from_field(f) == lable_from_field(pk.formfield()))][0]}
		except:
		    url_toks = django_utils.parse_url_parms(request)
		    kw = {pk.column:int(url_toks[-1]) if (str(url_toks[-1]).isdigit()) else -1}
		anObj = self.model.objects.get(**kw)
	    except Exception, details:
		anObj = self.model()
		
	    for field_name,aField in self.fields.iteritems():
		try:
		    if self.is_ModelChoiceField(aField):
			anObj.__setattr__(field_name,aField._value)
		    else:
			anObj.__setattr__(field_name,aField.value)
		except Exception, e: # ignore all the hidden fields or any other fields for which there is no data present.
		    info_string = _utils.formattedException(details=e)
	    for k,v in self.__extra_fields__.iteritems():
		try:
		    anObj.__setattr__(k,v)
		except Exception, e:
		    info_string = _utils.formattedException(details=e)
	    if (callable(callback_beforeSave)):
		callback_beforeSave(self,request,anObj)
	    try:
		anObj.save()
	    except Exception, details:
		self.__last_error__ = _utils.formattedException(details=details)
		if (callable(callback_error)):
		    callback_error(self,request)
	    finally:
		if (len(self.last_error) > 0):
		    if (callable(callback_validation_failed)):
			return callback_validation_failed(self,d_context)
		else:
		    if (callable(callback)):
			return callback(self,request)
	return None

    def field_validation():
        doc = '''field_validation is a tuple that looks like this (lambda,{'STATE':'Error Message','COUNTRY':'Another Error Message'})
	field validation is useful when two or more fields are being considered together as a single validation.
	'''
        def fset(self, field_validation):
            self.__field_validations__.append(field_validation)
        return locals()
    field_validation = property(**field_validation())
    
    def first_field_name():
        doc = '''defines the order in which fields appear once rendered as HTML.
	self.first_field_name = 'name-of-field' <-- defines the order of the fields from top to bottom by stating the one that comes first.
	'''
        def fset(self, field_name):
	    self.__field_ordering__ = []
	    if (self.fields.has_key(field_name)):
		self.__field_ordering__.append(field_name)
        return locals()
    first_field_name = property(**first_field_name())
    
    def next_field_name():
        doc = '''defines the order in which fields appear once rendered as HTML.
	self.next_field_name = 'name-of-field' <-- defines the order of the fields from top to bottom.
	'''
        def fset(self, field_name):
	    if (self.fields.has_key(field_name)):
		self.__field_ordering__.append(field_name)
        return locals()
    next_field_name = property(**next_field_name())
    
    def field_validations():
        doc = '''field_validations is a list of tuple that looks like this (lambda,{'STATE':'Error Message','COUNTRY':'Another Error Message'})
	field validation is useful when two or more fields are being considered together as a single validation.
	'''
        def fget(self):
            return self.__field_validations__
        return locals()
    field_validations = property(**field_validations())

    def email_fields():
        doc = '''returns one or more EmailField fields from the list of fields for the form.'''
        def fget(self):
            return [aField for field_name,aField in self.fields.iteritems() if (self.is_EmailField(aField))]
        return locals()
    email_fields = property(**email_fields())

    def get_freehost_by_name():
        doc = "get_freehost_by_name"
        def fget(self):
            return self.__get_freehost_by_name__
        def fset(self, get_freehost_by_name):
            self.__get_freehost_by_name__ = get_freehost_by_name if (callable(get_freehost_by_name)) else None
        return locals()
    get_freehost_by_name = property(**get_freehost_by_name())

    def model():
        doc = "model"
        def fget(self):
            return self.__model__
        def fset(self, model):
            self.__model__ = model
            self.__fields__ = fields.fields_for_model(model)
            self.__model_choice_fields__ = self.__model_choice_fields(self)
        return locals()
    model = property(**model())

    def form_name():
        doc = "form_name"
        def fget(self):
            return self.__form_name__
        def fset(self, form_name):
            self.__form_name__ = form_name
        return locals()
    form_name = property(**form_name())

    def target():
        doc = "target"
        def fget(self):
            return self.__target__
        def fset(self, target):
            self.__target__ = target
        return locals()
    target = property(**target())

    def action():
        doc = "action"
        def fget(self):
            return self.__action__
        def fset(self, action):
            self.__action__ = action
        return locals()
    action = property(**action())

    def fields():
        doc = "fields"
        def fget(self):
            return self.__fields__
        return locals()
    fields = property(**fields())
    
    def request():
        doc = "request"
        def fget(self):
            return self.__request__
        return locals()
    request = property(**request())

    def model_choice_fields():
        doc = "model_choice_fields"
        def fget(self):
            return self.__model_choice_fields__
        return locals()
    model_choice_fields = property(**model_choice_fields())
    
    def last_error():
        doc = "last_error"
        def fget(self):
            return self.__last_error__
        return locals()
    last_error = property(**last_error())

    def submit_button_title():
        doc = "submit_button_title"
        def fget(self):
            return self.__submit_button_title__
        def fset(self, submit_button_title):
            self.__submit_button_title__ = submit_button_title
        return locals()
    submit_button_title = property(**submit_button_title())
    
    def submit_button_value():
        doc = "submit_button_value"
        def fget(self):
            return self.__submit_button_value__
        def fset(self, submit_button_value):
            self.__submit_button_value__ = submit_button_value
        return locals()
    submit_button_value = property(**submit_button_value())
    
    def datetime_field_content():
        doc = "datetime_field_content"
        def fget(self):
            return self.__datetime_field_content__
        def fset(self, datetime_field_content):
            self.__datetime_field_content__ = datetime_field_content
        return locals()
    datetime_field_content = property(**datetime_field_content())
    
    def use_captcha():
        doc = "use_captcha"
        def fget(self):
            return self.__use_captcha__
        def fset(self, use_captcha):
            self.__use_captcha__ = use_captcha
        return locals()
    use_captcha = property(**use_captcha())
    
    def captcha_form_name():
        doc = "captcha_form_name"
        def fget(self):
            return self.__captcha_form_name__
        def fset(self, captcha_form_name):
            self.__captcha_form_name__ = captcha_form_name
        return locals()
    captcha_form_name = property(**captcha_form_name())
    
    def captcha_font_name():
        doc = "captcha_font_name"
        def fget(self):
            return self.__captcha_font_name__
        def fset(self, captcha_font_name):
            self.__captcha_font_name__ = captcha_font_name
        return locals()
    captcha_font_name = property(**captcha_font_name())
    
    def captcha_font_size():
        doc = "captcha_font_size"
        def fget(self):
            return self.__captcha_font_size__
        def fset(self, captcha_font_size):
            self.__captcha_font_size__ = captcha_font_size
        return locals()
    captcha_font_size = property(**captcha_font_size())

    def captcha_choices():
        doc = "captcha_choices"
        def fget(self):
            return self.__captcha_choices__
        def fset(self, captcha_choices):
            self.__captcha_choices__ = captcha_choices
        return locals()
    captcha_choices = property(**captcha_choices())

    def captcha_fill():
        doc = "captcha_fill"
        def fget(self):
            return self.__captcha_fill__
        def fset(self, captcha_fill):
            self.__captcha_fill__ = captcha_fill
        return locals()
    captcha_fill = property(**captcha_fill())

    def captcha_bgImage():
        doc = "captcha_bgImage"
        def fget(self):
            return self.__captcha_bgImage__
        def fset(self, captcha_bgImage):
            self.__captcha_bgImage__ = captcha_bgImage
        return locals()
    captcha_bgImage = property(**captcha_bgImage())
