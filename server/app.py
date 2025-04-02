from flask import Flask, request, session, jsonify, make_response

app = Flask(__name__)
app.json.compact = False

app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    session["hello"] = session.get("hello") or "World"
    session["goodnight"] = session.get("goodnight") or "Moon"

    response = make_response(jsonify({
        'session': {
            'session_key': key,
            'session_value': session[key],
            'session_accessed': session.accessed,
        },
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies],
    }), 200)

    response.set_cookie('mouse', 'Cookie')

    return response

@app.route('/cookies/set', methods=['POST'])
def set_cookie():
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return jsonify({'error': 'Missing key or value in request'}), 400

    response = make_response(jsonify({
        'message': f'Cookie {data["key"]} set successfully',
        'cookie': {data['key']: data['value']}
    }))
    response.set_cookie(data['key'], data['value'])
    return response

@app.route('/sessions/clear', methods=['POST'])
def clear_session():
    session.clear()
    response = make_response(jsonify({
        'message': 'Session cleared successfully',
        'session': dict(session)
    }))
    return response

@app.route('/cookies/view', methods=['GET'])
def view_cookies():
    return jsonify({
        'cookies': [{cookie: request.cookies[cookie]}
            for cookie in request.cookies]
    })

if __name__ == '__main__':
    app.run(port=5555)
