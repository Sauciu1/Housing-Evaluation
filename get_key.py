def get_key():
    def read_keys(file_path):
        with open(file_path, 'r') as file:
            keys = file.read().splitlines()
        return eval(keys[0])


    google_key = read_keys('keys.txt')["google_api"]
    return google_key