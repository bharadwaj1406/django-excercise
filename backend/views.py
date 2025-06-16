from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Min, Max
from .models import Country, State, City, User
from .serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    UserSerializer,
)

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password


def hello_world(request):
    return HttpResponse("Hello World")


class ListCreateCountry(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        is_bulk = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListCreateState(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        is_bulk = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListCreateCity(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        is_bulk = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BulkUpdateCountry(generics.GenericAPIView):
    serializer_class = CountrySerializer

    def put(self, request):
        errors = []
        for item in request.data:
            country = get_object_or_404(Country, id=item.get("id"))
            serializer = self.get_serializer(country, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append({"id": item.get("id"), "errors": serializer.errors})

        if errors:
            return Response(
                {"message": "Some updates failed", "details": errors}, status=400
            )
        return Response({"message": "Countries updated"}, status=200)


class BulkUpdateState(generics.GenericAPIView):
    serializer_class = StateSerializer

    def put(self, request):
        errors = []
        for item in request.data:
            state = get_object_or_404(State, id=item.get("id"))
            serializer = self.get_serializer(state, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append({"id": item.get("id"), "errors": serializer.errors})

        if errors:
            return Response(
                {"message": "Some updates failed", "details": errors}, status=400
            )
        return Response({"message": "States updated"}, status=200)


class BulkUpdateCity(generics.GenericAPIView):
    serializer_class = CitySerializer

    def put(self, request):
        errors = []
        for item in request.data:
            city = get_object_or_404(City, id=item.get("id"))
            serializer = self.get_serializer(city, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append({"id": item.get("id"), "errors": serializer.errors})

        if errors:
            return Response(
                {"message": "Some updates failed", "details": errors}, status=400
            )
        return Response({"message": "Cities updated"}, status=200)


class AllDataView(generics.ListAPIView):
    def get(self, request):
        countries = CountrySerializer(Country.objects.all(), many=True).data
        states = StateSerializer(State.objects.all(), many=True).data
        cities = CitySerializer(City.objects.all(), many=True).data

        return Response({"countries": countries, "states": states, "cities": cities})


class CitiesOfState(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(state_id=self.kwargs["state_id"])


class CitiesOfCountryName(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(state__country__name=self.kwargs["country_name"])


class CitiesOfCountryId(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(state__country_id=self.kwargs["country_id"])


class MinMaxPopulationView(generics.GenericAPIView):
    def get(self, request):
        agg = City.objects.aggregate(min=Min("population"), max=Max("population"))
        return Response({"min_population": agg["min"], "max_population": agg["max"]})


############
# User sign in and sign up
#############


class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print("SAVED USER:", user)
        print(type(user), "  before conversion")
        user = User.objects.get(
            username=user.username
        )  # Ensure we get the user instance after creation
        print(type(user), "   after conversion")
        # token, created = Token.objects.get_or_create(user=user)
        response_data = {
            "message": "User created successfully",
            "user_id": str(user.id),
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)
        # response.set_cookie(
        #     key='auth_token',
        #     value=token.key,
        #     httponly=True,
        #     samesite='None',
        #     secure=request.is_secure(), # Set Secure flag if served over HTTPS
        #     path='/' # Make cookie available site-wide
        # )
        return response


class SignInView(generics.GenericAPIView):
    serializer_class = (
        UserSerializer  # Not strictly needed for input if only username/password
    )
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
            # Check hashed password
            if check_password(password, user.password):
                token, created = Token.objects.get_or_create(user=user)
                response_data = {
                    "message": "Sign in successful",
                    "user_id": str(user.id),
                }

                response = Response(response_data, status=status.HTTP_200_OK)
                response.set_cookie(
                    key="auth_token",
                    value=token.key,
                    httponly=True,
                    samesite="None",
                    secure=request.is_secure(),  # Set Secure flag if served over HTTPS
                    path="/",  # Make cookie available site-wide
                )
                return response
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )  # Changed from "User does not exist" for clarity


class SignOutUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Requires token authentication to be set up

    def post(self, request, *args, **kwargs):
        try:
            # request.user.auth_token relies on TokenAuthentication being configured
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            # Handle cases where token might not exist or user is not authenticated via token
            pass

        response = Response(
            {"message": "User signed out successfully"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("auth_token", samesite="Lax", path="/")
        return response
