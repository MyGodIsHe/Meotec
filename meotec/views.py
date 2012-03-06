from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from forms import ManagerForm, form_factory,  BootstrapFormMixin
from meotec.base import BaseCommand, get_class_by_path
from models import Manager, Node


def home(request):
    return direct_to_template(request, 'meotec/home.html', {
        'nodes': Node.tree.all(),
        'managers': Manager.objects.all(),
    })


def run_init(request, manager_id, command):
    manager = get_object_or_404(Manager, pk=manager_id)
    command = manager.command(command)
    if not command:
        return HttpResponseNotFound()
    form_class = type('Form',
                      (forms.Form, BootstrapFormMixin),
                      dict(command.args))
    if request.GET:
        form = form_class(request.GET)
        if form.is_valid():
            return HttpResponseRedirect("%s?%s" % (reverse('meotec:run', args=[manager.id, command.name]),
                                                   request.META['QUERY_STRING']))
    else:
        form = form_class()
    return direct_to_template(request, 'meotec/init_form.html', {
        'path': request.path,
        'title': command.title,
        'form': form,
    })


def run(request, manager_id, command):
    manager = get_object_or_404(Manager, pk=manager_id)
    command = manager.command(command)
    if not command:
        return HttpResponseNotFound()
    nodes = request.GET.getlist('nodes[]')
    form_class = type('Form',
                      (forms.Form, BootstrapFormMixin),
                      dict(command.args))
    form = form_class(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest()
    answers = {}
    if isinstance(command, BaseCommand):
        answers.update(run_on_servers())
        answers.update(run_on_sites())
    else:
        return HttpResponseBadRequest()
    return direct_to_template(request, 'meotec/answer.html', {
        'answers': answers,
    })


def settings(request):
    return direct_to_template(request, 'meotec/settings.html', {
        'nodes': Node.tree.all(),
        'managers': Manager.objects.all(),
    })


def manager_add(request):
    if request.POST:
        print 0
        form = ManagerForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _(u'%s manager is added' % obj))
            return redirect('meotec:settings')
    else:
        form = ManagerForm()
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Manager Add'),
        'form': form,
    })


def manager_edit(request, id):
    manager = get_object_or_404(Manager, pk=id)
    if request.POST:
        form = ManagerForm(request.POST, instance=manager)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _(u'%s manager changed successfully' % obj))
            return redirect('meotec:settings')
    else:
        form = ManagerForm(instance=manager)
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Manager Edit'),
        'form': form,
    })


def manager_update(request):
    for manager in Manager.objects.all():
        manager.update()
    messages.success(request, _(u'Update is successful'))
    return redirect('meotec:settings')


def node_add(request, id, class_path):
    Entity = get_class_by_path(class_path)
    parent = get_object_or_404(Node, pk=id)
    NodeForm = form_factory(Entity)
    if request.POST:
        form = NodeForm(request.POST)
        if form.is_valid():
            obj = form.save()
            Node(
                name=form.cleaned_data['name'],
                parent=parent,
                content_object=obj,
            ).save()
            messages.success(request, _(u'%s is added' % obj))
            return redirect('meotec:settings')
    else:
        form = NodeForm()
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Node Add'),
        'form': form,
    })


def node_edit(request, id):
    node = get_object_or_404(Node, pk=id)
    if node.is_root_node():
        return HttpResponseBadRequest()
    NodeForm = form_factory(node.content_object.__class__)
    if request.POST:
        form = NodeForm(request.POST, initial={ 'name': node.name }, instance=node.content_object)
        if form.is_valid():
            obj = form.save()
            node.name = form.cleaned_data['name']
            node.save()
            messages.success(request, _(u'%s changed successfully' % obj))
            return redirect('meotec:settings')
    else:
        form = NodeForm(initial={ 'name': node.name }, instance=node.content_object)
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Node Edit'),
        'form': form,
    })


def node_del(request, id):
    node = get_object_or_404(Node, pk=id)
    if node.is_root_node():
        names = []
        for n in node.get_children():
            names.append(unicode(n))
            n.delete()
        if names:
            messages.success(request, _(u'%s deleted successfully' % ', '.join(names)))
    else:
        name = unicode(node)
        node.delete()
        messages.success(request, _(u'%s deleted successfully' % name))
    return redirect('meotec:settings')