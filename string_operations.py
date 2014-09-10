def string_equal(value_a, value_b):
    return value_a.lower() == value_b.lower()

def string_contain(haystack, needle):
    return needle.lower() in haystack.lower()
