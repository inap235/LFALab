class lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr = text[0]
        
    def navigate(self):
        self.pos +=1
        if self.pos > len(self.text):
            self.curr = None
        else: self.curr = self.text(self.pos)
        
        
    def skip_space(self):
        while self.curr is not None and self.curr.isspace():
            
               