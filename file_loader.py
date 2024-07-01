class file_loader():
    def load_file(self):
        identifier = any
        delimiter = '\n'

        loc_file = input("Localização do arquivo\n")
        identifier = input("Insira um identificador\n")
        delimiter = input ("Insira um delimitador\n")
        return self.loader(loc_file,identifier,delimiter)

    def loader(self,loc_file,identifier,delimiter):
        list = []

        with open(loc_file, 'r', encoding='utf-8') as f:
            text = f.read()
            
        f.close()
        if(delimiter != ''):
            lines = text.split(delimiter)
        else:
            lines = text.split("\n")
        if(identifier != ''):
            for line in lines:
                if line.lower().startswith(identifier.lower()):
                    words = line.split()
                    user_story = line.strip()
                    user_story = user_story.strip(words[0])
                    user_story = user_story.lstrip()
                    list.append(user_story)
        else:
            for line in lines:
                if(line != ''):
                    list.append(line.strip())
        return list