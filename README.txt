data_source目录为数据目录，包含activate（活动）,guide（指南）,news（新闻）,notdbj（非德巴金）子目录，和meta_tags.txt(外包提供的几个层级标签)
gen_data目录为处理数据的代码目录，包含content_extractor.py（从pdf,doc提取文章内容）；deal_tags_data.py（这里并没用到），gen_data.py（对文章分词，生成训练数据,步骤2）
feat_id.txt为特征编号。item_code为所有物品的向量化后的文本。sample.txt为生成的样本数据
model为模型训练加载和处理的目录，classify.py为训练模型，并且保存模型的文件。user_model.py为加载使用模型