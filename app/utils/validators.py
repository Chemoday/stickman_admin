from flask import request, abort, make_response, jsonify


def validate_int_json_data(argument_name):
    """
    Argument might be account_id, profile_id, user_id or anything else.
    """


    try:
        entity_id = request.json.get('{0}'.format(argument_name))
        if not entity_id:
            # abort wrong argument
            abort(make_response(jsonify({
                'result': 'ERROR',
                'reason': 'wrong parameter, awaiting <{0}>'.format(argument_name)})))
    except:
        #abort if no argument
        abort(make_response(jsonify({
            'result': 'ERROR',
            'reason': 'wrong parameter, awaiting <{0}>'.format(argument_name)})))

    if type(entity_id) != int:
        abort(make_response(jsonify({
            'result': 'ERROR',
            "reason": '<{0}> have wrong data type, must be int'.format(argument_name)}, 400)))

    elif entity_id < 0:
        abort(make_response(jsonify({
            'result': 'ERROR',
            'reason': '<{0} cant be negative'.format(argument_name)}, 400 )))

    #TODO
    #Currently server returning 200 response if got error
    #Need to make to return abort message.

    #TODO
    #make function to accept kwargs
    return entity_id


def validate_string_json_data(argument_name):
    """
    Argument might be account_id, profile_id, user_id or anything else.
    """


    try:
        string = request.json.get('{0}'.format(argument_name))
        if string is None:
            # abort wrong argument
            abort(make_response(jsonify({
                'result': 'ERROR',
                'reason': 'empty string, <{0}> argument cant be empty'.format(argument_name)})))
    except:
        #abort if no argument
        abort(make_response(jsonify({
            'result': 'ERROR',
            'reason': 'wrong parameter, awaiting <{0}>'.format(argument_name)})))

    if type(string) != str:
        abort(make_response(jsonify({
            'result': 'ERROR',
            "reason": '<{0}> have wrong data type, must be str'.format(argument_name)}, 400)))

    elif len(string) < 4:
        abort(make_response(jsonify({
            'result': 'ERROR',
            'reason': '<{0}> is too short'.format(argument_name)}, 400 )))

    #TODO
    #Currently server returning 200 response if got error
    #Need to make to return abort message.

    #TODO
    #make function to accept kwargs
    return string