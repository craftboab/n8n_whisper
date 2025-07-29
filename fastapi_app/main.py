import os
import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
import logging
from whisper_handler import get_whisper_handler

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Secretary API",
    description="音声入力対応のAI秘書API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数から設定を読み込み
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secretpassword@localhost:5432/ai_secretary")
N8N_BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678")

class AudioResponse(BaseModel):
    message: str
    transcription: Optional[str] = None
    language: Optional[str] = None
    confidence: Optional[float] = None
    status: str

class HealthResponse(BaseModel):
    status: str
    database_url: str
    n8n_url: str
    whisper_model: str

class VoiceCommandRequest(BaseModel):
    command: str

class VoiceCommandResponse(BaseModel):
    message: str
    command: str
    status: str

@app.get("/", response_model=dict)
async def root():
    """ルートエンドポイント"""
    return {
        "message": "AI Secretary API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        whisper_handler = get_whisper_handler()
        whisper_info = whisper_handler.get_model_info()
    except Exception as e:
        logger.error(f"Whisper初期化エラー: {str(e)}")
        whisper_info = {"model_name": "error"}
    
    return HealthResponse(
        status="healthy",
        database_url=DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "not_configured",
        n8n_url=N8N_BASE_URL,
        whisper_model=whisper_info.get("model_name", "unknown")
    )

@app.post("/audio/transcribe", response_model=AudioResponse)
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    音声ファイルをテキストに変換するエンドポイント
    Whisperを使用して音声認識を実行
    """
    try:
        # ファイル形式チェック
        if not audio_file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="音声ファイルのみ受け付けます")
        
        # ファイルサイズチェック（25MB制限）
        if audio_file.size > 25 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="ファイルサイズは25MB以下にしてください")
        
        # 音声ファイルを読み込み
        content = await audio_file.read()
        
        # ファイル拡張子を取得
        file_extension = audio_file.filename.split(".")[-1] if "." in audio_file.filename else "wav"
        
        # WhisperHandlerを使用して音声認識を実行
        whisper_handler = get_whisper_handler()
        result = whisper_handler.transcribe_from_bytes(
            audio_bytes=content,
            file_extension=file_extension,
            language=language
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=f"音声認識エラー: {result.get('error', 'Unknown error')}")
        
        logger.info(f"音声ファイル処理完了: {audio_file.filename}")
        
        return AudioResponse(
            message="音声認識が完了しました",
            transcription=result["transcription"],
            language=result["language"],
            confidence=result.get("confidence"),
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"音声処理エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"音声処理中にエラーが発生しました: {str(e)}")

@app.post("/process/voice-command", response_model=VoiceCommandResponse)
async def process_voice_command(request: VoiceCommandRequest):
    """
    音声コマンドを処理するエンドポイント
    n8nワークフローと連携
    """
    try:
        # n8nワークフローへのリクエスト処理
        # 実際の実装ではn8nのwebhookを呼び出す
        
        logger.info(f"音声コマンド処理: {request.command}")
        
        return VoiceCommandResponse(
            message="コマンドが処理されました",
            command=request.command,
            status="processed"
        )
        
    except Exception as e:
        logger.error(f"コマンド処理エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"コマンド処理中にエラーが発生しました: {str(e)}")

@app.get("/config")
async def get_config():
    """設定情報を取得するエンドポイント"""
    try:
        whisper_handler = get_whisper_handler()
        whisper_info = whisper_handler.get_model_info()
    except Exception as e:
        whisper_info = {"model_name": "error", "available_models": []}
    
    return {
        "database_url": DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "not_configured",
        "n8n_base_url": N8N_BASE_URL,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "whisper_model": whisper_info.get("model_name", "unknown"),
        "available_whisper_models": whisper_info.get("available_models", [])
    }

@app.get("/whisper/models")
async def get_whisper_models():
    """利用可能なWhisperモデルを取得するエンドポイント"""
    try:
        whisper_handler = get_whisper_handler()
        return {
            "current_model": whisper_handler.model_name,
            "available_models": whisper_handler.get_available_models(),
            "model_info": whisper_handler.get_model_info()
        }
    except Exception as e:
        logger.error(f"Whisperモデル情報取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Whisperモデル情報の取得に失敗しました: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    ) 