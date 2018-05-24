from flask import request, abort, make_response, jsonify


def validate_int_json_data(argument_name):

    #Argument might be account_id, profile_id, user_id or anything else.

    try:
        entity_id = request.json.get('{0}'.format(argument_name))
        if not entity_id:
            # abort wrong argument
            abort(make_response(jsonify({
            'error': 'wrong parameter, awaiting <{0}>'.format(argument_name)},
            400)))
    except:
        #abort if no argument
        abort(make_response(jsonify({
            'error': 'wrong parameter, awaiting <{0}>'.format(argument_name)},
            400)))

    if type(entity_id) != int:
        abort(make_response(jsonify({
            "error": '<{0}> have wrong data type, must be int'.format(argument_name)},
            400)))
    #TODO
    #Currently server returning 200 response if got error
    #Need to make to return abort message.
    return entity_id