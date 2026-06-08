from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter(prefix="/api/proto", tags=["proto"])


@router.post("/upload")
async def upload_proto(file: UploadFile):
    """上传 .proto 文件，编译 + 提取 schema（待实现）"""
    raise HTTPException(501, "Proto upload not implemented yet")


@router.get("/list")
async def list_protos():
    """列出已上传的 proto 文件（待实现）"""
    raise HTTPException(501, "Proto list not implemented yet")


@router.get("/{filename}/schema")
async def get_schema(filename: str):
    """获取指定 proto 的完整 schema（待实现）"""
    raise HTTPException(501, "Proto schema not implemented yet")


@router.delete("/{filename}")
async def delete_proto(filename: str):
    """删除 proto 文件（待实现）"""
    raise HTTPException(501, "Proto delete not implemented yet")
