def hash(password):
    import hashlib

    passwd_encoded = password.encode("utf-8")
    hash_obj = hashlib.sha1(passwd_encoded)

    hashed_passwd = hash_obj.hexdigest()
    return hashed_passwd.upper()


def request_data(passwd, get):
    hashed_passwd = (hash(passwd)[:5], hash(passwd)[5:])
    url = "https://api.pwnedpasswords.com/range/" + hashed_passwd[0]
    res =  get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error Fetching: {res.status_code}")
    return res, hashed_passwd[1]

def count_leaks(res, tail):
    hashes = tuple([(line.split(":")[0], line.split(":")[1].split('\r')[0]) for line in res.text.split("\n")])
    for hash, count in hashes:
        if hash == tail:
            return count
    else:
        return 0
