"""Test data module"""
# LoginPage
url = "https://thinking-tester-contact-list.herokuapp.com/"
eml = "testname@test.com"
psw = "Tester11"
invalid_eml = "incorrect_email"
invalid_psw = "incorrect_password"

# ContactListPage
url1 = "https://thinking-tester-contact-list.herokuapp.com/contactList"
url_contain1 = "contactList"

# AddContactPage
url2 = "https://thinking-tester-contact-list.herokuapp.com/addContact"
url_contain2 = "addContact"
fn = "First"
ln = "Last"
bd = "2000-01-01"
eml1 = "testname@test.com"
pn = "80291111111"
str1 = "Street 1"
str2 = "Street 2"
ct = "City"
stpr = "State"
pc = "123456"
cntr = "Belarus"
inv_pn = "123"
inv_eml = "123"
inv_bd = "123"
inv_pc = "abc"
error_message_add_new_contact = ("Contact validation failed: birthdate: "
                                 "Birthdate is invalid, email: Email "
                                 "is invalid, phone: Phone number is "
                                 "invalid, postalCode: Postal code is invalid")
error_message_empty_add_new_contact = ("Contact validation failed: firstName: "
                                       "Path `firstName` is required., "
                                       "lastName: Path `lastName` is "
                                       "required.")

# ContactDetails
url3 = "https://thinking-tester-contact-list.herokuapp.com/contactDetails"
url_contain3 = "contactDetails"

# EditContact
url4 = "https://thinking-tester-contact-list.herokuapp.com/editContact"
url_contain4 = "editContact"
fn_1 = "Ann"
ln_1 = "Ford"
bd_1 = "1980-12-31"
eml1_1 = "testexample123@example.com"
pn_1 = "80337654321"
str1_1 = "Edit 1"
str2_1 = "Edit 2"
ct_1 = "Town"
stpr_1 = "Province"
pc_1 = "000111"
cntr_1 = "Italy"
