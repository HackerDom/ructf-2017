SETTINGS

A robust, efficient unified configuration storage. 


API DESCRIPTION

The storage is controlled through a concise text-based protocol, which is described below.

Settings are organized in sections, each section having its own authorized users. Only the authorized users can modify settings in the section.
When a new section is added, SETTINGS service internally generates the first api-key to be used for authorized access. Other api-keys can be added later by any authorized user.

All communication with the service is conducted using stateless requests to TCP port 12345.

Request/response layout notes:
	The number in braces specifies the field length. The '|' symbol denotes a logical border between fields, it should not be included in request text. All field values are right-padded to the specified length with spaces.


Method 'add-section'

Adds a new configuration section. Returns the initial admin api-key for the section.

Request layout:
	add-section|section-name(20)

Response layout;
	status(2)|api-key(40)


Method 'add-apikey' 

Adds a new admin api-key to an existing section.

Request layout:
	add-apikey |section-name(20)|old-api-key(40)|new-api-key(40)

Response layout:
	status(2)


Method 'fix-section'

Applies a patch to a section.

Request layout:
	fix-section|section-name(20)|api-key(40)|(setting-name(20)|setting-value(85)){0..9}

Response layout:
	status(2)


Method 'get-section'

Reads a section. Returns a batch of settings starting from the given key. To read the entire section it may be required to call this method multiple times, shifting the from-setting-name value.


Request layout:
	get-section|section-name(20)|api-key(40)|from-setting-name(20)

Response layout:
	status(2)|settings-count(1)|(setting-name(20)|setting-value(85)){settings-count}


Method 'all-section'

Reads the list of all sections. Returns a batch of section names starting from the given section. To read the entire section list it may be required to call this method multiple times, shifting the from-section-name value.

Request layout:
	all-section|from-section-name(20)

Response layout:
 	status(2)|sections-count(2)|section-name(20){sections-count}


Response status values:

	ok - success
	bn - bad section name (section not found)
	mk - too many api-keys
	na - forbidden
	fl - unexpected error


LOCAL ADMIN MODE


The service also has a local admin mode which can be used to manually add api-keys to sections. This mode can be accessed only from the machine where the SETTINGS service is hosted.

Available local admin commands:

add-master-key <section-name> <new-api-key>
