from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # TODO: дописать, а пока пускай всегда будет True
        # return (
        #     request.method in permissions.SAFE_METHODS
        #     or obj.author == request.user
        #     or "Админ"
        #     or "Модератор"
        # )
        return True
