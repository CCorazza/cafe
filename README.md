# Un p'tit cafe?


### End-User bot commands:

The syntax to call a bot command is:
`:coffee: (command <args...>)`
or:
`serge: coffee command <args...>`

Shortcuts can be called this way:
`:coffee: [42]`
(so that means without parens.)

If you find that shortcuts are "buggy", remember that they need not to contain whitespace,
i.e: `[42]` would work, but not `[ 42 ]`.

The `serge: ` call must be only do a call, and not contain text around.
The other two, however, can be called anywhere, multiple times in a message, etc.



#### The list of commands:

`list`: Lists all breaks fitting in the `from` to `to` period.

    list
    :coffee: ?


`info`: Displays information about a certain break.

    info <id>
    :coffee: [<id>]


`create`: Create a new break

    create <hour> <minutes>
    :coffee: @<hour>:<minutes>
    :coffee: @<hour>h<minutes>


`join`: Join a certain break

    join <id>
    :coffee: +<id>


`leave`: Leave a certain break

    leave <id>
    :coffee: -<id>


`help`: Display a help message (or not)

    help [command]
    :coffee:
