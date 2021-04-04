import argparse
import os
import json

from random import randint


def gen_key(args):
    filepath = os.path.normpath(args.out)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "w")
    byte_arr = []
    for i in range(256):
        n = randint(0, 255)
        while n in byte_arr:
            n = randint(0, 255)
        byte_arr.append(n)
    f.write(json.dumps(byte_arr))
    f.close()


def encrypt(args):
    filepath = os.path.normpath(args.key)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "r")
    key_byte_arr = json.loads(f.read())
    f.close()

    filepath = os.path.normpath(args.input)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "rb")
    s = f.read()  # считывать через генератор
    f.close()

    if args.out is None:
        args.out = args.input + ".enc"

    filepath = os.path.normpath(args.out)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "wb")

    byte_s = bytearray(s)
    length = len(byte_s)
    for i in range(length):
        byte_s[i] = key_byte_arr[byte_s[i]]
    f.write(byte_s)
    f.close()


def decrypt(args):
    filepath = os.path.normpath(args.key)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "r")
    key_byte_arr = json.loads(f.read())
    f.close()

    filepath = os.path.normpath(args.input)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "rb")
    s = f.read()  # исправить
    f.close()

    if args.out is None:
        if args.input[-4:] == ".enc":
            args.out = args.input[:-4]
        else:
            args.out = args.input + ".dec"

    filepath = os.path.normpath(args.out)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "wb")

    byte_s = bytearray(s)
    length = len(byte_s)
    for i in range(length):
        byte_s[i] = key_byte_arr.index(byte_s[i])
    f.write(byte_s)
    f.close()


def make_model(args):
    files = args.list
    freq = [0] * 256
    total = 0
    for filename in files:
        with open(filename, "r") as f:
            g = open("newfile.txt", "w")
            s = f.read()
            length = len(s)
            for i in range(length):
                if (s[i] == ' ') or (s[i] == '\n'):
                    g.write(' ')
                elif 0 <= (ord(s[i]) - ord('A')) <= 25:
                    g.write(chr(ord(s[i]) + 32))
                elif 0 <= (ord(s[i]) - ord('a')) <= 25:
                    g.write(s[i])
            g.close()
        with open("newfile.txt", "rb") as f:
            s = f.read()
            length = len(s)
            total += length
            for i in range(length):
                freq[s[i]] += 1
    for i in range(256):
        freq[i] = freq[i] / total
    filepath = os.path.normpath(args.out)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "w")
    f.write(json.dumps(freq))
    f.close()


def broke(args):
    filepath = os.path.normpath(args.input)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "rb")
    s = f.read()
    f.close()

    filepath = os.path.normpath(args.model)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "r")
    arr = json.loads(f.read())
    f.close()

    model_freq = [(arr[i], i) for i in range(256)]
    model_freq = sorted(model_freq, key=lambda byte: byte[0])

    filepath = os.path.normpath(args.out)
    filepath = os.path.expanduser(filepath)
    f = open(filepath, "w")

    arr = [0] * 256
    length = len(s)
    for i in range(length):
        arr[s[i]] += 1
    for i in range(256):
        arr[i] = arr[i] / length
    freq = [(arr[i], i) for i in range(256)]
    freq = sorted(freq, key=lambda byte: byte[0])

    key_byte_arr = [0] * 256
    for i in range(256):
        key_byte_arr[model_freq[i][1]] = freq[i][1]
    f.write(json.dumps(key_byte_arr))
    f.close()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_genkey = subparsers.add_parser("genkey", help="Generate key")
parser_genkey.add_argument("-o", "--out", "--out-file", default="sec.key", help="Name of output file")
parser_genkey.set_defaults(func=gen_key)

parser_enc = subparsers.add_parser("enc", help="Encrypt")
parser_enc.add_argument("-k", "--key", default="sec.key", help="Name of file, containing key")
parser_enc.add_argument("input", help="Name of input file")
parser_enc.add_argument("-o", "--out", "--output.file", help="Name of output file")
parser_enc.set_defaults(func=encrypt)

parser_dec = subparsers.add_parser("dec", help="Decrypt")
parser_dec.add_argument("-k", "--key", default="sec.key", help="Name of file, containing key")
parser_dec.add_argument("input", help="Name of input file")
parser_dec.add_argument("-o", "--out", "--output.file", help="Name of output file")
parser_dec.set_defaults(func=decrypt)

parser_makemodel = subparsers.add_parser("makemodel", help="Creat model")
parser_makemodel.add_argument("list", nargs="*", help="List of files")
parser_makemodel.add_argument("-o", "--out", "--output.file", default="model.txt", help="Name of output file")
parser_makemodel.set_defaults(func=make_model)

parser_broke = subparsers.add_parser("broke", help="Broke the cypher")
parser_broke.add_argument("model", help="Name of file with model")
parser_broke.add_argument("input", help="name of encrypted file")
parser_broke.add_argument("-o", "--out", "--output.file", default="sec.key", help="Name of output file")
parser_broke.set_defaults(func=broke)

args = parser.parse_args()
args.func(args)
