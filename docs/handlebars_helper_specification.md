# Glynt Document Variable-set Specification #

This document is the specification document for clause variables that will be used in the glynt document system.
They are handlebars helper methods; and are simply javascript that can be modified and aliased ad nauseum.

They exist in order to make authoring a document as simple as possible

__The stanzas are constructed in the form:__

# Name #
Description

1. var name: type [*defaults|a|b|where * indicates default value for a param] description

__e.g.__

    Usage Example

** Additional info and usage notes **


# The Glynt Document variable Set #

1. **NB.** all strings must be indicated using " and not '
2. **NB.** when setting css class for a variable object use "_class" and not "class" as class is a reserved word


## Document Variables ##
Standard variables; the default value is defined by the content in-between the "{{#doc_var}}{{/doc_var}}" tags

1. name: String - The variable by which this object is referred to within the document context
2. inherit_from: String - the "name" of another variable that this variable inherits its initial value from. If the user changes the value of a doc_var that inherits_from then that field should stay set as the new value

__e.g.__

    {{#doc_var name="my_variable_name"}}Some Content Goes here and is the Default Value of the my_variable_name var{{/doc_var}}


## Choice Variables ##
Allow the user to select from a pre-determined set of variable options; or enter their own value if is_static=false

1. name: String - The variable by which this object is referred to within the document context
2. can_toggle: Boolean [true|*false] - Allows the user to turn this clause on or off
3. choices: String "a,b,c,d" - Will provide a selection of options the user can select from
4. is_static: Boolean [*true|false] - If true, then the user can choose only 1 of the variables specified by "choices". If false they can enter their own value as well as the ones provided by "choices"
5. initial: The initial value "a" *should be one of the provided options

__e.g.__


    {{#doc_choice name="my_variable_name" choices="a,b,c" is_static=true}}{{/doc_choice}}

** The default is always the first in the list. **


## Select Clause ##
Select clauses are designed to allow the user to select 1 or more statements or even sections of a document.

1. name: String - The variable by which this object is referred to within the document context
2. label: String - The text that will be shown in the helper html
3. multi: Boolean [true|*false] - Can the user select more than 1 of the clauses
4. can_toggle: Boolean [true|*false] - Allows the user to turn this clause on or off
5. can_increment: Boolean [true|*false] - Allows the user to add options to this current set; will create a copy of the first item and its contents (usually doc_vars)
6. join_by: String [*"\r"] - The string by which the selected option/s will be connected
7. selected: String ["1,3,n"] - the index (1 based) that are selected by default

__e.g.__

    {{#doc_select name="my_variable_name" label="My Variable Title"}}
    Clause A
    {option}
    Clause B
    {option}
    Clause C
    {{/doc_select}}


## Multi-Select Clauses ##
Allow the user to select more than 1 clause; and are simply the doc_select handler with multi set to true.

__e.g.__

    {{#doc_select name="my_variable_name" label="My Variable Title" multi=true}}
    Clause A
    {option}
    Clause B
    {option}
    Clause C
    {{/doc_select}}

** see Select Clause **


## Incrementor Clauses ##
Allow the user to expand on a set. Will create a clone of the first item in the set. If the first row
contains doc_var items, then those doc_var names will each have a +1 index appended "<doc_var_name>_{index}" appended to their id and name.
The first doc_var remains "<doc_var_name>" and recieves no index.

__e.g.__

    {{#doc_select name="my_variable_name" label="My Variable Title" can_increment=true}}
    {{#doc_var name="employee"}}Employee Name{{/doc_var}}
    {{/doc_select}}

** see Select Clause **


## Paragraph Note ##

Some paragraphs will need to be annotated and have help text associated with them.

1. takes no variables

__e.g.__

    {{#doc_note}}
    This is my wonderful paragraph with some text
    {note}
    This is my awesome explanation text, which wont confuse the user; but instead illuminate them...
    {{/doc_note}}


## Help Text ##

Some variable need a bit more explanation; in order to show this extra text we define it seperately using the help_for tag

1. varname: the name of the variable that this help text applies to

__e.g.__

    {{#help_for varname="my_var"}}Extended Help Text Goes here{{/help_for}}

