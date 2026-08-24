from pydantic import BaseModel


class OrderIngredientMappingBaseClass(BaseModel):
    order_id: int
    ingredient_id: int
    quantity: float


class OrderIngredientMappingReadClass(OrderIngredientMappingBaseClass):
    order_ingredient_mapping_id: int


class OrderIngredientMappingCreateClass(OrderIngredientMappingBaseClass):
    pass


class OrderIngredientMappingUpdateClass(BaseModel):
    order_id: int | None = None
    ingredient_id: int | None = None
    quantity: float | None = None
