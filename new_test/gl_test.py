from arbi_agent.model import generalized_list_factory as GLFactory


if __name__ == '__main__':
    gl1 = GLFactory.new_gl_from_gl_string("(TestGL \"TestGL\")")
    value = GLFactory.string_value("testGL")
    expression = GLFactory.value_expression(value)
    gl2 = GLFactory.new_generalized_list("TestGL", expression)
    print("gl built by string :", gl1)
    print("gl built by value and expression :", gl2)

    print()
    gl3 = GLFactory.new_gl_from_gl_string("(NestedGL (TestGL \"TestGL\") \"testing\")")
    print("nested gl :", gl3)
    expression = gl3.get_expression(0)
    print("retreiving first nested GL :", expression)
    value = expression.as_generalized_list().get_expression(0).as_value()
    print("retreiving nested GL's value :", value)

    print()
    gl = GLFactory.new_gl_from_gl_string("(TestGL \"TestGL\")")
    variable_gl1 = GLFactory.new_gl_from_gl_string("(TestGL $var)")
    print("variable GL :", variable_gl1)
    # unify test
    binding = gl.unify(variable_gl1, None)
    print("get binding :", binding)
    # evaluate test
    variable_gl2 = GLFactory.new_gl_from_gl_string("(EvalTest $var)")
    result_gl = variable_gl2.evaluate(binding)
    print("evaluated GL :", result_gl)

    print()
    hard_string = "\"testing\""
    hard_string = GLFactory.escape(hard_string)
    print("escaped string :", hard_string)
    hard_string = GLFactory.unescape(hard_string)
    print("unescaped string :", hard_string)








