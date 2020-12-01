from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (CreateView,
                                  DetailView,
                                  DeleteView,
                                  ListView,
                                  UpdateView)

from resources.forms import (GeopackageReviewForm,
                             GeopackageUpdateForm,
                             GeopackageUploadForm,)
from resources.models import Geopackage, GeopackageReview


def is_resources_manager(user: User) -> bool:
    """Check if user is the members of Resources Managers group."""

    return user.groups.filter(name="Style Managers").exists()


def check_geopackage_access(user: User, gpkg: Geopackage) -> bool:
    """Check if user is the creator of the GeoPackage or is_staff."""

    return user.is_staff or gpkg.creator == user or is_resources_manager(user)


class GeopackageCreateView(LoginRequiredMixin, CreateView):
    """
    Upload a GeoPackage File
    """

    form_class = GeopackageUploadForm
    template_name = 'resources/geopackage_form.html'
    success_message = "GeoPackage was uploaded successfully."

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        # style_notify(obj)
        msg = _(self.success_message)
        messages.success(self.request, msg, 'success', fail_silently=True)
        # return HttpResponseRedirect(reverse('geopackage_detail',
        #                                     kwargs={'pk': obj.id}))
        return HttpResponseRedirect(reverse('geopackage_list'))


class GeopackageDetailView(DetailView):
    model = Geopackage
    queryset = Geopackage.objects.all()
    context_object_name = 'geopackage_detail'

    def get_template_names(self):
        gpkg = self.get_object()
        if not gpkg.approved:
            return 'resources/geopackage_review.html'
        return 'resources/geopackage_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['creator'] = self.object.get_creator_name
        if self.object.geopackagereview_set.exists():
            if self.object.geopackagereview_set.last().reviewer.first_name:
                reviewer = "%s %s" % (
                    self.object.stylereview_set.last().reviewer.first_name,
                    self.object.stylereview_set.last().reviewer.last_name)
            else:
                reviewer = self.object.geopackagereview_set.last().reviewer \
                    .username
            context['reviewer'] = reviewer
        if user.is_staff or is_resources_manager(user):
            context['form'] = GeopackageReviewForm()
        return context


class GeopackageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a GeoPackage
    """

    model = Geopackage
    form_class = GeopackageUpdateForm
    context_object_name = 'geopackage'
    template_name = 'resources/geopackage_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        gpkg = self.get_object()
        user = self.request.user
        if not check_geopackage_access(user, gpkg):
            return render(request, 'resources/geopackage_permission_deny.html',
                          {'geopackage_name': gpkg.name,
                           'context': "You cannot delete this GeoPackage"})
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.require_action = False
        obj.approved = False
        obj.save()
        # style_notify(obj, created=False)
        msg = _("The GeoPackage has been successfully updated.")
        messages.success(self.request, msg, 'success', fail_silently=True)
        # return HttpResponseRedirect(reverse_lazy('geopackage_detail',
        #                                          kwargs={'pk': obj.id}))
        return HttpResponseRedirect(reverse('geopackage_list'))


class GeopackageListView(ListView):

    model = Geopackage
    context_object_name = 'geopackage_list'
    template_name = 'resources/geopackage_list.html'


class GeopackageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a GeoPackage.
    """

    model = Geopackage
    context_object_file = 'geopackage'
    success_url = reverse_lazy('geopackage_list')

    def dispatch(self, request, *args, **kwargs):
        gpkg = self.get_object()
        user = self.request.user
        if not check_geopackage_access(user, gpkg):
            return render(request, 'resources/geopackage_permission_deny.html',
                {'geopackage_name': gpkg.name,
                 'context': "You cannot delete this GeoPackage"})
        return super().dispatch(request, *args, **kwargs)


def geopackage_review(request, pk):
    """
    Submit a review and send email notification
    """

    gpkg = get_object_or_404(Geopackage, pk=pk)
    if request.method == 'POST':
        form = GeopackageReviewForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            GeopackageReview.objects.create(
                geopackage=gpkg,
                reviewer=request.user,
                comment=data['comment'])
            if data['approval'] == 'approve':
                gpkg.approved = True
                gpkg.require_action = False
                msg = _("The GeoPackage has been approved.")
                messages.success(request, msg, 'success', fail_silently=True)
            else:
                gpkg.approved = False
                gpkg.require_action = True
                msg = _("The GeoPackage has been rejected.")
                messages.success(request, msg, 'error', fail_silently=True)
            gpkg.save()
            # send email notification
            # style_approval_notify(style, style.creator, request.user)
    return HttpResponseRedirect(reverse('style_detail', kwargs={'pk': pk}))


def geopackage_download(request, pk):
    """
    Download GeoPackage and update its download_count value
    """

    gpkg = get_object_or_404(Geopackage, pk=pk)
    if not gpkg.approved:
        if not check_geopackage_access(request.user, gpkg):
            return render(
                request, 'resources/geopackage_permission_deny.html',
                {'geopackage_name': gpkg.name,
                 'context': 'Download failed. This GeoPackage is not approved'})
    else:
        gpkg.increase_download_counter()
        gpkg.save()
    with open(gpkg.gpkg_file.file.name, 'rb') as gpkg_file:
        file_content = gpkg_file.read()
        response = HttpResponse(file_content, content_type='application/gpkg')
        response['Content-Disposition'] = 'attachment; filename=%s.gpkg' % (
            gpkg.name
        )
        return response