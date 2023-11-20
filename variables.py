import random
import string
import os

emoji_list = ['🚀', '🎉', '🌈', '🐦', '🌺', '🍕', '🏆', '🍀', '🌊', '🎃', '📷', '🍭', '🍩', '🎅', '😎', '🌟', '🚗', '🎸', '🍦', '🍹', '💻', '🎨', '🚲', '🌟', '🍔', '🌮', '🎈', '🎮', '🎤', '🚁', '🎯', '🚤', '📚', '🍸', '🌠', '🎭', '🍻', '🚂', '🏰', '🎡', '🎥', '🚁', '🌌', '🎲', '🌄', '🎓']
admin_code = ''

def get_admin_code():
    global admin_code
    random.seed = (os.urandom(128))
    admin_code = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    return admin_code

