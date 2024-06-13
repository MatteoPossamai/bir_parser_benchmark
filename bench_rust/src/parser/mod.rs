use pilator::components::{items::RegexComponent, regex::Regex};

pub fn get_regex_for_bench() -> Vec<Regex> {
    let mut regexes = vec![];
    let const_val = Regex::new(vec![
        RegexComponent::ZeroOrMore(Regex::new(vec![RegexComponent::Literal("(".to_string())])),
        RegexComponent::Keyword("bv ".to_string()),
        RegexComponent::OneOrMore(Regex::new(vec![])),
        RegexComponent::ZeroOrMore(Regex::new(vec![RegexComponent::Literal(")".to_string())])),
    ]);
    let const_regex = Regex::new(vec![
        RegexComponent::ZeroOrMore(Regex::new(vec![RegexComponent::Literal("(".to_string())])),
        RegexComponent::Keyword("BExp_Const".to_string()),
        RegexComponent::Literal(" ".to_string()),
        RegexComponent::OneOrMore(const_val),
        RegexComponent::Literal(" ".to_string()),
        RegexComponent::ZeroOrMore(Regex::new(vec![RegexComponent::Literal(")".to_string())])),
    ]);
    regexes.push(const_regex);
    regexes
}
