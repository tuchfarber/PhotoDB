let login_page = new Vue({
    el: "#login-form",
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',
        error_text: '',
    },
    methods: {
        login: function(){
            axios({
                method: 'post',
                url: '/rest-auth/login/',
                data: {
                    username: this.username,
                    password: this.password,
                },
                headers: {
                    'X-CSRFToken': _get_cookie('csrftoken')
                }
            })
            .then(results => {
                window.location.href = '/'
            })
            .catch(error => {
                this.error_text = error;
            })
        }
    }
})
