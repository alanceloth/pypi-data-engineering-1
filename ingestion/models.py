from pydantic import BaseModel, Field
from typing import List, Optional, Union, Annotated

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

    