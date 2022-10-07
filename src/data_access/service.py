from src import VolunteerServiceModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.schemas.service.data_access import (
    VolunteerServiceInputSchema,
    VolunteerServiceSchema,
)


class VolunteerServiceDataAccess(
    BaseAsyncPostgresDataAccess[VolunteerServiceModel, VolunteerServiceInputSchema, VolunteerServiceSchema]
):
    _model = VolunteerServiceModel
    _input_schema = VolunteerServiceInputSchema
    _output_schema = VolunteerServiceSchema
