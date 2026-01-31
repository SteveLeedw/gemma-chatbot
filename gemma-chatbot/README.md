# 🤖 Gemma 로컬 챗봇

**완전 무료 & 오프라인** AI 챗봇 + 영한 번역기

Ollama와 Google의 Gemma 오픈소스 LLM을 사용하여 로컬에서 실행되는 챗봇입니다.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Offline](https://img.shields.io/badge/Offline-100%25-orange.svg)

---

## ✨ 주요 기능

- 🆓 **완전 무료** - API 비용 없음
- 🔒 **프라이버시 보장** - 모든 데이터가 로컬에서 처리
- 🌐 **오프라인 사용** - 설치 후 인터넷 불필요
- 🇰🇷 **영한 번역** - 영어 텍스트/문서를 한국어로 번역
- 💾 **대화 저장** - JSON 형식으로 대화 내역 저장

---

## 📦 설치 방법

### 1단계: Ollama 설치

[Ollama 공식 사이트](https://ollama.com)에서 다운로드 후 설치

```bash
# 설치 확인
ollama --version
```

### 2단계: Gemma 모델 다운로드

```bash
# 가벼운 버전 (권장, 2GB)
ollama pull gemma2:2b

# 중간 버전 (5GB)
ollama pull gemma2:9b

# 고성능 버전 (15GB)
ollama pull gemma2:27b
```

### 3단계: Python 패키지 설치

```bash
pip install ollama
```

### 4단계: 챗봇 실행

```bash
python gemma_chatbot.py
```

---

## 🎮 사용 방법

### 모드 전환

| 명령어 | 설명 |
|--------|------|
| `mode 대화` | 일반 대화 모드 |
| `mode 번역` | 영어→한국어 번역 |
| `mode 문서번역` | 문서 전체 번역 |

### 파일 번역

```
file C:\Users\Downloads\english_doc.txt
```

### 기타 명령어

| 명령어 | 설명 |
|--------|------|
| `save` | 대화 내역 저장 |
| `reset` | 대화 초기화 |
| `종료` 또는 `exit` | 프로그램 종료 |

---

## 💻 시스템 요구사항

| 모델 | RAM | 저장공간 | 권장 사양 |
|------|-----|----------|-----------|
| gemma2:2b | 4GB+ | 2GB | 일반 PC |
| gemma2:9b | 8GB+ | 5GB | 고사양 PC |
| gemma2:27b | 16GB+ | 15GB | 워크스테이션 |

---

## 📝 예시

### 번역 모드
```
당신: The quick brown fox jumps over the lazy dog.
챗봇: 빠른 갈색 여우가 게으른 개를 뛰어넘습니다.
```

### 대화 모드
```
당신: 파이썬이 뭐야?
챗봇: 파이썬은 배우기 쉽고 강력한 프로그래밍 언어입니다...
```

---

## 🔧 문제 해결

### "model not found" 오류
```bash
ollama pull gemma2:2b
```

### Ollama 연결 실패
```bash
# Ollama 서비스 실행 확인
ollama serve
```

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🙏 크레딧

- [Ollama](https://ollama.com) - 로컬 LLM 실행 플랫폼
- [Google Gemma](https://ai.google.dev/gemma) - 오픈소스 LLM

---

Made with ❤️ for Korean users
