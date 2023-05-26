from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    # TODO: дописать, а пока пускай всегда будет True
    # return (
    #     request.method in permissions.SAFE_METHODS
    #     or obj.author == request.user
    #     or "Админ"
    #     or "Модератор"
    # )
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )
