from rest_framework import generics, permissions
from users.models.userprofile import UserProfile
from users.serializer.profile_serializer import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.select_related(
            'user', 'province', 'district', 'sector', 'cell', 'village', 'sector'
        ).get_or_create(user=self.request.user)
        return profile