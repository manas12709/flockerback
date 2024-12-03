from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for polls (for simplicity)
polls = {}

@app.route('/api/polls', methods=['POST'])
def create_poll():
    data = request.get_json()
    poll_id = len(polls) + 1
    polls[poll_id] = {
        'question': data['question'],
        'options': {option: 0 for option in data['options']},
        'total_votes': 0
    }
    return jsonify({'message': 'Poll created successfully!', 'poll_id': poll_id}), 201

@app.route('/api/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = polls.get(poll_id)
    if poll:
        return jsonify(poll)
    return jsonify({'message': 'Poll not found'}), 404

@app.route('/api/polls/<int:poll_id>/vote', methods=['POST'])
def vote_poll(poll_id):
    data = request.get_json()
    option = data['option']

    poll = polls.get(poll_id)
    if not poll:
        return jsonify({'message': 'Poll not found'}), 404

    if option not in poll['options']:
        return jsonify({'message': 'Invalid option'}), 400

    poll['options'][option] += 1
    poll['total_votes'] += 1
    return jsonify({'message': 'Vote recorded successfully!', 'poll': poll})

if __name__ == '__main__':
    app.run(debug=True)
