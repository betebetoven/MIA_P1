def load_users_from_content(content):
    """Load users and groups from a string content into a dictionary structure."""
    lines = content.split("\n")
    

    data_structure = {}
    for line in lines:
        if line == '':
            continue
        parts = line.strip().split(",")
        if parts[1] == 'G':  # Group
            if parts[0] != '0':
                data_structure[parts[2]] = {}
        else:  # User
            if parts[0] != '0':
                group_name = parts[2]
                user_data = {
                    'id': parts[0],
                    'username': parts[3],
                    'password': parts[4]
                }
                if group_name in data_structure:
                    data_structure[group_name][parts[3]] = user_data
                else:
                    data_structure[group_name] = {parts[3]: user_data}

    return data_structure
