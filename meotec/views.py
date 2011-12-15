import urllib
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from forms import ManagerForm, ServerForm, SiteForm
from forms import BootstrapFormMixin
from meotec.commands import ServerCommand, SiteCommand, BaseCommand
from models import Manager, Server, Site


def home(request):
    return direct_to_template(request, 'meotec/home.html', {
        'servers': Server.objects.all(),
        'managers': Manager.objects.all(),
    })


def run_init(request, manager_id, command):
    manager = get_object_or_404(Manager, pk=manager_id)
    command = manager.command(command)
    if not command:
        raise Http404
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
    def run_on_servers():
        _answers = {}
        for server in Server.objects.filter(id__in=servers):
            try:
                answer = command.run(server, form.cleaned_data)
            except SystemExit:
                answer = 'Error: System Exit'
            except Exception, e:
                answer = e
            _answers[server]= (answer, {})
        return _answers

    def run_on_sites():
        _answers = {}
        for site in Site.objects.filter(id__in=sites):
            try:
                answer = command.run(site, form.cleaned_data)
            except SystemExit:
                answer = 'Error: System Exit'
            except Exception, e:
                answer = e
            if site.server not in _answers:
                _answers[site.server] = (None, {})
            _answers[site.server][1][site] = answer
        return _answers

    manager = get_object_or_404(Manager, pk=manager_id)
    command = manager.command(command)
    if not command:
        raise Http404
    servers, sites = request.GET.getlist('servers[]'), request.GET.getlist('sites[]')
    form_class = type('Form',
                      (forms.Form, BootstrapFormMixin),
                      dict(command.args))
    form = form_class(request.GET)
    if not form.is_valid():
        raise Http404
    answers = {}
    if isinstance(command, ServerCommand):
        answers.update(run_on_servers())
    elif isinstance(command, SiteCommand):
        answers.update(run_on_sites())
    elif isinstance(command, BaseCommand):
        answers.update(run_on_servers())
        answers.update(run_on_sites())
    else:
        raise
    return direct_to_template(request, 'meotec/answer.html', {
        'answers': answers,
    })


def settings(request):
    return direct_to_template(request, 'meotec/settings.html', {
        'servers': Server.objects.all(),
        'managers': Manager.objects.all(),
    })


def manager_add(request):
    if request.POST:
        form = ManagerForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('%s manager is added' % obj))
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
            messages.success(request, _('%s manager changed successfully' % obj))
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
    messages.success(request, _('Update is successful'))
    return redirect('meotec:settings')


def server_add(request):
    if request.POST:
        form = ServerForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('%s server is added' % obj))
            return redirect('meotec:settings')
    else:
        form = ServerForm()
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Server Add'),
        'form': form,
    })


def server_edit(request, id):
    server = get_object_or_404(Server, pk=id)
    if request.POST:
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('%s server changed successfully' % obj))
            return redirect('meotec:settings')
    else:
        form = ServerForm(instance=server)
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Server Edit'),
        'form': form,
    })


def site_add(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    if request.POST:
        form = SiteForm(request.POST)
        if form.is_valid():
            form.instance.server = server
            obj = form.save()
            messages.success(request, _('%s site is added' % obj))
            return redirect('meotec:settings')
    else:
        form = SiteForm()
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Add site to the server %s' % server),
        'form': form,
    })


def site_edit(request, server_id, id):
    site = get_object_or_404(Site, pk=id)
    if request.POST:
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _('%s site changed successfully' % obj))
            return redirect('meotec:settings')
    else:
        form = SiteForm(instance=site)
    return direct_to_template(request, 'meotec/simple_form.html', {
        'title': _('Site Edit %s' % site),
        'form': form,
    })