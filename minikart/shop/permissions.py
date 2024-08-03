from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to create products.
    """

    def has_permission(self, request, view):
        return request.user.user_type=="Seller"
        


