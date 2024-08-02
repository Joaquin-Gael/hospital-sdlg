$(document).ready(()=>{
    $('.navbar-burger').click(()=>{
        $('.navbar-burger').toggleClass('is-active')
        $('.navbar-menu').toggleClass('is-active')
    })
    $('#navbarDropdownLinkMore').click(()=>{
        $('#navbarDropdownMore').toggleClass('is-active')
    })
    $('#navbarDropdownLinkUser').click(()=>{
        $('#navbarDropdownUser').toggleClass('is-active')
    })
    $('#navbarDropdownLinkLogin').click(()=>{
        $(this).toggleClass('is-active')
    })
    $('#navbarDropdownLinkRegister').click(()=>{
        $(this).toggleClass('is-selected')
    })
    const theme = localStorage.getItem('theme') || 'default';
        loadTheme(theme);
        
        // Cambiar tema al hacer clic en una opción
        $('#lightThemeOption').click(function() {
            localStorage.setItem('theme', 'default');
            loadTheme('default');
        });

        $('#darkThemeOption').click(function() {
            localStorage.setItem('theme', 'dark');
            loadTheme('dark');
        });

    function loadTheme(theme) {
        let themeLink = $('#themeLink');
        if (theme === 'dark') {
            themeLink.attr('href', "{% static 'css/dark-theme.css' %}");
        } else {
            themeLink.attr('href', "{% static 'css/default-theme.css' %}");
        }
    }
})