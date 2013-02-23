from django.conf import settings
import hashlib, zlib
import cPickle as pickle
import urllib

SECRET = getattr(settings, 'SECRET_KEY', '1234')


def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with `decode_data`."""
    text = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
    m = hashlib.md5(SECRET + text).hexdigest()[:12]
    return m, text


def decode_data(hash, enc):
    """The inverse of `encode_data`."""
    text = urllib.unquote(enc)
    m = hashlib.md5(SECRET + text).hexdigest()[:12]
    if m != hash:
        raise Exception("Bad hash!")
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data

# hash, enc = encode_data(['Hello', 'Goodbye'])
# print hash, enc
# print decode_data(hash, enc)