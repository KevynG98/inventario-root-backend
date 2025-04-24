from rest_framework import serializers
from ..models.recepiesModels import Receta, RecetaDetalle, Medicamento, Paciente

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

class RecetaDetalleSerializer(serializers.ModelSerializer):
    medicamento = MedicamentoSerializer(read_only=True)
    medicamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicamento.objects.all(), source='medicamento', write_only=True
    )

    class Meta:
        model = RecetaDetalle
        fields = ['medicamento', 'medicamento_id', 'cantidad']

class RecetaSerializer(serializers.ModelSerializer):
    detalles = RecetaDetalleSerializer(many=True, read_only=True)
    paciente = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()
    
    class Meta:
        model = Receta
        fields = ['id', 'paciente', 'doctor', 'fecha_creacion', 'procesada', 'detalles']