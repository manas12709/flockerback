from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from database import db_session
from models.time_spent import TimeSpent

app = Flask(__name__)

@app.route('/api/track_time', methods=['POST'])
def track_time():
    data = request.json
    user_id = data.get('user_id')
    session_time_spent = data.get('time_spent')

    if not user_id or session_time_spent is None:
        return jsonify({'message': 'Invalid data'}), 400

    try:
        # Check if a record for the user exists
        time_record = TimeSpent.query.filter_by(user_id=user_id).first()

        if time_record:
            # Update total time spent
            time_record.total_time_spent += session_time_spent
        else:
            # Create a new record for the user
            time_record = TimeSpent(user_id=user_id, total_time_spent=session_time_spent)
            db_session.add(time_record)

        db_session.commit()
        return jsonify({'message': 'Time tracked successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'message': f'Error storing time data: {str(e)}'}), 500
