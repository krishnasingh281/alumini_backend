from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta

class CustomAccessToken(AccessToken):
    @property
    def lifetime(self):
        # Example: Different lifetimes for different user roles
        user_role = self.payload.get("role", "user") 
        if user_role == "admin":
            return timedelta(hours=3) 
        elif user_role == "alumni":
            return timedelta(hours=1)  
        else:
            return timedelta(hours=1) 