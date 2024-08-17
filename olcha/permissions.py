from rest_framework import permissions


class CustomPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Agar so'rov xavfsiz usullardan bo'lsa, ruxsat beriladi
        if request.method in permissions.SAFE_METHODS:
            return True

        # Agar so'rov foydalanuvchisi ob'ekt muallifi bo'lsa:
        if obj.author == request.user:

            # DELETE usuli superuser yoki staff foydalanuvchilarga ruxsat etiladi
            if request.method == 'DELETE' and (request.user.is_superuser or request.user.is_staff):
                return True

            # PUT yoki PATCH usullari muallif bo'lgan va staff bo'lmagan foydalanuvchilarga ruxsat etiladi
            if request.method in ['PUT', 'PATCH'] and not request.user.is_staff:
                return True

        # POST usuli faqat superuserga ruxsat etiladi
        if request.method == 'POST' and request.user.is_superuser:
            return True

        # Aks holda ruxsat berilmaydi
        return False