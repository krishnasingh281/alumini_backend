from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta

class CustomAccessToken(AccessToken):
    @property
    def lifetime(self):
        # Example: Different lifetimes for different user roles
        user_role = self.payload.get("role", "user") 
        if user_role == "admin":
            return timedelta(minutes=3) 
        elif user_role == "alumni":
            return timedelta(minutes=2)  
        else:
            return timedelta(minutes=1) 