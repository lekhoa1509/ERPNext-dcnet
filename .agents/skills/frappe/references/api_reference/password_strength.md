# API Reference: password_strength.py

**Language**: Python

**Source**: `utils/password_strength.py`

---

## Functions

### test_password_strength(password: str, user_inputs: 'Iterable[object] | None' = None) → '_Result'

Wrapper around zxcvbn.password_strength

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| password | str | - | - |
| user_inputs | 'Iterable[object] | None' | None | - |

**Returns**: `'_Result'`



### get_feedback(score: int, sequence: list) → 'PasswordStrengthFeedback'

Return the feedback dictionary consisting of ("warning","suggestions") for the given sequences.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| score | int | - | - |
| sequence | list | - | - |

**Returns**: `'PasswordStrengthFeedback'`



### get_match_feedback(match: '_Match', is_sole_match: bool) → 'PasswordStrengthFeedback'

Return feedback as a dictionary for a certain match.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | '_Match' | - | - |
| is_sole_match | bool | - | - |

**Returns**: `'PasswordStrengthFeedback'`



### get_dictionary_match_feedback(match: '_Match', is_sole_match: bool) → 'PasswordStrengthFeedback'

Return feedback for a match that is found in a dictionary.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | '_Match' | - | - |
| is_sole_match | bool | - | - |

**Returns**: `'PasswordStrengthFeedback'`



### fun_bruteforce()

**Returns**: (none)



### fun_dictionary()

**Returns**: (none)



### fun_spatial()

**Returns**: (none)



### fun_repeat()

**Returns**: (none)



### fun_sequence()

**Returns**: (none)



### fun_regex()

**Returns**: (none)



### fun_date()

**Returns**: (none)


