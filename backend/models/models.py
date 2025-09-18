from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    free = 'free'
    premium = 'premium'
    premium_plus = 'premium_plus'


class UserCreate(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterResponse(BaseModel):
    confirm_url: str
    email_task_id: str


class ResendEmailRequest(BaseModel):
    username: EmailStr


class PasswordResetRequest(BaseModel):
    username: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str