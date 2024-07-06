use pilator::components::{items::RegexComponent, regex::Regex};

pub fn get_regex_for_bench() -> Vec<Regex> {
    let mut regexes = vec![];
    let const_val = Regex::new(vec![
        RegexComponent::ZeroOrMore(Regex::new(vec![RegexComponent::Literal("(".to_string())])),
        RegexComponent::Keyword("bv ".to_string()),
        // RegexComponent::OneOrMore(Regex::new(vec![
        //     RegexComponent::Keyword("0".to_string()),
        //     RegexComponent::Keyword("1".to_string()),
        //     RegexComponent::Keyword("2".to_string()),
        //     RegexComponent::Keyword("3".to_string()),
        //     RegexComponent::Keyword("4".to_string()),
        //     RegexComponent::Keyword("5".to_string()),
        //     RegexComponent::Keyword("6".to_string()),
        //     RegexComponent::Keyword("7".to_string()),
        //     RegexComponent::Keyword("8".to_string()),
        //     RegexComponent::Keyword("9".to_string()),
        // ])),
        // RegexComponent::OneOrMore(Regex::new(vec![
        //     RegexComponent::Keyword("Bit1".to_string()),
        //     RegexComponent::Keyword("Bit2".to_string()),
        //     RegexComponent::Keyword("Bit4".to_string()),
        //     RegexComponent::Keyword("Bit8".to_string()),
        //     RegexComponent::Keyword("Bit16".to_string()),
        //     RegexComponent::Keyword("Bit32".to_string()),
        //     RegexComponent::Keyword("Bit64".to_string()),
        // ])),
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
