from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Union, Annotated, Type
from datetime import datetime
import pandas as pd


class PypiJobParameters(BaseModel):
    start_date: str = "2019-04-01"
    end_date: str = "2024-08-06"
    pypi_project: str = "duckdb"
    table_name: str
    gcp_project: str
    timestamp_column: str = "timestamp"
    destination: Annotated[
        Union[List[str], str], Field(default=["local"])
    ]   #local, s3, motherduck
    s3_path: Optional[str]
    aws_profile: Optional[str]

class File(BaseModel):
    filename: Optional[str]
    project: Optional[str]
    version: Optional[str]
    type: Optional[str]

class Libc(BaseModel):
    lib: Optional[str]
    version: Optional[str]


class Distro(BaseModel):
    name: Optional[str]
    version: Optional[str]
    id: Optional[str]
    libc: Optional[Libc]


class Implementation(BaseModel):
    name: Optional[str]
    version: Optional[str]


class Installer(BaseModel):
    name: Optional[str]
    version: Optional[str]


class System(BaseModel):
    name: Optional[str]
    release: Optional[str]

class Details(BaseModel):
    installer: Optional[Installer]
    python: Optional[str]
    implementation: Optional[Implementation]
    distro: Optional[Distro]
    system: Optional[System]
    cpu: Optional[str]
    openssl_version: Optional[str]
    setuptools_version: Optional[str]
    rustc_version: Optional[str]
    ci: Optional[bool]

class FileDownloads(BaseModel):
    timestamp: Optional[datetime] = None
    country_code: Optional[str] = None
    url: Optional[str] = None
    project: Optional[str] = None
    file: Optional[File] = None
    details: Optional[Details] = None
    tls_protocol: Optional[str] = None
    tls_cipher: Optional[str] = None

class TableValidationError(Exception):
    """Custom exception for Table validation errors."""

    pass

class DataFrameValidationError(Exception):
    """Custom exception for DataFrame validation errors."""

def validate_table(df: pd.DataFrame, model: Type[BaseModel]):
    """
    Validates each row of a DataFrame against a Pydantic model.
    Raises TableValidationError if any row fails validation.

    :param df: DataFrame to validate.
    :param model: Pydantic model to validate against.
    :raises: TableValidationError
    """
    errors = []

    for i, row in enumerate(df.to_dict(orient="records")):
        try:
            model(**row)
        except ValidationError as e:
            errors.append(f"Row {i} failed validation: {e}")

    if errors:
        error_message = "\n".join(errors)
        raise DataFrameValidationError(
            f"Table validation failed with the following errors:\n{error_message}"
        )
