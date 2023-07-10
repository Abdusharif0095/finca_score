from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(self, request, *args, **kwargs):
            group = None
            # print(request.user.is_authenticated)
            # print(request.user.groups.all())
            print("request is:", request)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(self, request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page!")

        return wrapper_func
    return decorator
