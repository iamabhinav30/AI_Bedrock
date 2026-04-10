from bedrock_client import client, model_id


def add_user_message(messages, text):
    messages.append({
        'role': 'user',
        'content': [{'text': text}]
    })


def add_assistant_message(messages, text):
    messages.append({
        'role': 'assistant',
        'content': [{'text': text}]
    })


def chat(messages, system=None, temperature=0.3, stop_sequences=None):
    params = {
        'modelId': model_id,
        'messages': messages,
        'inferenceConfig': {
            'temperature': temperature
        }
    }

    if stop_sequences:
        params['inferenceConfig']['stopSequences'] = stop_sequences

    if system:
        params['system'] = [{'text': system}]

    response = client.converse(**params)

    return response['output']['message']['content'][0]['text']
