from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _
from models import Manager


def customize(template, rules=None, extra_context=None):

    def wrapper(self):

        def parse(rules):
            for mark, rule in rules.items():
                if mark in field_as_text:
                    if rule[0]:
                        bf.field_as_text = field_as_text.replace(mark, rule[0])
                    if rule[1]:
                        bf.field_type = rule[1]
                    if len(rule) == 3:
                        parse(rule[2])
                    return

        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        fields, hidden_fields = [], []

        for name, field in self.fields.items():
            bf = forms.forms.BoundField(self, field, name)

            if bf.is_hidden:
                bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                field_as_text = str(bf)
                if rules:
                    parse(rules)
                fields.append(bf)

        context = {
            'fields': fields,
            'top_errors':top_errors,
            'hidden_fields': hidden_fields,
        }

        if extra_context:
            context.update(extra_context)
        return render_to_string(template , context)

    return wrapper


class BootstrapFormMixin(object):
    as_bootstrap = customize('meotec/bootstrap_form.html')


class ManagerForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Manager


def form_factory(Model):
    class Form(forms.ModelForm, BootstrapFormMixin):
        name = forms.CharField(label=_('Display name'), max_length=50)
        class Meta:
            model = Model
            exclude = ('content_type', 'object_id', 'content_object', 'parent')
    return Form