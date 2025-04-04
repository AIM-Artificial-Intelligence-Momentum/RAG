
from datetime import datetime, timedelta

def parse_clu_response(clu_response):
    parsed = {}
    try:
        entities = clu_response['result']['prediction']['entities']
        for ent in entities:
            parsed[ent['category']] = ent['text']
    except KeyError:
        return {}
    return parsed

def normalize_date(text):
    today = datetime.today()
    if "3월 말" in text:
        return ("2025-03-20", "2025-03-31")
    elif "4월 초" in text:
        return ("2025-04-01", "2025-04-10")
    elif "5월" in text:
        return ("2025-05-01", "2025-05-31")
    else:
        return (today.strftime("%Y-%m-%d"), (today + timedelta(days=10)).strftime("%Y-%m-%d"))

def build_kopis_query(entities):
    genre = entities.get("장르", "")
    region = entities.get("지역", "")
    date_text = entities.get("일정", "")
    start_date, end_date = normalize_date(date_text)

    return {
        "genre": genre,
        "region": region,
        "startDate": start_date,
        "endDate": end_date
    }

def make_gpt_prompt(entities, search_results):
    genre = entities.get("장르", "공연")
    region = entities.get("지역", "")
    date = entities.get("일정", "")
    budget = entities.get("예산", "예산 미정")

    prompt = f"""사용자가 원하는 공연 조건은 다음과 같습니다:
- 지역: {region}
- 장르: {genre}
- 일정: {date}
- 예산: {budget}

이에 해당하는 공연 추천 결과는 다음과 같습니다:
{search_results}

이를 바탕으로 사용자가 이해하기 쉬운 자연어로 공연 기획 요약을 생성해 주세요.
"""
    return prompt
