# RSearch
This is a search engine about XD resource. A forum.
使用python开发（再爬取到大量数据后整理时候用了c++）, 实现了对西电睿思论坛主题的搜索。主要步骤分3步：
- 第一步是爬虫，对睿思论坛爬取。先使用了广度优先遍历，然后根据睿思主题URL的特点在进行多线程多进程爬取
- 第二步对信息分词，建立倒排索引，放入数据库。
- 最后一步是网页呈现，然后根据用户输入获取信息分词后，进行排名（如PageRank算法）等，并呈现到网页上。
三者分别对应的包是 Spider， integration，web。
