"""
Gemma 오픈소스 LLM을 사용한 로컬 챗봇
- 완전 무료
- 네트워크 불필요 (설치 후)
- 개인정보 보호
- 영어 → 한국어 번역 기능
- 파일 번역 기능
"""

import ollama
import json
import os

# ============================================================
# 모드별 시스템 프롬프트
# ============================================================
SYSTEM_PROMPTS = {
    "대화": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 자연스럽게 대답해주세요.",
    "번역": """당신은 전문적인 영어→한국어 번역가입니다.
규칙:
1. 영어 텍스트를 정확하고 자연스럽게 한국어로 번역합니다.
2. 원문의 의미를 최대한 유지합니다.
3. 전문용어는 한국어 표준 번역어를 사용합니다.
4. 번역 결과만 출력합니다. 설명 불필요.""",
    "문서번역": """당신은 전문적인 문서 번역가입니다.
규칙:
1. 영어 문서 전체를 한국어로 번역합니다.
2. 원본의 형식(제목, 단락, 구조)을 유지합니다.
3. 전문용어는 한국어 표준 번역어를 사용합니다.
4. 번역된 문서만 출력합니다."""
}

def chat_with_gemma(user_message, conversation_history=[], model="gemma2:2b"):
    """
    Gemma와 대화하는 함수
    
    Args:
        user_message: 사용자 메시지
        conversation_history: 이전 대화 내역
        model: 사용할 Gemma 모델
    
    Returns:
        AI의 응답과 업데이트된 대화 내역
    """
    # 사용자 메시지를 대화 내역에 추가
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Ollama로 Gemma 모델 호출
        response = ollama.chat(
            model=model,
            messages=conversation_history,
            stream=False  # True로 하면 실시간 스트리밍
        )
        
        # AI 응답 추출
        ai_message = response['message']['content']
        
        # AI 응답을 대화 내역에 추가
        conversation_history.append({
            "role": "assistant",
            "content": ai_message
        })
        
        return ai_message, conversation_history
        
    except Exception as e:
        error_msg = f"오류 발생: {str(e)}"
        if "model" in str(e).lower():
            error_msg += "\n\n💡 Gemma 모델이 설치되지 않았을 수 있습니다."
            error_msg += "\n다음 명령어로 설치하세요: ollama pull gemma2:2b"
        return error_msg, conversation_history


def list_available_models():
    """설치된 모델 목록 확인"""
    try:
        models = ollama.list()
        return models
    except:
        return None


def switch_mode(mode, conversation_history):
    """모드 변경 및 시스템 프롬프트 업데이트"""
    if mode in SYSTEM_PROMPTS:
        conversation_history.clear()
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPTS[mode]
        })
        print(f"\n✅ [{mode}] 모드로 전환됨!")
        return True
    else:
        print(f"\n❌ 잘못된 모드입니다. 사용 가능: {', '.join(SYSTEM_PROMPTS.keys())}")
        return False


def translate_file(filepath, conversation_history, selected_model):
    """파일을 읽어서 번역 후 저장"""
    try:
        # 파일 읽기
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print("\n❌ 파일이 비어있습니다.")
            return

        # 문서번역 모드로 임시 전환
        temp_history = [{
            "role": "system",
            "content": SYSTEM_PROMPTS["문서번역"]
        }]

        # 번역 실행
        print("\n📄 번역 중... (파일이 클수록 시간이 걸릴 수 있습니다)")
        translated, _ = chat_with_gemma(content, temp_history, model=selected_model)

        # 번역된 파일 저장
        base, ext = os.path.splitext(filepath)
        output_path = f"{base}_korean{ext}"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)

        print(f"\n✅ 번역 완료!")
        print(f"💾 저장 경로: {output_path}")
        print(f"\n--- 번역 결과 ---\n{translated}\n--- 끝 ---")

    except FileNotFoundError:
        print(f"\n❌ 파일을 찾을 수 없습니다: {filepath}")
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")


def main():
    """메인 챗봇 루프"""
    print("=" * 60)
    print("🤖 Gemma 로컬 챗봇에 오신 것을 환영합니다!")
    print("   (완전 무료 & 오프라인 작동)")
    print("=" * 60)
    
    # 사용 가능한 Gemma 모델들
    available_models = {
        "1": ("gemma2:2b", "가장 가벼움 (2GB) - 빠른 속도"),
        "2": ("gemma2:9b", "중간 크기 (5GB) - 균형잡힌 성능"),
        "3": ("gemma2:27b", "큰 크기 (15GB) - 최고 성능"),
    }
    
    print("\n📦 사용할 모델을 선택하세요:")
    for key, (model, desc) in available_models.items():
        print(f"  {key}. {model} - {desc}")
    
    choice = input("\n선택 (1/2/3) [기본값: 1]: ").strip() or "1"
    selected_model = available_models.get(choice, available_models["1"])[0]
    
    print(f"\n✅ {selected_model} 모델을 사용합니다.")
    print("\n💡 사용 가능한 명령어:")
    print("  [모드 변경]")
    print("    mode 대화      → 일반 대화 모드")
    print("    mode 번역      → 영어→한국어 번역 모드")
    print("    mode 문서번역   → 문서 전체 번역 모드")
    print("  [파일 번역]")
    print("    file 파일경로   → 영어 파일을 한국어로 번역")
    print("    예: file C:\\Users\\Downloads\\test.txt")
    print("  [기타]")
    print("    save            → 대화 내역 저장")
    print("    reset           → 대화 초기화")
    print("    종료 / exit     → 프로그램 종료")
    print("=" * 60)
    
    # 기본 모드: 번역
    current_mode = "번역"
    conversation_history = [{
        "role": "system",
        "content": SYSTEM_PROMPTS[current_mode]
    }]
    print(f"\n✅ 기본 모드: [{current_mode}]")
    print("💡 영어 텍스트를 붙여넣기하면 바로 번역됩니다!")
    
    while True:
        # 사용자 입력 받기
        user_input = input("\n당신: ").strip()
        
        # 종료 명령 확인
        if user_input.lower() in ['종료', 'exit', 'quit']:
            print("\n챗봇: 안녕히 가세요! 좋은 하루 되세요! 👋")
            break
        
        # 대화 저장
        if user_input.lower() == 'save':
            filename = f"gemma_conversation_{len(conversation_history)}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation_history, f, ensure_ascii=False, indent=2)
            print(f"\n💾 대화가 '{filename}'에 저장되었습니다!")
            continue
        
        # 모드 변경
        if user_input.lower().startswith("mode "):
            mode = user_input[5:].strip()
            if switch_mode(mode, conversation_history):
                current_mode = mode
            continue

        # 파일 번역
        if user_input.lower().startswith("file "):
            filepath = user_input[5:].strip().strip('"').strip("'")
            translate_file(filepath, conversation_history, selected_model)
            continue
        
        # 대화 초기화 (현재 모드 유지)
        if user_input.lower() == 'reset':
            conversation_history.clear()
            conversation_history.append({
                "role": "system",
                "content": SYSTEM_PROMPTS[current_mode]
            })
            print(f"\n🔄 대화가 초기화되었습니다! (현재 모드: {current_mode})")
            continue
        
        if not user_input:
            continue
        
        # AI 응답 받기
        print("\n챗봇: ", end="", flush=True)
        ai_response, conversation_history = chat_with_gemma(
            user_input, 
            conversation_history,
            model=selected_model
        )
        
        print(ai_response)


if __name__ == "__main__":
    main()
