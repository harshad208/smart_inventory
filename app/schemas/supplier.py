from pydantic import BaseModel, EmailStr


class SupplierBase(BaseModel):
    name: str
    contact_person: str | None = None
    email: EmailStr
    phone: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SupplierBase):
    pass


class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True
