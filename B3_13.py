class HTML:
    def __init__(self, output=None):
        self.output = output
        self.sublevels = []

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.sublevels.append(other)
        return self

    def __exit__(self, *args):
        if not self.output:
            print("<html>")
            for sublevel in self.sublevels:
                print(sublevel.string)
            print("</html>")
        else:
            with open(self.output, "w") as f:
                f.write("<html>")
                for sublevel in self.sublevels:
                    f.write(sublevel.string)
                f.write("</html>")

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.sublevels = []
        self.internal = ""
        self.string = ""
    
    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.sublevels.append(other)
        return self

    def __exit__(self, *args):
        int_temp = ""
        opening = "<{tag}>\n".format(tag=self.tag)
        ending = "\n</{tag}>".format(tag=self.tag)
        i = 0
        if len(self.sublevels) > 0:
            for sublevel in self.sublevels:
                if i == 0:
                    self.internal += sublevel.string
                else:
                    self.internal += "\n" + sublevel.string
                i += 1
        self.string = opening + self.internal + ending

class Tag:
    def __init__(self, tag, is_single=False, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.kwargs = kwargs
        self.text = ""
        self.sublevels = []
        self.internal = ""
        self.string = ""

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.sublevels.append(other)
        return self

    def __exit__(self, *args):
        attrs = []
        for attribute, value in self.kwargs.items():
            if attribute == "klass":
                attribute = "class"
            value_str = str(value)
            if value_str.replace("(","") != value_str:
                value_str = value_str.replace(",","").replace("(","").replace(")","").replace("'","")
            attrs.append('%s="%s"' % (attribute, value_str))
        attrs = " ".join(attrs)
        
        if attrs == "":
            if self.tag == "div":
                opening = "    <{tag}>\n".format(tag=self.tag)
                ending = "\n    </{tag}>".format(tag=self.tag)
            else:
                if self.is_single:
                    opening = "    <{tag}".format(tag=self.tag)
                    ending = "/>".format(tag=self.tag)
                else:
                    opening = "    <{tag}>{text}".format(tag=self.tag, text=self.text)
                    ending = "</{tag}>".format(tag=self.tag)
        else:
            if self.tag == "div":
                opening = "    <{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
                ending = "\n    </{tag}>".format(tag=self.tag)
            else:
                if self.is_single:
                    opening = "    <{tag} {attrs}".format(tag=self.tag, attrs=attrs)
                    ending = "/>".format(tag=self.tag)
                else:
                    opening = "    <{tag} {attrs}>{text}".format(tag=self.tag, attrs=attrs, text=self.text)
                    ending = "</{tag}>".format(tag=self.tag)
        i = 0
        if len(self.sublevels) > 0:
            for sublevel in self.sublevels:
                if i == 0:
                    self.internal += sublevel.string
                else:
                    self.internal += "\n" + sublevel.string
                i += 1
        if self.tag == "div":
            str_temp = ""
            for line in self.internal.splitlines():
                str_temp += "    " + line + "\n"
            self.internal = str_temp.rstrip("\n")
        self.string = opening + self.internal + ending


if __name__ == "__main__":
    print("Базовое задание")
    with HTML(output=None) as doc: #можно указать имя файла для записи в файл, например "test.html"
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
    
    print("\nУсложнённый код для теста большей вложенности, если не отображён, значит идёт запись в файл")
    #вторая часть с изенённым кодом, чтобы проверить бОльшую вложенность
    with HTML(output="test.html") as doc: #для проверки идёт запись в файл
        with TopLevelTag("head") as head:

            with Tag("title") as title:
                title.text = "hello"
                head += title

            doc += head

        with TopLevelTag("body") as body:

            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:

                with Tag("div", klass=("class-2")) as div2:

                    with Tag("p") as paragraph:
                        paragraph.text = "another test"
                        div2 += paragraph

                    with Tag("img", is_single=True, src="/icon.png") as img:
                        div2 += img
                
                    div += div2
                
                body += div

            doc += body