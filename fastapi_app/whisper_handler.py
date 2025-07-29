import os
import whisper
import logging
from typing import Optional
import tempfile

logger = logging.getLogger(__name__)

class WhisperHandler:
    """OpenAI Whisperを使用した音声認識ハンドラー"""
    
    def __init__(self, model_name: str = "base"):
        """
        WhisperHandlerの初期化
        
        Args:
            model_name: 使用するWhisperモデル名 (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Whisperモデルを読み込み"""
        try:
            logger.info(f"Whisperモデル '{self.model_name}' を読み込み中...")
            self.model = whisper.load_model(self.model_name)
            logger.info("Whisperモデルの読み込みが完了しました")
        except Exception as e:
            logger.error(f"Whisperモデルの読み込みに失敗しました: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None) -> dict:
        """
        音声ファイルをテキストに変換
        
        Args:
            audio_file_path: 音声ファイルのパス
            language: 言語コード（例: 'ja', 'en'）。Noneの場合は自動検出
            
        Returns:
            dict: 変換結果を含む辞書
        """
        try:
            logger.info(f"音声ファイルの変換を開始: {audio_file_path}")
            
            # Whisperで音声認識を実行
            result = self.model.transcribe(
                audio_file_path,
                language=language,
                task="transcribe"
            )
            
            transcription = result.get("text", "").strip()
            language_detected = result.get("language", "unknown")
            
            logger.info(f"音声認識完了 - 言語: {language_detected}, 文字数: {len(transcription)}")
            
            return {
                "transcription": transcription,
                "language": language_detected,
                "status": "success",
                "confidence": result.get("confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"音声認識中にエラーが発生しました: {str(e)}")
            return {
                "transcription": "",
                "language": "unknown",
                "status": "error",
                "error": str(e)
            }
    
    def transcribe_from_bytes(self, audio_bytes: bytes, file_extension: str = "wav", language: Optional[str] = None) -> dict:
        """
        バイトデータから音声認識を実行
        
        Args:
            audio_bytes: 音声ファイルのバイトデータ
            file_extension: ファイル拡張子
            language: 言語コード
            
        Returns:
            dict: 変換結果を含む辞書
        """
        try:
            # 一時ファイルを作成
            with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # 音声認識を実行
            result = self.transcribe_audio(temp_file_path, language)
            
            # 一時ファイルを削除
            os.unlink(temp_file_path)
            
            return result
            
        except Exception as e:
            logger.error(f"バイトデータからの音声認識中にエラーが発生しました: {str(e)}")
            return {
                "transcription": "",
                "language": "unknown",
                "status": "error",
                "error": str(e)
            }
    
    def get_available_models(self) -> list:
        """利用可能なWhisperモデルのリストを取得"""
        return ["tiny", "base", "small", "medium", "large"]
    
    def get_model_info(self) -> dict:
        """現在のモデル情報を取得"""
        return {
            "model_name": self.model_name,
            "available_models": self.get_available_models(),
            "loaded": self.model is not None
        }

# グローバルインスタンス
whisper_handler = None

def get_whisper_handler() -> WhisperHandler:
    """WhisperHandlerのシングルトンインスタンスを取得"""
    global whisper_handler
    if whisper_handler is None:
        model_name = os.getenv("WHISPER_MODEL", "base")
        whisper_handler = WhisperHandler(model_name)
    return whisper_handler 