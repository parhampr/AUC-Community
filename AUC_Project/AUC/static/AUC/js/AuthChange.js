var auth = () => (window.location.href).includes('login')? ['', 'AUC Login'] : ['panel-active', 'AUC New User'],
    change = () => {
        let c = auth();
        document.body.className = c[0];
        document.title = c[1];
    },
    bullet_anim = () => {
            var el = document.getElementById("m-toggle_change");
            el.style.animation = 'none';
            el.offsetHeight; /* trigger reflow */
            el.style.animation = null; 

        // document.getElementById("m-toggle_change").style.animationPlayState = "running"
        // setTimeout(() => {
        //     document.getElementById("m-toggle_change").style.animationPlayState = "paused"
        // }, 600);
    }
(function () {
    if ((window.location.href).includes("register")) change();
})();

function changeAuthOption(){
    hf = window.location.href
    let id = hf.includes("register")? "login" : "register", 
        total = (hf.split('?').length > 1)? hf.split('?') : [hf, ''],
        url = total[0].split('/')
    url[url.length - 2] = id
    if (total[1] != "")
    url[url.length - 1] = "?"+total[1];
    window.history.pushState({'id':id}, 'page-'+id, url.join('/'));
    change();
    bullet_anim();
}


window.onload = () => {
    let x = document.getElementsByClassName('#toggle_account_sign');
    for (var i = 0; i < x.length; i++)
        x[i].addEventListener('click', changeAuthOption, false);
    
}

window.onpopstate = function(event) {
    location.reload();
};

