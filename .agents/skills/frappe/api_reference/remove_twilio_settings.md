# API Reference: remove_twilio_settings.py

**Language**: Python

**Source**: `patches/v13_0/remove_twilio_settings.py`

---

## Functions

### execute()

Add missing Twilio patch.

While making Twilio as a standaone app, we missed to delete Twilio records from DB through migration. Adding the missing patch.

**Returns**: (none)



### twilio_settings_doctype_in_integrations() → bool

Check Twilio Settings doctype exists in integrations module or not.

**Returns**: `bool`


