import re
import nltk 
from nltk.tokenize import word_tokenize , PunktSentenceTokenizer

class SymbolTable:
    def __init__(self):
        self.size = 30
        self.table = [None] * self.size

    def _hash(self, key):
        hash_value = 0
        for char in key:
            hash_value += ord(char)
        return hash_value % self.size

    def insert(self, key, value):
        hash_value = self._hash(key)
        if self.table[hash_value] is None:
            self.table[hash_value] =[(key, value)]

    def lookup(self, key):
        hash_value = self._hash(key)
        if self.table[hash_value] is not None:
            return self.table[hash_value]

        return None




class Scanner:
    def __init__(self):
        self.symbol_table=SymbolTable()
        self.sentence_tokenizer= PunktSentenceTokenizer()
    def tokenize(self,source_code):
        
        sentences = self.sentence_tokenizer.tokenize(source_code)

        keywords_mold = r'\b(?:write|read|loop|until|if|so)\b'
        symbol_mold= r'[\ [ \ ] \ ( \ ) \ ;]'
        operetion_mold=r'[+\ - \ * \ % \ = \ /]'
        identifire_mold=r'\b(?!write|read|loop|until|if|so)[a-zA-Z_]\w*\b'
        costant_mold=r'\b(\d+)\b'


        tokens=[]
        for sentence in sentences:
            words= word_tokenize(sentence)
            for mold , token_typ in[
                (keywords_mold,'id'),
                (symbol_mold,'symbol'),
                (operetion_mold,'op'),
                (identifire_mold,'id2'),
                (costant_mold,'digit')
                ]:
                compile_mold=re.compile(mold)
                for word in words:
                    match=compile_mold.match(word)
                    if match:
                        token_value= match.group()
                        symbol_info= self.symbol_table.lookup(token_value)
                        if symbol_info:
                            tokens.append({'type':symbol_info[0],'value':token_value})
                        else:

                            self.symbol_table.insert(token_typ,token_value)
                            tokens.append({'type':token_typ,'value':token_value})
        return tokens
    def display_symbol_table(self):
        print("\nSymbolTableNew")
        for entry in self.symbol_table.table:
            if entry is not None:
                print(f"{[entry[0]]}")
                        


            
            


def main():

    keywords =[("write",r"write"), ("read",r'read'), ("loop",r"loop"), ("until",r"until"), ("if",r"if"), ("so",r"so"), ("OpPr", r'('), ("ClPr", r")"), ("SC",r";"),
                ("OpBr", r"["), ("ClBr", r"]"), ("mod", r"%"), ("division",r"/"), ("sub",r"-"), ("sum", r"+"), ("star",r"*"), ("equal",r"=="), ("assignment", r"=")]

    source_code = """int row,col;
    write <<”Enter Row : ”;
    read>>row;
    write<<”Enter Col : ”;
    read>>col;
    loop (int i=1 ; i<=row ; i++)
        {
            loop (int j=1 ; j<=col ; j++)
                {
                        write<<i*j<<”  ”;
                }
                write<<endl<<endl;

        }
        """
    scanner = Scanner()
    tokens=scanner.tokenize(source_code)
    for token in tokens:
        print(token)
    scanner.display_symbol_table()
    symbol_table = SymbolTable()
    for key, value in keywords:
        symbol_table.insert(key, value)


    print(symbol_table.table)
if __name__ == "__main__":
    main()

