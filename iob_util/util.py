"""Util function around iob

This module contains iob util

Example:
    IOB decoding::

        convert_iob_to_dict(['私', 'は', '宇', '宙', '人'], ['O', 'O', 'B-C', 'I-C', 'I-C'])
        convert_iob_to_xml(['私', 'は', '宇', '宙', '人'], ['O', 'O', 'B-C', 'I-C', 'I-C'])

    IOB encoding::

        iobs = convert_xml_to_iob('私は<C value="N">宇宙人</C>', tag_lists=['C'], attr=['value'], tokenizer=list)
        print_iob(iobs)
"""

import sys
from xml.etree.ElementTree import iterparse
import xml.etree.ElementTree as ET


def split_tag(tag):
    if tag == "O":
        return tag, None
    else:
        t, l = tag.split('-')
        return t, l


def convert_iob_to_dict(tt, ii):
    """Convert iob to dict

    Convert tokens and IOB2 labels to dict format

    Args:
        tt (List): token list
        ii (List): IOB2 label list

    Returns:
        List: List of dict. Format = [{'span':(start_idx, end_idx), 'type': tag, 'word': word}]

    """
    assert len(tt) == len(ii), ''

    ii = ['O'] + ii + ['O']
    s_pos = -1
    word = ''
    result = []
    for idx in range(1, len(ii)-1):
        prefix, tag = split_tag(ii[idx])
        if is_chunk_start(ii[idx-1], ii[idx]):
            s_pos = idx - 1

        if s_pos != -1:
            word += tt[idx-1]

        if is_chunk_end(ii[idx], ii[idx+1]):
            result.append({'span':(s_pos, idx), 'type':tag, 'word':word})
            s_pos = -1
            word = ''

    return result


def convert_dict_to_xml(sent, dd):
    result = ''
    idx = 0
    for d in dd:
        s_pos, e_pos = d['span']
        while idx < s_pos:
            result += sent[idx]
            idx += 1

        if 'norm' in d:
            result += '<' + d['type'] + '>'
        else:
            result += '<' + d['type'] + '>'

        result += d['word']
        result += '</' + d['type'] + '>'

        idx = e_pos

    while idx < len(sent):
        result += sent[idx]
        idx += 1

    return result


def convert_iob_to_xml(tokens, iobs):
    """Convert iob to xml

    Convert tokens and IOB2 labels to xml format.

    Args:
        tt (List): token list
        ii (List): IOB2 label list

    Returns:
        str: Xml output.

    """
    dic = convert_iob_to_dict(tokens, iobs)
    return convert_dict_to_xml(''.join(tokens), dic)


def convert_xml_to_taglist(sent, tag_list=None, attr=None):
    text = '<sent>' + sent + '</sent>'
    parser = ET.XMLPullParser(['start', 'end'])
    parser.feed(text)

    ne_type = "O"
    ne_prefix = ""
    res = ""
    label = []
    tag_set = set()
    s_pos = -1
    idx = 0

    for event, elem in parser.read_events():
        isuse = (tag_list is None
                or (tag_list is not None and elem.tag in tag_list))

        if event == 'start':
            assert len(tag_set) < 2, "タグが入れ子になっています\n{}".format(sent)
            s_pos = idx

            if elem.attrib:
                attr_list = ''.join([v for k, v in elem.attrib.items() if k in attr])
            else:
                attr_list = ''

            word = elem.text if elem.text is not None else ""
            res += word
            idx += len(word)

            if elem.tag != 'sent' and isuse:
                tag_set.add(elem.tag)
                label.append((s_pos, idx-1, elem.tag + attr_list, word))

        if event == 'end':
            if elem.tag != 'sent' and isuse:
                tag_set.remove(elem.tag)
            word = elem.tail if elem.tail is not None else ""
            res += word
            idx += len(word)

    return res, label


def convert_taglist_to_iob(sent, label, tokenizer=list):
    tokens = tokenizer(sent)
    results = []

    idx = 0
    i = 0
    j = 0

    nebegin = True

    while j < len(sent) and idx < len(label):
        k = j + len(tokens[i]) - 1
        if k < label[idx][0]:
            results.append((tokens[i], 'O'))
        elif label[idx][0] <= k and nebegin:
            results.append((tokens[i], 'B-' + label[idx][2]))
            nebegin = False
        else:
            results.append((tokens[i], 'I-' + label[idx][2]))

        j += len(tokens[i])
        i += 1

        while idx < len(label) and label[idx][1] < j:
            idx += 1
            nebegin = True

    while i < len(tokens):
        results.append((tokens[i], 'O'))
        i += 1


    return results


def convert_xml_to_iob(sent, tag_list=None, attr=None, tokenizer=list):
    """Convert xml to iob.

    Convert xml to IOB2 format. You can limit valid tag and attribute.

    Args:
        sent (str): Input xml string.
        tag_list (List): List of valid tag.
        attr (List): List of valid attribute.
        tokenizer (callable): Tokenize function. str->List

    Returns:
        List (tuple): List of (token, IOB2 tag)
    """
    res, label = convert_xml_to_taglist(sent, tag_list=tag_list, attr=attr)
    return convert_taglist_to_iob(res, label, tokenizer=tokenizer)


def print_iob(iob):
    for t, l in iob:
        print(t + '\t' + l)


def is_chunk_end(tag, post_tag):
    prefix1, chunk_type1 = split_tag(tag)
    prefix2, chunk_type2 = split_tag(post_tag)

    if prefix1 == 'O':
        return False
    if prefix2 == 'O':
        return prefix1 != 'O'

    return chunk_type1 != chunk_type2

def is_chunk_start(prev_tag, tag):
    prefix1, chunk_type1 = split_tag(prev_tag)
    prefix2, chunk_type2 = split_tag(tag)

    if prefix2 == 'O':
        return False
    if prefix1 == 'O':
        return prefix2 != 'O'

    return chunk_type1 != chunk_type2

def load_iob(fn, z=True):
    """Load IOB2 file.

    Load IOB2 file.

    Args:
        fn (str): File path of IOB2 file.
        z (bool): Output format. True means this returns [(token, IOB2)] and False means [token_list, IOB2_list]

    """
    with open(fn, 'r') as f:
        iobs = [lines.split('\n') for lines in f.read().split('\n\n') if lines != '']
        iobs = [[i.split('\t') for i in ii] for ii in iobs]

    if not z:
        iobs = [list(zip(*iob)) for iob in iobs]
        return [list(iob[0]) for iob in iobs], [list(iob[1]) for iob in iobs]

    return iobs


"""
if __name__ == "__main__":
    # data path
    data = sys.argv[1]

    # 属性リスト
    attr_list = ['MOD']

    # 有効なタグリスト
    valid_tag = ['C']
    #valid_tag = None

    # tokenizer
    # 文字単位だと
    tokenizer = list
    mecab = MeCab.Tagger('-Owakati')
    tokenizer = Tokenizer(mecab).tokenize

    # 東大BERT
    mecab = MeCab.Tagger('-Owakati -d /opt/mecab/lib/mecab/dic/mecab-ipadic-neologd -u /opt/mecab/lib/mecab/dic/MANBYO_201907_Dic-utf8.dic')
    tokenizer = Tokenizer(mecab).tokenize

    
    with open(data, 'r') as f:
        for i, line in enumerate(f):
            line = line.rstrip()

            if not line:
                continue

            #res, tags = convert_xml_to_taglist(line, valid_tag, attr=attr_list)
            #tag_list = convert_taglist_to_iob(res, tags)
            tag_list = convert_xml_to_iob(line, valid_tag, attr_list)

            #print_iob(tag_list)
            #print("")

            tokens, iobs = zip(*tag_list)

            res = convert_iob_to_xml(list(tokens), list(iobs))
            print(load_iob('sample.txt', z=False))
"""
