from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import AddressDetails
from schemas.address import AddressClassCreate
from services.base import BaseService


class AddressService(BaseService[AddressDetails]):
    def __init__(self, session: AsyncSession):
        print("-------------------------------- Entering AddressService.__init__")
        self.session = session
        super().__init__(AddressDetails, session)

    async def add_address(self, address_data: AddressClassCreate):
        print("-------------------------------- Entering AddressService.add_address")
        data = AddressDetails(
            **address_data.model_dump(),
        )
        return await self._create(data)

    async def get_address_by_id(self, address_id: UUID):
        print(
            "-------------------------------- Entering AddressService.get_address_by_id"
        )
        return await self._get(address_id)

    async def update_address(self, address_id: UUID, address_data: AddressClassCreate):
        print("-------------------------------- Entering AddressService.update_address")

        address = await self._get(address_id)

        if address is None:
            return None

        address.address_line_1 = address_data.address_line_1 or address.address_line_1
        address.address_line_2 = address_data.address_line_2 or address.address_line_2
        address.city = address_data.city or address.city
        address.state_name = address_data.state_name or address.state_name
        address.pincode = address_data.pincode or address.pincode
        address.country = address_data.country or address.country
        address.google_maps_link = (
            address_data.google_maps_link or address.google_maps_link
        )

        return await self._update(address)

    async def delete_address(self, address_id: UUID):
        print("-------------------------------- Entering AddressService.delete_address")

        address = await self._get(address_id)

        if address is None:
            return None

        return await self._delete(address)
