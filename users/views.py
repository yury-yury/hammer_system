from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, CallbackToken
from users.serializers import LoginSerializer, VerifyTokenSerializer, TokenResponseSerializer, ProfileSerializer
from users.utils import send_sms_with_callback_token, create_authentication_token


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(CreateAPIView):
    """
    The LoginView class is a CBV serving POST requests to the address "login/". Inherited from the CreateAPIView
    generic in the rest_framework.generics module. When the user contacts this address,
    it receives data from the database, if it is not available, it creates a new instance,
    sends a 4-digit digital code for authentication.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """
        The post function overrides the parent class method to ensure that the POST request is correctly processed.
        It implements the functional of finding or creating a user by the entered phone number,
        generating a 4-digit digital token for confirming the authentication
        and sending it as an SMS to the entered phone number.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "user": serializer.data,
            "next_page": f"http://127.0.0.1:8000/verify/{serializer.data['id']}"
        }

        if serializer.is_valid:
            user = User.objects.get(pk=serializer.data['id'])
            callback_token = CallbackToken.objects.filter(user=user).first()
            send_sms_with_callback_token(user, callback_token, **kwargs)

        return Response(data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyTokenView(APIView):
    """
    The VerifyTokenView class is a CBV for handling a POST request to the /verify/<int:pk> URL.
    Inherited from the APIView base class from the rest_framework.views module.
    Provides verification of the entered authentication confirmation token and generation of a user authorization token.
    """
    serializer_class = VerifyTokenSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs) -> Response:
        """
        The post function overrides the logic of the parent class method. When the method is called,
        it calls the validation of the received data using the serializer, creates or receives an authorization token.
        On success, it returns a Response object containing the authorization token; on invalid data,
        it returns a Response object containing a description of the error.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            auth_token = create_authentication_token(user)

            if auth_token:
                token_serializer = TokenResponseSerializer(data={"token": auth_token.key, }, partial=True)
                if token_serializer.is_valid():
                    # Return our key for consumption.
                    return Response(token_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Couldn\'t log you in. Try again later.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveUpdateAPIView):
    """
    The ProfileView class is a CBV for handling GET and PATCH requests made to the URL '/profile/'.
    Provides viewing the profile of the current user and changing his data,
    also contains functionality that provides the input of a referral code.
    Inherited from the base generic RetrieveUpdateAPIView from the rest_framework.generics module.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self) -> User:
        """
        The get_object function overrides the method of the parent class, replaces the logic of getting the object
        of the work of the methods. Makes it possible for the view to work without explicitly specifying an object
        as a URL parameter. Restricts access to profiles of other users. When called,
        the method takes no other parameters than its own instance of the class.
        Returns an instance of the authorized user who made the request.
        """
        return self.request.user

    @extend_schema(deprecated=True)
    def put(self, request, *args, **kwargs) -> None:
        """
        The put function overrides the parent class method. Disables its functionality, since the use of the method
        is not provided for by this implementation. Raises a NotImplementedError when accessed.
        """
        raise NotImplementedError
