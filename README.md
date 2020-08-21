# IOB-util
IOB2のutil

## インストール
`pip install git+https://github.com/ujiuji1259/IOB-util.git`

## 使い方
### xml -> IOB2
```
>>> from iob_util import convert_xml_to_iob
>>> xml = '私は<c value="N">宇宙人</c>です．'
>>> convert_xml_to_iob(xml, tokenizer=list)
[('私', 'O'), ('は', 'O'), ('宇', 'B-c'), ('宙', 'I-c'), ('人', 'I-c'), ('で', 'O'), ('す', 'O'), ('．', 'O')]

>>> convert_xml_to_iob(xml, tag_list=['c'], attr=['value'])
[('私', 'O'), ('は', 'O'), ('宇', 'B-cN'), ('宙', 'I-cN'), ('人', 'I-cN'), ('で', 'O'), ('す', 'O'), ('．', 'O')]

>>> convert_xml_to_iob(xml, tag_list=[], attr=['value'])
[('私', 'O'), ('は', 'O'), ('宇', 'O'), ('宙', 'O'), ('人', 'O'), ('で', 'O'), ('す', 'O'), ('．', 'O')]
```

### IOB2 -> (xml, dict)
```
>>> from iob_util import convert_iob_to_xml, convert_iob_to_dict
>>> tokens = ['私', 'は', '宇', '宙', '人', 'で', 'す', '．']
>>> iobs = ['O', 'O', 'B-cN', 'I-cN', 'I-cN', 'O', 'O', 'O']
>>> convert_iob_to_xml(tokens, iobs)
'私は<cN>宇宙人</cN>です．'

>>> convert_iob_to_dict(tokens, iobs)
[{'span': (2, 5), 'type': 'cN', 'word': '宇宙人'}]
```

### util
sample.iob
```
私\tO
は\tO
宇\tC
宙\tC
人\tC
だ\tO

私\tO
は\tO
宇\tC
宙\tC
人\tC
だ\tO
```

```
>>> from iob_util import load_iob, unzip_iob
>>> load_iob('sample.iob', z=True)
[[['私', 'O'], ['は', 'O'], ['宇', 'C'], ['宙', 'O'], ['人', 'O'], ['で', 'O'], ['す', 'O']], [['私', 'O'], ['は', 'O'], ['宇', 'C'], ['宙', 'O'], ['人', 'O'], ['で', 'O'], ['す', 'O']]]

>>> load_iob('sample.iob', z=False)
([['私', 'は', '宇', '宙', '人', 'で', 'す'], ['私', 'は', '宇', '宙', '人', 'で', 'す']], [['O', 'O', 'C', 'O', 'O', 'O', 'O'], ['O', 'O', 'C', 'O', 'O', 'O', 'O']])

>>> iob = [['私', 'O'], ['は', 'O'], ['宇', 'C'], ['宙', 'O'], ['人', 'O'], ['で', 'O'], ['す', 'O']]
>>> unzip_iob(iob)
(['私', 'は', '宇', '宙', '人', 'で', 'す'], ['O', 'O', 'C', 'O', 'O', 'O', 'O'])
```

## ドキュメント
[こちら](https://ujiuji1259.github.io/IOB-util/)
