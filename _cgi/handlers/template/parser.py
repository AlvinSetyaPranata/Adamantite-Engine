from tempfile import NamedTemporaryFile, TemporaryFile
from adamantite._cgi.handlers.template.template import Handle
from adamantite._cgi.handlers.exceptions import Template_Not_Found, Invalid_Component
import os
import re



class Context_Cache:
    """
    All output from the processor are defined as Meta instances in this class
    """

    def __str__(self):
        return f"CacheContext object in {hex(id(self))}"

class Base_Html_Parser:
    """
    extending from other script:
    {extends %<components>% from 'script.html'}

    evaluation:
    {evaluate}
    
    {/evaluate}

    block: (used for extending)
    {block <component_name>}

    {/block}

    inject: (used for injecting the components that has been imported to target file) (statements that have block tag will be ignored)
    {inject <component_name>}


    """
    def __init__(self):
        self.__extend_pattern = re.compile(r"\{\s*extends\s*%\s*[\w\,\s]+%\s*from\s*(\'|\")[\w/]+\.[\w/]+(\'|\")\}")
        self.__blocking_patterns = (re.compile(r"\{\s*block\s+\w+\s*\}"), re.compile(r"\{\s*/block\}"))
        self.__inject_patterns = re.compile(r"\{\s*inject\s+[\w]+\s*\}")
        self.place_var = re.compile(r"\{[A-Za-z_]*[\w]*\}")
        self.components_pattern = re.compile(r"%\s*[\w,]+\s*[\w,]*\s*%")

    def cleaning_tags(self, content_tags):
        new = []
        is_tags = False
        for pattern in (self.find_extend_statements, self.find_blocking_statements, self.find_inject_statements):
            for line in content_tags:
                if pattern(line):
                    is_tags = True
                    break

            if not is_tags:
                new.append(line)

            is_tags = False

        return new

    def get_required_components(self, string):
        # return [component.split(",") for component in self.components_pattern.findall(string)]
        components = []


        for req_component in self.components_pattern.finditer(string):
            start_, end_ = req_component.span()

            req_component = string[start_+1:end_-1]

            for component in req_component.split(","):
                components.append(component.strip())

        return components


    def find_extend_statements(self, content):
        # matches = [content[match.span()[0]:match.span()[1]] for match in self.__extend_pattern.finditer(content)]
        matches = []

        for match in self.__extend_pattern.finditer(content):
            start, end = match.span()
            matches.append(content[start:end])

        return matches


    def find_blocking_statements(self, content):
        """
        Return the begining, end position of content block and the name of the block
        """

        begin_blocks, end_blocks, block_names = [], [], []
        begin_block_pattern, end_block_pattern = self.__blocking_patterns


        for match in begin_block_pattern.finditer(content):
            start, end = match.span()

            begin_blocks.append(end)
            block_names.append(content[start+1:end-1].split()[1])

        for match in end_block_pattern.finditer(content):
            end_blocks.append(match.span()[0])

        if len(begin_blocks) != len(end_blocks):
            raise Exception("Unclosed block statements or closed block statements with no opening block statements!")

        return list(zip(begin_blocks, end_blocks, block_names))


    def find_inject_statements(self, splited_content):
        matches_positions = []

        for i in range(len(splited_content)):
            for _ in self.__inject_patterns.finditer(splited_content[i]):
                matches_positions.append((i, splited_content[i].split()[-1][:-1]))

        return matches_positions

    def __evaluate(self, content):
        pass


    def __place_var(self, content, param=None):
        pass



class Processors(Base_Html_Parser):
    def __init__(self):
        super().__init__()
        self.t_handler = Handle()
        self.__temp_memory = Context_Cache()

    
    def get_from_memory(self, *names):
        """
        return ordered attributes from temporary memory
        """
        return [getattr(self.__temp_memory, name) for name in names if hasattr(self.__temp_memory, name)]


    def modify_content(self, content, components, add_suffix="\n", splitter="\n"):
        splited_content = content.split(splitter)
        inject_positions = self.find_inject_statements([line.strip() for line in splited_content])
        new_positions = []

        count_component = {component:0 for component in components}


        for i in range(len(splited_content)):
            for inject_i in inject_positions:
                if inject_i[0] == i:
                    new_positions.append(components[inject_i[-1]])
                    count_component[inject_i[-1]] += 1

                else:
                    new_positions.append(splited_content[i])

    
        return splitter.join(self.cleaning_tags(new_positions)), [x for x in count_component if count_component[x] == 0]


    def find_components(self, content, required_components):
        """
        Return the dictionary of given filenames, target_tag_positions and their components that in :required_components
        components for each filenames is formed as dictionary with component_name as key.
        """

        results = {}

        components_ = self.find_blocking_statements(content[-1])
        found_components = []
        components_name = []

        for x in components_:
            start_pos, end_pos, block_name = x
            
            if block_name in components_name:
                raise Invalid_Component(f"Conflict Component detected!")

            if block_name in required_components:
                components_name.append(block_name)
                found_components.append(content[-1][start_pos:end_pos].strip())
                required_components.remove(block_name)

        if len(found_components) != len(components_name):
            raise Exception("Line 208")

        for i in range(len(components_name)):
            results[components_name[i]] = found_components[i]

        return results


    def read_template(self, statement):
        filename_pattern = re.compile(r"(\'|\")[\w/\.]+(\'|\")")

        for match in filename_pattern.finditer(statement):
            start, end = match.span()
            file = statement[start+1:end-1]

        content, status_code = self.t_handler.get_template(file)

        if status_code == "404":
            raise Template_Not_Found(f"cannot found \"{file}\"!")

        return (file, content)


    def process_extend(self, content):
        matches = self.find_extend_statements(content) 
        res = []

        for match in matches:
            template_name = match.split()[-1]

            if template_name.endswith("}"):
                template_name = template_name[1:-2]

            else:
                template_name = template_name[1:-1]

            res.append(self.find_components(self.read_template(match), set(self.get_required_components(match))))


        res2 = res.pop(0)
        res2.update(*res[:])


        setattr(self.__temp_memory, "extended_components", res2)

        compiled_content, unused_component = self.modify_content(content, res2)


        # self.report(f"removing all unused components from temporary memory...", level=2)
        for u_component in unused_component:
            # self.report(f"Unused components! detected: {u_component}", level=2)
            del self.__temp_memory.extended_components[u_component]


        return compiled_content


class Html_String(Processors):
    def __init__(self, html_string, params=None):
        super().__init__()
        self.content = html_string
        self.params = params
        self.file_ = TemporaryFile(mode="w", suffix=".html")

    def compile_(self):
        """
        Return the compiled template content
        """
        return super().process_extend(self.content.strip())

    def __del__(self):
        self.file_.close()
        os.unlink(self.file_.name)



