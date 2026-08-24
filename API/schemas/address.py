from uuid import UUID

from schemas.base import BaseSchema, BaseUpdateSchema


class AddressClassBase(BaseSchema):
    contact_name: str
    contact_number: str
    address_line_1: str
    address_line_2: str | None
    city: str
    state_name: str
    pincode: str
    country: str
    google_maps_link: str | None


class AddressClassRead(AddressClassBase):
    address_id: UUID


class AddressClassCreate(AddressClassBase):
    pass


class AddressClassUpdate(BaseUpdateSchema):
    contact_name: str | None = None
    contact_number: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_name: str | None = None
    pincode: str | None = None
    country: str | None = None
    google_maps_link: str | None = None
