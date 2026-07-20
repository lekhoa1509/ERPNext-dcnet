ALLOWED: dict[tuple[str, str], str] = {
	("Draft", "Active"): "submit",
	("Active", "Suspended"): "suspend",
	("Suspended", "Active"): "resume",
	("Active", "Expired"): "expire",
	("Suspended", "Expired"): "expire",
	("Active", "Cancelled"): "cancel",
	("Suspended", "Cancelled"): "cancel",
	("Draft", "Cancelled"): "cancel",
	("Active", "Revised"): "revise",
	("Cancelled", "Revised"): "revise_from_cancel",
}


def assert_transition(current: str, target: str) -> None:
	if (current, target) not in ALLOWED:
		raise ValueError(f"Transition not allowed: {current} -> {target}")
