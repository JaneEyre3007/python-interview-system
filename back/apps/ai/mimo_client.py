import requests
import json
from duckduckgo_search import DDGS


def search_questions(topic, question_type, difficulty, count=5):
    type_keywords = {
        'choice': '选择题',
        'fill': '填空题',
        'code': '编程题',
        'short': '简答题'
    }

    query = f"{topic} Python面试题 {type_keywords.get(question_type, '面试题')} {difficulty}"

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=count * 2, region='cn-zh'))
            return results
    except Exception as e:
        print(f"搜索失败: {e}")
        return []


def save_token_usage(api_type, prompt_tokens, completion_tokens, user=None, model_name='mimo-v2.5-pro'):
    from .models import TokenUsage
    try:
        TokenUsage.objects.create(
            user=user,
            api_type=api_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=model_name
        )
    except Exception as e:
        print(f"保存Token记录失败: {e}")


def get_user_ai_config(user):
    if user and hasattr(user, 'ai_config') and user.ai_config.is_active:
        config = user.ai_config
        return {
            'api_key': config.api_key,
            'api_url': config.api_url,
            'model_name': config.model_name
        }
    return None


class MiMoClient:
    def _call_api(self, messages, temperature=0.7, max_tokens=2000, user=None):
        config = get_user_ai_config(user)
        if not config:
            raise Exception('请先在个人设置中配置AI模型（点击右上角用户名 → AI配置）')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config["api_key"]}'
        }

        payload = {
            'model': config['model_name'],
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': False
        }

        try:
            response = requests.post(config['api_url'], headers=headers, json=payload, timeout=120)

            if response.status_code != 200:
                print(f"API URL: {config['api_url']}")
                print(f"Request payload: {json.dumps(payload, ensure_ascii=False)}")
                print(f"Response status: {response.status_code}")
                print(f"Response body: {response.text}")

            response.raise_for_status()
            data = response.json()

            if 'choices' in data and len(data['choices']) > 0:
                return data, config['model_name']
            elif 'output' in data:
                return {'choices': [{'message': {'content': data['output']}}]}, config['model_name']
            elif 'content' in data:
                return {'choices': [{'message': {'content': data['content']}}]}, config['model_name']
            else:
                return data, config['model_name']
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")

    def _extract_content(self, result):
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0].get('message', {}).get('content', '')
        return ''

    def _extract_token_usage(self, result):
        usage = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        return prompt_tokens, completion_tokens

    def generate_question(self, topic='Python', question_type='choice', difficulty='medium', count=1, user=None):
        type_desc = {
            'choice': '选择题（含4个选项A/B/C/D）',
            'fill': '填空题',
            'code': '编程题',
            'short': '简答题'
        }

        search_results = search_questions(topic, question_type, difficulty, count)

        search_context = ""
        if search_results:
            search_context = "\n\n以下是搜索到的相关内容：\n"
            for i, result in enumerate(search_results[:3], 1):
                title = result.get('title', '')
                body = result.get('body', '')[:500]
                search_context += f"\n{i}. {title}\n{body}\n"

        prompt = f"""根据搜索结果，整理{count}道{topic}的{difficulty}难度{type_desc.get(question_type, '面试题')}。

{search_context}

返回JSON格式：
{{"questions": [{{"content": "题目", "options": {{"A": "", "B": "", "C": "", "D": ""}}, "answer": "答案", "explanation": "解析"}}]}}

注意：只返回JSON，不要markdown标记，不要其他内容。"""

        messages = [
            {'role': 'system', 'content': '你是一个专业的中文Python面试题整理专家。请根据搜索结果整理出标准的面试题目，所有内容必须是中文。'},
            {'role': 'user', 'content': prompt}
        ]

        result, model_name = self._call_api(messages, temperature=0.3, max_tokens=4000, user=user)
        content = self._extract_content(result)

        prompt_tokens, completion_tokens = self._extract_token_usage(result)
        save_token_usage('generate', prompt_tokens, completion_tokens, user, model_name)

        try:
            import re
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*$', '', content)
            content = content.strip()

            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
            return {'questions': [], 'raw_response': content}
        except (json.JSONDecodeError, ValueError):
            return {'questions': [], 'raw_response': content}

    def evaluate_answer(self, question, correct_answer, user_answer, user=None):
        prompt = f"""请评判以下Python面试题的答案：

题目：{question}

正确答案：{correct_answer}

用户答案：{user_answer}

请给出：
1. 是否正确（正确/部分正确/错误）
2. 得分（0-10分）
3. 详细的反馈和改进建议

请用简洁的中文回答。"""

        messages = [
            {'role': 'system', 'content': '你是一个专业的Python面试评判专家，能够公正、准确地评判答案并给出建设性反馈。'},
            {'role': 'user', 'content': prompt}
        ]

        result, model_name = self._call_api(messages, temperature=0.3, user=user)
        content = self._extract_content(result)

        prompt_tokens, completion_tokens = self._extract_token_usage(result)
        save_token_usage('evaluate', prompt_tokens, completion_tokens, user, model_name)

        return content


mimo_client = MiMoClient()


def generate_questions(topic='Python', question_type='choice', difficulty='medium', count=1, user=None):
    return mimo_client.generate_question(topic, question_type, difficulty, count, user)


def evaluate_answer(question, correct_answer, user_answer, user=None):
    return mimo_client.evaluate_answer(question, correct_answer, user_answer, user)
