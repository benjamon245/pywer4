const ROOT_URL = "pywer4"
let level = 3
let nblines = 6
let nbcols = 7
let grid_lock = false

$("#nblines").val(nblines)
$("#nbcols").val(nbcols)
$("#level").val(level)

// Recreate the grid from scratch and register event for user to play
function refresh_table() {
    grid_lock = true // Prevents any action on the grid from the user
    $("#mytable").empty()
    let i, j
    for (j = nblines; j >= 1; j--) {
        $("#mytable").append(`<tr id='l${j}'></tr>`)

        for (i = 1; i <= nbcols; i++) {
            $("#l" + j).append(`<td class='cell' line=${j} col=${i}></td>`)

        }

    }
    cell_click()
    grid_lock = false
    $("#message").html("Bonne chance !");
}

// Initial grid creation
refresh_table()
$("#message").html("Bienvenue");

// Refresh the grid if someone submit the settings form
$("form").submit(function () {
        nblines = Number($("#nblines").val())
        nbcols = Number($("#nbcols").val())
        level = Number($("#level").val())
        refresh_table()

    }
)
// Register the actions in case of click on the grid
function cell_click() {

    $(".cell").click(
        function () {
            if (grid_lock == false) { // Only if the grid isn't already locked
                grid_lock = true
                var clicked_cell = $(this)

                // list user tokens
                const user_tokens = []
                $(".cell[player=user]").each(
                    function () {
                        const coord = [Number($(this).attr("line")), Number($(this).attr("col"))]
                        user_tokens.push(coord)
                    }
                )

                // list computer tokens
                const computer_tokens = []
                $(".cell[player=computer]").each(
                    function () {
                        const coord = [Number($(this).attr("line")), Number($(this).attr("col"))]
                        computer_tokens.push(coord)
                    }
                )

                // build inputs for remote call
                var state = {
                    "nblines": nblines,
                    "nbcols": nbcols,
                    "level": level,
                    "user_tokens": user_tokens,
                    "computer_tokens": computer_tokens
                }

                var user_input = {
                    "state": state,
                    "user_move": [Number(clicked_cell.attr("line")), Number(clicked_cell.attr("col"))]
                }

                // remote call to check user move
                user_input_json = JSON.stringify(user_input)
                $.post(`/${ROOT_URL}/user_play`,
                    {parameter: user_input_json},
                    function (data, status) {

                        // Valid user move
                        if (!data["valid_move"]) {
                            grid_lock = false
                        } else {
                            clicked_cell.attr("player", "user")

                            state["user_tokens"].push(user_input["user_move"])
                            if (data["user_win"]) { // If the user won
                                $("#message").html("<p win='user'>Bravo !</p>")
                                // Highlight winning tokens
                                data["squares"].forEach(
                                    function (elt) {
                                        l = elt[0]
                                        c = elt[1]
                                        $(`.cell[line=${l}][col=${c}]`).attr("win", "user")
                                    }
                                )
                            } else if (data["full"]) { // If the grid is full with no winner
                                $("#message").html("Égalité !")
                            } else {
                                // Remote call to get computer move
                                state_json = JSON.stringify(state)
                                $("#message").html("une seconde : l'ordinateur réfléchit");
                                $.post(`/${ROOT_URL}/computer_play`,
                                    {parameter: state_json},
                                    function (data, status) {
                                        // Applying computer move
                                        l = data["move"][0]
                                        c = data["move"][1]
                                        $(`.cell[line=${l}][col=${c}]`).attr("player", "computer")
                                        if ((data["computer_win"] == false) && (data["full"] == false)) { // The game continues
                                            grid_lock = false
                                            $("#message").html("A toi de jouer !");
                                        } else if (data["computer_win"]) { // If the computer won
                                            $("#message").html("<p win='computer'>Loser !</p>")
                                            // Highlight winning tokens
                                            data["squares"].forEach(
                                                function (elt) {
                                                    l = elt[0]
                                                    c = elt[1]
                                                    $(`.cell[line=${l}][col=${c}]`).attr("win", "computer")
                                                }
                                            )
                                        } else {
                                            $("#message").html("Égalité !") // If the grid is full with no winner
                                        }
                                    }
                                )
                            }
                        }
                    }
                )

            }
        }
    )
}