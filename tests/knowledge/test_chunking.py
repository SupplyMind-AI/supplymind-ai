from supplymind.features.knowledge.infrastructure.chunking import chunk_text
def test_chunking_overlap():
 c=chunk_text('abcdefghij'*10,chunk_size=30,overlap=5);assert len(c)>1;assert c[0][-5:]==c[1][:5]
