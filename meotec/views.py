from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from forms import ManagerForm, ServerForm, SiteForm
from models import Manager, Server, Site


def home(request):
    return direct_to_template(request, 'meotec/home.html', {
        'servers': Server.objects.all(),
        'managers': Manager.objects.all(),
    })


def action(request):
    return direct_to_template(request, 'meotec/action.html', {
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