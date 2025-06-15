from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Min, Max
from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer


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
