var isNightMode = () => localStorage.getItem(btoa('NIGHT_MODE')) == 'true',
    changeColorScheme = () => { 
        document.getElementsByTagName('HTML')[0].className = (isNightMode() ? 'dark' : ''); 
        document.querySelector('meta[name="color-scheme"]').content = (isNightMode() ? 'dark' : 'light'); },
    changeDarkModeIcon = () => { $('#switch').removeClass('fas far').addClass(isNightMode() ? 'fas' : 'far').attr('title', (index, attr) => attr == 'NIGHT MODE IS ON' ? 'NIGHT MODE IS OFF' : 'NIGHT MODE IS ON');},
    NightModeStatus = () => $('#switch').attr('class').indexOf("far") >= 0;

(function() {
    if (localStorage.getItem(btoa('NIGHT_MODE'))) changeColorScheme();
    document.getElementsByTagName('HTML')[0].style.overflow = 'hidden';
})(); 

document.addEventListener('readystatechange', event => {
    if (event.target.readyState === "complete") {
        setTimeout(() => {
            $('.loader').fadeOut('slow', function(){
                $(this).remove();
            })
            $('HTML').removeAttr('style');
        }, 300);
        changeDarkModeIcon();
        console.log('complete');

        document.getElementById('switch').addEventListener('click', () => {
            localStorage.setItem(btoa('NIGHT_MODE'), NightModeStatus());
            changeColorScheme();
            changeDarkModeIcon();
        })

    }
});

var types = {
    'error': 'fa-exclamation-circle',
    'success': 'fa-check-circle',
    'info': 'fa-info-circle'
}
var message = (args) => {
    let icon = args[2] ? `<img src='${args[2]}' alt='user-info'>` : `<i class="fas ${types[args[0]]}"></i>`;
    return $(`
    <div class="alert-box al-${args[0]} d-flex justify-content-between align-items-center my-2 ms-3">
    <div class="alert-content d-flex align-items-center">
        <div class="alert-icon d-flex align-items-center justify-content-center">
            ${icon}
        </div>
        <div class="alert-text px-2">
            <span><b>${args[1]}</b></span>
        </div>
    </div>
    <i class="fas fa-times-circle mx-2" style="font-size: 20px;" id="alert-close" role="button"></i>
</div>
    `);
}
function timeout(ms) {
    return new Promise(function (resolve) {
        setTimeout(resolve, ms);
    });
}

async function fireevents(a) {
    a.css('transform', 'translateX(-150%)');
    await timeout(400);
    a.addClass('closeSlide');
    await timeout(400);
    a.remove();
}

function add_alertNotfications(AlertN, CloseManually=false) {
    let m = message(AlertN), started = undefined;
    m.appendTo($('#alert-container'));
    setTimeout(() => {
        m.css({
            'opacity': '1',
            'transform': 'translateY(0px)'
        })
    }, 10);
    let x = setTimeout(() => {
        started = 1;
        fireevents(m);
    }, 8000);
    if (CloseManually) {
        m.addClass('Cmiam') //Close me immediately but manually
        clearTimeout(x)
    };
    m.find('#alert-close').on('click', function(){
        if (!started)
        {
            clearTimeout(x);
            fireevents(m);
        }
    })
}

