def chunk_text(text:str,*,chunk_size:int,overlap:int)->list[str]:
 if chunk_size<=0 or overlap<0 or overlap>=chunk_size: raise ValueError('Invalid chunk configuration.')
 text='\n'.join(line.strip() for line in text.splitlines() if line.strip())
 out=[];start=0
 while start<len(text):
  end=min(start+chunk_size,len(text));out.append(text[start:end])
  if end==len(text): break
  start=end-overlap
 return out
