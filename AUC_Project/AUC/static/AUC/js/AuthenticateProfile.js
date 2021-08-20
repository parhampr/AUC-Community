function validateLoginEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validateNewPassword(pass) {
    let message = '';
    if (pass.length < 8)
        message = "The password must be at least 8 characters long.";
    else if (!(/^(?=.*?[A-Z])/.test(pass)))
        message = "The password must contain at least one UPPERCASE."
    else if (!(/^(?=.*?[a-z])/.test(pass)))
        message = "The password must contain at least one LOWERCASE."
    else if (!(/^(?=.*?[0-9])/.test(pass)))
        message = "The password must contain at least one DIGIT."
    $('#signup-errors').text(message).fadeIn('normal');
    return message == '';
}

$('.signup-container>form').on('submit', function (e) {
    if (!validateNewPassword($(this).find('#id_password').val()))
        e.preventDefault();
})

let check_login_field = null, 
    prev_values = (() => {
        let users = {}
        return {
            getUser : function(username){
                // console.log(users)
                return ((username in users) && (users[username] != ""))? username: "";
            },
            getImageUrl: function(username){
                // console.log(users)
                return users[username];
            },
            SetNewUser: function(username){
                users[username] = ""
                // console.log(users)
            },
            setImageUrl: function(username, ImageURL){
                users[username] = ImageURL
                // console.log(users)
            }
        }
    })(),
    Check = {
        1 : ['fas fa-user', 'Username/Email', 'username'],
        2 : ['fas fa-user', 'Username', 'username'],
        3 : ['fas fa-envelope', 'Email', 'email']
    };
var Inputvalue = (input) => input.val().trim();

$('.login-container #login_username').on("keyup", function () {
    if (check_login_field) clearTimeout(check_login_field);
    const field = Inputvalue($(this));
    let status = Check[1];
    console.log(field.length)
    if (field.length < 1){
        $('#user-login').prop('src', variableClassess['df']);
        $('#user-check').hide();
    }
    else{
        if (validateLoginEmail(field))status = Check[3];
        else status = Check[2];
        check_login_field = setTimeout(() => {
            if (field == prev_values.getUser(field)){
                console.log("PREVIOUS USER")
                $('#user-login').prop('src', prev_values.getImageUrl(field))
                $('#user-check').removeClass().addClass(variableClassess[prev_values.getImageUrl(field).includes(variableClassess["df"])? "t": "c"]).show();
            }
            else
            $.ajax(
            {
                url: variableClassess["ucu"],
                method: 'POST',
                data: {"username_email": field },
                timeout: 5000,
                beforeSend: function () {
                    $('#loader').css('display', 'block');
                    $('.login-container #user-check').removeClass().addClass(variableClassess["p"]).show();
                    prev_values.SetNewUser(field);
                },
                success: function (response) {
                    setTimeout(()=> {
                        if (response['exists']==1) 
                            $('#user-login').prop('src', response['url']);
                        else if (response['exists']==0)
                            $('#user-login').prop('src', variableClassess['df']);
                        prev_values.setImageUrl(field, $('#user-login').prop('src'));  
                        $('#user-check').removeClass().addClass(variableClassess[response["exists"] == 1 ? "c" : "t"]).show();              
                    }, 900);
                    },
                    complete: function() {
                        setTimeout(() => {
                            $('#loader').css('display', 'none');   
                        }, 800);
                    }, 
                    error: () => {
                        $('#user-login').prop('src', variableClassess['df'])
                        $('#user-check').removeClass().hide();
                }

                });
        }, 1500);
    
    }
    $('#validate-icon').removeClass().addClass(status[0]);
    $('.login-container label[for="username"]').text(status[1])
    $(this).attr('name', status[2]);



});

$('.show_hide_pass').on('click', function () {
    let input = $(this).parent().find('input');
    input.attr('type', (index, attr) => attr == 'text' ? 'password' : 'text');
    $(this).removeClass('text password').addClass(input.attr('type'));
})