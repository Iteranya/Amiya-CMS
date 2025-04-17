from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import ai_config
router = APIRouter()

class ConfigSchema(BaseModel):
    system_note: str
    ai_endpoint: str
    base_llm: str
    temperature: float
    ai_key: str

    class Config:
        orm_mode = True

@router.get("/config", response_model=ConfigSchema)
async def get_config():
    """
    Retrieve the current configuration.
    """
    current_config = ai_config.load_or_create_config()
    return current_config

@router.put("/config", response_model=ConfigSchema)
async def update_config(config_data: ConfigSchema):
    """
    Update the configuration.
    
    Send a JSON payload with all keys. Example:
    {
      "system_note": "New note",
      "ai_endpoint": "https://api.example.com/v1",
      "base_llm": "your-model",
      "temperature": 0.7,
      "ai_key": "your-new-api-key"
    }
    """
    try:
        # Create a new Config instance from the Pydantic model data
        new_config = ai_config.Config(**config_data.dict())
        ai_config.save_config(new_config)
        return new_config
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating configuration: {str(e)}")

@router.delete("/config/reset", response_model=ConfigSchema)
async def reset_config():
    """
    Reset the configuration back to its default values.
    """
    try:
        default_config = ai_config.Config()  # Instantiated with default values in your dataclass
        ai_config.save_config(default_config)
        return default_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting configuration: {str(e)}")