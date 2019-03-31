# Check if the questions are grammarly correct
def check_grammar(sentence):
    import language_check
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(sentence)
    new_s = language_check.correct(sentence, matches)

    return new_s 