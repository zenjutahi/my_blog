from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsOwnerOrReadOnly(BasePermission):
	message = 'You must be owner of this object'
	#my_safe_method = ['PUT','GET']
	#def has_permission(self, request, view):
	#	if request.method in self.my_safe_method:
	#		return True
	#	return False

	def has_object_permission(self, request, view, obj):
		#member = Membership.objects.get(user=request.user) ....n such for permission customization
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user