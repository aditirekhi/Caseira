from pydantic import BaseModel


class OrderRecipeMappingBaseClass(BaseModel):
    order_id: int
    recipe_id: int
    quantity: int
    price: float


class OrderRecipeMappingReadClass(OrderRecipeMappingBaseClass):
    order_recipe_mapping_id: int


class OrderRecipeMappingCreateClass(OrderRecipeMappingBaseClass):
    pass


class OrderRecipeMappingUpdateClass(BaseModel):
    order_id: int | None = None
    recipe_id: int | None = None
    quantity: int | None = None
    price: float | None = None
