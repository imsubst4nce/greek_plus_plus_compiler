program okprog
{
    declare x,y;
    declare z;

    function add(in a, in b)
    {
        return a + b
    }

    x := 5;
    y := 10;
    z := add(in x, in y);

    while x < 20
        if [x <= 15 and y >= 10]
            x := x + 1;

    switchcase
        when x = 10 : x := x + 1
        when x = 11 : x := x + 2
        default :      x := x + 3
    ;

    incase
        when x = 5  : x := x + 1
        when x = 20 : x := x + 2
    ;

    untilcase
        when x = 1 : x := x + 1
        when x = 2 : x := x + 2
        until x > 10
    ;

    forcase y = 3
        when x = 1 : x := x + 1
        when x = 2 : x := x + 2
        when x = 3 : {
                        x := x + 1;
                        x := x + 2
                     }
}

