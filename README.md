# IOB-util
IOB2のutil

## インストール
`pip install git+https://github.com/ujiuji1259/IOB-util.git`

## 使い方
### xml -> IOB2
```
>>> from iob_util import convert_xml_to_iob
>>> xml = '私は<c value="N">宇宙人</c>です．'
>>> convert_xml_to_iob(xml)
[('私', 'O'), ('は', 'O'), ('宇', 'B-c'), ('宙', 'I-c'), ('人', 'I-c'), ('で', 'O'), ('す', 'O'), ('．', 'O')]

>>> convert_xml_to_iob(xml, tag_list=['c'], attr=['value'])
[('私', 'O'), ('は', 'O'), ('宇', 'B-cN'), ('宙', 'I-cN'), ('人', 'I-cN'), ('で', 'O'), ('す', 'O'), ('．', 'O')]

>>> convert_xml_to_iob(xml, tag_list=[], attr=['value'])
[('私', 'O'), ('は', 'O'), ('宇', 'O'), ('宙', 'O'), ('人', 'O'), ('で', 'O'), ('す', 'O'), ('．', 'O')]
```

### IOB2 -> (xml, dict)
```
>>> from iob_util import convert_iob_to_xml, convert_iob_to_dict
>>> 
```

## ドキュメント
[こちら](https://ujiuji1259.github.io/IOB-util/)
