class ExpressionList:

    def __init__(self):
        self.expression_list = []

    def add(self, expression):
        self.expression_list.append(expression)

    def add_by_index(self, index, expression):
        self.expression_list.insert(index, expression)

    def remove(self, expression):
        self.expression_list.remove(expression)

    def remove_by_index(self, index):
        del self.expression_list[index]

    def get(self, index):
        return self.expression_list[index]

    def clear(self):
        self.expression_list.clear()

    def get_expression_list(self):
        return self.expression_list
