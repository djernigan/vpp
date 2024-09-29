from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)

@app.route('/participants', methods=['POST'])
def parse_request():
    ders = []
    
    if not request.json or not 'eventid' in request.json:
        abort(400)
    event = {
        'eventid': request.json['eventid'],
        'kwh': request.json.get('kwh', 0),
        'start': request.json.get('start', 0),
        'stop': request.json.get('stop', 0),
    }
    for i in range(len(request.json.get('ders'))):
        ders.append(request.json.get('ders')[i])
    return jsonify({'participants': pick_participants(event['kwh'], event['stop'] - event['start'], ders)}), 200

def pick_participants(kwh, hours, ders):
    ders.sort(key=lambda der: der['kw'])
    participants = []
    total = 0
    i = 0
    for i in range(len(ders)):
        total = total + ders[i]['kw'] * hours
        if total > kwh:
            break
        participants.append(ders[i])
    return participants
       
if __name__ == '__main__':
    app.run(debug=True)
