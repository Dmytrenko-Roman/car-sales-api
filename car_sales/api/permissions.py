from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    methods: tuple

    def has_permission(self, request, views):
        return request.method in self.methods


class AllowCreate(CustomPermission):
    methods = ("POST",)


class AllowGetRetrieve(CustomPermission):
    methods = ("GET",)
