from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class DeleteGroup(LoginRequiredMixin, generic.DeleteView):
    model = Group
    success_url = reverse_lazy('groups:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs.get('slug'))

    def delete(self,*args,**kwargs):
        messages.success(self.request,f"{kwargs.get('slug')} group deleted!")
        return super().delete(*args,**kwargs)

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        group = get_object_or_404(Group,slug=kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=request.user,group=group)

        except IntegrityError:
            messages.warning(request, f"Warning, already a member of {group.name}")

        else:
            messages.success(request, f"You are now a member of the <strong>{group.name}</strong> group.")

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=request.user,
                group__slug=kwargs.get("slug")
            ).get()

        except GroupMember.DoesNotExist:
            messages.warning(request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
