from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "ProtoTester"
    upload_dir: Path = Path(__file__).parent.parent / "uploaded_protos"
    compiled_dir: Path = Path(__file__).parent.parent / "compiled_protos"
    config_dir: Path = Path(__file__).parent.parent / "configs"

    def ensure_dirs(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
