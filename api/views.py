from rest_framework.views import APIView
from rest_framework.response import Response
from .models import create_dynamic_model, ModelSchema
from .serializers import TableRequestSerializer
from utils.schema import SchemaEditor
from rest_framework import status


class TableApiView(APIView):
    """This view handles POST requests to create dynamic tables"""

    def post(self, request):
        table_serializer = TableRequestSerializer(data=request.data)

        if table_serializer.is_valid():
            table_name = table_serializer.validated_data['table_name']
            fields = table_serializer.validated_data['fields']

            try:
                existing_model = ModelSchema.objects.filter(table_name=table_name)
                if existing_model:
                    return Response({"message":f"Table {table_name} already exists. "
                                               f"Create a table with a different name."},
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                Response({"Error message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            dynamic_model = create_dynamic_model(table_name, fields)

            # Create and apply migrations for the model creation
            schema_editor = SchemaEditor()
            schema_editor.create_model(dynamic_model, fields)

            ModelSchema.objects.create(table_name=table_name)

            return Response(table_serializer.data, status=status.HTTP_201_CREATED)

        return Response(table_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

