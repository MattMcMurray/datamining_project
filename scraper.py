from lxml import html
from lxml import etree
import requests

page = requests.get('http://www.nytimes.com/movie/review?res=9506E3DE1E38E333A25756C2A9649C946191D6CF')
tree = html.fromstring(page.content)
etree.strip_tags(tree, 'strong')
paragraphs = tree.xpath('//div[@id="articleBody"]/p/text()')

strPara = ''
for para in paragraphs:
	strPara = strPara + para + '\n'
print 'Paragraphs: ', strPara
